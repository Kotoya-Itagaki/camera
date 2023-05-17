import image_capture


class CameraController():
    recorder = image_capture.Image_Capture()

    def rec_start_order(self) -> bool:
        if not self.recorder.is_recording:
            self.recorder.rec_start()
            is_record_start = True

        else:
            print('すでに録画中')
            is_record_start = False

        return is_record_start

    def rec_stop_order(self) -> bool:
        if self.recorder.is_recording:
            self.recorder.rec_stop()
            is_record_end = True
            # S3に動画を保存

        else:
            print('録画していません')
            is_record_end = False

        return is_record_end