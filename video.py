import datetime as dt
import threading
import time

import cv2

from camera_image import Camera


class VideoWriter:
    """動画を作成するクラス"""

    def __init__(self, camera: Camera, codec, config):
        """
        args:
            camera(Camera): カメラのインスタンス
            codec(cv2.VideoWriter_fourcc): 動画のコーデック
            config(ConfigParser): 設定ファイルから読み込んだ情報
        """
        self.camera = camera
        self.codec = codec
        self.write_fps = config.getint('DEFAULT', 'write_fps')
        self.read_width = config.getint('DEFAULT', 'read_width')
        self.read_height = config.getint('DEFAULT', 'read_height')
        self.save_video_dir = './video'
        self.video = None
        self.is_writing = False

    def _get_file_name(self):
        """ファイル名を取得する"""

        start_time = dt.datetime.now()
        return f"{self.save_video_dir}/{start_time.strftime('%Y%m%d_%H%M%S%f')[:-3]}.mp4"

    def create(self):
        """動画を作成する"""

        self.base_time = time.time()
        self.file_name = self._get_file_name()
        self.video = cv2.VideoWriter(self.file_name, self.codec, self.write_fps, (self.read_width, self.read_height))

    def write(self, camera):
        """
        動画を記録するスレッド

        """

        process_time = 1 / self.write_fps
        current_time = process_time

        while self.is_writing:
            ref_time = time.perf_counter()
            cv2.waitKey(1)
            frame = camera.frame

            current_time = current_time + (time.perf_counter() - ref_time)
            ref_time = time.perf_counter()

            # write_FPSが実際の性能より低い場合
            if (process_time > current_time):
                current_time = current_time + (time.perf_counter() - ref_time)
                continue

            # write_FPSが実際の性能より高い場合
            while(process_time <= current_time):
                self.video.write(frame)

                current_time = current_time + (time.perf_counter() - ref_time) - process_time
                ref_time = time.perf_counter()

    def rec_start(self):
        """録画を開始する"""

        self.create()
        self.is_writing = True

        # 動画書き込みのスレッドを起動する
        self.video_thread = threading.Thread(target=self.write, args=(self.camera,))
        self.video_thread.setDaemon(True)
        self.video_thread.start()

    def rec_stop(self):
        """録画を終了する"""

        self.is_writing = False

        # 動画書き込みのスレッドの終了を待ち、動画を保存する
        self.video_thread.join()
        self._release()

        return self.file_name

    def _release(self):
        """動画をリリースする"""

        self.video.release()
        self.video = None

    def get_video_duration(self):
        """動画の長さを取得(検証用)"""

        # 動画の長さを取得
        video_capture = cv2.VideoCapture(self.file_name)
        video_frame_count = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        video_duration = int(video_frame_count / self.write_fps)
        video_capture.release()

        return video_duration