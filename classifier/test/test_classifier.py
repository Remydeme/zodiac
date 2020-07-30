import unittest

from classifier.articles_classifier import ArticleClassifier
import os

class Test_Classifier(unittest.TestCase):


    def setUp(self):
        self.classifier = ArticleClassifier(ngram=(1, 2), max_feature=20000)
        self.classifier_bis = ArticleClassifier(ngram=(1, 2), max_feature=20000)

    # Test object creation
    def test_not_null(self):
        self.assertNotEqual(self.classifier, None)

    def test_save_classifier(self):
        save_path = './store_model.weigths'
        self.classifier.save_weights(path=save_path)
        self.assertEqual(os.path.exists(save_path), True)
        os.remove(save_path)

    def test_load_classifier_weights(self):
        save_path = './store_model.weights'
        self.classifier.save_weights(path=save_path)
        self.classifier.load_weights(path=save_path)
        self.classifier_bis.load_weights(path=save_path)
        self.assertEqual(self.classifier.classifier_, self.classifier_bis.classifier_)
        os.remove(save_path)

if __name__=="__main__":
    unittest.main()

