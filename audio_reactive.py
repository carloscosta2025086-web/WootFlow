"""
Motor de áudio reativo para o teclado Wooting.
Captura áudio do sistema (WASAPI loopback via PyAudioWPATCH) e converte
em dados de frequência usando FFT para efeito equalizer no teclado.
"""

import threading
import time
import math

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import pyaudiowpatch as pyaudio
    HAS_PYAUDIO = True
except ImportError:
    HAS_PYAUDIO = False


# ============================================================================
# Configuração
# ============================================================================
BLOCK_SIZE = 1024
NUM_BANDS = 14     # Número de bandas de frequência (colunas do 60HE)


class AudioReactive:
    """
    Captura áudio do sistema via WASAPI loopback e calcula bandas de
    frequência em tempo real. Reage ao som geral do computador
    (altifalantes / headphones), não ao microfone.
    """

    def __init__(self):
        self._running = False
        self._thread = None
        self._pa = None
        self._stream = None
        self._lock = threading.Lock()

        # Dados de frequência (0.0 - 1.0 por banda)
        self._bands = [0.0] * NUM_BANDS
        self._peak = [0.0] * NUM_BANDS
        self._volume = 0.0

        # Configurações ajustáveis
        self.sensitivity = 1.5
        self.smoothing = 0.3
        self.peak_decay = 0.95
        self.noise_floor = 0.02

        # Dispositivo
        self._device_name = "Unknown"
        self._channels = 2
        self._sample_rate = 48000

    @staticmethod
    def available() -> bool:
        return HAS_NUMPY and HAS_PYAUDIO

    def _find_loopback(self):
        """Encontra o dispositivo WASAPI loopback do output padrão."""
        if not HAS_PYAUDIO:
            return None
        try:
            if self._pa is None:
                self._pa = pyaudio.PyAudio()
            p = self._pa

            wasapi = p.get_host_api_info_by_type(pyaudio.paWASAPI)
            default_out = p.get_device_info_by_index(wasapi["defaultOutputDevice"])

            # Procurar dispositivo loopback correspondente
            for i in range(p.get_device_count()):
                dev = p.get_device_info_by_index(i)
                if dev.get("isLoopbackDevice") and default_out["name"] in dev["name"]:
                    return dev

            # Fallback: qualquer dispositivo loopback
            for i in range(p.get_device_count()):
                dev = p.get_device_info_by_index(i)
                if dev.get("isLoopbackDevice"):
                    return dev

            return None
        except Exception:
            return None

    def start(self) -> bool:
        """Inicia a captura de áudio do sistema."""
        if not self.available():
            return False
        if self._running:
            return True

        loopback = self._find_loopback()
        if loopback is None:
            return False

        self._device_name = loopback["name"].replace(" [Loopback]", "")
        self._channels = loopback["maxInputChannels"]
        self._sample_rate = int(loopback["defaultSampleRate"])

        self._running = True
        self._thread = threading.Thread(
            target=self._capture_loop,
            args=(loopback["index"],),
            daemon=True,
        )
        self._thread.start()
        return True

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)
            self._thread = None
        if self._pa:
            try:
                self._pa.terminate()
            except Exception:
                pass
            self._pa = None

    @property
    def running(self) -> bool:
        return self._running

    @property
    def device_name(self) -> str:
        return self._device_name

    def get_bands(self) -> list[float]:
        with self._lock:
            return self._bands.copy()

    def get_peaks(self) -> list[float]:
        with self._lock:
            return self._peak.copy()

    def get_volume(self) -> float:
        with self._lock:
            return self._volume

    def _capture_loop(self, device_index: int):
        """Thread de captura de áudio do sistema."""
        try:
            if self._pa is None:
                self._pa = pyaudio.PyAudio()

            self._stream = self._pa.open(
                format=pyaudio.paFloat32,
                channels=self._channels,
                rate=self._sample_rate,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=BLOCK_SIZE,
            )

            while self._running:
                try:
                    raw = self._stream.read(BLOCK_SIZE, exception_on_overflow=False)
                    data = np.frombuffer(raw, dtype=np.float32)
                    self._process_audio(data, self._sample_rate)
                except Exception:
                    time.sleep(0.01)

            self._stream.stop_stream()
            self._stream.close()
        except Exception:
            self._running = False

    def _process_audio(self, data: "np.ndarray", sr: int):
        """Processa o bloco de áudio: FFT → bandas de frequência."""
        # Converter para mono se stereo
        if self._channels > 1:
            mono = data.reshape(-1, self._channels).mean(axis=1)
        else:
            mono = data

        # Volume RMS
        rms = float(np.sqrt(np.mean(mono ** 2)))
        volume = min(1.0, rms * self.sensitivity * 10)

        # Aplicar janela de Hanning antes do FFT
        windowed = mono * np.hanning(len(mono))

        # FFT
        fft = np.abs(np.fft.rfft(windowed))
        fft_len = len(fft)

        # Mapear frequências para bandas (escala logarítmica)
        min_freq = 30
        max_freq = min(16000, sr // 2)
        band_edges = np.logspace(
            np.log10(min_freq), np.log10(max_freq), NUM_BANDS + 1
        )

        freq_per_bin = sr / (2 * fft_len)
        new_bands = []
        for i in range(NUM_BANDS):
            lo = int(band_edges[i] / freq_per_bin)
            hi = int(band_edges[i + 1] / freq_per_bin)
            lo = max(1, min(lo, fft_len - 1))
            hi = max(lo + 1, min(hi, fft_len))
            band_val = float(np.mean(fft[lo:hi]))
            band_val = min(1.0, band_val * self.sensitivity * 4)
            if band_val < self.noise_floor:
                band_val = 0.0
            new_bands.append(band_val)

        # Suavização e picos
        with self._lock:
            for i in range(NUM_BANDS):
                self._bands[i] = (
                    self._bands[i] * self.smoothing
                    + new_bands[i] * (1 - self.smoothing)
                )
                if self._bands[i] > self._peak[i]:
                    self._peak[i] = self._bands[i]
                else:
                    self._peak[i] *= self.peak_decay
                    if self._peak[i] < self.noise_floor:
                        self._peak[i] = 0.0

            self._volume = volume * (1 - self.smoothing) + self._volume * self.smoothing
