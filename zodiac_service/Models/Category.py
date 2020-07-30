


class Category(object):


    def __init__(self, name):
        """
        Object that represent a category
        :param name: {str}
            category name
        """
        self.name_ = name


    def __dict__(self):
        return {'name' : self.name_}