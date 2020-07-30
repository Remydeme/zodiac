import flask
from flask import Flask
from zodiac_service.DB.db import createDB
from zodiac_service.Handler.UpdateData import fetch_mails, store_email_into_couchbase
from zodiac_service.Models.DataUpdateState import DataUpdateState


class Service(object):

    def __init__(self):
        self._db = createDB()

    def getDB(self):
        return self._db


# python server
def createAndConfigureFlaskApp():
    app = Flask("zodiac")
    return app


# instances
service = Service()
app = createAndConfigureFlaskApp()


@app.route('/v1/data/update/launch', methods=['GET', 'POST'])
def updateStart():
    #create an update
    state = DataUpdateState(batch_size=0)
    df = fetch_mails()
    store_email_into_couchbase(df, service.getDB())
    return "<p> update mails data </p>"


@app.route('/v1/data/update/state')
def updateState():
    pass


if __name__ == "__main__":
    app.run(port="8080", host="localhost", debug=True)
