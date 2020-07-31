import uuid
import datetime


class DataUpdateState(object):

    def __init__(self, batch_size):
        """
        Track a data update progression.
        :param batch_size:
        """
        self.id = f"{uuid.uuid4()}"
        self._created = datetime.datetime.time()
        self._progression = 0
        self._ended = None
        self._batch_size = 0
        self.type = "update"

    def __dict__(self):
        return {'created': self._created, 'progression': self._progression, 'ended': self._ended,
                'batch_size': self._batch_size}
