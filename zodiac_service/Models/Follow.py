



class Follow(object):



    def __init__(self, userId):
        """
        Represent a follower
        :args
        ----
            :arg user_id
             unique_id that idenitfy a user

        """
        self._userId = userId



    def __dict__(self):
        return {'userID' : self._userId}