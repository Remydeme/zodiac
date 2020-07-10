# Zodiac classifier 

Multi label classifier

---

## Installation 


``` python

pip install zodiac

```


## Example 

```python 
from classifier.article_classifier import ArticleClassifier
from classifier.cleaner import ArticleCleaner

df = pd.read_csv('csv_file.csv')

text_list = df['text'].to_list()

cleaner = ArticleCleaner()

cleaned_text = cleaner.transform(text_list)

classifier = ArcticleClassifier(ngram=(1,2))

classifier.fit(cleaned_text)

# return the jaccard score 
classifier.score()
 
# save your model 
classifier.save_wrights(path='./model_1900.weights')

```
