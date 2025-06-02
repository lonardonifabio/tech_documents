#!/usr/bin/env python3
"""
Debug script to analyze Ollama responses and identify JSON parsing issues
"""

import ollama
import json
import re

def test_ollama_json_response():
    """Test Ollama response and debug JSON parsing issues"""
    print("=== Ollama JSON Response Debug ===\n")
    
    try:
        # Test basic connection
        models = ollama.list()
        print("✓ Ollama is running")
        
        if 'models' in models and models['models']:
            # Use the first available model
            model_name = models['models'][0]['name']
            print(f"Using model: {model_name}\n")
            
            # Test with a simple JSON prompt
            prompt = """Analyze this document and provide a JSON response with the following structure:
{
    "title": "Clean, readable title",
    "summary": "summary of the document content with max 400 characters",
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "category": "just one of: AI, Machine Learning, Data Science, Analytics, Business, Technology, Research",
    "difficulty": "just one of: Beginner, Intermediate, Advanced",
    "authors": ["author1", "author2"] or [] if not found,
    "content_preview": "First 100 characters of meaningful content"
}

Document filename: test_document.pdf
Document content:
This is a test document about machine learning algorithms and their applications in data science.

Respond only with valid JSON, no additional text."""

            print("Sending prompt to Ollama...")
            response = ollama.generate(
                model=model_name,
                prompt=prompt,
                options={
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 500
                }
            )
            
            print(f"Raw response object: {response}")
            print(f"Response keys: {list(response.keys())}")
            
            if 'response' in response:
                response_text = response['response'].strip()
                print(f"\nRaw response text:")
                print(f"'{response_text}'")
                print(f"\nResponse length: {len(response_text)}")
                print(f"Response type: {type(response_text)}")
                
                # Check for common issues
                print(f"\nDiagnostic checks:")
                print(f"- Starts with {{: {response_text.startswith('{')}")
                print(f"- Ends with }}: {response_text.endswith('}')}")
                print(f"- Contains newlines: {'\\n' in response_text}")
                print(f"- Contains extra text before JSON: {not response_text.lstrip().startswith('{')}")
                print(f"- Contains extra text after JSON: {not response_text.rstrip().endswith('}')}")
                
                # Try to find JSON in the response
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    json_part = json_match.group(0)
                    print(f"\nExtracted JSON part:")
                    print(f"'{json_part}'")
                    
                    try:
                        parsed = json.loads(json_part)
                        print(f"\n✓ Successfully parsed JSON:")
                        print(json.dumps(parsed, indent=2))
                    except json.JSONDecodeError as e:
                        print(f"\n✗ JSON parsing failed: {e}")
                        print(f"Error at position: {e.pos}")
                        if e.pos < len(json_part):
                            print(f"Character at error position: '{json_part[e.pos]}'")
                            print(f"Context around error: '{json_part[max(0, e.pos-10):e.pos+10]}'")
                else:
                    print(f"\n✗ No JSON structure found in response")
                
                # Try direct parsing
                try:
                    parsed = json.loads(response_text)
                    print(f"\n✓ Direct JSON parsing successful:")
                    print(json.dumps(parsed, indent=2))
                except json.JSONDecodeError as e:
                    print(f"\n✗ Direct JSON parsing failed: {e}")
            else:
                print("✗ No 'response' key in Ollama response")
                
        else:
            print("✗ No models available")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ollama_json_response()
