import configparser
import os
import threading
import time

os.environ['OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS'] = '0'
import cv2

from camera_image import Camera
from logger import get_logger
from video import VideoWriter


log = get_logger(__name__)


class Image_Capture:
    def __init__(self):
        self.is_recording = False
        self.snapshot_dir = './snapshot'

        # snapshotフォルダの作成
        if not os.path.exists(self.snapshot_dir):
            os.mkdir(self.snapshot_dir)

        # 設定ファイル読み込み
        try:
            config = configparser.ConfigParser()
            config.read('./config.ini')
            self.location = config.get('DEFAULT', 'location')
            self.rec_time = config.getint('DEFAULT', 'rec_time_sec')
            self.write_fps = config.getint('DEFAULT', 'write_fps')
            self.read_width = config.getint('DEFAULT', 'read_width')
            self.read_height = config.getint('DEFAULT', 'read_height')

        except FileNotFoundError:
            raise

        # カメラに接続する
        self.camera = Camera(config)

    def rec_start(self):
        log.info('=====================================')
        log.info('=============== START ===============')
        log.info('=====================================')

        self.is_recording = True
        recorder = threading.Thread(target=self.recording)
        recorder.setDaemon(True)
        recorder.start()

    def recording(self):
        # フレームを読み込み続けるスレッドを起動
        frame_reader = threading.Thread(target=self.camera.read_frame)
        frame_reader.setDaemon(True)
        frame_reader.start()

        log.info('録画を開始します。')
        codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.video_writer = VideoWriter(self.camera, codec, self.write_fps, self.read_width, self.read_height)
        self.video_writer.rec_start()

        measured_time = time.time()

        while(self.is_recording):
            # ディスプレイにカメラから取得した画像を表示
            cv2.imshow(self.location, self.camera.frame)

            # S3に画像を3秒間隔でアップロード
            if time.time() - measured_time > 3:
                cv2.imwrite(f'{self.snapshot_dir}/{self.location}.jpeg', self.camera.frame)
                measured_time = time.time()

            # 終了処理 (設定した時間が経過すると終了)
            if time.time() > (self.video_writer.base_time + self.rec_time * 60):
                self.rec_stop()

            # 強制終了時
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                self.is_recording = False
                log.info(f'[q]が押されたのでシステムを終了します。')

                # 動画を保存する
                if self.video_writer.video:
                    # 保存(error)
                    log.info('録画中のため、強制保存します。')
                    self.video_writer.rec_stop()

                break

    def rec_stop(self):
        self.is_recording = False
        log.info('録画を終了します。')
        self.video_writer.rec_stop()
        log.info('動画を保存しました。')