# Solution for Ollama Errors in GitHub Actions

## Problems Resolved

### 1. Error "bind: address already in use"
**Problem**: The Ollama service was being started multiple times causing conflicts on port 11434.

**Solution**: 
- Added `pkill -f ollama || true` to terminate existing processes
- Implemented status check with timeout to verify Ollama is ready
- Added retry logic for model pulling

### 2. Error "Failed to parse Ollama response"
**Problem**: The DeepSeek-R1 model returns responses that start with `<think>` tags instead of pure JSON.

**Solution**:
- Created new script `fixed_ollama_processor.py` with robust parsing
- Implemented `clean_json_response()` function that handles thinking tags
- Added regex extraction as fallback for individual fields
- Improved prompt to explicitly request JSON only

### 3. Problem with manifest pulling
**Problem**: Timeout or network issues during model download.

**Solution**:
- Implemented retry logic with 3 attempts
- Added delay between attempts
- Improved error handling

## Modified Files

### 1. `.github/workflows/process-documents.yml`
- Improved Ollama management with status checks
- Added retry logic for model pulling
- Changed script from `updated_ollama_processor.py` to `fixed_ollama_processor.py`

### 2. `scripts/fixed_ollama_processor.py` (NEW)
- Robust handling of DeepSeek responses with `<think>` tags
- Improved JSON parsing with regex fallback
- Optimized prompt to avoid thinking tags
- Enhanced data validation and cleaning

## Fix Features

### DeepSeek Response Handling
```python
def clean_json_response(self, response_text: str) -> str:
    # Remove <think> tags and content
    if response_text.startswith('<think>'):
        think_end = response_text.find('</think>')
        if think_end != -1:
            response_text = response_text[think_end + 8:].strip()
    
    # Remove other XML tags
    response_text = re.sub(r'<[^>]+>', '', response_text).strip()
```

### Improved Prompt
```python
prompt = f"""You must respond with ONLY valid JSON, no other text or tags.

Analyze this document and provide a JSON response with exactly this structure:
{{
    "title": "Clean, readable title",
    "summary": "summary of the document content with max 400 characters",
    ...
}}

IMPORTANT: Respond ONLY with the JSON object, no thinking process, no explanations, no additional text."""
```

### Ollama Status Check
```bash
# Wait for Ollama to be ready with timeout
for i in {1..30}; do
  if curl -s http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
    echo "Ollama is ready!"
    break
  fi
  echo "Waiting... ($i/30)"
  sleep 2
done
```

## Testing and Verification

To test the fix locally:

```bash
# 1. Start Ollama
ollama serve &

# 2. Download the model
ollama pull deepseek-r1:1.5b

# 3. Test the script
cd scripts
python fixed_ollama_processor.py --force
```

## Expected Results

After implementing the fix:
- ✅ Ollama starts correctly without port conflicts
- ✅ DeepSeek model downloads successfully
- ✅ Responses are parsed correctly even with `<think>` tags
- ✅ Documents are processed and saved to `documents.json`
- ✅ GitHub Actions workflow completes successfully

## Monitoring

Logs should show:
```
INFO - Successfully parsed JSON after cleaning
INFO - Successfully analyzed [filename] with Ollama
INFO - Documents database updated successfully
```

Instead of:
```
WARNING - Failed to parse Ollama response for [filename], using fallback
