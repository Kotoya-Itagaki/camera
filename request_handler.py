import socketserver
from http.server import BaseHTTPRequestHandler


def run_server(controller):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(501)
            self.end_headers()

        def do_POST(self):
            self.send_response(200)
            self.end_headers()
            controller.rec_start()

    port = 8112
    with socketserver.TCPServer(("", port), Handler) as server:
        print("serving at port", port)
        server.serve_forever()
