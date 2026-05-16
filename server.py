import os
os.chdir('/home/Nerart/Pobrane/temp/Server/')
from http.server import HTTPServer, SimpleHTTPRequestHandler
class CORSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        super().end_headers()
HTTPServer(('0.0.0.0', 80), CORSHandler).serve_forever()
