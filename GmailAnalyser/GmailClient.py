from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors
import pandas as pd
import base64
import email


from GmailAnalyser.GmailAnalytics import GMailAnalytics
"""
Description of the GMAIL API : https://developers.google.com/gmail/api/v1/reference/users/messages#resource
"""


class GMailClient:
    """
    Class used to connect to a gmail account using user credentials
    """
    _service = None
    _scope = []
    _userID = ""

    def __init__(self, path_to_credentials, scope= ['https://www.googleapis.com/auth/gmail.readonly'], userID="me"):
        """
        @:param path_to_credentials : path to the user credetnials file download from gmailPai console
        @:param scope : operation readonly by default
        @:param userId: The user's email address. The special value me can be used to indicate the authenticated user.
        """
        self._path_to_credentials = path_to_credentials
        self._scope = scope
        self._userID = userID
        self._creds = None
        self._init()

    def _init(self):
        """
            The file token.pickle stores the user's access and refresh tokens, and is
            created automatically when the authorization flow completes for the first
            time.
        """
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            #If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self._path_to_credentials, self._scope)
                    creds = flow.run_local_server(port=0)
                #Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            self._service = build('gmail', 'v1', credentials=creds)
        except Exception:
            print("Failed to create service an error occured ")




    def MessageIDSMatchingQuery(self, labelsIds, maxResults=None, query='', userID='me'):
        """
        MessageMatchingQuery it's a fucntion that fetch all the message ID that match the labelID
        Args:
            :param labelsIds {numpy.array}: list of label id. (label are category associated to an email ex: UNREAD,
            IMPORTANT, SPAM, ...)
            :param query {str}: what are the messages we are looking for ex: 'people' message that contains people inOnly
                return messages matching the specified query. Supports the same query format as the Gmail search box.
                For example, "from:someuser@example.com rfc822msgid:<somemsgid@example.com> is:unread". Parameter cannot be
                used when accessing the api using the gmail.metadata scope.
            :param userID {str}: User's email address. The special value "me" can be used to indicate the authenticated
            user.
        :return:
            {dico}: dictionnary containing all the message informations
        """
        try:
            response = self._service.users().messages().list(userId=userID, labelIds=labelsIds, q=query, maxResults=maxResults).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])
            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self._service.users().messages().list(userId=userID, labelIds=labelsIds, q=query,
                                                                 pageToken=page_token).execute()
                messages.extend(response['messages'])
                return messages
        except errors.HttpError as error:
            print(f"Http error occured {error}")
            return  None


    def ListID(self):
        """
        In your mailbox your emails can be tagged with different categories, SPAM, UNREAD, IMPORTANT, MAILINGLIST
        this function return the ID associated with this classes. This ID allow you to fetch all the email labelled with
        a given tag.
        Args:
        :return:
            dico{str:str} : dico that contains the couple category and id.
        """
        results = self._service.users().labels().list(userId=self._userID).execute()
        labels = results.get('labels', [])
        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            return {label['name']:label['id'] for label in labels}


    def _clean_email_text(self, text):
        if type(text) is str:
            splited = text.split('\n')
            body = ""
            for field in splited:
                if len(field) > 0:
                    if field[0] != '>':
                        body += field + '\n'
            return body
        return None

    def GetMessage(self, userID, msgID):
        """
        Get a Message raw data with given ID.
        Args:
          userID {str}: User's email address. The special value "me" can be used to indicate the authenticated user.
          msgID: The ID of the Message required.

        Returns:
          {dict} : dictionnary that contains all the message informations
        """
        try:
            message = self._service.users().messages().get(userId=userID, id=msgID, format='raw').execute()
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ascii'))
            email_data = email.message_from_bytes(msg_str)
            email_dico = {}
            for key in email_data.keys():
                email_dico[key] = email_data[key]
            payload = email_data._payload
            if type(payload) is list:
                email_dico["body"] = self._clean_email_text(payload[0]._payload)
                email_dico["is_initial_mail"] = False
            elif type(payload) is str:
                email_dico["body"] = payload
                email_dico["is_initial_mail"] = True
            else:
                email_dico["body"] = 'empty'
            email_dico['threadId'] = message['threadId']
            email_dico["is_initial_mail"] = False
            return email_dico
        except errors.HttpError as error:
            print(f'An error occurred: {error}')
            return None
        except Exception as error:
            print(f'An error occured while fetching parameters : {error}')
            return message




    def MessageFromForums(self, query, maxResults=None):
        """
        Fetch all the message from the forum section.
        Note : Used 'me' as default UserID
        :parameter
        -----------
            :param : query {string}i
                    to filter the message filter
            :param  : userID {string}
                        userID {str}: User's email address. The special value "me" can be used to indicate the authenticated user.
            :param : maxResults {int}
                    limit the result to this value. example : if set to 1 you will only get one mail. (Only if there is
                     elements that match the query)
        :return:
            {pandas.DataFrame} : dataframe that contains all the message metadata and the message text
        """
        try:
            message_ids_array = client.MessageIDSMatchingQuery(query=query, labelsIds=['CATEGORY_FORUMS'], maxResults=maxResults)
            messages = []
            if message_ids_array != None:
                for ids in message_ids_array:
                    message_id = ids['id']
                    message = self.GetMessage(userID=self._userID, msgID=message_id)
                    messages.append(message)
                dataframe = pd.DataFrame(messages)
                # Only keep the field containing the useful informations
                dataframe = dataframe[['body', 'X-Spam-Checked-In-Group', 'X-Original-Sender', 'To', 'Date', 'From',
                                       'In-Reply-To', 'Delivered-To', 'Cc', 'Subject', 'threadId', 'is_initial_mail']]
                dataframe.rename(columns={'X-Spam-Checked-In-Group' : "mailing-list", "X-Original-Sender" : "origin",
                                          "From" : "identity"}, inplace=True)
                dataframe['Date'] = pd.to_datetime(dataframe['Date'])
                print(f'Done processing your forum mail that match the following query : {query}')
                return dataframe
            return None
        except Exception as error:
            print(f"Error occured {error}")
            return None







if __name__ == "__main__":
    client = GMailClient(path_to_credentials='/credentials.json')
    mails_df = client.MessageFromForums(query='people',  maxResults=1)
    print(mails_df.body[0])
    analyser = GMailAnalytics()
    analyser.fit(dataframe=mails_df)
    mails_df = analyser.__transform()
    #analyser.df_.to_csv('./people_forums_mail.csv', header=True)


