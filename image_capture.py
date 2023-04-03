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


def main(controller):
    """main function"""

    log.info('=====================================')
    log.info('=============== START ===============')
    log.info('=====================================')

    # 設定ファイル読み込み
    try:
        config = configparser.ConfigParser()
        config.read('./config.ini')
        location = config['DEFAULT']['location']
        rec_time = config['DEFAULT']['rec_time']

    except FileNotFoundError:
        raise

    # カメラに接続する
    camera = Camera(config)

    # フレームを読み込み続けるスレッドを起動
    frame_reader = threading.Thread(target=camera.read_frame)
    frame_reader.setDaemon(True)
    frame_reader.start()

    codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video_writer = VideoWriter(camera, codec, config)

    while(True):
        # ディスプレイにカメラから取得した画像を表示
        frame = camera.frame
        cv2.imshow(location, frame)

        # 動画を作成
        if controller.rec_start_order:

            # 開始処理
            if video_writer.video is None:
                log.info('録画を開始します。')
                video_writer.rec_start()

            # 終了処理 (録画終了フラグを立てるか、設定した時間が経過すると終了)
            if controller.rec_stop_order or time.time() > (video_writer.base_time + rec_time * 60):
                log.info('録画を終了します。')
                video_writer.rec_stop()
                log.info('動画を保存しました。')

                controller.state_refresh()

        # 強制終了時
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            log.info(f'[q]が押されたのでシステムを終了します。')

            # 動画を保存する
            if video_writer.video:
                # 保存(error)
                log.info('録画中のため、強制保存します。')
                video_writer.rec_stop()

            break