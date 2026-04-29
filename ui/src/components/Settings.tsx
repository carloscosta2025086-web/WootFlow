interface Props {
  connected: boolean;
  device?: { model: string; layout: string };
  mode: string;
  send: (data: Record<string, unknown>) => void;
}

export function Settings({ connected, device, mode, send }: Props) {
  return (
    <div className="flex flex-col gap-6 h-full overflow-y-auto pr-2 custom-scroll">
      <div>
        <h2 className="text-lg font-semibold text-white">Definições</h2>
        <p className="text-xs text-gray-500">Configuração da aplicação</p>
      </div>

      {/* Device info */}
      <div className="bg-dark-800 rounded-xl border border-dark-600 p-5">
        <h3 className="text-sm font-medium text-gray-300 mb-3">Dispositivo</h3>
        <div className="flex items-center gap-3 mb-3">
          <div className={`w-3 h-3 rounded-full ${connected ? "bg-green-500 animate-pulse" : "bg-red-500"}`} />
          <span className="text-sm text-gray-400">
            {connected && device
              ? `${device.model} (${device.layout})`
              : connected
              ? "Teclado conectado"
              : "Nenhum teclado detectado"}
          </span>
        </div>
        <button
          onClick={() => send({ action: "reconnect" })}
          className="px-4 py-2 rounded-lg text-sm bg-dark-700 text-gray-300 border border-dark-500 hover:bg-dark-600 transition-all"
        >
          ↻ Reconectar
        </button>
      </div>

      {/* LEDs off */}
      <div className="bg-dark-800 rounded-xl border border-dark-600 p-5">
        <h3 className="text-sm font-medium text-gray-300 mb-3">LEDs</h3>
        <div className="flex gap-2">
          <button
            onClick={() => send({ action: "set_mode", mode: "off" })}
            className={`px-4 py-2 rounded-lg text-sm transition-all ${
              mode === "off"
                ? "bg-red-500/20 text-red-400 border border-red-500/30"
                : "bg-dark-700 text-gray-300 border border-dark-500 hover:bg-dark-600"
            }`}
          >
            ⏻ Desligar LEDs
          </button>
          {mode === "off" && (
            <button
              onClick={() => send({ action: "set_mode", mode: "effect" })}
              className="px-4 py-2 rounded-lg text-sm bg-accent-cyan/15 text-accent-cyan border border-accent-cyan/30 hover:bg-accent-cyan/25 transition-all"
            >
              ✦ Ligar LEDs
            </button>
          )}
        </div>
      </div>

      {/* About */}
      <div className="bg-dark-800 rounded-xl border border-dark-600 p-5">
        <h3 className="text-sm font-medium text-gray-300 mb-3">Sobre</h3>
        <div className="space-y-1 text-sm text-gray-500">
          <p>WootFlow Control v3.2.1</p>
          <p>Layout: ISO PT 60HE</p>
          <p>Backend: Python + FastAPI + WebSocket</p>
          <p>Frontend: React + Tailwind + pywebview</p>
        </div>
      </div>

      {/* Tech stack */}
      <div className="bg-dark-800 rounded-xl border border-dark-600 p-5">
        <h3 className="text-sm font-medium text-gray-300 mb-3">Stack</h3>
        <div className="grid grid-cols-2 gap-2 text-xs text-gray-500">
          <span>● WootFlow SDK Bridge</span>
          <span>● PyAudioWPATCH (WASAPI)</span>
          <span>● pynput (input hooks)</span>
          <span>● FastAPI + uvicorn</span>
          <span>● React 19</span>
          <span>● Tailwind CSS 3</span>
          <span>● pywebview</span>
          <span>● Vite</span>
        </div>
      </div>
    </div>
  );
}
