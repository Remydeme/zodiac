import nltk
import re
import sys
import warnings
from sklearn.base import TransformerMixin, BaseEstimator
import unidecode
if not sys.warnoptions:
    warnings.simplefilter("ignore")

import spacy
import fr_core_news_sm

print(f'Spacy version {spacy.__version__}')
nlp = fr_core_news_sm.load()
stop_words = spacy.lang.fr.STOP_WORDS
punctuations = spacy.lang.punctuation.LIST_PUNCT

def cleanHtml(sentence):
    """
    remove all Html canvas from the sentence
    :param sentence {str} sentence
    :return:
        {str}: sentence without html canvas
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(sentence))
    return cleantext

def cleanPunc(sentence):
    """
        function to clean the word of any punctuation or special characters
        Args
        :param: sentence {str} uncleaned sentence
        :returns
            {str}: clean sentence

    """
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n"," ")
    return cleaned

def keepAlpha(sentence):
    """
    Remove all characters that are not alphanumeric
    :parameter
    ----------
        :param sentence: {str}
            uncleaned sentence
    :return:
    """
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent

def removeAccent(sentence):
    """
    Remove accent from the string
    :param sentence:
    :return:
    """
    cleaned_sentence = unidecode.unidecode(sentence)
    return cleaned_sentence

def removedDuplicateSpace(sentence):
    return " ".join(sentence.split())



def standardiseText(sentence):
        cleaned_text = sentence.replace(r"http\S+", "")
        cleaned_text = cleaned_text.replace(r"http", "")
        cleaned_text = cleaned_text.replace(r"@\S+", "")
        #cleaned_text = sentence.replace(r"[^A-Za-z0-9(),!?@\'\`\"\_\n]", " ")
        cleaned_text = cleaned_text.replace(r"@", "at")
        return cleaned_text

def prepareText(text, punctuation=True, lemming=True, stop_word=True):
    """
    Prepare the text by removing punctuation, stop words and doing lemming
    :param text:
    :return: text
    """
    clean_text = nlp(text)

    # lowering word
    # lemming
    # if words is pronoun don't apply lemming because spacy convert the words
    # in "_PRON-"
    if lemming == True:
        clean_text = [word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in clean_text]

    # remove stop words
    if stop_word == True:
        clean_text = [word for word in clean_text if (word not in stop_words)]
    # remove punctuation
    if punctuation == True:
        clean_text = [word for word in clean_text if word.isalpha()]

    # remove single char [b-Z] we only keep 'a'
    clean_text = [word for word in clean_text if (len(word) != 1 and word != 'a')]

    # clean_text = [ word for word in clean_text if (word not in noisy_words)]

    return clean_text


def clean_text(text):
    """
    Take a text in parameter and apply cleaning functions.
    :arg
        :param text {str}: uncleaned text
    :return:
        {str} : cleaned text
    """
    text = text.lower()
    text = cleanHtml(text)
    text = cleanPunc(text)
    text = removeAccent(text)
    text = standardiseText(text)
    text = removedDuplicateSpace(text)
    return text



class TextCleaner(TransformerMixin, BaseEstimator):


    def __init__(self):
        """
         Clean a text
        """
        pass

    def fit(self):
        return self

    def transform(self, texts):
        """
        Transform the array of text removing punctuation and html sign.
        :param texts (list): list of text
        :return:
            (list) cleaned texts
        """
        self.cleaned_text_ = [clean_text(text) for text in texts]
        return self.cleaned_text_



def cleaner_test():
    pass
