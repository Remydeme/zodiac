# GmailAnalyser

This directory contains two object :

* GmailClient : use to fetch email from the server 
* GmailAnalytics : Use to analyse the mail dataframe. It add new column of 
    informations.  

---

## Installation

```bash 

pip install zodiac

```

You need to follow the instruction at this adress : https://developers.google.com/gmail/api/guides
Once you have your credentials.json file you can start using GmailClient. 


## Exemple 


```python 
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



```




