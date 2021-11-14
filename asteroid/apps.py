from django.apps import AppConfig


class AsteroidConfig(AppConfig):
    name = 'asteroid'
    _runned = False

    def ready(self):
        if self.apps.apps_ready and not self._runned:
            self._runned = True
            self._run()

    def _run(self):
        from asteroid.utils import Utils
        Utils()
