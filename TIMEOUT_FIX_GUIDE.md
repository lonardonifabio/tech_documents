# Timeout Issue Fix Guide

## Problem
Users were experiencing timeout errors with the message: "Response timeout. The AI service is taking too long to respond. Try asking a simpler question or check your connection."

## Root Causes Identified

1. **Too Aggressive Timeouts**: Original timeouts were 8-15 seconds, which is too short for AI model responses
2. **Incorrect API Format**: Some Ollama versions are sensitive to request format
3. **Model Loading Time**: First requests can take longer as models load into memory
4. **Missing Error Handling**: Limited debugging information for troubleshooting

## Fixes Applied

### 1. Extended Timeouts (UPDATED)
- **All Environments**: 300 seconds (5 minutes) - was 8-45s
- **Minimum Timeout**: 300 seconds for all memory tiers
- **Generous Buffer**: Allows for model loading and complex responses

### 2. Improved API Request Format
```typescript
// Simplified request body - some Ollama versions are picky
const requestBody = {
  model: this.model,
  messages: messages,
  stream: false,
  options: {
    temperature: this.temperature,
    num_predict: this.maxTokens,
  }
};
```

### 3. Enhanced Debugging
- Added comprehensive console logging
- Better error messages with specific troubleshooting steps
- Connection status indicators
- Model availability checks

### 4. Better Error Messages
Instead of generic timeout, users now get:
```
Response timeout after 300 seconds. The AI model might be loading or the question is too complex. Try:

1. Asking a simpler question
2. Waiting for the model to fully load
3. Checking if Ollama is running: "ollama list"
```

### 5. Connection Diagnostics
- Real-time connection status
- Model availability checking
- Retry buttons for connection and model loading
- Step-by-step setup instructions

## Testing the Fix

### 1. Check Console Logs
Open browser DevTools (F12) and look for:
- 🤖 Sending message to Ollama
- 🔄 Attempt 1/3
- 📤 Request body
- 📥 Response status
- ✅ Response received

### 2. Verify Ollama Setup
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Should return JSON with available models
# If not, start Ollama:
ollama serve

# Pull a model if none available:
ollama pull mistral:7b-instruct
```

### 3. Test Different Questions
Start with simple questions:
- "What is this document about?"
- "Who are the authors?"
- "What are the key topics?"

### 4. Monitor Performance
- First question may take 30-60 seconds (model loading)
- Subsequent questions should be faster (5-15 seconds)
- Check memory usage doesn't exceed system limits

## Common Issues & Solutions

### Issue: Still Getting Timeouts
**Solution**: 
1. Check if model is actually loaded: `ollama list`
2. Try a smaller model: `ollama pull llama3.2:3b`
3. Increase system memory or close other applications
4. Check console logs for specific error details

### Issue: "No Models Found"
**Solution**:
```bash
ollama pull mistral:7b-instruct
# or for low memory systems:
ollama pull llama3.2:3b
```

### Issue: Connection Failed
**Solution**:
1. Ensure Ollama is running: `ollama serve`
2. Check port 11434 is not blocked by firewall
3. Try restarting Ollama service

### Issue: Slow Responses
**Solution**:
1. Use smaller models (3B parameters instead of 7B+)
2. Reduce max_tokens in environment config
3. Clear chat history frequently
4. Close other memory-intensive applications

## Performance Optimization

### For GitHub Spaces Free Tier:
- Use `llama3.2:3b` model (~2GB)
- Limit responses to 300 tokens
- Keep conversation history to 5 messages
- 300-second timeout (5 minutes)

### For Local Development:
- Use `mistral:7b-instruct` model (~4GB)
- 500 token responses
- 10 message history
- 300-second timeout (5 minutes)

### For High-Memory Systems:
- Use `llama3.1:8b` model (~5GB)
- 800 token responses
- 15 message history
- 300-second timeout (5 minutes)

## Monitoring Tools

### Browser Console
Check for these log patterns:
```
🤖 Sending message to Ollama: {message: "...", model: "mistral:7b-instruct"}
🔄 Attempt 1/3
📤 Request body: {...}
📥 Response status: 200 OK
✅ Response received: {message: {...}}
```

### Environment Info Button
Click the ℹ️ button in chat header to see:
- Memory tier detection
- Recommended models
- Current timeout settings
- Device capabilities

## Verification Steps

1. ✅ Ollama service running (`ollama serve`)
2. ✅ Model downloaded (`ollama list`)
3. ✅ Connection test passes (`curl localhost:11434/api/tags`)
4. ✅ Browser console shows successful requests
5. ✅ Chat responds within timeout period
6. ✅ No error messages in chat interface

## Support

If issues persist after applying these fixes:

1. Check browser console for detailed error logs
2. Verify Ollama version compatibility
3. Test with different models/sizes
4. Monitor system resource usage
5. Try restarting both Ollama and the web application

The timeout issue should now be resolved with these comprehensive fixes and improved error handling.
