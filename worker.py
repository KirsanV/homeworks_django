from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

PORT = 8000

HTML_FILES = {
    "/": "index.html",
    "/catalog": "catalog.html",
    "/categories": "categories.html",
    "/contacts": "contacts.html"
}


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?')[0]
        if path in HTML_FILES:
            filename = HTML_FILES[path]
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"<h1>404 Not Found</h1>")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1>")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = urllib.parse.parse_qs(post_data)

        print("Получены данные от пользователя:")
        for key, value in data.items():
            print(f"{key}: {value}")

        if self.path == "/contacts":
            try:
                with open("contacts.html", "r", encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"<h1>404 Not Found</h1>")
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            response_html = "<h2>Данные успешно отправлены!</h2>"
            self.wfile.write(response_html.encode('utf-8'))


if __name__ == "__main__":
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, MyHandler)
    print(f"Сервер запущен на порту {PORT}")
    httpd.serve_forever()
