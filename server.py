import os
import sys
import platform
from http.server import HTTPServer, SimpleHTTPRequestHandler

os.chdir('/home/Nerart/Pobrane/temp/Server/')

class CORSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        super().end_headers()

answer = input("Use default port (80)? (y/n): ").strip().lower()

if answer == 'y':
    port = 80
else:
    while True:
        try:
            port = int(input("Enter port number: ").strip())
            break
        except ValueError:
            print("Invalid input, please enter a number.")

host = '0.0.0.0'
server_dir = os.getcwd()
python_version = platform.python_version()

print(f"Server address: http://{host}:{port}")
print(f"Serving directory: {server_dir}")
print(f"Python version: {python_version}")

HTTPServer((host, port), CORSHandler).serve_forever()
