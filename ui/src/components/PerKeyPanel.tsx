import { useState } from "react";
import type { AppState, RGB } from "../types";
import { ColorPicker } from "./ColorPicker";
import { KeyboardPreview } from "./KeyboardPreview";

interface Props {
  state: AppState;
  send: (data: Record<string, unknown>) => void;
}

export function PerKeyPanel({ state, send }: Props) {
  const [selectedKey, setSelectedKey] = useState<{ row: number; col: number } | null>(null);
  const [currentColor, setCurrentColor] = useState<RGB>({ r: 0, g: 255, b: 200 });
  const [keyColors, setKeyColors] = useState<Map<string, RGB>>(new Map());

  const activateMode = () => {
    send({ action: "set_mode", mode: "perkey" });
  };

  const handleKeyClick = (row: number, col: number) => {
    setSelectedKey({ row, col });
    // Apply current color to clicked key
    const newColors = new Map(keyColors);
    newColors.set(`${row}-${col}`, { ...currentColor });
    setKeyColors(newColors);
    send({
      action: "set_perkey",
      row,
      col,
      color: [currentColor.r, currentColor.g, currentColor.b],
    });
  };

  const applyAll = () => {
    send({ action: "set_all_perkey", color: [currentColor.r, currentColor.g, currentColor.b] });
    // Fill all possible key positions visually (SDK rows 1-5, cols 0-13)
    const newColors = new Map<string, RGB>();
    for (let row = 1; row <= 5; row++) {
      for (let col = 0; col <= 13; col++) {
        newColors.set(`${row}-${col}`, { ...currentColor });
      }
    }
    setKeyColors(newColors);
  };

  return (
    <div className="flex flex-col gap-5 h-full overflow-y-auto pr-2 custom-scroll">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-white">Edição Per-Key</h2>
          <p className="text-xs text-gray-500">Clica numa tecla para aplicar a cor selecionada</p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={activateMode}
            className={`px-4 py-2 rounded-lg text-sm transition-all
              ${state.mode === "perkey"
                ? "bg-accent-cyan/15 text-accent-cyan border border-accent-cyan/30"
                : "bg-dark-700 text-gray-400 border border-dark-500 hover:bg-dark-600"
              }`}
          >
            {state.mode === "perkey" ? "✓ Ativo" : "Ativar"}
          </button>
          <button
            onClick={applyAll}
            className="px-4 py-2 rounded-lg text-sm bg-dark-700 text-gray-300 border border-dark-500 hover:bg-dark-600"
          >
            Aplicar a Todas
          </button>
          <button
            onClick={() => {
              setKeyColors(new Map());
              send({ action: "reset_perkey" });
            }}
            className="px-4 py-2 rounded-lg text-sm bg-dark-700 text-gray-300 border border-dark-500 hover:bg-dark-600"
          >
            ↺ Reset
          </button>
        </div>
      </div>

      {/* Keyboard */}
      <div className="bg-dark-800 rounded-xl border border-dark-600 p-4 flex justify-center">
        <KeyboardPreview
          selectedKey={selectedKey}
          onKeyClick={handleKeyClick}
          keyColors={keyColors}
        />
      </div>

      {/* Color picker */}
      <ColorPicker
        label="Cor da Tecla"
        color={currentColor}
        onChange={(c) => setCurrentColor(c)}
      />

      {selectedKey && (
        <p className="text-xs text-gray-500">
          Tecla selecionada: Row {selectedKey.row}, Col {selectedKey.col}
        </p>
      )}
    </div>
  );
}
