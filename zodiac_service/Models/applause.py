class Applause(object):
    def __init__(self, number, user_id):
        """
        Reactions of the user to an email quality
        :param number: {int}
            Number of reactions (illimite)
        :param user_id:
            User unique identifier
        """
        self._number = number
        self._user_id = user_id

    def __dict__(self):
        return {'number': self._number, 'user_id': self._user_id}
