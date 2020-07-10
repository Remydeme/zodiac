# Zodiac

The zodiac project contains several tools allowing to exploit and process these emails.
* A client to fetch your email and store it into a dataframe 
* A multi-label classifier
* cleaning functions
* A class to enrich your mail dataframe

---

## Instalation

```
pip install zodiac 

```

## Exemple 

```
from classifier.article_classifier import ArticleClassifier
from classifier.cleaner import ArticleCleaner
from GmailAnalyser.GmailClient import GmailClient
from GmailAnalyser.GmailAnalytics import GmailAnalytics


# Create client object with our credentials.json file
# This operation must create a token.pickle file in the directory 
# where  you execute this code
client = GMailClient(path_to_credentials='/credentials.json')

# This method fetch all the mail from your forum that
# are from:people mailing list 
mails_df = client.MessageFromForums(query='people',  maxResults=1)

# display the body of the first mail in the dataframe 
print(mails_df.body[0])

# initialise an analytics object 
analyser = GMailAnalytics()

# enrich the dataframe using the analyser 
analyser.fit(dataframe=mails_df)


# return all the email text as list 
text_list = df['body'].to_list()


cleaner = ArticleCleaner()

cleaned_text = cleaner.transform(text_list)

classifier = ArcticleClassifier(ngram=(1,2))

classifier.load_weights(path='model_weights.weights')

# return the jaccard score for each element 
classifier.predict_proba(text_list)

# save your model 
classifier.save_wrights(path='./model_1900.weights')
```

## Licence 

MIT Licence
