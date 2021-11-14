import csv
import os
import time
import threading
from itertools import groupby
import pathlib
import numpy as np
from watchdog.observers import Observer
from .CsvHandler import CsvHandler
from .models import Asteroid, Observatory, Device, Sighting


class Utils:
    event_list_flag = 0

    def __init__(self):
        self.__src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'avistamientos')
        self.watcher_thread = threading.Thread(name="Hilo", target=self.run_daemon, daemon=True)

    def run(self):
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
                        self.run_avistamientos(event.src_path)
                    self.event_list_flag = 0
                time.sleep(1)
        except (KeyboardInterrupt, OSError):
            event_observer.stop()
            event_handler.stop()
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

    def run_avistamientos(self, file):
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

            observatory = Observatory.objects.filter(id=observatory_code)
            if not observatory.exists():
                observatory = Observatory.objects.create(id=observatory_code)
            else:
                observatory = observatory.get()

            device = Device.objects.filter(id=device_code)
            if not device.exists():
                device = Device.objects.create(id=device_code, device_resolution=device_resolution,
                                               observatory=observatory)
            else:
                device = device.get()

            for ast in asteroids:
                ast = ast.tolist()
                asteroid = Asteroid.objects.filter(body=ast)
                if asteroid.exists():
                    asteroid = asteroid.get()
                    continue
                asteroid = Asteroid(body=ast)
                asteroid.save()
                break

            if not Sighting.objects.filter(date=date, time=time, matrix=plain_matrix, device=device,
                                           observatory=observatory, asteroid=asteroid).exists():
                Sighting.objects.create(date=date, time=time, matrix=plain_matrix, device=device,
                                        observatory=observatory, asteroid=asteroid)
        path = pathlib.Path(file)
        if not path.exists():
            path.rename(os.path.join(os.path.dirname(file), 'registered', os.path.basename(file)))
        else:
            path.replace(os.path.join(os.path.dirname(file), 'registered', os.path.basename(file)))
