


class User(object):



    def __init__(self, type, mail, preferences, added, following=None, follower=None):
        """
        Represent a zodiac user
        Args
        ---
            :arg type {str}
                type of that identify the schema
            :arg mail {str}
                user email adress
            :arg preferences {list}
                list of user preferences
            :arg added {date}
                added date
            :arg following {list}
                list of user id that the user followed
            :arg followed {list}
                list of user id that follow the user 
        """
        self._type = type
        self._mail = mail
        self._preferences = preferences
        self._added = added
        self._following = following
        self._follower = follower



    def __dict__(self):
        followers = None
        followings = None
        if self._following != None:
            followers = [follower.__dict__() for follower in self._follower]
        if self._follower != None:
            followings = [following.__dict__() for following in self._following]
        return {'type': self._type, 'mail': self._mail, 'preferences': self._preferences, 'follower': followers, 'following': followings}
