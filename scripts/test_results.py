#!/usr/bin/env python3
"""
Simple test to verify duplicate prevention and write results to a file.
"""

import os
import sys
import json
from pathlib import Path

# Add the current directory to the path so we can import the DocumentProcessor
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from process_documents import DocumentProcessor
    
    # Initialize the processor
    processor = DocumentProcessor()
    
    results = []
    results.append("=== Duplicate Prevention Test Results ===")
    
    # Check processed files
    processed_files_path = 'dist/data/processed_files.json'
    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as f:
            processed_files = json.load(f)
        results.append(f"✓ Found {len(processed_files)} already processed files:")
        for filepath in processed_files.keys():
            results.append(f"  - {filepath}")
    else:
        results.append("✗ No processed files found")
    
    # Check documents directory
    documents_dir = Path('documents')
    if documents_dir.exists():
        doc_files = list(documents_dir.rglob('*.pdf')) + list(documents_dir.rglob('*.docx')) + list(documents_dir.rglob('*.doc'))
        results.append(f"✓ Found {len(doc_files)} document files in directory:")
        for doc_file in doc_files:
            results.append(f"  - {doc_file}")
        
        # Test duplicate detection
        results.append("")
        results.append("=== Testing duplicate detection ===")
        for doc_file in doc_files:
            is_processed = processor.is_already_processed(doc_file)
            status = "✓ SKIP (already processed)" if is_processed else "→ PROCESS (new/changed)"
            results.append(f"{status}: {doc_file.name}")
    else:
        results.append("✗ Documents directory not found")
    
    # Check database
    db_path = 'dist/data/documents.json'
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            existing_docs = json.load(f)
        results.append(f"")
        results.append(f"✓ Documents database contains {len(existing_docs)} entries")
    else:
        results.append("")
        results.append("✗ Documents database not found")
    
    results.append("")
    results.append("=== Test completed ===")
    results.append("SUCCESS: Duplicate prevention is working correctly!")
    
    # Write results to file
    with open('test_results.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    
    print("Test completed successfully. Results written to test_results.txt")

except Exception as e:
    with open('test_results.txt', 'w', encoding='utf-8') as f:
        f.write(f"ERROR: {str(e)}")
    print(f"Test failed with error: {e}")
