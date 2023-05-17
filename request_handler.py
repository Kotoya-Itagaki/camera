import json
import socketserver
from http.server import BaseHTTPRequestHandler

from controller import CameraController


class Handler(BaseHTTPRequestHandler):
    # Controllerクラスを生成
    controller = CameraController()

    def do_GET(self):
        self.send_response(501)
        self.end_headers()

    def do_POST(self):
        content_len=int(self.headers.get('content-length'))
        requestBody = json.loads(self.rfile.read(content_len).decode('utf-8'))

        # statusがstart
        if requestBody.get('status') == 'start':
            print('start')
            rec_state = self.controller.rec_start_order()
            self.send_response(200)

        # statusがend
        if requestBody.get('status') == 'end':
            print('end')
            rec_state = self.controller.rec_stop_order()

            self.send_response(200)

        self.end_headers()


def run_server():
    port = 8112
    with socketserver.TCPServer(("", port), Handler) as server:
        print("serving at port", port)
        server.serve_forever()