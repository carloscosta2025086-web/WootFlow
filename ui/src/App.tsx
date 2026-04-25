import { useState, useMemo } from "react";
import { useWebSocket } from "./hooks/useWebSocket";
import { Sidebar } from "./components/Sidebar";
import { EffectsPanel } from "./components/EffectsPanel";
import { SoundReactive } from "./components/SoundReactive";
import { PerKeyPanel } from "./components/PerKeyPanel";
import { Settings } from "./components/Settings";
import { KeyboardPreview } from "./components/KeyboardPreview";
import type { Page } from "./types";
import type { RGB } from "./types";

export default function App() {
  const { state, audio, frame, connected, send } = useWebSocket();
  const [page, setPage] = useState<Page>("effects");

  // Convert frame data to Map<string, RGB> for KeyboardPreview
  const keyColors = useMemo(() => {
    if (!frame?.colors) return undefined;
    const map = new Map<string, RGB>();
    for (const [key, val] of Object.entries(frame.colors)) {
      map.set(key, { r: val[0], g: val[1], b: val[2] });
    }
    return map;
  }, [frame]);

  if (!state) {
    return (
      <div className="h-screen bg-dark-900 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-accent-cyan border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-500 text-sm">A ligar ao servidor...</p>
          <p className="text-gray-600 text-xs mt-2">
            {connected ? "✓ WebSocket conectado, à espera de dados..." : "Tentando conectar..."}
          </p>
          <p className="text-gray-600 text-xs mt-1">
            Endpoints: ws://127.0.0.1:9120/ws
          </p>
          <p className="text-gray-500 text-xs mt-3 max-w-xs">
            Se isto demorar muito, abre o browser console (F12) para diagnósticos.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen bg-dark-900 text-white flex overflow-hidden">
      {/* Titlebar drag region */}
      <div
        className="fixed top-0 left-0 right-0 h-9 z-50"
        style={{ WebkitAppRegion: "drag" } as React.CSSProperties}
      />

      {/* Sidebar */}
      <Sidebar
        page={page}
        onPageChange={setPage}
        connected={state.connected}
        wsConnected={connected}
      />

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0 pt-9">
        {/* Top bar with keyboard preview (always visible) */}
        {page !== "perkey" && (
          <div className="bg-dark-800/50 border-b border-dark-600 p-4 flex justify-center shrink-0">
            <KeyboardPreview
              selectedKey={null}
              onKeyClick={() => {}}
              keyColors={keyColors}
            />
          </div>
        )}

        {/* Page content */}
        <div className="flex-1 p-6 overflow-y-auto custom-scroll">
          {page === "effects" && <EffectsPanel state={state} send={send} />}
          {page === "sound" && <SoundReactive state={state} audio={audio} send={send} />}
          {page === "perkey" && <PerKeyPanel state={state} send={send} />}
          {page === "settings" && (
            <Settings
              connected={state.connected}
              device={state.device}
              mode={state.mode}
              send={send}
            />
          )}
        </div>
      </div>
    </div>
  );
}
