import os
import sys
import platform
from http.server import HTTPServer, SimpleHTTPRequestHandler

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


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

try:
    HTTPServer((host, port), CORSHandler).serve_forever()
except PermissionError:
    print(f"\nPermission denied for port {port}.")
    if os.name == 'nt':
        print("Try running this terminal as Administrator, or choose a port above 1024.")
    else:
        print("Try running with 'sudo', or choose a port above 1024.")
    sys.exit(1)
except OSError as e:
    print(f"\nCould not start server: {e}")
    print("The port may already be in use — try a different one.")
    sys.exit(1)
