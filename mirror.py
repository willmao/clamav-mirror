import logging
import os
import signal
import time

from cvdupdate.cvdupdate import CVDUpdate

# database update interval
DEFAULT_DATABASE_UPDATE_INTERVAL_HOUR = 4


class ClamavMirror:
    def __init__(self, update_interval_hour: int):
        self._update_interval_hour = update_interval_hour
        self._running = False

    @staticmethod
    def update():
        m = CVDUpdate(config='', verbose=False)
        errors = m.db_update()
        if errors > 0:
            logging.error(f"errors found when update, number: {errors}")

    def start(self):
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        self._running = True
        logging.info("Performing initial update")
        while self._running:
            logging.info("performing update")
            self.update()
            logging.info(f"sleep {self._update_interval_hour * 3600} seconds before next update")
            time.sleep(self._update_interval_hour * 3600)

    def stop(self, signum, frame):
        logging.info(f"begin to stop mirror: {signum}, {frame}")
        self._running = False


if __name__ == "__main__":
    logging.basicConfig(level="INFO")

    update_interval = os.getenv("DATABASE_UPDATE_INTERVAL_HOUR", DEFAULT_DATABASE_UPDATE_INTERVAL_HOUR)
    logging.info(f"update clamav database every {update_interval} hour")

    mirror = ClamavMirror(update_interval_hour=int(update_interval))
    mirror.start()
