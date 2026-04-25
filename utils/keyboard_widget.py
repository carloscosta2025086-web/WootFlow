"""
Widget visual do teclado Wooting 60HE para CustomTkinter.
Mostra uma representação gráfica do teclado com cores per-key,
clicável para edição individual de teclas.
"""

import customtkinter as ctk
import math


# ============================================================================
# Layout do teclado 60HE ISO PT (posições e tamanhos das teclas)
# Cada tecla: (row, col, x, width, label)
# row/col = posições SDK reais (rows 1-5, cols 0-13)
# x e width em unidades de 1U (uma tecla standard)
# ============================================================================
KEYBOARD_LAYOUT_60HE = [
    # Row 1 (SDK): ESC, 1-0, ', «, BACKSPACE
    [
        (1, 0, 0, 1.0, "Esc"),
        (1, 1, 1, 1.0, "1"), (1, 2, 2, 1.0, "2"), (1, 3, 3, 1.0, "3"),
        (1, 4, 4, 1.0, "4"), (1, 5, 5, 1.0, "5"), (1, 6, 6, 1.0, "6"),
        (1, 7, 7, 1.0, "7"), (1, 8, 8, 1.0, "8"), (1, 9, 9, 1.0, "9"),
        (1, 10, 10, 1.0, "0"), (1, 11, 11, 1.0, "'"), (1, 12, 12, 1.0, "«"),
        (1, 13, 13, 2.0, "⌫"),
    ],
    # Row 2 (SDK): TAB, Q-P, +, ´, Enter top (ISO)
    [
        (2, 0, 0, 1.5, "Tab"),
        (2, 1, 1.5, 1.0, "Q"), (2, 2, 2.5, 1.0, "W"), (2, 3, 3.5, 1.0, "E"),
        (2, 4, 4.5, 1.0, "R"), (2, 5, 5.5, 1.0, "T"), (2, 6, 6.5, 1.0, "Y"),
        (2, 7, 7.5, 1.0, "U"), (2, 8, 8.5, 1.0, "I"), (2, 9, 9.5, 1.0, "O"),
        (2, 10, 10.5, 1.0, "P"), (2, 11, 11.5, 1.0, "+"), (2, 12, 12.5, 1.0, "´"),
        (2, 13, 13.5, 1.5, "↵"),
    ],
    # Row 3 (SDK): CAPS, A-L, Ç, º, ~, ENTER
    [
        (3, 0, 0, 1.75, "Caps"),
        (3, 1, 1.75, 1.0, "A"), (3, 2, 2.75, 1.0, "S"), (3, 3, 3.75, 1.0, "D"),
        (3, 4, 4.75, 1.0, "F"), (3, 5, 5.75, 1.0, "G"), (3, 6, 6.75, 1.0, "H"),
        (3, 7, 7.75, 1.0, "J"), (3, 8, 8.75, 1.0, "K"), (3, 9, 9.75, 1.0, "L"),
        (3, 10, 10.75, 1.0, "Ç"), (3, 11, 11.75, 1.0, "º"),
        (3, 12, 12.75, 1.0, "~"),
        (3, 13, 13.75, 1.25, "↵"),
    ],
    # Row 4 (SDK): LSHIFT (ISO), <, Z-/, RSHIFT
    [
        (4, 0, 0, 1.25, "⇧"),
        (4, 1, 1.25, 1.0, "<"),
        (4, 2, 2.25, 1.0, "Z"), (4, 3, 3.25, 1.0, "X"), (4, 4, 4.25, 1.0, "C"),
        (4, 5, 5.25, 1.0, "V"), (4, 6, 6.25, 1.0, "B"), (4, 7, 7.25, 1.0, "N"),
        (4, 8, 8.25, 1.0, "M"), (4, 9, 9.25, 1.0, ","), (4, 10, 10.25, 1.0, "."),
        (4, 11, 11.25, 1.0, "-"),
        (4, 13, 12.25, 2.75, "⇧"),
    ],
    # Row 5 (SDK): LCTRL, LWIN, LALT, SPACE, ALTGR, MENU, RCTRL, FN
    [
        (5, 0, 0, 1.25, "Ctrl"),
        (5, 1, 1.25, 1.25, "Win"),
        (5, 2, 2.5, 1.25, "Alt"),
        (5, 6, 3.75, 6.25, ""),
        (5, 10, 10.0, 1.0, "AltGr"),
        (5, 11, 11.0, 1.0, "≡"),
        (5, 12, 12.0, 1.0, "Ctrl"),
        (5, 13, 13.0, 2.0, "Fn"),
    ],
]


class KeyboardWidget(ctk.CTkCanvas):
    """
    Widget visual do teclado Wooting 60HE.
    Mostra as teclas com cores, permite clicar para selecionar/editar.
    """

    def __init__(self, master, width=650, height=220, **kwargs):
        super().__init__(master, width=width, height=height,
                         bg="#0e0e16", highlightthickness=0, **kwargs)

        self._width = width
        self._height = height
        self._key_rects = {}     # (row, col) → canvas rectangle id
        self._key_texts = {}     # (row, col) → canvas text id
        self._key_colors = {}    # (row, col) → (r, g, b)
        self._selected_key = None
        self._on_key_click = None
        self._on_key_hover = None

        # Calcular dimensões
        self._padding = 8
        self._gap = 3
        total_units = 15.0  # 15U de largura total
        usable_w = width - 2 * self._padding
        usable_h = height - 2 * self._padding
        self._unit_w = (usable_w - self._gap * 14) / total_units
        self._row_h = (usable_h - self._gap * 4) / 5
        self._corner = 4  # raio dos cantos arredondados

        self._draw_keyboard()

        self.bind("<Button-1>", self._on_click)
        self.bind("<Motion>", self._on_motion)

    def set_key_click_callback(self, callback):
        """Define callback para clique em tecla: callback(row, col, label)."""
        self._on_key_click = callback

    def set_key_hover_callback(self, callback):
        """Define callback para hover: callback(row, col, label) ou callback(None, None, None)."""
        self._on_key_hover = callback

    def _draw_keyboard(self):
        """Desenha todas as teclas do teclado."""
        for row_data in KEYBOARD_LAYOUT_60HE:
            for row, col, x_pos, w_units, label in row_data:
                self._draw_key(row, col, x_pos, w_units, label)

    def _draw_key(self, row: int, col: int, x_pos: float, w_units: float, label: str):
        """Desenha uma tecla individual."""
        x = self._padding + x_pos * (self._unit_w + self._gap)
        visual_row = row - 1  # SDK rows 1-5 → visual rows 0-4
        y = self._padding + visual_row * (self._row_h + self._gap)
        w = w_units * self._unit_w + (w_units - 1) * self._gap
        h = self._row_h

        # Cor padrão
        color = self._key_colors.get((row, col), (30, 30, 50))
        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

        # Desenhar retângulo arredondado
        rect_id = self._create_rounded_rect(x, y, x + w, y + h, self._corner, hex_color)
        self._key_rects[(row, col)] = rect_id

        # Texto da tecla
        text_color = "#ffffff" if sum(color) < 400 else "#000000"
        font_size = 8 if len(label) > 2 else 9
        text_id = self.create_text(
            x + w / 2, y + h / 2, text=label,
            fill=text_color, font=("Segoe UI", font_size, "bold"),
        )
        self._key_texts[(row, col)] = text_id

    def _create_rounded_rect(self, x1, y1, x2, y2, r, fill):
        """Cria retângulo com cantos arredondados."""
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1, x2, y1 + r,
            x2, y2 - r,
            x2, y2, x2 - r, y2,
            x1 + r, y2,
            x1, y2, x1, y2 - r,
            x1, y1 + r,
            x1, y1, x1 + r, y1,
        ]
        return self.create_polygon(points, fill=fill, outline="#1a1a2e", smooth=True, width=1)

    def set_key_color(self, row: int, col: int, r: int, g: int, b: int):
        """Atualiza a cor de uma tecla na visualização."""
        self._key_colors[(row, col)] = (r, g, b)
        rect_id = self._key_rects.get((row, col))
        if rect_id:
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            self.itemconfig(rect_id, fill=hex_color)
            # Ajustar cor do texto para contraste
            text_id = self._key_texts.get((row, col))
            if text_id:
                brightness = r * 0.299 + g * 0.587 + b * 0.114
                text_color = "#000000" if brightness > 128 else "#ffffff"
                self.itemconfig(text_id, fill=text_color)

    def set_all_colors(self, color_map: dict):
        """Atualiza todas as cores de uma vez. color_map: {(row,col): (r,g,b)}."""
        for (row, col), (r, g, b) in color_map.items():
            self.set_key_color(row, col, r, g, b)

    def clear_all(self, color: tuple = (30, 30, 50)):
        """Limpa todas as teclas para uma cor base."""
        r, g, b = color
        for row_data in KEYBOARD_LAYOUT_60HE:
            for row, col, *_ in row_data:
                self.set_key_color(row, col, r, g, b)

    def highlight_key(self, row: int, col: int, outline_color: str = "#00d1d1"):
        """Destaca uma tecla (seleção)."""
        # Remover destaque anterior
        if self._selected_key:
            old_rect = self._key_rects.get(self._selected_key)
            if old_rect:
                self.itemconfig(old_rect, outline="#1a1a2e", width=1)

        self._selected_key = (row, col)
        rect_id = self._key_rects.get((row, col))
        if rect_id:
            self.itemconfig(rect_id, outline=outline_color, width=2)

    def _find_key_at(self, mx: int, my: int) -> tuple | None:
        """Encontra a tecla na posição do mouse."""
        for row_data in KEYBOARD_LAYOUT_60HE:
            for row, col, x_pos, w_units, label in row_data:
                x = self._padding + x_pos * (self._unit_w + self._gap)
                visual_row = row - 1  # SDK rows 1-5 → visual rows 0-4
                y = self._padding + visual_row * (self._row_h + self._gap)
                w = w_units * self._unit_w + (w_units - 1) * self._gap
                h = self._row_h
                if x <= mx <= x + w and y <= my <= y + h:
                    return (row, col, label)
        return None

    def _on_click(self, event):
        key = self._find_key_at(event.x, event.y)
        if key:
            row, col, label = key
            self.highlight_key(row, col)
            if self._on_key_click:
                self._on_key_click(row, col, label)

    def _on_motion(self, event):
        key = self._find_key_at(event.x, event.y)
        if key and self._on_key_hover:
            self._on_key_hover(key[0], key[1], key[2])
        elif self._on_key_hover:
            self._on_key_hover(None, None, None)

    def get_all_key_positions(self) -> list:
        """Retorna lista de todas as posições de teclas [(row, col, label), ...]."""
        result = []
        for row_data in KEYBOARD_LAYOUT_60HE:
            for row, col, x_pos, w_units, label in row_data:
                result.append((row, col, label))
        return result
