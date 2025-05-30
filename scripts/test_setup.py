#!/usr/bin/env python3
"""
Test script to verify the optimized setup works correctly
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import ollama
        print("✓ ollama imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ollama: {e}")
        return False
    
    try:
        import PyPDF2
        print("✓ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import PyPDF2: {e}")
        return False
    
    try:
        from ollama_processor import OllamaDocumentProcessor
        print("✓ OllamaDocumentProcessor imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import OllamaDocumentProcessor: {e}")
        return False
    
    return True

def test_directory_structure():
    """Test that required directories exist"""
    print("\nTesting directory structure...")
    
    base_dir = Path.cwd()
    required_dirs = ['documents', 'data', 'src', 'components']
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"✗ {dir_name}/ directory missing")
            return False
    
    return True

def test_processor_initialization():
    """Test that the processor can be initialized"""
    print("\nTesting processor initialization...")
    
    try:
        from ollama_processor import OllamaDocumentProcessor
        processor = OllamaDocumentProcessor()
        print("✓ OllamaDocumentProcessor initialized successfully")
        print(f"  - Documents directory: {processor.documents_dir}")
        print(f"  - Data directory: {processor.data_dir}")
        print(f"  - Model: {processor.model_name}")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize processor: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Testing Optimized Document Processing Setup ===\n")
    
    tests = [
        test_imports,
        test_directory_structure,
        test_processor_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"=== Test Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("✓ All tests passed! The setup is ready to use.")
        print("\nNext steps:")
        print("1. Install Ollama: curl -fsSL https://ollama.ai/install.sh | sh")
        print("2. Start Ollama: ollama serve")
        print("3. Pull DeepSeek model: ollama pull deepseek-r1:1.5b")
        print("4. Process documents: python scripts/ollama_processor.py")
    else:
        print("✗ Some tests failed. Please check the setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()
