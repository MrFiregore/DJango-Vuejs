import csv
import glob
import os
import time
import threading
from itertools import groupby
import pathlib
import numpy as np
from watchdog.observers import Observer
from .CsvHandler import CsvHandler
from .models import Asteroid, Observatory, Device, Sighting
from django.conf import settings


class Utils:
    event_list_flag = 0

    def __init__(self):
        self.__src_path = os.path.join(settings.BASE_DIR, 'sightings')
        self.watcher_thread = threading.Thread(target=self.run_daemon, daemon=True)

    def run(self):
        for file in glob.glob(
                os.path.join(self.__src_path, '*.csv')):
            self.run_sightings(file)

        try:
            self.watcher_thread.start()
        except (KeyboardInterrupt, OSError):
            self.watcher_thread.join()

    def run_daemon(self):
        event_handler = CsvHandler()
        event_handler.start()

        event_observer = Observer()
        event_observer.schedule(
            event_handler,
            self.__src_path,
            recursive=False
        )
        event_observer.start()

        try:
            while True:
                if self.event_list_flag == 0:
                    self.event_list_flag = 1
                    while not event_handler.event_q.empty():
                        event, ts = event_handler.event_q.get()
                        self.run_sightings(event.src_path)
                    self.event_list_flag = 0
                time.sleep(1)
        except (KeyboardInterrupt, OSError):
            event_observer.stop()
        event_observer.join()

    @staticmethod
    def nonzero_submatrix(ar):
        try:
            ar = np.array(ar)
            il = 0
            while not np.any(ar[il, :]):
                il += 1

            iu = ar.shape[0]
            while not np.any(ar[iu - 1, :]):
                iu -= 1

            jl = 0
            while not np.any(ar[il:iu, jl]):
                jl += 1

            ju = ar.shape[1]
            while not np.any(ar[il: iu, ju - 1]):
                ju -= 1

            return ar[il:iu, jl:ju].copy()

        except IndexError:
            return None

    @staticmethod
    def csv_dict_list(file_path):
        f = open(file_path)
        dict_list = []
        try:
            reader = csv.DictReader(f, delimiter='\t')
            for line in reader:
                dict_list.append(line)
        finally:
            f.close()
        return dict_list

    def run_sightings(self, file):
        """
        Process a sighting csv file and store into DB

        Args:
            file (str): absolute path to CSV file

        Returns:
            None:
        """
        for i in self.csv_dict_list(file):
            date = i.get('date')
            time = i.get('time')
            device_resolution = i.get('device_resolution')
            observatory_code = i.get('observatory_code')
            device_code = i.get('device_code')
            device_matrix = i.get('device_matrix')
            w, h = [int(x) for x in device_resolution.split('x')]
            plain_matrix = list(map(int, device_matrix[:w * h]))
            matrix = np.array(plain_matrix).reshape(h, w)
            mask = matrix.any(0)
            asteroids = [np.array(self.nonzero_submatrix(matrix[:, [*g]])) for k, g in
                         groupby(np.arange(len(mask)), lambda x: mask[x] != 0) if k]

            observatory, created = Observatory.objects.get_or_create(id=observatory_code)
            device, created = Device.objects.get_or_create(id=device_code, defaults={'device_resolution':device_resolution, "observatory":observatory})

            for ast in asteroids:
                ast = ast.tolist()
                asteroid, created = Asteroid.objects.get_or_create(body=ast)
                Sighting.objects.create(date=date, time=time, matrix=plain_matrix, device=device,
                                               observatory=observatory, asteroid=asteroid)
        path = pathlib.Path(file)
        (path.replace if path.exists() else path.rename)(os.path.join(settings.BASE_DIR, 'sightings', 'registered', os.path.basename(file)))
