from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from database import insert_user, get_user_by_email, update_user, delete_user

class MyHandler(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*") 
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS,PUT,DELETE")
        self.send_header("Access-Control-Allow-Headers", "content-type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        user_data = json.loads(post_data.decode('utf-8'))

        if self.path == '/register':
            email = user_data.get("email")
            name = user_data.get("name")
            password = user_data.get("password")  
            success = insert_user(name, email, password)
            
            
            self._send_response({"success": success})

        elif self.path == '/login':
            email = user_data.get("email")
            password = user_data.get("password")
            
            
            user = get_user_by_email(email)
            if user and user["password"] == password:
                self._send_response({"success": True, "message": "Successful login!"})
            else:
                self._send_response({"success": False, "message": "Invalid credentials!"})

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        user_data = json.loads(put_data.decode('utf-8'))

        if self.path == '/update':
            email = user_data.get("email")
            name = user_data.get("name", None)
            password = user_data.get("password", None)
            success = update_user(email, name, password)
            self._send_response({"success": success})

    def do_DELETE(self):
        content_length = int(self.headers['Content-Length'])
        delete_data = self.rfile.read(content_length)
        user_data = json.loads(delete_data.decode('utf-8'))

        if self.path == '/delete':
            email = user_data.get("email")
            success = delete_user(email)
            self._send_response({"success": success})

    def _send_response(self, data):
        self.send_response(200)
        self._send_cors_headers() 
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

# HTTP server
if __name__ == "__main__":
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Starting server on http://127.0.0.1:8000...')
    httpd.serve_forever()
