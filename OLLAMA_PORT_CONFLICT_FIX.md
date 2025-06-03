# Ollama Port Conflict Fix

## Problem Description

The application was experiencing deployment failures on GitHub Actions with the error:

```
Error: listen tcp 127.0.0.1:11434: bind: address already in use
```

This occurred because multiple GitHub Actions workflows were trying to start Ollama on the same port (11434) simultaneously, causing port binding conflicts.

## Root Cause

The issue was caused by:

1. **Multiple concurrent workflows** - Several GitHub Actions workflows (`process-documents.yml`, `process_documents_with_ollama.yml`, `deploy-site.yml`) could run simultaneously
2. **Fixed port usage** - All workflows tried to use the default Ollama port 11434
3. **Insufficient cleanup** - Previous Ollama processes weren't properly terminated before starting new ones
4. **Race conditions** - When multiple workflows triggered on the same push event, they competed for the same port

## Solution Overview

The fix implements a **dynamic port allocation strategy** with the following components:

### 1. Dynamic Port Assignment
- Each workflow now generates a random port in the range 11434-12434
- Port conflicts are detected and resolved automatically
- Environment variables are used to pass port information between workflow steps

### 2. Enhanced Process Cleanup
- Aggressive cleanup of existing Ollama processes before starting new ones
- Port-specific process termination
- Proper wait times for process cleanup

### 3. Ollama Client Configuration
- Updated Python scripts to use custom Ollama hosts
- Environment variable-based configuration
- Fallback mechanisms for when Ollama is unavailable

### 4. Workflow Isolation
- Each workflow uses its own port space
- Reduced dependency on Ollama for non-critical workflows
- Graceful degradation when Ollama is unavailable

## Files Modified

### GitHub Actions Workflows

#### 1. `.github/workflows/process-documents.yml`
- **Before**: Used fixed port 11434 with basic cleanup
- **After**: Dynamic port allocation with comprehensive cleanup
- **Key Changes**:
  ```bash
  # Generate random port
  OLLAMA_PORT=$((11434 + $RANDOM % 1000))
  
  # Set environment variables
  echo "OLLAMA_HOST=127.0.0.1:$OLLAMA_PORT" >> $GITHUB_ENV
  
  # Start Ollama with custom port
  export OLLAMA_HOST=127.0.0.1:$OLLAMA_PORT
  ollama serve &
  ```

#### 2. `.github/workflows/process_documents_with_ollama.yml`
- **Before**: Simple Ollama startup without port management
- **After**: Dynamic port allocation with proper environment setup
- **Key Changes**: Similar port management as above

#### 3. `.github/workflows/deploy-site.yml`
- **Before**: Always tried to run Ollama processing
- **After**: Optional Ollama processing with fallback to existing data
- **Key Changes**:
  ```bash
  # Check if Ollama is available
  if command -v ollama >/dev/null 2>&1; then
    # Try to process with Ollama
  else
    # Use existing documents.json
  fi
  ```

### Python Scripts

#### 1. `scripts/fixed_ollama_processor.py`
- **Before**: Used default Ollama client configuration
- **After**: Configurable Ollama host from environment variables
- **Key Changes**:
  ```python
  # Configure Ollama host from environment variable
  self.ollama_host = os.getenv('OLLAMA_HOST', '127.0.0.1:11434')
  if not self.ollama_host.startswith('http'):
      self.ollama_host = f"http://{self.ollama_host}"
  
  # Use custom client
  client = ollama.Client(host=self.ollama_host)
  ```

#### 2. `scripts/incremental_ollama_processor.py`
- **Before**: Inherited default Ollama configuration
- **After**: Inherits custom host configuration from parent class
- **Key Changes**: Added logging for Ollama host configuration

### New Utility

#### `scripts/ollama_port_manager.py`
A new utility script for managing Ollama port conflicts:

- **Port Detection**: Check if ports are in use
- **Process Cleanup**: Kill processes using specific ports
- **Port Allocation**: Find free ports automatically
- **Environment Setup**: Configure Ollama environment variables

Usage:
```bash
# Find a free port
python scripts/ollama_port_manager.py find-port

# Setup Ollama with safe port
python scripts/ollama_port_manager.py setup

# Cleanup existing Ollama processes
python scripts/ollama_port_manager.py cleanup

# Check if port is in use
python scripts/ollama_port_manager.py check 11434
```

## How the Fix Works

### Workflow Execution Flow

1. **Process Cleanup**: Each workflow starts by killing any existing Ollama processes
2. **Port Selection**: A random port is generated in the range 11434-12434
3. **Port Verification**: The selected port is checked for availability
4. **Environment Setup**: `OLLAMA_HOST` and related variables are configured
5. **Ollama Startup**: Ollama is started with the custom port
6. **Health Check**: The workflow waits for Ollama to become responsive
7. **Processing**: Documents are processed using the custom Ollama instance

### Python Script Integration

1. **Environment Detection**: Scripts read `OLLAMA_HOST` from environment variables
2. **Client Configuration**: Ollama client is configured with the custom host
3. **Fallback Handling**: If Ollama is unavailable, scripts use fallback analysis
4. **Error Recovery**: Robust error handling for connection issues

## Benefits

### ✅ **Eliminates Port Conflicts**
- Multiple workflows can run simultaneously without conflicts
- Each workflow uses its own port space
- Automatic conflict detection and resolution

### ✅ **Improved Reliability**
- Workflows no longer fail due to port binding issues
- Better process cleanup prevents zombie processes
- Graceful degradation when Ollama is unavailable

### ✅ **Better Resource Management**
- Workflows only start Ollama when needed
- Proper cleanup prevents resource leaks
- Reduced competition for system resources

### ✅ **Enhanced Debugging**
- Clear logging of port assignments
- Better error messages for troubleshooting
- Environment variable visibility

## Testing the Fix

### Local Testing
```bash
# Test port manager
python scripts/ollama_port_manager.py setup

# Test document processor with custom port
OLLAMA_HOST=127.0.0.1:11500 python scripts/fixed_ollama_processor.py

# Test port conflict detection
python scripts/ollama_port_manager.py check 11434
```

### GitHub Actions Testing
1. **Push changes** to trigger workflows
2. **Monitor workflow logs** for port assignments
3. **Verify concurrent execution** doesn't cause conflicts
4. **Check document processing** completes successfully

## Monitoring and Maintenance

### Log Monitoring
Look for these log messages to verify the fix is working:

```
Using Ollama port: 11567
Started Ollama with PID: 1234 on port 11567
Ollama is ready on port 11567!
Initialized processor with model: mistral:7b
Ollama host: http://127.0.0.1:11567
```

### Common Issues and Solutions

#### Issue: Port still in use after cleanup
**Solution**: Increase cleanup wait times or use the port manager utility

#### Issue: Ollama client connection errors
**Solution**: Verify `OLLAMA_HOST` environment variable is set correctly

#### Issue: Workflows timing out
**Solution**: Check if Ollama model pulling is taking too long

## Future Improvements

1. **Port Reservation System**: Implement a more sophisticated port reservation mechanism
2. **Shared Ollama Instance**: Use a single Ollama instance across workflows with request queuing
3. **Container Isolation**: Use Docker containers for better process isolation
4. **Health Monitoring**: Add more comprehensive health checks for Ollama instances

## Rollback Plan

If issues occur, you can rollback by:

1. **Revert workflow files** to use fixed port 11434
2. **Remove custom host configuration** from Python scripts
3. **Use original Ollama client** without custom host parameter

However, this will restore the original port conflict issue.

## Conclusion

This fix resolves the Ollama port binding conflicts by implementing dynamic port allocation and better process management. The solution is robust, scalable, and maintains backward compatibility while significantly improving deployment reliability.
