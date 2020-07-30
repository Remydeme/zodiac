import unittest
from classifier.cleaner import TextCleaner


class test_cleaner(unittest.TestCase):

    def setUp(self):
        self.cleaner = TextCleaner()

    # - test punctation cleaning
    def test_punctuation_cleaning(self):
        text = 'Salut tout le monde!'
        cleaned = self.cleaner.transform([text])
        self.assertNotEqual(cleaned[0], 'Hello world')

    def test_punction_cleaning_1(self):
        text = 'Salut tout le monde!'
        expected = 'salut tout le monde'
        cleaned = self.cleaner.transform([text])
        self.assertEqual(cleaned[0], expected)


    def test_remove_accent(self):
        text = 'As-tu ouvert un compte épargne'
        expected = 'as tu ouvert un compte epargne'

    def test_clean_html(self):
        text = 'Je suis </br> à la maison </canvas>'
        expected = 'je suis a la maison'
        cleaned = self.cleaner.transform([text])
        self.assertEqual(cleaned[0], expected)

    def test_clean_email_adress(self):
        text = "c'est mon adresse e-mail demeremy@gmail.com"
        expected = "cest mon adresse e-mail demeremyatgmail com"
        cleaned = self.cleaner.transform([text])
        self.assertEqual(cleaned[0], expected)

    def test_tranform_return_type(self):
        text = "cest mon adresse e-mail demeremy@gmail.com             "
        expected = "demeremyatgmail.com c est mon adresse e mail"
        cleaned = self.cleaner.transform(text)
        self.assertEqual(type(cleaned), list)


if __name__ == "__main__":
    unittest.main()
