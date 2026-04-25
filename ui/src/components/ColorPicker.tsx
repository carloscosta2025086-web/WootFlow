import { useRef, useEffect, useCallback, useState } from "react";
import type { HSV, RGB } from "../types";

// ── Color conversion ──
function hsvToRgb(h: number, s: number, v: number): RGB {
  const c = v * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = v - c;
  let r = 0, g = 0, b = 0;
  if (h < 60)       { r = c; g = x; }
  else if (h < 120) { r = x; g = c; }
  else if (h < 180) { g = c; b = x; }
  else if (h < 240) { g = x; b = c; }
  else if (h < 300) { r = x; b = c; }
  else              { r = c; b = x; }
  return {
    r: Math.round((r + m) * 255),
    g: Math.round((g + m) * 255),
    b: Math.round((b + m) * 255),
  };
}

function rgbToHsv(r: number, g: number, b: number): HSV {
  const r1 = r / 255, g1 = g / 255, b1 = b / 255;
  const max = Math.max(r1, g1, b1), min = Math.min(r1, g1, b1);
  const d = max - min;
  let h = 0;
  if (d > 0) {
    if (max === r1) h = ((g1 - b1) / d + 6) % 6;
    else if (max === g1) h = (b1 - r1) / d + 2;
    else h = (r1 - g1) / d + 4;
    h *= 60;
  }
  const s = max > 0 ? d / max : 0;
  return { h, s, v: max };
}

// ── Presets ──
const PRESETS: RGB[] = [
  { r: 0, g: 255, b: 200 },   // cyan
  { r: 255, g: 0, b: 100 },   // pink
  { r: 255, g: 0, b: 0 },     // red
  { r: 0, g: 255, b: 0 },     // green
  { r: 0, g: 100, b: 255 },   // blue
  { r: 255, g: 255, b: 0 },   // yellow
  { r: 255, g: 100, b: 0 },   // orange
  { r: 160, g: 0, b: 255 },   // purple
  { r: 255, g: 255, b: 255 }, // white
  { r: 0, g: 0, b: 0 },       // off
];

interface Props {
  color: RGB;
  onChange: (c: RGB) => void;
  label?: string;
}

export function ColorPicker({ color, onChange, label = "Cor" }: Props) {
  const svCanvasRef = useRef<HTMLCanvasElement>(null);
  const hueCanvasRef = useRef<HTMLCanvasElement>(null);
  const [hsv, setHsv] = useState<HSV>(() => rgbToHsv(color.r, color.g, color.b));
  const [draggingSV, setDraggingSV] = useState(false);
  const [draggingHue, setDraggingHue] = useState(false);

  // Sync HSV when external color changes
  useEffect(() => {
    const newHsv = rgbToHsv(color.r, color.g, color.b);
    // Only update if significantly different
    if (Math.abs(newHsv.h - hsv.h) > 2 || Math.abs(newHsv.s - hsv.s) > 0.02 || Math.abs(newHsv.v - hsv.v) > 0.02) {
      setHsv(newHsv);
    }
  }, [color.r, color.g, color.b]);

  // Draw SV square
  const drawSV = useCallback(() => {
    const canvas = svCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const W = 200, H = 200;
    canvas.width = W;
    canvas.height = H;

    // Hue base color
    const base = hsvToRgb(hsv.h, 1, 1);

    // White → hue gradient (horizontal)
    const gH = ctx.createLinearGradient(0, 0, W, 0);
    gH.addColorStop(0, "white");
    gH.addColorStop(1, `rgb(${base.r},${base.g},${base.b})`);
    ctx.fillStyle = gH;
    ctx.fillRect(0, 0, W, H);

    // Black overlay (vertical)
    const gV = ctx.createLinearGradient(0, 0, 0, H);
    gV.addColorStop(0, "rgba(0,0,0,0)");
    gV.addColorStop(1, "rgba(0,0,0,1)");
    ctx.fillStyle = gV;
    ctx.fillRect(0, 0, W, H);

    // Cursor
    const cx = hsv.s * W;
    const cy = (1 - hsv.v) * H;
    ctx.beginPath();
    ctx.arc(cx, cy, 7, 0, Math.PI * 2);
    ctx.strokeStyle = "white";
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(cx, cy, 5, 0, Math.PI * 2);
    ctx.strokeStyle = "black";
    ctx.lineWidth = 1;
    ctx.stroke();
  }, [hsv.h, hsv.s, hsv.v]);

  // Draw hue bar
  const drawHue = useCallback(() => {
    const canvas = hueCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const W = 20, H = 200;
    canvas.width = W;
    canvas.height = H;

    const g = ctx.createLinearGradient(0, 0, 0, H);
    for (let i = 0; i <= 360; i += 30) {
      const c = hsvToRgb(i, 1, 1);
      g.addColorStop(i / 360, `rgb(${c.r},${c.g},${c.b})`);
    }
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    // Indicator
    const y = (hsv.h / 360) * H;
    ctx.fillStyle = "white";
    ctx.fillRect(0, y - 2, W, 4);
    ctx.strokeStyle = "#000";
    ctx.lineWidth = 1;
    ctx.strokeRect(0, y - 2, W, 4);
  }, [hsv.h]);

  useEffect(() => { drawSV(); }, [drawSV]);
  useEffect(() => { drawHue(); }, [drawHue]);

  const updateFromSV = (e: React.MouseEvent | MouseEvent) => {
    const canvas = svCanvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const s = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    const v = Math.max(0, Math.min(1, 1 - (e.clientY - rect.top) / rect.height));
    const newHsv = { ...hsv, s, v };
    setHsv(newHsv);
    onChange(hsvToRgb(newHsv.h, newHsv.s, newHsv.v));
  };

  const updateFromHue = (e: React.MouseEvent | MouseEvent) => {
    const canvas = hueCanvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const h = Math.max(0, Math.min(360, ((e.clientY - rect.top) / rect.height) * 360));
    const newHsv = { ...hsv, h };
    setHsv(newHsv);
    onChange(hsvToRgb(newHsv.h, newHsv.s, newHsv.v));
  };

  // Mouse drag handlers
  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (draggingSV) updateFromSV(e);
      if (draggingHue) updateFromHue(e);
    };
    const onUp = () => {
      setDraggingSV(false);
      setDraggingHue(false);
    };
    if (draggingSV || draggingHue) {
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseup", onUp);
    }
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
    };
  }, [draggingSV, draggingHue, hsv]);

  const setRGB = (key: "r" | "g" | "b", val: string) => {
    const v = Math.max(0, Math.min(255, parseInt(val) || 0));
    const newColor = { ...color, [key]: v };
    onChange(newColor);
  };

  return (
    <div className="flex flex-col gap-3">
      <span className="text-xs text-gray-400 uppercase tracking-wider">{label}</span>

      <div className="flex gap-3 items-start">
        {/* SV Square */}
        <canvas
          ref={svCanvasRef}
          className="rounded-lg cursor-crosshair"
          style={{ width: 200, height: 200 }}
          onMouseDown={(e) => { setDraggingSV(true); updateFromSV(e); }}
        />

        {/* Hue bar */}
        <canvas
          ref={hueCanvasRef}
          className="rounded cursor-pointer"
          style={{ width: 20, height: 200 }}
          onMouseDown={(e) => { setDraggingHue(true); updateFromHue(e); }}
        />

        {/* Controls */}
        <div className="flex flex-col gap-2 min-w-[120px]">
          {/* Preview */}
          <div
            className="w-full h-10 rounded-lg border border-dark-500"
            style={{ background: `rgb(${color.r},${color.g},${color.b})` }}
          />

          {/* RGB inputs */}
          {(["r", "g", "b"] as const).map((ch) => (
            <label key={ch} className="flex items-center gap-2">
              <span className="text-xs text-gray-500 w-3 uppercase">{ch}</span>
              <input
                type="number"
                min={0}
                max={255}
                value={color[ch]}
                onChange={(e) => setRGB(ch, e.target.value)}
                className="w-full bg-dark-700 border border-dark-500 rounded px-2 py-1 text-sm text-white
                  focus:outline-none focus:border-accent-cyan"
              />
            </label>
          ))}

          {/* Hex */}
          <div className="text-xs text-gray-500 text-center mt-1">
            #{color.r.toString(16).padStart(2, "0")}
            {color.g.toString(16).padStart(2, "0")}
            {color.b.toString(16).padStart(2, "0")}
          </div>
        </div>
      </div>

      {/* Presets */}
      <div className="flex gap-1.5 flex-wrap">
        {PRESETS.map((p, i) => (
          <button
            key={i}
            onClick={() => onChange(p)}
            className="w-7 h-7 rounded-md border border-dark-500 hover:scale-110 transition-transform"
            style={{ background: `rgb(${p.r},${p.g},${p.b})` }}
            title={`${p.r}, ${p.g}, ${p.b}`}
          />
        ))}
      </div>
    </div>
  );
}
