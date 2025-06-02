# Complete Solution for Ollama GitHub Actions Errors

## Problems Identified

### 1. Port Conflict Error: "bind: address already in use"
**Root Cause**: Ollama service was already running when the workflow tried to start it again on port 11434.

**Symptoms**:
```
Error: listen tcp 127.0.0.1:11434: bind: address already in use
pkill: killing pid 2389 failed: Operation not permitted
```

### 2. DeepSeek Response Parsing Failures
**Root Cause**: DeepSeek-R1 model returns responses with `<think>` tags that break JSON parsing.

**Symptoms**:
```
WARNING - Failed to parse Ollama response for [filename], using fallback
```

## Complete Solution

### 1. Fixed GitHub Workflow (process-documents-fixed.yml)

**Key Improvements**:
- **Thorough Process Cleanup**: Uses `sudo pkill` with `-9` flag for force termination
- **Port Conflict Resolution**: Checks and kills processes using port 11434
- **Extended Timeout**: Increased wait time from 30 to 60 iterations
- **Better Error Handling**: Comprehensive diagnostics and error reporting
- **Retry Logic**: 5 attempts for model pulling with 300-second timeout
- **Model Testing**: Verifies model works before proceeding

**Critical Changes**:
```bash
# Kill any existing Ollama processes more thoroughly
sudo pkill -f ollama || true
sudo pkill -9 ollama || true
sleep 3

# Check if port 11434 is still in use and kill the process
if lsof -ti:11434 2>/dev/null; then
  echo "Port 11434 is in use, killing process..."
  sudo kill -9 $(lsof -ti:11434) || true
  sleep 2
fi

# Extended timeout and better verification
for i in {1..60}; do
  if curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    echo "Ollama is ready!"
    break
  fi
  echo "Waiting... ($i/60)"
  sleep 3
done
```

### 2. Ultimate Ollama Processor (ultimate_ollama_processor.py)

**Key Features**:
- **Multi-Method JSON Parsing**: 4 different parsing strategies
- **DeepSeek Thinking Tag Handling**: Removes `<think>` sections automatically
- **Regex Field Extraction**: Fallback extraction for individual fields
- **JSON Repair**: Attempts to fix malformed JSON
- **Smart Fallback**: Intelligent analysis when Ollama fails
- **Robust Validation**: Ensures all required fields are present and valid

**Parsing Strategy Hierarchy**:
1. **Direct JSON Parsing**: Try to parse response as-is
2. **Cleaned JSON Parsing**: Remove thinking tags and parse
3. **Regex Field Extraction**: Extract individual fields using patterns
4. **JSON Repair**: Fix common JSON formatting issues

**Example DeepSeek Response Handling**:
```python
def extract_json_from_response(self, response_text: str) -> Optional[str]:
    # Handle DeepSeek thinking format
    if '<think>' in response_text:
        think_end = response_text.find('</think>')
        if think_end != -1:
            response_text = response_text[think_end + 8:].strip()
    
    # Remove XML-like tags
    response_text = re.sub(r'<[^>]+>', '', response_text).strip()
    
    # Try multiple JSON extraction patterns
    json_patterns = [
        r'\{(?:[^{}]|{[^{}]*})*\}',  # Complete nested JSON
        r'\{[^{}]*\}',               # Simple JSON
        r'\{[^{}]*\[[^\]]*\][^{}]*\}' # JSON with arrays
    ]
```

### 3. Improved Prompt Engineering

**Ultra-Specific Prompt**:
```python
prompt = f"""RESPOND WITH ONLY JSON. NO THINKING. NO EXPLANATIONS.

{{
    "title": "document title here",
    "summary": "brief summary under 300 characters",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "category": "one of: AI, Machine Learning, Data Science, Analytics, Business, Technology, Research",
    "difficulty": "one of: Beginner, Intermediate, Advanced",
    "authors": ["author1"] or [],
    "content_preview": "first 80 characters of content"
}}

Document: {filename}
Text: {text}

JSON ONLY:"""
```

**Generation Options**:
```python
options={
    "temperature": 0.0,  # Deterministic responses
    "top_p": 0.8,
    "num_predict": 500,  # Limit response length
    "stop": ["\n\n", "```", "<think>", "Note:", "Explanation:"]
}
```

## Implementation Steps

### Step 1: Use the Fixed Workflow
Replace your current workflow with the fixed version:
```bash
# Rename current workflow to backup
mv .github/workflows/process-documents.yml .github/workflows/process-documents-backup.yml

# Use the fixed workflow
mv .github/workflows/process-documents-fixed.yml .github/workflows/process-documents.yml
```

### Step 2: Update the Processor Script
Update your workflow to use the ultimate processor:
```yaml
- name: Process documents with Ollama (Fixed)
  env:
    OLLAMA_MODEL: deepseek-r1:1.5b
  run: |
    echo "Processing documents with Ollama and DeepSeek..."
    python scripts/ultimate_ollama_processor.py --force
    echo "Documents processed successfully"
```

### Step 3: Test Locally (Optional)
```bash
# Install Ollama locally
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve &

# Pull the model
ollama pull deepseek-r1:1.5b

# Test the processor
cd scripts
python ultimate_ollama_processor.py --force
```

## Expected Results

### Before Fix:
```
ERROR: listen tcp 127.0.0.1:11434: bind: address already in use
WARNING - Failed to parse Ollama response for [filename], using fallback
```

### After Fix:
```
INFO - Started Ollama with PID: [pid]
INFO - Ollama is ready!
INFO - Model pulled successfully!
INFO - Successfully parsed extracted JSON
INFO - Successfully analyzed [filename] with Ollama
INFO - Documents database updated successfully
```

## Monitoring and Troubleshooting

### Success Indicators:
- ✅ No port conflict errors
- ✅ Model downloads successfully
- ✅ JSON parsing succeeds for most documents
- ✅ `documents.json` is updated with proper metadata
- ✅ Workflow completes without errors

### If Issues Persist:

1. **Check Ollama Logs**:
   ```bash
   # In the workflow, add debugging
   echo "Checking Ollama status:"
   ps aux | grep ollama
   curl -v http://127.0.0.1:11434/api/tags
   ```

2. **Test Model Manually**:
   ```bash
   # Test the model directly
   echo '{"model": "deepseek-r1:1.5b", "prompt": "Hello", "stream": false}' | \
   curl -X POST http://127.0.0.1:11434/api/generate -d @-
   ```

3. **Enable Debug Logging**:
   ```python
   # In the processor script
   logging.basicConfig(level=logging.DEBUG)
   ```

## Alternative Models

If DeepSeek continues to cause issues, consider these alternatives:

```yaml
env:
  OLLAMA_MODEL: llama3.2:3b  # More stable, less thinking tags
  # or
  OLLAMA_MODEL: qwen2.5:3b   # Good JSON compliance
  # or  
  OLLAMA_MODEL: mistral:7b   # Reliable for structured output
```

## Files Created/Modified

1. **`.github/workflows/process-documents-fixed.yml`** - Fixed workflow
2. **`scripts/ultimate_ollama_processor.py`** - Robust processor
3. **`scripts/COMPLETE_OLLAMA_FIX.md`** - This documentation

## Summary

This solution addresses both the port conflict and JSON parsing issues through:
- Comprehensive process management in the workflow
- Multi-strategy response parsing in the processor
- Better error handling and diagnostics
- Fallback mechanisms for reliability

The fix should resolve both the "address already in use" error and the "Failed to parse Ollama response" warnings, resulting in successful document processing.
