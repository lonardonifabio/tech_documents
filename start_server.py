#!/usr/bin/env python3
"""
Simple HTTP server to serve the AI & Data Science Document Library
Run this script to start the web server and view the document library.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def main():
    # Set the port
    PORT = 8000
    
    # Change to the project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Create the HTTP server
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🚀 Starting AI & Data Science Document Library server...")
            print(f"📂 Serving files from: {project_dir}")
            print(f"🌐 Server running at: http://localhost:{PORT}")
            print(f"📖 Document Library: http://localhost:{PORT}/src/index.html")
            print(f"📊 Documents JSON: http://localhost:{PORT}/data/documents.json")
            print("\n💡 The browser will open automatically in a few seconds...")
            print("🛑 Press Ctrl+C to stop the server\n")
            
            # Open the browser automatically
            webbrowser.open(f"http://localhost:{PORT}/src/index.html")
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: Port {PORT} is already in use.")
            print(f"💡 Try stopping other servers or use a different port.")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
