🔥 LIVING HEATMAP - AJUSTES IMPLEMENTADOS
═════════════════════════════════════════════════════════════

✅ MUDANÇAS REALIZADAS:

1️⃣  AQUECIMENTO ACUMULATIVO
   • _press_heat: 0.95 → 0.18
   • Antes: Um clique ativava imediatamente a tecla
   • Agora: Precisa de ~5-6 cliques para chegar ao overheat
   • Efeito: Muito mais gradual e recompensador

2️⃣  VIZINHOS AQUECEM POUCO
   • Spread para vizinhos: 0.08 → 0.05 (5%)
   • Antes: Vizinhos aqueciam bastante
   • Agora: Vizinhos recebem apenas 5% do calor
   • Efeito: Foco na tecla principal, pouca propagação

3️⃣  ARREFECIMENTO MUITO LENTO
   • _cooldown_rate: 1.8 → 0.35
   • Antes: Arrefecia em ~0.5 segundos
   • Agora: Arrefecia em ~3 segundos
   • Efeito: O calor persiste por mais tempo

═════════════════════════════════════════════════════════════

🎮 COMPORTAMENTO ESPERADO:

Digitação:
────────
Pressiona 'A' 1x → Temp: 0.18 (verde, frio)
Pressiona 'A' 2x → Temp: 0.36 (verde claro)
Pressiona 'A' 3x → Temp: 0.54 (amarelo, morno)
Pressiona 'A' 4x → Temp: 0.72 (laranja, quente)
Pressiona 'A' 5x → Temp: 0.90 (vermelho, muito quente)
Pressiona 'A' 6x → Temp: 1.00 (BRANCO - OVERHEAT!)

Gaming (WASD sustentado):
────────────────────────
Digitação rápida + sustentada:
W, A, S, D, W, A, S, D, ...
→ Acumula calor com cada pressionamento
→ Eventualmente entra em overheat (flickering branco)

Arrefecimento:
──────────────
Após parar de pressionar → Arrefece MUITO lentamente
→ A tecla ainda está quente 5-10 segundos depois
→ Cria uma "memória térmica" realista

═════════════════════════════════════════════════════════════

📊 NÚMEROS EXATOS:

Pressionamento:
  • Calor por clique: 0.18 (18%)
  • Cliques para 0.9: 5 cliques
  • Cliques para 1.0: 6 cliques

Propagação:
  • Spread para vizinhos: 5% apenas
  • Vizinhos diretos: 8 (horizontal + diagonal)
  • Vizinhos longe: nenhum

Arrefecimento:
  • Taxa: 0.35 temperatura/segundo
  • 1.0 → 0.0: ~2.9 segundos
  • Configurável via: effect.speed (multiplicador)

═════════════════════════════════════════════════════════════

🎯 CONFIGURAÇÃO RECOMENDADA:

Para um arrefecimento ainda mais lento, você pode:
──────────────────────────────────────────────────

effect.speed = 0.5  # Arrefecimento 2x mais lento
effect.speed = 0.25 # Arrefecimento 4x mais lento
effect.speed = 0.1  # Arrefecimento EXTREMAMENTE lento

Exemplo:
  effect._cooldown_rate = 0.35
  effect.speed = 0.25
  → Arrefecimento final: ~0.35 * 0.25 / 60 = ~0.0015 por frame
  → Tempo total: ~10+ segundos

═════════════════════════════════════════════════════════════

✨ RESULTADO FINAL:

✅ Efeito muito mais gradual
✅ Pressionamentos acumulam (5-6 cliques = overheat)
✅ Vizinhos aquecem minimamente (5%)
✅ Arrefecimento lento (2-3+ segundos)
✅ Comportamento fisicamente plausível
✅ Sensação de "memória térmica"

═════════════════════════════════════════════════════════════

🧪 TESTAR:

python tools/test_new_heatmap_behavior.py

Mostra:
  • Teste 1: Aquecimento acumulativo (5-6 cliques)
  • Teste 2: Vizinhos com 5% de calor
  • Teste 3: Arrefecimento lento
  • Teste 4: Cenário realista combinado

═════════════════════════════════════════════════════════════

📝 STATUS:

✅ Alterações implementadas
✅ Testes passaram
✅ Pronto para usar
✅ Comportamento validado

Se desejar ajustes adicionais (ex: arrefecimento ainda mais lento),
use os parâmetros configuráveis ou ajuste os valores em effects_engine.py
