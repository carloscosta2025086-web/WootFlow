import { useEffect, useRef, useState, useCallback } from "react";
import type { AppState, AudioData, FrameData } from "../types";

function getWsCandidates(): string[] {
  const candidates = new Set<string>();

  if (typeof window !== "undefined") {
    const scheme = window.location.protocol === "https:" ? "wss" : "ws";
    if (window.location.host) {
      candidates.add(`${scheme}://${window.location.host}/ws`);
    }
  }

  candidates.add("ws://127.0.0.1:9120/ws");
  candidates.add("ws://localhost:9120/ws");
  return Array.from(candidates);
}

const RECONNECT_DELAY = 2000;
const CONNECT_TIMEOUT = 5000;

export function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null);
  const [state, setState] = useState<AppState | null>(null);
  const [audio, setAudio] = useState<AudioData | null>(null);
  const [frame, setFrame] = useState<FrameData | null>(null);
  const frameRef = useRef<Record<string, number[]>>({});
  const [connected, setConnected] = useState(false);
  const reconnectTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const connectTimer = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);
  const endpointIndex = useRef(0);
  const wsCandidates = useRef<string[]>(getWsCandidates());

  const connect = useCallback(() => {
    if (
      wsRef.current?.readyState === WebSocket.OPEN ||
      wsRef.current?.readyState === WebSocket.CONNECTING
    ) {
      return;
    }

    const urls = wsCandidates.current;
    const wsUrl = urls[endpointIndex.current % urls.length];

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    clearTimeout(connectTimer.current);
    connectTimer.current = setTimeout(() => {
      if (ws.readyState === WebSocket.CONNECTING) {
        ws.close();
      }
    }, CONNECT_TIMEOUT);

    ws.onopen = () => {
      clearTimeout(connectTimer.current);
      setConnected(true);
    };

    ws.onmessage = (ev) => {
      try {
        const msg = JSON.parse(ev.data);
        if (msg.type === "state") {
          setState(msg as AppState);
        } else if (msg.type === "audio") {
          setAudio(msg as AudioData);
        } else if (msg.type === "frame") {
          const fd = msg as FrameData;
          if (fd.delta) {
            // Merge delta into accumulated frame
            const merged = { ...frameRef.current };
            for (const [k, v] of Object.entries(fd.colors)) {
              if (v[0] === 0 && v[1] === 0 && v[2] === 0) {
                delete merged[k];
              } else {
                merged[k] = v;
              }
            }
            frameRef.current = merged;
          } else {
            // Full frame — replace
            frameRef.current = { ...fd.colors };
          }
          setFrame({ colors: frameRef.current, delta: false });
        }
      } catch {
        // ignore parse errors
      }
    };

    ws.onclose = () => {
      clearTimeout(connectTimer.current);
      setConnected(false);
      endpointIndex.current = (endpointIndex.current + 1) % wsCandidates.current.length;
      clearTimeout(reconnectTimer.current);
      reconnectTimer.current = setTimeout(connect, RECONNECT_DELAY);
    };

    ws.onerror = () => ws.close();
  }, []);

  useEffect(() => {
    connect();
    return () => {
      clearTimeout(connectTimer.current);
      clearTimeout(reconnectTimer.current);
      wsRef.current?.close();
    };
  }, [connect]);

  const send = useCallback((data: Record<string, unknown>) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  return { state, audio, frame, connected, send };
}
