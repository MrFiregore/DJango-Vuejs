import csv
import glob
import os
import time
from itertools import groupby
import pathlib
import numpy as np
from watchdog.events import RegexMatchingEventHandler
from watchdog.observers import Observer
import asyncio
from asteroid.models import Asteroid, Observatory, Device, Sighting


# from watchgod import awatch

class Utils():
    CSV_REGEX = [r".*\.csv$"]

    def __init__(self):
        # super().__init__(self.CSV_REGEX)
        self.__src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'avistamientos')
        # self.__event_observer = Observer()
        # self.__event_handler = self
        # for changes in awatch(self.__src_path):
        #     print(changes)

    def on_created(self, event):
        print(event)
        pass

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )

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

    def run_avistamientos(self):
        for file in glob.glob(
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'avistamientos', '*.csv')):
            csv = self.csv_dict_list(file)
            for i in csv:
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

                ###########################
                # @TODO
                # no se si es por la errata del documento o que pero en la primera matriz salen dos asteroides
                # a pesar de que solo hay uno por avistamiento
                # por lo que solo pondre un break hasta reslver la duda
                ###########################

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
