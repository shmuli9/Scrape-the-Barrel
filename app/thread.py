from threading import Thread

from flask import current_app


class CThread(Thread):
    """
    Custom thread based on threading.Thread, which automatically gives flask context to the run function
    Usage is identical to threading.Thread
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_app = current_app._get_current_object()

    def run(self):
        with self.current_app.app_context():
            super().run()
