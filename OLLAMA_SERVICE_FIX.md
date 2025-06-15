# Ollama Service Fix

This document explains how to fix the "address already in use" error when starting Ollama service.

## Problem
When starting Ollama service, you might encounter this error:
```
Error: listen tcp 127.0.0.1:11434: bind: address already in use
```

This happens when:
- A previous Ollama instance is still running
- Another process is using port 11434
- The service wasn't properly shut down

## Solutions

### Option 1: Use the Bash Script (Recommended for Linux/macOS)
```bash
./scripts/start_ollama_service.sh
```

### Option 2: Use the Python Script (Cross-platform)
```bash
python scripts/start_ollama_service.py
```

### Option 3: Manual Fix
```bash
# Kill existing Ollama processes
pkill -f "ollama serve"
pkill -f "ollama"

# Kill process using port 11434
lsof -ti:11434 | xargs kill -9

# Start Ollama service
ollama serve &
```

### Option 4: For GitHub Actions/CI
Replace the simple `ollama serve &` command in your workflow with:
```yaml
- name: Start Ollama Service
  run: |
    # Kill any existing Ollama processes
    pkill -f "ollama serve" || true
    pkill -f "ollama" || true
    sleep 2
    
    # Kill process using port 11434 if still occupied
    if lsof -Pi :11434 -sTCP:LISTEN -t >/dev/null 2>&1; then
      lsof -ti:11434 | xargs kill -9 || true
      sleep 2
    fi
    
    # Start Ollama service
    ollama serve &
    sleep 5
    
    # Verify service is running
    curl -s http://127.0.0.1:11434/api/tags || exit 1
```

## Features of the Fix Scripts

Both scripts provide:
- ✅ Automatic detection and killing of existing Ollama processes
- ✅ Port conflict resolution
- ✅ Service health verification
- ✅ Proper error handling and logging
- ✅ Timeout protection

## Usage in Your Workflow

Instead of:
```bash
ollama serve &
```

Use:
```bash
./scripts/start_ollama_service.sh
```

Or:
```bash
python scripts/start_ollama_service.py
```

This ensures a clean start every time and prevents the "address already in use" error.
