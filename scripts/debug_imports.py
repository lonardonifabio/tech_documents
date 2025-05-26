#!/usr/bin/env python3
"""
Debug script to test imports and basic functionality
"""

print("Starting debug script...")

# Test basic imports
try:
    import os
    import json
    import hashlib
    from datetime import datetime
    from pathlib import Path
    print("✓ Basic imports successful")
except Exception as e:
    print(f"✗ Basic imports failed: {e}")

# Test ollama import
try:
    import ollama
    print("✓ Ollama import successful")
except Exception as e:
    print(f"✗ Ollama import failed: {e}")

# Test langchain imports
try:
    from langchain_community.document_loaders import PyPDFLoader
    print("✓ PyPDFLoader import successful")
except Exception as e:
    print(f"✗ PyPDFLoader import failed: {e}")

# Test if we can list documents
try:
    documents_dir = Path('documents')
    pdf_files = list(documents_dir.glob('*.pdf'))
    print(f"✓ Found {len(pdf_files)} PDF files")
    for pdf in pdf_files[:3]:  # Show first 3
        print(f"  - {pdf.name}")
except Exception as e:
    print(f"✗ Error listing documents: {e}")

# Test PDF loading
if 'PyPDFLoader' in locals():
    try:
        pdf_files = list(Path('documents').glob('*.pdf'))
        if pdf_files:
            test_file = pdf_files[0]
            print(f"Testing PDF loading with: {test_file.name}")
            loader = PyPDFLoader(str(test_file))
            docs = loader.load()
            print(f"✓ Successfully loaded PDF with {len(docs)} pages")
            if docs:
                print(f"  First page preview: {docs[0].page_content[:100]}...")
        else:
            print("No PDF files found to test")
    except Exception as e:
        print(f"✗ PDF loading failed: {e}")

print("Debug script completed.")
