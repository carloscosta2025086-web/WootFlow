"""
Screen Ambience - Captura e repliquação dinâmica de cores do ecrã em tempo real.
Análise contínua do conteúdo visual com sincronização de iluminação RGB.

Funcionalidades:
- Captura de ecrã otimizada
- Análise de cores dominantes por regiões (grid 3x3 ou 5x5)
- Suavização temporal (fade smoothing)
- Suporte multi-display
- Modos: Cinemático (suave), Dinâmico (rápido), Gaming (alta resposta)
"""

import time
import threading
from collections import deque
from typing import Dict, Hashable, List, Optional, Tuple
from dataclasses import dataclass
import numpy as np

try:
    from PIL import ImageGrab, ImageOps
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import mss
    HAS_MSS = True
except ImportError:
    HAS_MSS = False


# ============================================================================
# TIPOS E CONFIGURAÇÕES
# ============================================================================

@dataclass
class ScreenAmbienceConfig:
    """Configuração do perfil Screen Ambience."""
    mode: str = "cinematic"  # "cinematic", "dynamic", "gaming"
    fps: int = 60  # 30-120 FPS
    grid_size: int = 3  # 3x3 ou 5x5
    brightness: float = 1.0  # 0.0-2.0
    color_sensitivity: str = "medium"  # "low", "medium", "high"
    smoothing_factor: float = 0.7  # 0.0-1.0 (maior = mais suave)
    exclude_black: bool = True  # Excluir pixels muito escuros
    exclude_white: bool = False  # Excluir pixels muito claros
    black_threshold: int = 30  # RGB < threshold
    white_threshold: int = 220  # RGB > threshold
    monitor_index: int = 0  # Monitor principal
    sample_area_scale: float = 0.85  # Tamanho relativo da área amostrada por tecla


@dataclass
class RegionColor:
    """Cor de uma região com histórico para suavização."""
    region_id: int
    current_color: Tuple[int, int, int]
    previous_color: Tuple[int, int, int]
    color_history: deque  # Últimas N cores para smoothing


class ScreenCapture:
    """Captura otimizada de ecrã com suporte a múltiplos monitores."""
    
    def __init__(self, monitor_index: int = 0, scale_factor: float = 0.5):
        """
        Inicializa captura de ecrã.
        
        Args:
            monitor_index: Índice do monitor (0 = principal)
            scale_factor: Fator de escala (0.5 = 50% menor)
        """
        self.monitor_index = monitor_index
        self.scale_factor = scale_factor
        self.capture_method = None
        self._init_capture()
    
    def _init_capture(self):
        """Detecta melhor método de captura disponível."""
        if HAS_MSS:
            self.capture_method = "mss"
            try:
                self.mss_instance = mss.mss()
            except Exception as e:
                print(f"[Screen Ambience] MSS init failed: {e}")
                self.mss_instance = None
        
        if not self.capture_method and HAS_PIL:
            self.capture_method = "pil"
        
        if not self.capture_method:
            raise RuntimeError(
                "Nenhum módulo de captura disponível. "
                "Instale 'mss' ou 'Pillow': pip install mss Pillow"
            )
        
        print(f"[Screen Ambience] Usando método de captura: {self.capture_method}")
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """Captura frame atual do ecrã."""
        try:
            if self.capture_method == "mss" and self.mss_instance:
                return self._capture_mss()
            else:
                return self._capture_pil()
        except Exception as e:
            print(f"[Screen Ambience] Erro na captura: {e}")
            return None
    
    def _capture_mss(self) -> Optional[np.ndarray]:
        """Captura via MSS (mais rápido)."""
        monitors = self.mss_instance.monitors
        monitor_slot = self.monitor_index + 1  # slot 0 agrega todos os monitores
        if monitor_slot >= len(monitors):
            return None
        
        monitor = monitors[monitor_slot]
        screenshot = self.mss_instance.grab(monitor)
        
        # Converter para numpy array
        frame = np.array(screenshot)
        # MSS retorna BGRA — converter para RGB invertendo os canais B e R
        frame = frame[:, :, 2::-1]  # BGRA[:, :, 2::-1] = RGB

        # Redimensionar se necessário
        if self.scale_factor < 1.0:
            # Downsample leve sem depender de PIL no caminho MSS.
            step = max(1, int(round(1.0 / self.scale_factor)))
            frame = frame[::step, ::step]
        
        return frame
    
    def _capture_pil(self) -> Optional[np.ndarray]:
        """Captura via PIL ImageGrab."""
        screenshot = ImageGrab.grab()
        
        # Redimensionar se necessário
        if self.scale_factor < 1.0:
            new_size = (
                int(screenshot.width * self.scale_factor),
                int(screenshot.height * self.scale_factor)
            )
            screenshot = screenshot.resize(new_size, ImageOps.LANCZOS)
        
        frame = np.array(screenshot)
        if frame.shape[2] == 4:  # RGBA
            frame = frame[:, :, :3]
        
        return frame


class ColorAnalyzer:
    """Análise de cores dominantes em regiões."""
    
    def __init__(self, config: ScreenAmbienceConfig):
        self.config = config
        self.grid_size = config.grid_size
    
    def analyze_frame(self, frame: np.ndarray) -> List[Tuple[int, int, int]]:
        """
        Analisa frame e retorna cores dominantes por região.
        
        Args:
            frame: Array numpy (H, W, 3) do ecrã
        
        Returns:
            Lista de cores RGB por região (grid_size * grid_size elementos)
        """
        height, width = frame.shape[:2]
        colors = []
        
        region_height = height // self.grid_size
        region_width = width // self.grid_size
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                y_start = row * region_height
                y_end = (row + 1) * region_height if row < self.grid_size - 1 else height
                x_start = col * region_width
                x_end = (col + 1) * region_width if col < self.grid_size - 1 else width
                
                region = frame[y_start:y_end, x_start:x_end]
                dominant_color = self._get_dominant_color(region)
                colors.append(dominant_color)
        
        return colors

    def analyze_regions(
        self,
        frame: np.ndarray,
        sample_regions: Dict[Hashable, Tuple[float, float, float, float]],
    ) -> Dict[Hashable, Tuple[int, int, int]]:
        """Analisa pequenas regiões normalizadas do frame e retorna cor por ID."""
        height, width = frame.shape[:2]
        colors: Dict[Hashable, Tuple[int, int, int]] = {}

        for sample_id, (center_x, center_y, region_width, region_height) in sample_regions.items():
            half_width = max(1, int(round((region_width * width) / 2)))
            half_height = max(1, int(round((region_height * height) / 2)))
            x = min(width - 1, max(0, int(round(center_x * (width - 1)))))
            y = min(height - 1, max(0, int(round(center_y * (height - 1)))))

            x_start = max(0, x - half_width)
            x_end = min(width, x + half_width + 1)
            y_start = max(0, y - half_height)
            y_end = min(height, y + half_height + 1)

            region = frame[y_start:y_end, x_start:x_end]
            colors[sample_id] = self._get_dominant_color(region)

        return colors
    
    def _get_dominant_color(self, region: np.ndarray) -> Tuple[int, int, int]:
        """Extrai cor dominante de uma região usando média ponderada por saturação."""
        if region.size == 0:
            return (0, 0, 0)

        # Normalizar para (N, 3)
        pixels = region.reshape(-1, 3).astype(np.float32)

        # Filtrar pixels negros usando brilho (canal máximo).
        # Anteriormente usava np.all(canal > threshold) que eliminava pixels
        # coloridos escuros (ex. roxo escuro R=80, G=15, B=180 → excluído
        # porque G<30). Agora só exclui se o pixel for realmente escuro em todos
        # os canais (brightness = max channel).
        if self.config.exclude_black:
            brightness = np.max(pixels, axis=1)
            pixels = pixels[brightness > self.config.black_threshold]

        if self.config.exclude_white:
            min_ch = np.min(pixels, axis=1)
            pixels = pixels[min_ch < self.config.white_threshold]

        if len(pixels) == 0:
            return (0, 0, 0)

        # Peso por saturação: pixels mais vivos (alta saturação) dominam.
        # Substitui a mediana que desaturava quando a região tinha cores mistas.
        max_ch = np.max(pixels, axis=1)
        min_ch_f = np.min(pixels, axis=1)
        saturation = (max_ch - min_ch_f) / (max_ch + 1e-6)
        # Base weight de 0.2 garante que regiões neutras (cinzento/branco)
        # também produzem uma cor em vez de devolver preto.
        weights = saturation + 0.2
        total_weight = float(weights.sum())

        weighted = (pixels * weights[:, np.newaxis]).sum(axis=0) / total_weight

        # Aplicar sensibilidade de cor
        if self.config.color_sensitivity == "low":
            weighted = weighted * 0.6
        elif self.config.color_sensitivity == "high":
            weighted = np.clip(weighted * 1.4, 0, 255)

        # Aplicar brilho global
        weighted = np.clip(weighted * self.config.brightness, 0, 255)

        return tuple(int(c) for c in weighted)


class TemporalSmoother:
    """Suavização temporal para evitar flicker."""
    
    def __init__(self, smoothing_factor: float = 0.7, history_size: int = 5):
        """
        Args:
            smoothing_factor: 0.0 (sem suavização) a 1.0 (máxima suavização)
            history_size: Número de frames anteriores a considerar
        """
        self.smoothing_factor = smoothing_factor
        self.history_size = history_size
        self.color_history: Dict[Hashable, deque] = {}
    
    def smooth(self, region_id: Hashable, color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """
        Suaviza cor aplicando exponential moving average.
        
        Args:
            region_id: ID da região
            color: Cor RGB atual
        
        Returns:
            Cor suavizada
        """
        if region_id not in self.color_history:
            self.color_history[region_id] = deque([color], maxlen=self.history_size)
            return color
        
        history = self.color_history[region_id]
        history.append(color)
        
        # Média ponderada exponencial
        smoothed = [0, 0, 0]
        total_weight = 0
        
        for i, prev_color in enumerate(reversed(history)):
            weight = (self.smoothing_factor ** i)
            for j in range(3):
                smoothed[j] += prev_color[j] * weight
            total_weight += weight
        
        smoothed = tuple(int(c / total_weight) for c in smoothed)
        return smoothed


class ScreenAmbienceEngine:
    """Motor principal do Screen Ambience."""
    
    def __init__(self, config: Optional[ScreenAmbienceConfig] = None):
        self.config = config or ScreenAmbienceConfig()
        self.is_running = False
        self.thread = None
        
        # Componentes
        self.capture = ScreenCapture(
            monitor_index=self.config.monitor_index,
            scale_factor=0.35  # 35% da resolução para performance
        )
        self.analyzer = ColorAnalyzer(self.config)
        self.smoother = TemporalSmoother(self.config.smoothing_factor)
        
        # Callbacks
        self.on_colors_updated = None
        self.sample_regions: Dict[Hashable, Tuple[float, float, float, float]] = {}
        
        # Performance tracking
        self.frame_times = deque(maxlen=30)
        self.last_frame_time = time.time()
    
    def set_on_colors_updated(self, callback):
        """Define callback para quando cores forem atualizadas."""
        self.on_colors_updated = callback

    def set_sample_regions(self, sample_regions: Dict[Hashable, Tuple[float, float, float, float]]):
        """Define regiões normalizadas para amostragem por LED/tecla."""
        self.sample_regions = dict(sample_regions)
    
    def start(self):
        """Inicia o engine."""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print(f"[Screen Ambience] Engine iniciado - Mode: {self.config.mode}, FPS: {self.config.fps}")
    
    def stop(self):
        """Para o engine."""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        print("[Screen Ambience] Engine parado")
    
    def _run_loop(self):
        """Loop principal de captura e análise."""
        frame_time = 1.0 / self.config.fps
        
        while self.is_running:
            loop_start = time.time()
            
            # Capturar frame
            frame = self.capture.capture_frame()
            if frame is None:
                time.sleep(0.01)
                continue
            
            if self.sample_regions:
                raw_colors = self.analyzer.analyze_regions(frame, self.sample_regions)
                smoothed_colors = {
                    sample_id: self.smoother.smooth(sample_id, color)
                    for sample_id, color in raw_colors.items()
                }
            else:
                raw_colors = self.analyzer.analyze_frame(frame)

                # Suavizar cores
                smoothed_colors = []
                for region_id, color in enumerate(raw_colors):
                    smoothed_color = self.smoother.smooth(region_id, color)
                    smoothed_colors.append(smoothed_color)
            
            # Callback
            if self.on_colors_updated:
                try:
                    self.on_colors_updated(smoothed_colors)
                except Exception as e:
                    print(f"[Screen Ambience] Erro no callback: {e}")
            
            # Frame timing
            elapsed = time.time() - loop_start
            self.frame_times.append(elapsed)
            
            # Sleep para manter FPS
            sleep_time = max(0, frame_time - elapsed)
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas de performance."""
        if not self.frame_times:
            return {}
        
        frame_times_list = list(self.frame_times)
        avg_frame_time = sum(frame_times_list) / len(frame_times_list)
        actual_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
        
        return {
            "actual_fps": actual_fps,
            "avg_frame_time_ms": avg_frame_time * 1000,
            "mode": self.config.mode,
            "grid_size": self.config.grid_size,
        }


def create_ambience_engine(mode: str = "cinematic", fps: int = 60) -> ScreenAmbienceEngine:
    """Factory para criar engine com modo pré-configurado."""
    config_preset = {
        "cinematic": {
            "fps": 30,
            "grid_size": 3,
            "smoothing_factor": 0.85,
            "color_sensitivity": "medium",
            "brightness": 0.9,
        },
        "dynamic": {
            "fps": 60,
            "grid_size": 4,
            "smoothing_factor": 0.6,
            "color_sensitivity": "high",
            "brightness": 1.0,
        },
        "gaming": {
            "fps": 120,
            "grid_size": 5,
            "smoothing_factor": 0.4,
            "color_sensitivity": "high",
            "brightness": 1.2,
        },
    }
    
    if mode not in config_preset:
        mode = "cinematic"
    
    preset = config_preset[mode]
    config = ScreenAmbienceConfig(mode=mode, fps=fps, **preset)
    
    return ScreenAmbienceEngine(config)
