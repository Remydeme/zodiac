import unittest

from GmailAnalyser.GmailClient import GMailClient


class TestGmailAnalyser(unittest.TestCase):


    def setUp(self):
        self.client = GMailClient(path_to_credentials='./credentials.json')

    # - check fetch list of ID
    def test_fetch_list_ID(self):
        expected = ['']
        listID = self.client.ListID()
        self.assertEqual(listID, expected)

    # - check not None
    def test_init(self):
        self.assertNotEqual(self.client, None)

    # - check config
    def test_client_fetch_page(self):
        mails_df = self.client.MessageFromForums(query='people', maxResults=1)
        expected = (2, 12)
        self.assertEqual(mails_df.shape, expected)
    # -  
    def test_fetch_list_id(self):
        maxResults = 1
        query = 'people'
        expected = (2,4)
        message_ids_array = self.client.MessageIDSMatchingQuery(query=query, labelsIds=['CATEGORY_FORUMS'],
                                                           maxResults=maxResults)
        self.assertEqual(message_ids_array, expected)






if __name__ == "__main__":
    unittest.main()
