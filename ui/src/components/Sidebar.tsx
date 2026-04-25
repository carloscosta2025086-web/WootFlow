import type { Page } from "../types";

const NAV_ITEMS: { id: Page; label: string; icon: string }[] = [
  { id: "effects", label: "Efeitos", icon: "✦" },
  { id: "sound", label: "Som", icon: "♫" },
  { id: "perkey", label: "Per-Key", icon: "⌨" },
  { id: "settings", label: "Definições", icon: "⚙" },
];

interface Props {
  page: Page;
  onPageChange: (p: Page) => void;
  connected: boolean;
  wsConnected: boolean;
}

export function Sidebar({ page, onPageChange, connected, wsConnected }: Props) {
  return (
    <aside className="w-16 bg-dark-800 border-r border-dark-600 flex flex-col items-center py-4 gap-1 select-none"
      style={{ WebkitAppRegion: "no-drag" } as React.CSSProperties}>

      {/* Logo */}
      <div className="mb-4 text-accent-cyan font-bold text-lg tracking-wider">W</div>

      {/* Nav buttons */}
      {NAV_ITEMS.map((item) => (
        <button
          key={item.id}
          onClick={() => onPageChange(item.id)}
          className={`w-11 h-11 rounded-lg flex flex-col items-center justify-center text-xs gap-0.5 transition-all duration-200
            ${page === item.id
              ? "bg-dark-500 text-accent-cyan shadow-lg shadow-accent-cyan/10"
              : "text-gray-500 hover:text-gray-300 hover:bg-dark-700"
            }`}
          title={item.label}
        >
          <span className="text-base">{item.icon}</span>
          <span className="text-[9px] leading-none">{item.label}</span>
        </button>
      ))}

      <div className="flex-1" />

      {/* Status */}
      <div className="flex flex-col items-center gap-2 mb-2">
        <div className={`w-2 h-2 rounded-full ${connected ? "bg-green-500" : "bg-red-500"}`}
          title={connected ? "Teclado conectado" : "Teclado desconectado"} />
        <div className={`w-2 h-2 rounded-full ${wsConnected ? "bg-accent-cyan" : "bg-gray-600"}`}
          title={wsConnected ? "Servidor online" : "Servidor offline"} />
      </div>
    </aside>
  );
}
