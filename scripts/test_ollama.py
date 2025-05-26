#!/usr/bin/env python3
"""
Simple script to test Ollama connectivity and diagnose issues
"""

import ollama
import json

def test_ollama_connection():
    """Test basic Ollama connectivity"""
    print("Testing Ollama connection...")
    
    try:
        # Test basic connection
        models = ollama.list()
        print(f"✓ Ollama is running")
        print(f"Response: {models}")
        
        if 'models' in models:
            available_models = [model['name'] for model in models['models']]
            print(f"Available models: {available_models}")
            
            # Test with a simple prompt
            if available_models:
                test_model = available_models[0]
                print(f"\nTesting with model: {test_model}")
                
                response = ollama.generate(
                    model=test_model,
                    prompt="Say hello in JSON format: {\"message\": \"hello\"}"
                )
                
                print(f"Test response: {response}")
                
                if 'response' in response:
                    print(f"Response text: {response['response']}")
                else:
                    print("No 'response' key in response")
            else:
                print("No models available")
        else:
            print("No 'models' key in response")
            
    except Exception as e:
        print(f"✗ Ollama connection failed: {e}")
        print("Make sure Ollama is running with: ollama serve")
        print("And that you have a model installed, e.g.: ollama pull llama2")

if __name__ == "__main__":
    test_ollama_connection()
