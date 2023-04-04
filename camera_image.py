import os
import re
import time

os.environ['OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS'] = '0'
import cv2
import numpy as np

from logger import get_logger


log = get_logger(__name__)


class Camera:
    text_position = (25, 25) # テキスト位置
    text_color = (0, 255, 255) # テキスト色

    def __init__(self, config):
        self.camera_address = config.get('DEFAULT', 'camera_address')
        self.width = config.getint('DEFAULT', 'read_width')
        self.height = config.getint('DEFAULT', 'read_height')
        self.fps = config.getint('DEFAULT', 'read_fps')
        self.location = config.get('DEFAULT', 'location')
        self.retry_sec = config.getint('DEFAULT', 'retry_sec')
        self.capture = None

        # カメラのアドレスが数字のみで構成されている場合、int型にキャスト
        if re.fullmatch('[0-9]+', self.camera_address):
            self.camera_address = int(self.camera_address)

        # カメラと接続する
        self.connect_camera()

        # フレームに初期値として、黒い画像をセット
        self.frame = self.generate_black_image()

    def connect_camera(self):
        """
        カメラに接続する

        接続できるまで再試行を繰り返し、無限ループする

        returns:
            capture(cv2.VideoCapture class)
        """

        while(True):
            self.capture = cv2.VideoCapture(self.camera_address, cv2.CAP_DSHOW)

            if self.capture.isOpened():
                log.info(f'カメラに接続しました。camera:{self.camera_address}')
                self.capture.set(cv2.CAP_PROP_FPS, self.fps)
                self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                break

            else:
                log.error(f'カメラに接続できませんでした。camera:{self.camera_address}')
                time.sleep(self.retry_sec)

    def read_frame(self):
        """
        フレームを読み続けるスレッド

        args:
            capture(cv2.VideoCapture class)

        """

        while(True):
            ret, frame = self.capture.read()

            if not ret:
                log.warn('カメラから画像が読み取れませんでした。')

                # 黒の画像を生成する
                self.generate_black_image()

                # カメラに再接続する
                self.capture = self.connect_camera()

            else:
                self.frame = cv2.resize(frame, (self.width, self.height))

    def generate_black_image(self):
        """
        黒い画像を生成する
        """

        black_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        return cv2.resize(black_frame, (self.width, self.height))