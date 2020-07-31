"""
Object that represent an email
"""
import uuid

class Email(object):

    def __init__(self, user_id, to, body, subject, number_of_reply, thread_id, is_initial_email, send_date,
                 categories=None, reactions=None, type="email", ):
        """
        :param user_id: {str}
            user unique identifier
        :param to:
            the receiver of the mail
        :param body: {str}
            the content of the mail
        :param subject: {str}
            what the mail is about
        :param number_of_reply: {int}
            the number of response to the mail. This value is update during the time each time we this email get a new
            response
        :param thread_id: {str}
            The thread to which the mail belong. There is a thread ID only if there are reponses to the mail.
        :param is_initial_email: {boolean}
            boolean that indicate if the mail is the initial mail that have been sent
        :param categories: {list}
            categories identified by the classifier to wich the mail belong
        :param reactions: {list}
            list of reactions. See reaction object for more informations
        :param send_date: {str}
            date at wich this email have been sent
        :param type: {str}
            type is mail
        """
        self._id = f"{uuid.uuid4()}"
        self._type = type
        self._user_id = user_id
        self._to = to
        self._body = body
        self._subject = subject
        self._number_of_reply = number_of_reply
        self._thread_id = thread_id
        self._is_initial_email = is_initial_email
        self._categories = categories
        self._reactions = reactions
        self._send_date = send_date

    def getID(self):
        return self._id

    def __dict__(self):
        categories = []
        reactions = []
        if self._categories != None:
            categories = [category.__dict__() for category in self._categories]

        if self._reactions != None:
            reactions = [reaction.__dict__() for reaction in self._reactions]

        return {'type': self._type, 'user_id': self._user_id, "to": self._to,
                "body": self._body, "subject": self._subject, "number_of_reply": self._number_of_reply,
                "thread_id": self._thread_id, "is_initial_mail": self._is_initial_email,
                "categories": categories, "reactions": reactions,
                "send_date": self._send_date}
