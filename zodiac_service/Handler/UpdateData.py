from GmailAnalyser.GmailClient import GMailClient, GMailAnalytics
from zodiac_service.Models.Email import Email
from zodiac_service.Models.Follow import Follow
from zodiac_service.Models.Category import Category

client = GMailClient(path_to_credentials='credentials.json')


# fertch the data periodically

def fetch_mails():
    """
    fetch all the mails from the mailing list. Prepare them and build a dataframe.
    :arg
    ----
        :arg
    :return: {pandas.Dataframe}
    --------
        Dataframe that contains the mail bodies and all the metadatas
    """
    mails_df = client.MessageFromForums(query='newer_than:2d', maxResults=10)
    analyser = GMailAnalytics()
    analyser = analyser.fit(dataframe=mails_df)
    transformed_df = analyser.transform(dataframe=mails_df)
    return transformed_df


def store_email_into_couchbase(dataframe, DB):
    """
    Take a dataframe dataframe and store all the data into the sever
    :param dataframe:
        Dataframe that contains mail contents and metadatas
    """
    for row in range(len(dataframe)):
        origin = dataframe.loc[row, "origin"]
        body = dataframe.loc[row, "body"]
        to = dataframe.loc[row, "To"]
        date = dataframe.loc[row, "Date"]
        reply = dataframe.loc[row, "In-Reply-To"]
        subject = dataframe.loc[row, "Subject"]
        threadId = dataframe.loc[row, "threadId"]
        isInitialMail = 1 if dataframe.loc[row, "is_initial_mail"] == True else 0

        email = Email(user_id=origin, body=body,to=to, subject=subject, number_of_reply=0, thread_id=threadId,
                      is_initial_email=isInitialMail, send_date=f"{date}")
        DB.addEmail(uid=email.getID(), email=email)
