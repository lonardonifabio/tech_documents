#!/usr/bin/env python3
"""
Test script for the fixed Ollama processor
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from ollama_processor_fixed import FixedOllamaDocumentProcessor

def test_json_parsing():
    """Test the JSON parsing functionality"""
    processor = FixedOllamaDocumentProcessor()
    
    # Test cases with different types of malformed JSON responses
    test_cases = [
        # Valid JSON
        '{"title": "Test Document", "summary": "A test summary", "keywords": ["test", "document"], "category": "Technology", "difficulty": "Beginner", "authors": [], "content_preview": "Test content"}',
        
        # JSON with extra text before and after
        'Here is the analysis:\n{"title": "Test Document", "summary": "A test summary", "keywords": ["test", "document"], "category": "Technology", "difficulty": "Beginner", "authors": [], "content_preview": "Test content"}\nThat completes the analysis.',
        
        # JSON with trailing comma
        '{"title": "Test Document", "summary": "A test summary", "keywords": ["test", "document"], "category": "Technology", "difficulty": "Beginner", "authors": [], "content_preview": "Test content",}',
        
        # Incomplete JSON (should fall back to regex extraction)
        '{"title": "Test Document", "summary": "A test summary", "keywords": ["test", "document"], "category": "Technology"',
        
        # No JSON at all (should return None)
        'This is just plain text with no JSON structure.',
    ]
    
    print("=== Testing JSON Parsing ===\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test case {i}:")
        print(f"Input: {test_case[:100]}{'...' if len(test_case) > 100 else ''}")
        
        result = processor.parse_ollama_response(test_case)
        
        if result:
            print(f"✓ Successfully parsed: {result}")
        else:
            print("✗ Failed to parse (will use fallback)")
        
        print("-" * 50)

def test_fallback_analysis():
    """Test the fallback analysis functionality"""
    processor = FixedOllamaDocumentProcessor()
    
    test_filenames = [
        "machine_learning_guide.pdf",
        "data_science_handbook.pdf",
        "business_analytics_report.pdf",
        "python_programming_tutorial.pdf",
        "unknown_document.pdf"
    ]
    
    print("\n=== Testing Fallback Analysis ===\n")
    
    for filename in test_filenames:
        print(f"Testing filename: {filename}")
        result = processor._get_fallback_analysis(filename)
        print(f"Result: {result}")
        print("-" * 50)

if __name__ == "__main__":
    test_json_parsing()
    test_fallback_analysis()
    
    print("\n=== Summary ===")
    print("The fixed processor includes:")
    print("1. Robust JSON parsing with multiple fallback strategies")
    print("2. Regex-based field extraction when JSON parsing fails")
    print("3. Improved validation and cleaning of analysis data")
    print("4. Better error handling and logging")
    print("5. Enhanced prompts for more consistent Ollama responses")
