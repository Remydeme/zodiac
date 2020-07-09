import json
import os


class EventExtractor():
    def __init__(self, path_to_jars='/Users/remy.deme/PycharmProjects/zodiac/python-sutime/jars'):
        self.sutime_ = SUTime(jars=path_to_jars, mark_time_ranges=True, language='french', include_range=True)


    def extract_event(self, text):
        """
        :parameter
        ----------
            :param text: text from wich we want to extract the event
        :returns
        --------
            :return: json
                json containing all the date parse from the text
        """
        return json.dumps(self.sutime_.parse(text), sort_keys=True, indent=4)



