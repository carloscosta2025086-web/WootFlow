import { useRef, useEffect, useCallback } from "react";
import type { CSSProperties } from "react";
import type { AppState, AudioData } from "../types";

interface Props {
  state: AppState;
  audio: AudioData | null;
  send: (data: Record<string, unknown>) => void;
}

const BAR_COLORS = [
  "#00ff55", "#22ff44", "#44ff33", "#66ff22", "#88ff11",
  "#aaee00", "#cccc00", "#eeaa00", "#ff8800", "#ff6600",
  "#ff4400", "#ff2200", "#ff0000", "#ff0044",
];

export function SoundReactive({ state, audio, send }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const sensitivity = state._sensitivity ?? 1.5;
  const smoothing = state._smoothing ?? 0.3;
  const sensPct = Math.round(((sensitivity - 0.1) / (5 - 0.1)) * 100);
  const smoothPct = Math.round(smoothing * 100);

  const drawBars = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const W = canvas.clientWidth;
    const H = canvas.clientHeight;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    ctx.scale(dpr, dpr);

    ctx.clearRect(0, 0, W, H);

    if (!audio) return;

    const numBands = audio.bands.length;
    const barW = (W - (numBands - 1) * 4) / numBands;
    const maxH = H - 20;

    for (let i = 0; i < numBands; i++) {
      const x = i * (barW + 4);
      const val = Math.min(1, audio.bands[i]);
      const h = val * maxH;
      const peak = Math.min(1, audio.peaks[i]) * maxH;

      // Bar gradient (bottom to top)
      const grad = ctx.createLinearGradient(x, H, x, H - maxH);
      grad.addColorStop(0, "#00ff55");
      grad.addColorStop(0.5, "#cccc00");
      grad.addColorStop(0.8, "#ff6600");
      grad.addColorStop(1, "#ff0044");

      // Bar
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.roundRect(x, H - h, barW, h, [3, 3, 0, 0]);
      ctx.fill();

      // Peak indicator
      if (peak > 2) {
        ctx.fillStyle = BAR_COLORS[i] || "#ff0044";
        ctx.fillRect(x, H - peak - 3, barW, 3);
      }

      // Frequency label
      ctx.fillStyle = "#555";
      ctx.font = "9px system-ui";
      ctx.textAlign = "center";
      const freqs = ["30", "60", "120", "250", "500", "1k", "2k", "4k", "6k", "8k", "10k", "12k", "14k", "16k"];
      ctx.fillText(freqs[i] || "", x + barW / 2, H - 2);
    }

    // Volume meter
    const volW = 4;
    const volH = audio.volume * maxH;
    ctx.fillStyle = "#00ffc8";
    ctx.fillRect(W - volW - 2, H - volH - 10, volW, volH);
  }, [audio]);

  useEffect(() => {
    drawBars();
  }, [drawBars]);

  // Redraw at ~30fps when audio is streaming
  useEffect(() => {
    if (!state.audioRunning) return;
    drawBars();
  }, [audio, state.audioRunning, drawBars]);

  const toggle = () => {
    if (state.audioRunning) {
      send({ action: "stop_audio" });
    } else {
      send({ action: "start_audio" });
    }
  };

  return (
    <div className="flex flex-col gap-4 h-full wf-page-entrance">
      {/* Header & toggle */}
      <div className="flex items-center justify-between wf-panel">
        <div>
          <h2 className="text-lg font-semibold text-white">Som Reativo</h2>
          <p className="text-xs text-gray-400">Equalizer em tempo real com captura WASAPI Loopback</p>
        </div>
        <button
          onClick={toggle}
          className={`px-5 py-2 rounded-xl font-medium text-sm transition-all duration-300 border
            ${state.audioRunning
              ? "bg-red-500/20 text-red-300 border-red-500/40 hover:bg-red-500/30"
              : "bg-white/10 text-white border-white/20 hover:bg-white/15"
            }`}
        >
          {state.audioRunning ? "⏹ Parar" : "▶ Iniciar"}
        </button>
      </div>

      {!state.audioAvailable && (
        <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl px-4 py-3 text-sm text-yellow-300">
          PyAudioWPATCH não disponível. Instala com: pip install pyaudiowpatch
        </div>
      )}

      {/* Equalizer visualization */}
      <div className="flex-1 wf-panel p-4 min-h-[220px]">
        <canvas
          ref={canvasRef}
          className="w-full h-full"
          style={{ minHeight: 180 }}
        />
      </div>

      {/* Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 wf-panel">
        <label className="flex flex-col gap-1">
          <span className="text-xs text-gray-300 flex justify-between">
            Sensibilidade
            <span className="text-white">{sensitivity.toFixed(1)}</span>
          </span>
          <input
            type="range"
            min={10}
            max={500}
            value={Math.round(sensitivity * 100)}
            onChange={(e) => send({ action: "set_audio_sensitivity", value: +e.target.value / 100 })}
            className="wf-slider"
            style={{ "--p": `${sensPct}%` } as CSSProperties}
          />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-xs text-gray-300 flex justify-between">
            Suavização
            <span className="text-white">{smoothing.toFixed(2)}</span>
          </span>
          <input
            type="range"
            min={0}
            max={95}
            value={Math.round(smoothing * 100)}
            onChange={(e) => send({ action: "set_audio_smoothing", value: +e.target.value / 100 })}
            className="wf-slider"
            style={{ "--p": `${smoothPct}%` } as CSSProperties}
          />
        </label>
      </div>
    </div>
  );
}
