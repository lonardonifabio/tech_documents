import os
import shutil
import json
from pathlib import Path

def build_site():
    """Build static site for GitHub Pages"""

    # Create dist directory
    dist_dir = Path('dist')
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

    # Copy HTML and JS files
    shutil.copytree('src', dist_dir / 'src')

    # Copy index.html to root
    shutil.copy('src/index.html', dist_dir / 'index.html')

    # Copy documents database
    if Path('data').exists():
        shutil.copytree('data', dist_dir / 'data')
    else:
        # Create empty database if it doesn't exist
        (dist_dir / 'data').mkdir()
        with open(dist_dir / 'data' / 'documents.json', 'w') as f:
            json.dump([], f)

    print("Build completed in /dist")

if __name__ == "__main__":
    build_site()
