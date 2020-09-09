from threading import Thread

from flask import current_app


class CThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_app = current_app._get_current_object()

    def run(self):
        with self.current_app.app_context():
            super().run()
