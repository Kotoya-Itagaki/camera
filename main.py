import os
import sys
import threading
from http.server import BaseHTTPRequestHandler

import image_capture
from controller import CameraController



def main():
    # Controllerクラスを生成
    controller = CameraController()

    # カメラ起動メソッドを別スレッドで起動
    cli = threading.Thread(target=image_capture.main, args=(controller,))
    cli.start()


if __name__ == '__main':
    main()