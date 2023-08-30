from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from database import insert_user  

class MyHandler(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        
        self.send_header("Access-Control-Allow-Origin", "*") 
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")

    def do_OPTIONS(self):
        
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path == '/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            user_data = json.loads(post_data.decode('utf-8'))
            
            email = user_data.get("email")
            name = user_data.get("name")
            password = user_data.get("password")  
            
            success = insert_user(name, email, password)

            # response
            self.send_response(200)
            self._send_cors_headers() 
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": success}).encode())

# HTTP server
if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Starting server on http://127.0.0.1:8000...')
    httpd.serve_forever()
