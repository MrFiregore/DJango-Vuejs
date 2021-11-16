import threading
import time
from queue import Queue
from watchdog.events import FileSystemEventHandler


class CsvHandler(FileSystemEventHandler):

    def __init__(self, pattern=None):
        self.event_q = Queue()
        self.dummyThread = None
        self.pattern = pattern or ".csv"

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(self.pattern):
            self.event_q.put((event, time.time()))

    def start(self):
        try:
            self.dummyThread = threading.Thread(target=self._process, daemon=True)
            self.dummyThread.start()
        except (KeyboardInterrupt, OSError) as e:
            self.dummyThread.join()

    @staticmethod
    def _process():
        while True:
            time.sleep(1)
