# 🤖 AI Document Chat Setup for GitHub Pages

This guide explains how to set up the AI chat feature when using this application on GitHub Pages.

## 🌐 How It Works

This application is hosted on **GitHub Pages** (static hosting), but the AI chat feature requires **Ollama** to run locally on your computer. The web app connects to your local Ollama instance to provide AI-powered document analysis.

```
┌─────────────────┐    HTTPS    ┌─────────────────┐    HTTP     ┌─────────────────┐
│   GitHub Pages  │ ◄────────── │  Your Browser   │ ◄────────── │ Local Ollama    │
│   (Web App)     │             │                 │             │ (AI Models)     │
└─────────────────┘             └─────────────────┘             └─────────────────┘
```

## 🚀 Quick Setup

### Step 1: Install Ollama

**Windows:**
1. Download from [ollama.ai/download](https://ollama.ai/download)
2. Run the installer
3. Restart your terminal/command prompt

**macOS:**
```bash
# Using Homebrew (recommended)
brew install ollama

# Or download from ollama.ai/download
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Start Ollama Service

Open a terminal/command prompt and run:

```bash
# Start Ollama service
ollama serve
```

Keep this terminal window open - Ollama needs to keep running.

### Step 3: Install AI Models

Open a **new** terminal/command prompt (keep the first one running) and install models:

```bash
# Install recommended models
ollama pull mistral:7b-instruct    # ~4GB - Good balance
ollama pull llama3.2:3b           # ~2GB - Faster, smaller
ollama pull phi3:mini             # ~2GB - Microsoft's efficient model

# Verify installation
ollama list
```

### Step 4: Enable CORS (Critical!)

Since the web app runs on GitHub Pages (HTTPS) and connects to local Ollama (HTTP), you need to enable CORS:

**Method 1: Environment Variable (Recommended)**
```bash
# Stop Ollama first (Ctrl+C in the first terminal)

# Windows (Command Prompt)
set OLLAMA_ORIGINS=*
ollama serve

# Windows (PowerShell)
$env:OLLAMA_ORIGINS="*"
ollama serve

# macOS/Linux
export OLLAMA_ORIGINS="*"
ollama serve
```

**Method 2: Permanent Setup**

Create a startup script:

**Windows (create `start-ollama.bat`):**
```batch
@echo off
set OLLAMA_ORIGINS=*
ollama serve
```

**macOS/Linux (create `start-ollama.sh`):**
```bash
#!/bin/bash
export OLLAMA_ORIGINS="*"
ollama serve
```

### Step 5: Test the Setup

1. **Verify Ollama is running:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Open the GitHub Pages app** in your browser

3. **Click on any document** to open the preview

4. **Look for the chat panel** on the right side

5. **Click "Retry Connection"** - you should see a green "Connected" status

## 🔧 Troubleshooting

### ❌ "Ollama Not Connected"

**Check if Ollama is running:**
```bash
curl http://localhost:11434/api/tags
```

If this fails:
- Make sure you ran `ollama serve`
- Check if another process is using port 11434
- Try restarting Ollama

### ❌ CORS Errors in Browser Console

**Symptoms:** Connection fails, browser console shows CORS errors

**Solution:** Enable CORS as described in Step 4:
```bash
export OLLAMA_ORIGINS="*"  # macOS/Linux
set OLLAMA_ORIGINS=*       # Windows
ollama serve
```

### ❌ "No Models Found"

**Check installed models:**
```bash
ollama list
```

**Install a model:**
```bash
ollama pull mistral:7b-instruct
```

### ❌ Slow Responses

**For better performance:**
1. Use smaller models: `llama3.2:3b` or `phi3:mini`
2. Close other applications to free up RAM
3. Ensure you have at least 8GB RAM available

### ❌ Connection Works But Chat Doesn't Respond

**Check model is loaded:**
```bash
# Test direct API call
curl -X POST http://localhost:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral:7b-instruct",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": false
  }'
```

## 📊 Recommended Models by System

| System RAM | Recommended Model | Size | Performance |
|------------|------------------|------|-------------|
| 4-8 GB     | `phi3:mini`      | ~2GB | Fast, basic |
| 8-16 GB    | `llama3.2:3b`    | ~2GB | Good balance |
| 16+ GB     | `mistral:7b-instruct` | ~4GB | Best quality |

## 🔄 Daily Usage

Once set up, your daily workflow is:

1. **Start Ollama:**
   ```bash
   export OLLAMA_ORIGINS="*"  # If not permanent
   ollama serve
   ```

2. **Open the GitHub Pages app** in your browser

3. **Start chatting** with documents!

## 🛡️ Security Notes

- **Ollama runs locally** - no data is sent to external servers
- **Your documents stay private** - only metadata is shared with the local AI
- **CORS setting** (`OLLAMA_ORIGINS="*"`) allows any website to connect to your local Ollama
  - Only enable this when using the chat feature
  - Consider using specific origins for better security: `OLLAMA_ORIGINS="https://yourusername.github.io"`

## 🆘 Getting Help

If you're still having issues:

1. **Check the browser console** (F12) for error messages
2. **Verify Ollama logs** in the terminal where you ran `ollama serve`
3. **Test with curl** commands provided above
4. **Try a different model** if one isn't working

## 💡 Tips for Best Experience

- **Keep Ollama running** in a dedicated terminal window
- **Use smaller models** for faster responses
- **Close unnecessary applications** to free up RAM
- **Ask specific questions** about documents for better responses
- **Use the suggested questions** as starting points

---

**Need more help?** Check the [Ollama documentation](https://github.com/ollama/ollama) or create an issue in this repository.
