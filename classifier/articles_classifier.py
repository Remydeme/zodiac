from sklearn.feature_extraction.text import TfidfVectorizer
from skmultilearn.problem_transform import ClassifierChain
import joblib
import pandas as pd
import plotly.express as px
from sklearn.metrics import jaccard_score
from sklearn.svm import SVC
from sklearn.base import ClassifierMixin
import sys
import warnings
import spacy
import fr_core_news_sm
from classifier.cleaner import prepareText

if not sys.warnoptions:
    warnings.simplefilter("ignore")

print(f'Spacy version {spacy.__version__}')
nlp = fr_core_news_sm.load()
stop_words = spacy.lang.fr.STOP_WORDS
punctuations = spacy.lang.punctuation.LIST_PUNCT




class ArticleClassifier(ClassifierMixin):


    def __init__(self, ngram=(1, 3), tokenizer=prepareText, max_feature=20000):
        """
        This classifier is a multi-label classifier. It have been trained on octo-articles dataset.
        You can train it using the fit function
        :parameter
        ----------
            :param ngram {tuple}:
                    default '(1,3)'  ngram_range for the tfidfVectorizer
            :param tokenizer {func}:
                    tokenizer used by tfidfvectorizer to prepapre the Data
            :param max_feature {int}:
                    limit the matrix composition to the 'max_feature' most important element
        """
        self.vectorizer_ = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=ngram, norm='l2',
                                     tokenizer=tokenizer, max_features=max_feature)
        # initialize classifier chains multi-label classifier
        self.classifier_ = ClassifierChain(SVC(probability=True))


        pass

    def fit(self, X, y):
        """
        fit the model to the data. Train the classifier
        Note: You should use the zodiac.classifier.cleaner on all the texts before you fit the data

        :parameter
        ----------
            :param X: (list)
                list of clean text (you can use zodiac.cleaner.TextCleaner)
            :param y: (numpy.array)
                array of labels
        """
        self.x_vec_ = self.vectorizer_.fit_transform(X)

        # Training logistic regression model on train data
        self.classifier_.fit(self.x_vec_, y)


    def predict(self, x):
        """
        Predict class labels for samples in X.
        :parameter
        ----------
        :param X: {list of str}
            list of string
        :return: list of float
            return the predicted class for each element
        """
        x_vec = self.vectorizer_.transform(x)
        return self.classifier_.predict(x_vec)

    def predict_proba(self, x):
        """
        Probability estimates.
        The returned estimates for all classes are ordered by the label of classes.
        :parameter
        ----------
        :param X: {list of str}
            list of string
        :return: list of float
            return the predicted class for each element
        """
        x_vec = self.vectorizer_.transform(x)
        return self.classifier_.predict_proba(x_vec)

    def score(self, X, y, average='samples', threshold=0.5):
        """
        Compute the jaccard score using the given parameters
        :parameter
        -----------
            :param x_test(list):
                list of text
            :param y_true (list):
                texts labels
            :param average:
                default 'average'.
        :return:
        -------
            score : float
                jaccard score
        """
        self.x_test_vec_ = self.vectorizer_.transform(X)
        predictions = self.classifier_.predict_proba(self.x_test_vec_)
        score = jaccard_score(y, predictions >= threshold, average=average)
        return score


    def show_stats(self,x_test ,y):
        """
        compute the jaccard score for differents threshold and display the jaccard scores using plotly scatter method

        :parameter
        ----------
            :param x_test: (list)
                text list
            :param y:
                list of label
        """
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
        x_test_vec = self.vectorizer_.transform(x_test)
        predictions_probas = self.classifier_.predict_proba(x_test_vec)
        jaccard_scores = []
        for threshold in thresholds:
            # print("For threshold: ", val)
            pred = predictions_probas.copy()
            ensemble_jaccard_score = jaccard_score(y, predictions_probas >= threshold, average='samples')
            jaccard_scores.append(ensemble_jaccard_score)
        self.jaccard_scores_threshold_df_ = pd.DataFrame({'threshold': thresholds, 'jaccard_score': jaccard_scores})

    def load_weights(self, path):
        """
        Load the weights of the model from path
        :parameter
        ---
        :param path {str}:
            path to the model weights
        """
        joblib.load(path)


    def save_weights(self, path):
        """
        Save the model weights locally
        :parameter
        ----------
            :param path {str}:
                    path to the directory to store the classifier wieghts
        """
        joblib.dump(self.classifier_, path)






