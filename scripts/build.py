import os
import shutil
import json
from pathlib import Path

def build_site():
    """Build del sito statico per GitHub Pages"""

    # Crea directory dist
    dist_dir = Path('dist')
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

    # Copia file HTML e JS
    shutil.copytree('src', dist_dir / 'src')

    # Copia index.html nella root
    shutil.copy('src/index.html', dist_dir / 'index.html')

    # Copia database documenti
    if Path('data').exists():
        shutil.copytree('data', dist_dir / 'data')
    else:
        # Crea database vuoto se non esiste
        (dist_dir / 'data').mkdir()
        with open(dist_dir / 'data' / 'documents.json', 'w') as f:
            json.dump([], f)

    print("Build completato in /dist")

if __name__ == "__main__":
    build_site()
