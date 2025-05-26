import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
import ollama
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain.schema import Document

class DocumentProcessor:
    def __init__(self):
        self.processed_files = self.load_processed_files()
        self.documents_db = []

    def load_processed_files(self):
        if os.path.exists('dist/data/processed_files.json'):
            with open('data/processed_files.json', 'r') as f:
                return json.load(f)
        return {}

    def save_processed_files(self):
        os.makedirs('data', exist_ok=True)
        with open('data/processed_files.json', 'w') as f:
            json.dump(self.processed_files, f)

    def get_file_hash(self, filepath):
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def load_document(self, filepath):
        file_ext = Path(filepath).suffix.lower()
    
        if file_ext == '.pdf':
            loader = PyPDFLoader(str(filepath))  # Converti in stringa
        elif file_ext in ['.docx', '.doc']:
            loader = Docx2txtLoader(str(filepath))  # Converti in stringa
        else:
            return None
    
        return loader.load()

    def summarize_with_llama(self, text):
        prompt = f"""
        Analizza questo documento accademico e fornisci:
        1. Un riassunto di 2-3 frasi
        2. 5 parole chiave principali
        3. Categoria (es: Machine Learning, Deep Learning, NLP, Computer Vision, Data Science)
        4. Livello di difficoltà (Beginner/Intermediate/Advanced)

        Documento:
        {text[:4000]}

        Rispondi in formato JSON:
        ```json
        {{
            "summary": "...",
            "keywords": ["keyword1", "keyword2", ...],
            "category": "...",
            "difficulty": "..."
        }}
        ```
        """

        response = ollama.generate(model='llama2:7b', prompt=prompt)

        try:
            # Estrai JSON dalla risposta
            json_start = response['response'].find('{')
            json_end = response['response'].rfind('}') + 1
            json_str = response['response'][json_start:json_end]
            return json.loads(json_str)
        except:
            return {
                "summary": "Documento di intelligenza artificiale e data science",
                "keywords": ["AI", "Data Science"],
                "category": "General",
                "difficulty": "Intermediate"
            }

    def process_documents(self):
        documents_dir = Path('documents')
        new_documents = []

        for filepath in documents_dir.rglob('*'):
            if not filepath.is_file():
                continue

            if filepath.suffix.lower() not in ['.pdf', '.docx', '.doc']:
                continue

            file_hash = self.get_file_hash(filepath)

            if str(filepath) in self.processed_files:
                if self.processed_files[str(filepath)] == file_hash:
                    continue

            print(f"Processing: {filepath}")

            # Carica documento
            docs = self.load_document(filepath)
            if not docs:
                continue

            # Combina tutto il testo
            full_text = " ".join([doc.page_content for doc in docs])

            # Genera metadati con Llama
            metadata = self.summarize_with_llama(full_text)

            # Crea entry per database
            doc_entry = {
                "id": hashlib.md5(str(filepath).encode()).hexdigest(),
                "filename": filepath.name,
                "filepath": str(filepath),
                "upload_date": datetime.now().isoformat(),
                "file_size": filepath.stat().st_size,
                "summary": metadata["summary"],
                "keywords": metadata["keywords"],
                "category": metadata["category"],
                "difficulty": metadata["difficulty"],
                "content_preview": full_text[:500] + "..." if len(full_text) > 500 else full_text
            }

            new_documents.append(doc_entry)
            self.processed_files[str(filepath)] = file_hash

        if new_documents:
            self.update_database(new_documents)
            self.save_processed_files()
            print(f"Processed {len(new_documents)} new documents")

    def update_database(self, new_documents):
        # Carica database esistente
        db_path = 'data/documents.json'
        if os.path.exists(db_path):
            with open(db_path, 'r') as f:
                existing_docs = json.load(f)
        else:
            existing_docs = []

        # Aggiungi nuovi documenti
        existing_docs.extend(new_documents)

        # Salva database aggiornato
        os.makedirs('data', exist_ok=True)
        with open(db_path, 'w') as f:
            json.dump(existing_docs, f, indent=2)

if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.process_documents()
