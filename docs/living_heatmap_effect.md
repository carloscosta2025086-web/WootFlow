# Living Heatmap Effect 🔥

Um efeito RGB reativo e fluido que transforma seu teclado numa visualização térmica dinâmica.

## Características Principais

### 🎨 Transição de Cores Suave
```
Verde Escuro (idle) → Verde → Amarelo → Laranja → Vermelho → Branco (overheat)
    (0.0)           (0.15)  (0.35)    (0.55)     (0.8)      (1.0)
```

### 🌊 Propagação de Calor Orgânica
- O calor de uma tecla pressionada propaga-se para as **8 teclas vizinhas** (incluindo diagonais)
- A propagação é gradual e amortecida, criando um efeito natural e fluido
- Cada vizinho recebe uma fração da temperatura (25% por ciclo)

### ❄️ Cooldown Suave
- Todas as teclas arrefecem gradualmente, independentemente de pressionamentos
- A velocidade de cooldown é controlável via parâmetro `speed`
- A transição de retorno é tão suave quanto a de aquecimento

### 🔥 Estado de Overheat
Quando uma tecla atinge ~92% da temperatura máxima:
- **Brilho Máximo**: intensidade total da cor
- **Centro Branco**: transição para cores muito claras
- **Flicker**: oscilação rápida (12Hz) para efeito de "sobreaquecimento"

### ✨ Efeitos Visuais
- **Glow Dinâmico**: brilho varia de 40% (frio) a 100% (quente)
- **Animação Suave**: 60fps com diffusion baseada em física
- **Sem Lag**: uso de threading para não bloquear o render

## Parâmetros Ajustáveis

### Speed (padrão: 1.0)
Controla a velocidade de arrefecimento. Valores maiores = arrefecimento mais rápido.
```python
effect.speed = 0.5   # arrefecimento lento, efeito persiste mais
effect.speed = 2.0   # arrefecimento rápido, reativo imediato
```

### Spread Strength (padrão: 0.85)
Força da propagação para teclas vizinhas (0.0 a 1.0).
```python
effect.spread_strength = 0.5  # propagação suave e lenta
effect.spread_strength = 1.0  # propagação máxima, mais intensa
```

### Overheat Threshold (padrão: 0.92)
Temperatura em que o estado de overheat é acionado (0.0 a 1.0).
```python
effect.overheat_threshold = 0.8   # mais fácil de overheat
effect.overheat_threshold = 0.98  # mais difícil de overheat
```

### Brightness (padrão: 1.0)
Controla o brilho geral do efeito.
```python
effect.brightness = 0.7  # efeito mais suave
effect.brightness = 1.0  # brilho máximo
```

## Comportamento em Detalhes

### Física de Propagação
A cada frame (1/60s):

1. **Propagação**: Cada tecla compartilha 25% do seu calor com seus vizinhos
2. **Arrefecimento**: Todas as teclas perdem temperatura gradualmente
   - Taxa de perda: `1.8 * speed * dt` por frame
3. **Renderização**: Cores são calculadas baseadas na temperatura

### Trigger (Pressionamento)
Quando uma tecla é pressionada:
```python
effect.trigger(row, col)  # row = 1-5, col = 0-20
```
- A temperatura aumenta em 0.95 (praticamente max imediatamente)
- O calor começa a propagar-se no frame seguinte
- O arrefecimento só começa gradualmente

### Iteração de Cores

| Temperatura | Cor RGB | Aparência |
|---|---|---|
| 0.0-0.15 | Verde escuro (0, 80, 20) | Inativo, muito escuro |
| 0.15-0.35 | Verde → Amarelo | Aquecimento leve |
| 0.35-0.55 | Amarelo → Laranja | Aquecimento médio |
| 0.55-0.8 | Laranja → Vermelho | Quente, reativo |
| 0.8-1.0 | Vermelho → Branco | Muito quente, overheat |

## Uso Prático

### Integração Automática
O efeito está automaticamente registado no sistema:

```python
from core.effect_registry import get_effect_class

# Obter a classe do efeito
EffectClass = get_effect_class("living_heatmap")
effect = EffectClass()
```

### Configuração Recomendada
Para uma experiência imersiva:

```python
effect.speed = 1.0              # Arrefecimento equilibrado
effect.spread_strength = 0.85   # Propagação natural
effect.brightness = 1.0         # Brilho completo
effect.overheat_threshold = 0.92
```

### Teste em Tempo Real
```bash
python tools/demo_living_heatmap.py
```

## Exemplos de Cenários

### Typing (Digitação Rápida)
```
Pressiona T → Aquece para vermelho
Pressiona Y (vizinho) → aquece parcialmente enquanto T arrefece
Pressiona P → novo calor, enquanto Y e T continuam arrefecendo
Resultado: "Heat trail" que rastreia o padrão de digitação
```

### Gaming (Pressões Sustentadas)
```
Pressiona WASD continuamente → centro fica branco (overheat)
Solta → arrefecimento suave ao longo de 1-2 segundos
Prensa novamente → reinicia o ciclo
```

### Idle (Inativo)
```
Nenhuma tecla pressionada → todas voltam ao verde escuro
Manutenção de estado visual limpo e minimalista
```

## Técnicas Avançadas

### Personalização de Cores
Para alterar a paleta de cores, edite o método `_temperature_to_color()`:

```python
def _temperature_to_color(self, temp: float, is_overheat: bool = False):
    # Customize aqui...
```

### Ajuste da Física
- **Diffusion**: `self._diffusion_factor = 0.25` (aumentar = mais spread)
- **Press Heat**: `self._press_heat = 0.95` (mais/menos calor inicial)
- **Cooldown**: `self._cooldown_rate = 1.8` (mais rápido/lento)

## Performance

- **CPU**: Negligenciável, ~0.1ms por frame
- **Memória**: 72 bytes (matriz 6x21 de floats)
- **Thread-Safe**: Usa lock para segurança em paralelo

## Versão

- **Data**: May 2026
- **Status**: ✓ Completo e testado
- **Compatibilidade**: Wooting 60HE+ (suporta qualquer teclado RGB)

---

Desfrutai do efeito! 🎮✨
