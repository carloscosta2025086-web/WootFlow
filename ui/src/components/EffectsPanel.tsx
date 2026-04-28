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

  return (
    <div className="flex flex-col gap-6 h-full overflow-y-auto pr-2 custom-scroll">
      {/* Effect grid by category */}
      {Object.entries(CATEGORIES).map(([cat, ids]) => (
        <div key={cat}>
          <h3 className="text-xs text-gray-500 uppercase tracking-wider mb-2">{cat}</h3>
          <div className="grid grid-cols-3 gap-2">
            {ids.filter(id => effectMap.has(id)).map((id) => (
              <button
                key={id}
                onClick={() => setEffect(id)}
                className={`px-3 py-2.5 rounded-lg text-sm transition-all duration-200 text-left
                  ${state.effect === id
                    ? "bg-accent-cyan/15 text-accent-cyan border border-accent-cyan/30 shadow-lg shadow-accent-cyan/5"
                    : "bg-dark-700 text-gray-300 border border-dark-500 hover:bg-dark-600 hover:text-white"
                  }`}
              >
                {effectMap.get(id)}
              </button>
            ))}
          </div>
        </div>
      ))}

      {/* Divider */}
      <div className="border-t border-dark-600" />

      {/* Controls */}
      <div className="flex flex-col gap-4">
        {/* Brightness */}
        <label className="flex flex-col gap-1">
          <span className="text-xs text-gray-400 flex justify-between">
            Brilho
            <span className="text-accent-cyan">{Math.round(state.brightness * 100)}%</span>
          </span>
          <input
            type="range"
            min={0}
            max={100}
            value={Math.round(state.brightness * 100)}
            onChange={(e) => send({ action: "set_brightness", value: +e.target.value / 100 })}
            className="accent-cyan-400"
          />
        </label>

        {/* Speed */}
        <label className="flex flex-col gap-1">
          <span className="text-xs text-gray-400 flex justify-between">
            Velocidade
            <span className="text-accent-cyan">{state.speed.toFixed(1)}x</span>
          </span>
          <input
            type="range"
            min={10}
            max={500}
            value={Math.round(state.speed * 100)}
            onChange={(e) => send({ action: "set_speed", value: +e.target.value / 100 })}
            className="accent-cyan-400"
          />
        </label>

        {state.effect === "magnetic_keys" && (
          <label className="flex flex-col gap-1">
            <span className="text-xs text-gray-400 flex justify-between">
              Campo de Influência
              <span className="text-accent-cyan">{magneticInfluence.toFixed(1)}</span>
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
              className="accent-cyan-400"
            />
          </label>
        )}

        {state.effect === "liquid_flow" && (
          <label className="flex flex-col gap-1">
            <span className="text-xs text-gray-400 flex justify-between">
              Deformação por Input
              <span className="text-accent-cyan">{liquidDeform.toFixed(2)}</span>
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
              className="accent-cyan-400"
            />
          </label>
        )}

        {/* Colors */}
        <div className="grid grid-cols-2 gap-4">
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
