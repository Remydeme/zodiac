import pandas as pd
import spacy
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import numpy as np

print(f'Spacy version {spacy.__version__}')



class GMailAnalytics(TransformerMixin, BaseEstimator):

    nlp = spacy.load('fr_core_news_sm')
    stop_words = spacy.lang.fr.STOP_WORDS
    punctuations = spacy.lang.punctuation.LIST_PUNCT

    def __init__(self):
        self.vectorizer_ = TfidfVectorizer(ngram_range=(1, 3), tokenizer=self._prepareText)



    def fit(self, dataframe):
        if type(dataframe) != pd.DataFrame:
            self.df_ = dataframe
            return self
        else:
            raise TypeError(f"{dataframe} is {type(dataframe)} but expected type is {pd.DataFrame}")

    def transform(self):
        """
            Apply all the tranformation on the mail dataframe
        :return:
        """
        self.__analyse_thread(self.df_)
        self.df_['response'] = self.df_.Subject.apply(isResponse)
        self.df_['body'] = self.df_.body.apply(cleanBody)
        self.__standardize_text()
        self.hotMail = self.hotMail(self.df_)
        #self.df_['theme'] = self.df_.body.apply(self._theme)
        return self.df_

    def __hotMail(self, dataframe):
        """
        Analyse the dataframe that contains all the mail informations and add a row
        parameter
        ---------
            :param dataframe:
        :returns
        --------
            :return: pandas.Dataframe
                dataframe sort by mail importance (we use the number of response to the mail to determine is importance)
        """
        dataframe = dataframe[dataframe.is_initial_mail == True]
        dataframe = dataframe.sort_values(by='importance_thread', ascending=False)
        return dataframe

    def __filter(self, emails):
        """
        This function return a dataframe containing all the message that was send by 'emails' adress list
          :parameter
          ----------
                emails list: list of email adress used to filter the the mails dataframe
          return:
            pd.DataFrame
        """
        dataframe = self.df_
        filtered_emails_list = []
        for email in emails:
            mails = self.dataframe[dataframe.origin == email]
            filtered_emails_list.append(mails)
        return pd.concat(filtered_emails_list)

    def __prepareText(self, text, punctuation=True, lemming=True, stop_word=True):
            """
            Prepare the text by removing punctuation, stop words and doing lemming
            :param text:
            :return: text
            """
            clean_text = self.nlp(text)

            # lowering word
            # lemming
            # if words is pronoun don't apply lemming because spacy convert the words
            # in "_PRON-"
            if lemming == True:
                clean_text = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in
                              clean_text]

            # remove stop words
            if stop_word == True:
                clean_text = [word for word in clean_text if (word not in self.stop_words)]
            # remove punctuation
            if punctuation == True:
                clean_text = [word for word in clean_text if word.isalpha()]

            # remove single char [b-Z] we only keep 'a'
            clean_text = [word for word in clean_text if (len(word) != 1 and word != 'a')]

            # clean_text = [ word for word in clean_text if (word not in noisy_words)]

            return clean_text

    def __standardize_text(self, text_field='body'):
        self.df_[text_field] = self.df_[text_field].str.replace(r"http\S+", "")
        self.df_[text_field] = self.df_[text_field].str.replace(r"http", "")
        self.df_[text_field] = self.df_[text_field].str.replace(r"@\S+", "")
        self.df_[text_field] = self.df_[text_field].str.replace(r"[^A-Za-z0-9(),!?@\'\`\"\_\n]", " ")
        self.df_[text_field] = self.df_[text_field].str.replace(r"@", "at")

    def __theme(self, text):
        threadId = self.df_.threadId.unique()
        for id in threadId:
            message = self.df_[[self.df_['threadId'] == id]]['body'].to_list()
            transformed = self.vectorizer.fit_transform([text])
            words_imp = transformed.toarray()
            max_word = np.argmax(words_imp[0], axis=0)
        return self.vectorizer.get_feature_names()[max_word]


    def __importance(self):
        """
        Analyse the text and return the important word in the text
        :return:
        """

    def __cleaner(self, text, lemming=True, stop_words=True, punctuation=True):
        """
           Prepare the text by removing punctuation, stop words and doing lemming
           :param text:
           :return: text
           """
        clean_text = self.nlp(text)
        # lowering word
        # lemming
        # if words is pronoun don't apply lemming because spacy convert the words
        # in "_PRON-"
        if lemming == True:
            clean_text = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in
                          clean_text]
        # remove stop words
        if stop_words == True:
            clean_text = [word for word in clean_text if (word not in stop_words)]
        # remove punctuation
        if punctuation == True:
            clean_text = [word for word in clean_text if word.isalpha()]

        # remove single char [b-Z] we only keep 'a'
        clean_text = [word for word in clean_text if (len(word) != 1 and word != 'a')]

        # clean_text = [ word for word in clean_text if (word not in noisy_words)]
        return clean_text



    def __clean(self, df):
        self.df_ = df.snippet.apply(self.__cleaner)


    def __analyse_history(self, dataframe):
        """
        Analyse the 'historyId' field of the dataframe, it attribute a score to each field
        :param dataframe: The dataframe that contains the mails informations
        :return
         {pandas.Dataframe}: dataframe that contains a score associated to each historyId. this score represent
         the number of message linked to the thread
        """
        historyId = dataframe.historyId.unique()
        for id in historyId:
            count = dataframe[dataframe['historyId'] == id].size
            dataframe.loc[dataframe['historyId'] == id, 'importance_thread'] = count

    def __analyse_thread(self, dataframe):
        """
        Analyse the thredId field of the dataframe, it attribute a score to each field
        :param dataframe: The dataframe that contains the mails informations
        :return pandas.Dataframe:
            dataframe that contains a score associated to each threadId. this score represent the number of message
            linked to the thread
        """
        threadId = dataframe.threadId.unique()
        for id in threadId:
            count = len(dataframe[dataframe['threadId'] == id])
            dataframe.loc[dataframe['threadId'] == id, 'importance_thread'] = count

    def __transformPayload(self, payload):
        """
        this function parse the payload and extract all the information
        Arg:
            :param payload {string}: payload that contains information about the mail (ex : sender, size)
        :return
            {dict}: A dictionnary containing the payload fields
        """
        s = payload
        char_list = ['\t', ',', '\n', '{', '}', '[', ']', '\'', '\"', ' ']
        clean_word_list = []
        for word in s.split('\':'):
            for char in char_list:
                word = word.replace(char, '')
            if word != 'partId':
                clean_word_list.append(word)
        return {x: y for x, y in zip(*[iter(clean_word_list)] * 2)}





    def exploit_payload(self):
        """
        Get all the metadata from the payload
        from
        to
        :return:
        """
        pass




def isResponse(text):
    if type(text) is str:
        return True if 'Re' in text else False
    else:
        return None


def cleanBody(text):
    patterns = ['Le [\w]{3}[\s]+[\d]{1,2} ', 'Part[\s]+of[\s]+Accenture', 'On[\s]+[\w]{3},[\s]+[\w]{3}[\s]+[\w]{1,2},']
    if type(text) is str:
        for pattern in patterns:
            reg = re.split(pattern[0], text)
            if len(reg) > 1:
                return reg[0]
    return text



