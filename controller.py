import image_capture


class CameraController():
    recorder = image_capture.Image_Capture()

    def rec_start_order(self):
        if not self.recorder.is_recording:
            self.recorder.rec_start()

        else:
            print('すでに録画中')

    def rec_stop_order(self):
        if self.recorder.is_recording:
            self.recorder.rec_stop()

            # S3に動画を保存

        else:
            print('録画していません')