export interface AppState {
  connected: boolean;
  mode: "effect" | "audio" | "perkey" | "off";
  effect: string;
  effects: [string, string][]; // [id, name]
  brightness: number;
  speed: number;
  color1: number[];
  color2: number[];
  audioRunning: boolean;
  audioAvailable: boolean;
  pynputAvailable: boolean;
  device?: {
    model: string;
    layout: string;
  };
}

export interface AudioData {
  bands: number[];
  peaks: number[];
  volume: number;
}

export interface FrameData {
  colors: Record<string, number[]>; // "row-col" → [r, g, b]
  delta: boolean;
}

export type Page = "effects" | "sound" | "perkey" | "settings";

export interface HSV {
  h: number; // 0-360
  s: number; // 0-1
  v: number; // 0-1
}

export interface RGB {
  r: number;
  g: number;
  b: number;
}

// Keyboard layout: ISO PT 60HE
export interface KeyDef {
  row: number; // SDK row (1-5)
  col: number; // SDK col
  x: number;   // visual x position (units)
  w: number;   // width (units)
  label: string;
}
