import { useRef, useEffect, useCallback } from "react";
import type { KeyDef, RGB } from "../types";

// ── ISO PT 60HE layout ──
// Each key: [row(SDK), col(SDK), x_pos, width, label]
const LAYOUT: KeyDef[] = [
  // Row 1 — Number row
  { row: 1, col: 0, x: 0, w: 1, label: "Esc" },
  { row: 1, col: 1, x: 1, w: 1, label: "1" },
  { row: 1, col: 2, x: 2, w: 1, label: "2" },
  { row: 1, col: 3, x: 3, w: 1, label: "3" },
  { row: 1, col: 4, x: 4, w: 1, label: "4" },
  { row: 1, col: 5, x: 5, w: 1, label: "5" },
  { row: 1, col: 6, x: 6, w: 1, label: "6" },
  { row: 1, col: 7, x: 7, w: 1, label: "7" },
  { row: 1, col: 8, x: 8, w: 1, label: "8" },
  { row: 1, col: 9, x: 9, w: 1, label: "9" },
  { row: 1, col: 10, x: 10, w: 1, label: "0" },
  { row: 1, col: 11, x: 11, w: 1, label: "'" },
  { row: 1, col: 12, x: 12, w: 1, label: "«" },
  { row: 1, col: 13, x: 13, w: 2, label: "⌫" },

  // Row 2 — QWERTY
  { row: 2, col: 0, x: 0, w: 1.5, label: "Tab" },
  { row: 2, col: 1, x: 1.5, w: 1, label: "Q" },
  { row: 2, col: 2, x: 2.5, w: 1, label: "W" },
  { row: 2, col: 3, x: 3.5, w: 1, label: "E" },
  { row: 2, col: 4, x: 4.5, w: 1, label: "R" },
  { row: 2, col: 5, x: 5.5, w: 1, label: "T" },
  { row: 2, col: 6, x: 6.5, w: 1, label: "Y" },
  { row: 2, col: 7, x: 7.5, w: 1, label: "U" },
  { row: 2, col: 8, x: 8.5, w: 1, label: "I" },
  { row: 2, col: 9, x: 9.5, w: 1, label: "O" },
  { row: 2, col: 10, x: 10.5, w: 1, label: "P" },
  { row: 2, col: 11, x: 11.5, w: 1, label: "+" },
  { row: 2, col: 12, x: 12.5, w: 1, label: "´" },
  // Enter spans row 2 col 13 + row 3 col 13 (ISO L-shape, shown as rectangle on row 3)

  // Row 3 — Home row
  { row: 3, col: 0, x: 0, w: 1.75, label: "Caps" },
  { row: 3, col: 1, x: 1.75, w: 1, label: "A" },
  { row: 3, col: 2, x: 2.75, w: 1, label: "S" },
  { row: 3, col: 3, x: 3.75, w: 1, label: "D" },
  { row: 3, col: 4, x: 4.75, w: 1, label: "F" },
  { row: 3, col: 5, x: 5.75, w: 1, label: "G" },
  { row: 3, col: 6, x: 6.75, w: 1, label: "H" },
  { row: 3, col: 7, x: 7.75, w: 1, label: "J" },
  { row: 3, col: 8, x: 8.75, w: 1, label: "K" },
  { row: 3, col: 9, x: 9.75, w: 1, label: "L" },
  { row: 3, col: 10, x: 10.75, w: 1, label: "Ç" },
  { row: 3, col: 11, x: 11.75, w: 1, label: "º" },
  { row: 3, col: 12, x: 12.75, w: 1, label: "~" },
  { row: 3, col: 13, x: 13.75, w: 1.25, label: "↵" },

  // Row 4 — Shift row (ISO: col1 = <, Z at col2)
  { row: 4, col: 0, x: 0, w: 1.25, label: "Shift" },
  { row: 4, col: 1, x: 1.25, w: 1, label: "<" },
  { row: 4, col: 2, x: 2.25, w: 1, label: "Z" },
  { row: 4, col: 3, x: 3.25, w: 1, label: "X" },
  { row: 4, col: 4, x: 4.25, w: 1, label: "C" },
  { row: 4, col: 5, x: 5.25, w: 1, label: "V" },
  { row: 4, col: 6, x: 6.25, w: 1, label: "B" },
  { row: 4, col: 7, x: 7.25, w: 1, label: "N" },
  { row: 4, col: 8, x: 8.25, w: 1, label: "M" },
  { row: 4, col: 9, x: 9.25, w: 1, label: "," },
  { row: 4, col: 10, x: 10.25, w: 1, label: "." },
  { row: 4, col: 11, x: 11.25, w: 1, label: "-" },
  { row: 4, col: 13, x: 12.25, w: 2.75, label: "Shift" },

  // Row 5 — Bottom row
  { row: 5, col: 0, x: 0, w: 1.25, label: "Ctrl" },
  { row: 5, col: 1, x: 1.25, w: 1.25, label: "Win" },
  { row: 5, col: 2, x: 2.5, w: 1.25, label: "Alt" },
  // Spacebar — 7 individual LEDs (cols 3-9), switch at col 6
  { row: 5, col: 3, x: 3.75, w: 0.893, label: "" },
  { row: 5, col: 4, x: 4.643, w: 0.893, label: "" },
  { row: 5, col: 5, x: 5.536, w: 0.893, label: "" },
  { row: 5, col: 6, x: 6.429, w: 0.893, label: "" },
  { row: 5, col: 7, x: 7.321, w: 0.893, label: "" },
  { row: 5, col: 8, x: 8.214, w: 0.893, label: "" },
  { row: 5, col: 9, x: 9.107, w: 0.893, label: "" },
  { row: 5, col: 10, x: 10, w: 1.25, label: "AltGr" },
  { row: 5, col: 11, x: 11.25, w: 1.25, label: "Menu" },
  { row: 5, col: 12, x: 12.5, w: 1.25, label: "Ctrl" },
  { row: 5, col: 13, x: 13.75, w: 1.25, label: "Fn" },
];

const UNIT = 44;     // px per key unit
const GAP = 3;       // gap between keys
const PAD = 16;      // canvas padding
const RADIUS = 6;    // corner radius

interface Props {
  selectedKey: { row: number; col: number } | null;
  onKeyClick: (row: number, col: number) => void;
  keyColors?: Map<string, RGB>;
  accentColor?: string;
}

export function KeyboardPreview({
  selectedKey,
  onKeyClick,
  keyColors,
  accentColor = "#00ffc8",
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const totalW = 15 * UNIT + PAD * 2;
    const totalH = 5 * UNIT + PAD * 2;
    canvas.width = totalW * dpr;
    canvas.height = totalH * dpr;
    canvas.style.width = `${totalW}px`;
    canvas.style.height = `${totalH}px`;
    ctx.scale(dpr, dpr);

    // Background
    ctx.clearRect(0, 0, totalW, totalH);

    for (const key of LAYOUT) {
      const visualRow = key.row - 1; // SDK rows 1-5 → visual rows 0-4
      const x = PAD + key.x * UNIT + GAP / 2;
      const y = PAD + visualRow * UNIT + GAP / 2;
      const w = key.w * UNIT - GAP;
      const h = UNIT - GAP;

      // Key color
      const ck = keyColors?.get(`${key.row}-${key.col}`);
      const isSelected =
        selectedKey?.row === key.row && selectedKey?.col === key.col;

      // Background
      if (ck) {
        ctx.fillStyle = `rgb(${ck.r}, ${ck.g}, ${ck.b})`;
      } else {
        ctx.fillStyle = "#1e1e2e";
      }

      ctx.beginPath();
      ctx.roundRect(x, y, w, h, RADIUS);
      ctx.fill();

      // Border
      if (isSelected) {
        ctx.strokeStyle = accentColor;
        ctx.lineWidth = 2;
      } else {
        ctx.strokeStyle = "#333346";
        ctx.lineWidth = 1;
      }
      ctx.stroke();

      // Label
      const textBright = ck
        ? (ck.r * 0.299 + ck.g * 0.587 + ck.b * 0.114) > 128
        : false;
      ctx.fillStyle = textBright ? "#000000" : "#a0a0b8";
      ctx.font = "11px system-ui, -apple-system, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(key.label, x + w / 2, y + h / 2);
    }
  }, [selectedKey, keyColors, accentColor]);

  useEffect(() => {
    draw();
    window.addEventListener("resize", draw);
    return () => window.removeEventListener("resize", draw);
  }, [draw]);

  const handleClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    for (const key of LAYOUT) {
      const vr = key.row - 1;
      const x = PAD + key.x * UNIT + GAP / 2;
      const y = PAD + vr * UNIT + GAP / 2;
      const w = key.w * UNIT - GAP;
      const h = UNIT - GAP;
      if (mx >= x && mx <= x + w && my >= y && my <= y + h) {
        onKeyClick(key.row, key.col);
        return;
      }
    }
  };

  return (
    <canvas
      ref={canvasRef}
      onClick={handleClick}
      className="cursor-pointer rounded-xl"
      style={{ maxWidth: "100%" }}
    />
  );
}
