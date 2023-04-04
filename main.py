import os
import sys
import threading
from http.server import BaseHTTPRequestHandler

import image_capture
import request_handler
from controller import CameraController


def main():
    # Controllerクラスを生成
    controller = CameraController()

    # ソケット通信の開始メソッドを別スレッドで起動
    run_server_thread = threading.Thread(target=request_handler.run_server, args=(controller,))
    run_server_thread.setDaemon(True)
    run_server_thread.start()

    # カメラ起動メソッドを別スレッドで起動
    image_capture_thread = threading.Thread(target=image_capture.main, args=(controller,))
    image_capture_thread.start()


if __name__ == '__main__':
    main()