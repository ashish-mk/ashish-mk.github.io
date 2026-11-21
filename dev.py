#!/usr/bin/env python3
"""
Local development server for Ashish Kulkarni's website.
Builds the site and starts an HTTP server serving the dist/ folder.
"""

import sys
import os
import http.server
import socketserver
from pathlib import Path
from build import build, DIST_DIR

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIST_DIR), **kwargs)

    def end_headers(self):
        # Disable caching in dev server
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

def main():
    print("=" * 60)
    print("Building website...")
    build()
    print("=" * 60)
    print(f"Starting local preview server at: http://localhost:{PORT}")
    print(f"From inside WSL2 or Windows browser, visit: http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 60)

    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
