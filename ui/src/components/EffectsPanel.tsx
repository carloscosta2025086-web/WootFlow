import type { CSSProperties } from "react";
import type { AppState, RGB } from "../types";
import { ColorPicker } from "./ColorPicker";

interface Props {
  state: AppState;
  send: (data: Record<string, unknown>) => void;
}

// Effect categories for visual grouping
const CATEGORIES: Record<string, string[]> = {
  "Estáticas": ["solid_color", "gradient"],
  "Ondas": ["rainbow_wave", "color_wave", "ocean", "aurora", "liquid_flow"],
  "Pulso": ["breathing", "spectrum_cycle", "heartbeat"],
  "Reativas": ["reactive_typing", "ripple", "magnetic_keys", "jello"],
  "Partículas": ["raindrop", "sparkle", "starfield", "matrix_rain"],
  "Ambiente": ["fire", "lava", "screen_ambience"],
};

export function EffectsPanel({ state, send }: Props) {
  const setEffect = (name: string) => {
    send({ action: "set_effect", name });
  };

  const effectMap = new Map(state.effects);
  const magneticInfluence = state.effectParams?.magneticInfluence ?? 3.0;
  const liquidDeform = state.effectParams?.liquidDeform ?? 0.55;
  const brightnessPct = Math.round(state.brightness * 100);
  const speedPct = Math.round((state.speed / 5) * 100);
  const magneticPct = Math.round(((magneticInfluence - 1.2) / (6 - 1.2)) * 100);
  const deformPct = Math.round((liquidDeform / 1.5) * 100);

  return (
    <div className="flex flex-col gap-5 h-full overflow-y-auto pr-2 custom-scroll wf-page-entrance">
      {/* Effect grid by category */}
      {Object.entries(CATEGORIES).map(([cat, ids]) => (
        <section key={cat} className="wf-panel">
          <h3 className="wf-section-title">{cat}</h3>
          <div className="grid grid-cols-2 xl:grid-cols-3 gap-2">
            {ids.filter(id => effectMap.has(id)).map((id) => (
              <button
                key={id}
                onClick={() => setEffect(id)}
                className={`px-3 py-2.5 rounded-xl text-sm transition-all duration-200 text-left border
                  ${state.effect === id
                    ? "bg-white/10 text-white border-white/20 shadow-lg shadow-black/30"
                    : "bg-white/5 text-gray-300 border-white/10 hover:bg-white/10 hover:text-white"
                  }`}
              >
                {effectMap.get(id)}
              </button>
            ))}
          </div>
        </section>
      ))}

      {/* Controls */}
      <div className="flex flex-col gap-4 wf-panel">
        <h3 className="wf-section-title">Controlos</h3>

        {/* Brightness */}
        <label className="flex flex-col gap-1">
          <span className="text-xs text-gray-300 flex justify-between">
            Brilho
            <span className="text-white">{brightnessPct}%</span>
          </span>
          <input
            type="range"
            min={0}
            max={100}
            value={brightnessPct}
            onChange={(e) => send({ action: "set_brightness", value: +e.target.value / 100 })}
            className="wf-slider"
            style={{ "--p": `${brightnessPct}%` } as CSSProperties}
          />
        </label>

        {/* Speed */}
        <label className="flex flex-col gap-1">
          <span className="text-xs text-gray-300 flex justify-between">
            Velocidade
            <span className="text-white">{state.speed.toFixed(1)}x</span>
          </span>
          <input
            type="range"
            min={10}
            max={500}
            value={Math.round(state.speed * 100)}
            onChange={(e) => send({ action: "set_speed", value: +e.target.value / 100 })}
            className="wf-slider"
            style={{ "--p": `${speedPct}%` } as CSSProperties}
          />
        </label>

        {state.effect === "magnetic_keys" && (
          <label className="flex flex-col gap-1">
            <span className="text-xs text-gray-300 flex justify-between">
              Campo de Influência
              <span className="text-white">{magneticInfluence.toFixed(1)}</span>
            </span>
            <input
              type="range"
              min={12}
              max={60}
              value={Math.round(magneticInfluence * 10)}
              onChange={(e) =>
                send({
                  action: "set_effect_param",
                  param: "magneticInfluence",
                  value: +e.target.value / 10,
                })
              }
              className="wf-slider"
              style={{ "--p": `${magneticPct}%` } as CSSProperties}
            />
          </label>
        )}

        {state.effect === "liquid_flow" && (
          <label className="flex flex-col gap-1">
            <span className="text-xs text-gray-300 flex justify-between">
              Deformação por Input
              <span className="text-white">{liquidDeform.toFixed(2)}</span>
            </span>
            <input
              type="range"
              min={0}
              max={150}
              value={Math.round(liquidDeform * 100)}
              onChange={(e) =>
                send({
                  action: "set_effect_param",
                  param: "liquidDeform",
                  value: +e.target.value / 100,
                })
              }
              className="wf-slider"
              style={{ "--p": `${deformPct}%` } as CSSProperties}
            />
          </label>
        )}

        {/* Colors */}
        <div className="flex items-center justify-center py-1">
          <button
            onClick={() => send({ action: "set_color2", color: state.color1 })}
            className="wf-primary-btn"
            title="Sincroniza cor secundária com a cor primária"
          >
            Sync Cores
          </button>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          <ColorPicker
            label="Cor Primária"
            color={{ r: state.color1[0], g: state.color1[1], b: state.color1[2] }}
            onChange={(c: RGB) => send({ action: "set_color1", color: [c.r, c.g, c.b] })}
          />
          <ColorPicker
            label="Cor Secundária"
            color={{ r: state.color2[0], g: state.color2[1], b: state.color2[2] }}
            onChange={(c: RGB) => send({ action: "set_color2", color: [c.r, c.g, c.b] })}
          />
        </div>
      </div>
    </div>
  );
}
