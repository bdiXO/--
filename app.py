import http.server
import socketserver
import requests
import json

# This script serves the HTML file AND acts as a data proxy
PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # If the browser asks for /data, we fetch from Bybit for it
        if self.path.startswith('/get_bybit_data'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Fetch real data from Bybit directly via Python (No CORS block here)
            url = "https://api.bybit.com/v5/market/kline?category=inverse&symbol=BTCUSD&interval=5&limit=100"
            data = requests.get(url).json()
            self.wfile.write(json.dumps(data).encode())
        else:
            # Otherwise, serve the HTML file like normal
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server started at http://localhost:{PORT}")
    httpd.serve_forever()