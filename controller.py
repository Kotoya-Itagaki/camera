class CameraController():
    def __init__(self):
        self._rec_start_order= False
        self._rec_stop_order = False

    @property
    def rec_start_order(self):
        return self._rec_start_order

    @property
    def rec_stop_order(self):
        return self._rec_stop_order

    def rec_start(self):
        """
        image_capture.pyに動画の作成開始を伝える
        """

        if not self.rec_start_order:
            self._rec_start_order = True

    def rec_stop(self):
        """
        image_capture.pyに動画の作成終了を伝える
        """

        if self.rec_start_order:
            self._rec_stop_order = True

    def state_refresh(self):
        self._rec_start_order = False
        self._rec_stop_order = False