import { useRef, useEffect, useCallback, useMemo, useState, type CSSProperties } from "react";
import type { HSV, RGB } from "../types";

function clamp(v: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, v));
}

function hsvToRgb(h: number, s: number, v: number): RGB {
  const c = v * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = v - c;
  let r = 0, g = 0, b = 0;
  if (h < 60) { r = c; g = x; }
  else if (h < 120) { r = x; g = c; }
  else if (h < 180) { g = c; b = x; }
  else if (h < 240) { g = x; b = c; }
  else if (h < 300) { r = x; b = c; }
  else { r = c; b = x; }
  return {
    r: Math.round((r + m) * 255),
    g: Math.round((g + m) * 255),
    b: Math.round((b + m) * 255),
  };
}

function rgbToHsv(r: number, g: number, b: number): HSV {
  const r1 = r / 255;
  const g1 = g / 255;
  const b1 = b / 255;
  const max = Math.max(r1, g1, b1);
  const min = Math.min(r1, g1, b1);
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

function rgbToHsl(r: number, g: number, b: number): { h: number; s: number; l: number } {
  const rn = r / 255;
  const gn = g / 255;
  const bn = b / 255;
  const max = Math.max(rn, gn, bn);
  const min = Math.min(rn, gn, bn);
  const l = (max + min) / 2;
  let h = 0;
  let s = 0;

  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case rn:
        h = (gn - bn) / d + (gn < bn ? 6 : 0);
        break;
      case gn:
        h = (bn - rn) / d + 2;
        break;
      default:
        h = (rn - gn) / d + 4;
        break;
    }
    h *= 60;
  }

  return { h, s: s * 100, l: l * 100 };
}

function hslToRgb(h: number, s: number, l: number): RGB {
  const sn = clamp(s / 100, 0, 1);
  const ln = clamp(l / 100, 0, 1);
  const c = (1 - Math.abs(2 * ln - 1)) * sn;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = ln - c / 2;
  let r = 0;
  let g = 0;
  let b = 0;

  if (h < 60) { r = c; g = x; }
  else if (h < 120) { r = x; g = c; }
  else if (h < 180) { g = c; b = x; }
  else if (h < 240) { g = x; b = c; }
  else if (h < 300) { r = x; b = c; }
  else { r = c; b = x; }

  return {
    r: Math.round((r + m) * 255),
    g: Math.round((g + m) * 255),
    b: Math.round((b + m) * 255),
  };
}

function rgbToHex(c: RGB): string {
  return `#${c.r.toString(16).padStart(2, "0")}${c.g.toString(16).padStart(2, "0")}${c.b.toString(16).padStart(2, "0")}`.toUpperCase();
}

function hexToRgb(hex: string): RGB | null {
  const clean = hex.trim().replace(/^#/, "");
  if (!/^[0-9a-fA-F]{6}$/.test(clean)) return null;
  return {
    r: parseInt(clean.slice(0, 2), 16),
    g: parseInt(clean.slice(2, 4), 16),
    b: parseInt(clean.slice(4, 6), 16),
  };
}

const PRESETS: RGB[] = [
  { r: 0, g: 255, b: 200 },
  { r: 0, g: 162, b: 255 },
  { r: 119, g: 67, b: 255 },
  { r: 255, g: 0, b: 123 },
  { r: 255, g: 74, b: 64 },
  { r: 255, g: 193, b: 7 },
  { r: 110, g: 255, b: 91 },
  { r: 255, g: 255, b: 255 },
  { r: 0, g: 0, b: 0 },
];

interface Props {
  color: RGB;
  onChange: (c: RGB) => void;
  label?: string;
}

export function ColorPicker({ color, onChange, label = "Cor" }: Props) {
  const svCanvasRef = useRef<HTMLCanvasElement>(null);
  const [hsv, setHsv] = useState<HSV>(() => rgbToHsv(color.r, color.g, color.b));
  const [draggingSV, setDraggingSV] = useState(false);
  const [hexInput, setHexInput] = useState<string>(rgbToHex(color));

  const historyKey = useMemo(() => `wootflow.colors.history.${label}`.toLowerCase(), [label]);
  const favKey = useMemo(() => `wootflow.colors.favs.${label}`.toLowerCase(), [label]);

  const [history, setHistory] = useState<string[]>(() => {
    try {
      const parsed = JSON.parse(localStorage.getItem(historyKey) || "[]");
      return Array.isArray(parsed) ? parsed.slice(0, 10) : [];
    } catch {
      return [];
    }
  });

  const [favorites, setFavorites] = useState<string[]>(() => {
    try {
      const parsed = JSON.parse(localStorage.getItem(favKey) || "[]");
      return Array.isArray(parsed) ? parsed.slice(0, 10) : [];
    } catch {
      return [];
    }
  });

  const currentHex = useMemo(() => rgbToHex(color), [color]);
  const currentHsl = useMemo(() => rgbToHsl(color.r, color.g, color.b), [color]);

  useEffect(() => {
    setHexInput(currentHex);
    const updated = rgbToHsv(color.r, color.g, color.b);
    if (Math.abs(updated.h - hsv.h) > 1 || Math.abs(updated.s - hsv.s) > 0.01 || Math.abs(updated.v - hsv.v) > 0.01) {
      setHsv(updated);
    }
  }, [color.r, color.g, color.b, currentHex]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setHistory((prev) => {
        if (prev[0] === currentHex) return prev;
        const next = [currentHex, ...prev.filter((c) => c !== currentHex)].slice(0, 10);
        localStorage.setItem(historyKey, JSON.stringify(next));
        return next;
      });
    }, 220);
    return () => window.clearTimeout(timer);
  }, [currentHex, historyKey]);

  const drawSV = useCallback(() => {
    const canvas = svCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const W = 168;
    const H = 168;
    canvas.width = W;
    canvas.height = H;

    const base = hsvToRgb(hsv.h, 1, 1);

    const gH = ctx.createLinearGradient(0, 0, W, 0);
    gH.addColorStop(0, "white");
    gH.addColorStop(1, `rgb(${base.r},${base.g},${base.b})`);
    ctx.fillStyle = gH;
    ctx.fillRect(0, 0, W, H);

    const gV = ctx.createLinearGradient(0, 0, 0, H);
    gV.addColorStop(0, "rgba(0,0,0,0)");
    gV.addColorStop(1, "rgba(0,0,0,1)");
    ctx.fillStyle = gV;
    ctx.fillRect(0, 0, W, H);

    const cx = hsv.s * W;
    const cy = (1 - hsv.v) * H;
    ctx.beginPath();
    ctx.arc(cx, cy, 7, 0, Math.PI * 2);
    ctx.strokeStyle = "#ffffff";
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(cx, cy, 10, 0, Math.PI * 2);
    ctx.strokeStyle = "rgba(0,0,0,0.45)";
    ctx.lineWidth = 3;
    ctx.stroke();
  }, [hsv.h, hsv.s, hsv.v]);

  useEffect(() => {
    drawSV();
  }, [drawSV]);

  const updateFromSV = (e: React.MouseEvent | MouseEvent) => {
    const canvas = svCanvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const s = clamp((e.clientX - rect.left) / rect.width, 0, 1);
    const v = clamp(1 - (e.clientY - rect.top) / rect.height, 0, 1);
    const newHsv = { ...hsv, s, v };
    setHsv(newHsv);
    onChange(hsvToRgb(newHsv.h, newHsv.s, newHsv.v));
  };

  useEffect(() => {
    const onMove = (e: MouseEvent) => {
      if (draggingSV) updateFromSV(e);
    };
    const onUp = () => setDraggingSV(false);
    if (draggingSV) {
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseup", onUp);
    }
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
    };
  }, [draggingSV, hsv]);

  const setRGB = (key: "r" | "g" | "b", val: string) => {
    const v = clamp(parseInt(val, 10) || 0, 0, 255);
    onChange({ ...color, [key]: v });
  };

  const setHSL = (key: "h" | "s" | "l", val: string) => {
    const hsl = {
      h: key === "h" ? clamp(parseInt(val, 10) || 0, 0, 360) : currentHsl.h,
      s: key === "s" ? clamp(parseInt(val, 10) || 0, 0, 100) : currentHsl.s,
      l: key === "l" ? clamp(parseInt(val, 10) || 0, 0, 100) : currentHsl.l,
    };
    onChange(hslToRgb(hsl.h, hsl.s, hsl.l));
  };

  const onHexBlur = () => {
    const parsed = hexToRgb(hexInput);
    if (parsed) onChange(parsed);
    else setHexInput(currentHex);
  };

  const toggleFavorite = () => {
    setFavorites((prev) => {
      const has = prev.includes(currentHex);
      const next = has ? prev.filter((x) => x !== currentHex) : [currentHex, ...prev].slice(0, 10);
      localStorage.setItem(favKey, JSON.stringify(next));
      return next;
    });
  };

  const pickScreenColor = async () => {
    try {
      const picker = (window as Window & { EyeDropper?: new () => { open: () => Promise<{ sRGBHex: string }> }; }).EyeDropper;
      if (!picker) return;
      const sample = await new picker().open();
      const parsed = hexToRgb(sample.sRGBHex);
      if (parsed) onChange(parsed);
    } catch {
      // Ignore when user cancels eyedropper.
    }
  };

  const updateHSVSlider = (key: "h" | "s" | "v", val: string) => {
    const next = {
      h: key === "h" ? clamp(parseInt(val, 10) || 0, 0, 360) : hsv.h,
      s: key === "s" ? clamp((parseInt(val, 10) || 0) / 100, 0, 1) : hsv.s,
      v: key === "v" ? clamp((parseInt(val, 10) || 0) / 100, 0, 1) : hsv.v,
    };
    setHsv(next);
    onChange(hsvToRgb(next.h, next.s, next.v));
  };

  return (
    <section
      className="wf-color-card"
      style={{
        "--cp-r": color.r,
        "--cp-g": color.g,
        "--cp-b": color.b,
      } as CSSProperties}
    >
      <header className="wf-color-header">
        <span className="wf-color-label">{label}</span>
        <div className="wf-chip-row">
          <button className="wf-icon-btn" onClick={toggleFavorite} title="Favorito">{favorites.includes(currentHex) ? "★" : "☆"}</button>
          <button className="wf-icon-btn" onClick={pickScreenColor} title="Eyedropper">⌁</button>
        </div>
      </header>

      <div className="wf-color-main">
        <canvas
          ref={svCanvasRef}
          className="wf-sv-canvas"
          onMouseDown={(e) => {
            setDraggingSV(true);
            updateFromSV(e);
          }}
        />

        <div className="wf-color-side">
          <div
            className="wf-color-preview"
            style={{
              background: `rgb(${color.r}, ${color.g}, ${color.b})`,
              boxShadow: `0 0 26px rgba(${color.r}, ${color.g}, ${color.b}, 0.42)`,
            }}
          />

          <div className="wf-value-stack">
            <label className="wf-input-row">
              <span>HEX</span>
              <input
                className="wf-field"
                value={hexInput}
                onChange={(e) => setHexInput(e.target.value)}
                onBlur={onHexBlur}
              />
            </label>
            <label className="wf-input-row">
              <span>R</span>
              <input className="wf-field" value={color.r} onChange={(e) => setRGB("r", e.target.value)} />
            </label>
            <label className="wf-input-row">
              <span>G</span>
              <input className="wf-field" value={color.g} onChange={(e) => setRGB("g", e.target.value)} />
            </label>
            <label className="wf-input-row">
              <span>B</span>
              <input className="wf-field" value={color.b} onChange={(e) => setRGB("b", e.target.value)} />
            </label>
            <label className="wf-input-row">
              <span>H</span>
              <input className="wf-field" value={Math.round(currentHsl.h)} onChange={(e) => setHSL("h", e.target.value)} />
            </label>
            <label className="wf-input-row">
              <span>S</span>
              <input className="wf-field" value={Math.round(currentHsl.s)} onChange={(e) => setHSL("s", e.target.value)} />
            </label>
            <label className="wf-input-row">
              <span>L</span>
              <input className="wf-field" value={Math.round(currentHsl.l)} onChange={(e) => setHSL("l", e.target.value)} />
            </label>
          </div>
        </div>
      </div>

      <div className="wf-slider-group">
        <label>
          <span>Hue</span>
          <input
            type="range"
            min={0}
            max={360}
            value={Math.round(hsv.h)}
            onChange={(e) => updateHSVSlider("h", e.target.value)}
            className="wf-slider wf-slider-hue"
            style={{ "--p": `${Math.round((hsv.h / 360) * 100)}%` } as CSSProperties}
          />
        </label>
        <label>
          <span>Saturation</span>
          <input
            type="range"
            min={0}
            max={100}
            value={Math.round(hsv.s * 100)}
            onChange={(e) => updateHSVSlider("s", e.target.value)}
            className="wf-slider"
            style={{ "--p": `${Math.round(hsv.s * 100)}%` } as CSSProperties}
          />
        </label>
        <label>
          <span>Value</span>
          <input
            type="range"
            min={0}
            max={100}
            value={Math.round(hsv.v * 100)}
            onChange={(e) => updateHSVSlider("v", e.target.value)}
            className="wf-slider"
            style={{ "--p": `${Math.round(hsv.v * 100)}%` } as CSSProperties}
          />
        </label>
      </div>

      <div className="wf-swatches">
        <div>
          <span className="wf-swatches-title">Presets</span>
          <div className="wf-dot-row">
            {PRESETS.map((p, i) => {
              const hex = rgbToHex(p);
              return (
                <button
                  key={`${hex}-${i}`}
                  className="wf-dot"
                  style={{ background: hex }}
                  title={hex}
                  onClick={() => onChange(p)}
                />
              );
            })}
          </div>
        </div>

        <div>
          <span className="wf-swatches-title">Histórico</span>
          <div className="wf-dot-row">
            {history.slice(0, 8).map((hex) => (
              <button
                key={hex}
                className="wf-dot"
                style={{ background: hex }}
                title={hex}
                onClick={() => {
                  const parsed = hexToRgb(hex);
                  if (parsed) onChange(parsed);
                }}
              />
            ))}
          </div>
        </div>

        <div>
          <span className="wf-swatches-title">Favoritos</span>
          <div className="wf-dot-row">
            {favorites.slice(0, 8).map((hex) => (
              <button
                key={hex}
                className="wf-dot"
                style={{ background: hex }}
                title={hex}
                onClick={() => {
                  const parsed = hexToRgb(hex);
                  if (parsed) onChange(parsed);
                }}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
