# WootFlow WebSocket Infinite Loading - Diagnostic Guide

## O que está a acontecer?

Se o WootFlow fica a mostrar "A ligar ao servidor..." infinitamente, significa que:
1. **A UI (pywebview) abriu corretamente**, OU
2. **O backend (FastAPI/uvicorn) não iniciou**, OU
3. **A conexão WebSocket está falhando**

---

## ✅ Passo-a-Passo Diagnóstico

### 1. **Corre o script de diagnóstico**

```powershell
cd C:\Users\bl4z3\Documents\GitHub\WootFlow
python scripts/diagnose_ws_issue.py
```

Este script verifica:
- ✓ Se a porta 9120 está em uso
- ✓ Se o servidor responde a /health
- ✓ Se VC++ Redistributable está instalado
- ✓ Se WebView2 está instalado
- ✓ Últimas linhas do log de debug

### 2. **Verifica se a porta 9120 está ocupada**

```powershell
netstat -ano | findstr :9120
```

**Se aparecer algo:**
```
TCP    127.0.0.1:9120        0.0.0.0:0        LISTENING     12345
```

Força o encerramento do processo:
```powershell
taskkill /PID 12345 /F
```

### 3. **Verifica o arquivo de log**

O log deve estar em um destes locais:
- `%LOCALAPPDATA%\WootFlow\logs\wootflow_debug.log` (preferido)
- `C:\Users\bl4z3\Documents\GitHub\WootFlow\wootflow_debug.log`
- `%TEMP%\wootflow_debug.log`

**Procura por:**
- `[ERROR]` ou `CRITICAL` — indica erro no startup
- `CONNECTION REFUSED` — porta não aberta
- `PORT 9120 ALREADY IN USE` — conflito de porta
- `Keyboard connected` — SDK inicializou OK
- `Health check failed` — servidor não respondeu

### 4. **Se o log mostrar erro de SDK ou Keyboard**

Possíveis causas:
- Keyboard desligado/desconectado
- Drivers USB faltando
- Timeout ao ligar ao SDK

**Solução:**
1. Desconecta e reconecta o keyboard USB
2. Reinicia o WootFlow
3. Se persiste, experimenta outro porto USB

### 5. **Usa os diagnósticos no ecrã de loading**

Se a app ficar em loading, o próprio ecrã já mostra:
- estado da ligação (`connecting`, `retrying`, `error`)
- tentativa atual
- endpoint em uso
- se o backend está alcançável
- último erro de ligação

Anota esses campos para facilitar o diagnóstico.

---

## 🔧 Soluções Comuns

### **Problema: Porta 9120 em uso**
```powershell
# 1. Identifica o processo
netstat -ano | findstr :9120

# 2. Mata o processo
taskkill /PID <pid> /F

# 3. Tenta novamente o WootFlow
```

### **Problema: Dependências faltando**
```powershell
# Reinstala tudo
.\install_all.ps1
```

### **Problema: VC++ Redistributable faltando**
Download: https://support.microsoft.com/en-us/help/2977003

### **Problema: WebView2 faltando**
Download: https://developer.microsoft.com/en-us/microsoft-edge/webview2/

### **Problema: SDK/Keyboard não responde**
1. Desconecta o keyboard
2. Espera 5 segundos
3. Reconecta em outro porto USB
4. Reinicia o WootFlow

### **Problema: Porta 9120 precisa mudar**
Se 9120 está bloqueada e não consegues libertar:

1. Abre `main_desktop.py`
2. Procura `_start_server()` e `_wait_for_server()`
3. Muda `9120` para outra porta (ex: `9121`)
4. Salva e reconstrói:
```powershell
cd ui
npm run build
cd ..
.\.venv\Scripts\python.exe -m PyInstaller WootFlow.spec --clean -y
```

---

## 📊 Informações de Debug

Quando reportas um problema, inclui:
1. **Output do script diagnóstico** (`diagnose_ws_issue.py`)
2. **Últimas 50 linhas do log** (`wootflow_debug.log`)
3. **Dados no ecrã de loading** — status, tentativa, endpoint, backend e erro
4. **Output de `netstat -ano | findstr :9120`**

---

## 🚀 Se Nada Disso Funcionar

1. **Desinstala completamente:**
   ```powershell
   rm -r $env:LOCALAPPDATA\WootFlow
   rm -r $PSScriptRoot\build
   rm -r $PSScriptRoot\dist
   ```

2. **Reinstala tudo:**
   ```powershell
   .\install_all.ps1
   cd ui
   npm run build
   cd ..
   .\.venv\Scripts\python.exe -m PyInstaller WootFlow.spec --clean -y
   ```

3. **Executa novamente e coleta logs:**
   - Abre PowerShell
   - Corre `python -m pdb WootFlow.exe` (debugger)
   - Ou corre `python main_desktop.py` (direto)

4. **Contacta com:**
   - Log de erro completo
   - Output do diagnóstico
   - OS/Windows version
   - Python version (`python --version`)

---

## 🔍 Quick Commands Reference

```powershell
# Diagnóstico rápido
python scripts/diagnose_ws_issue.py

# Ver logs em tempo real
Get-Content "$env:LOCALAPPDATA\WootFlow\logs\wootflow_debug.log" -Tail 50 -Wait

# Verificar porta
netstat -ano | findstr :9120

# Reinstalar dependências
.\install_all.ps1

# Reconstruir aplicação
cd ui
npm run build
cd ..
.\.venv\Scripts\python.exe -m PyInstaller WootFlow.spec --clean -y

# Executar direto (útil para debug)
python main_desktop.py
```

---

Última atualização: v3.0.12 (WS Diagnostics)
