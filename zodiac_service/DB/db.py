from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator, ClusterOptions
from couchbase.exceptions import BucketAlreadyExistsException, BucketDoesNotExistException, BucketNotFoundException
from zodiac_service.config.config import CreateConfig



def createDB():
    return DB()


class DB():

    def __init__(self, config=None):
        """
        Create a DB object using config
        :param config:
        """

        self._cluster = self.createCluster(couchbaseConfig=config)
        self._emailBucket = self._cluster.bucket("email")
        self._emailBucket = self._cluster.bucket("moto")


    def createUserBucketIfNotExists(self):
        bucket_name = "user"
        try:
            bucket = self._cluster.bucket(bucket_name)
            return bucket
        except BucketDoesNotExistException:
            bucket = self._cluster
            ## The CREATE PRIMARY INDEX step is only needed the first time you run this script
            self._cluster.query_indexes().create_primary_index(bucket_name)
            return bucket

    def createEmailBucketIfNotExists(self):
        bucket_name = "email"
        bucket = self._cluster.bucket(bucket_name)
        cb = bucket.default_collection()
        ## The CREATE PRIMARY INDEX step is only needed the first time you run this script
        self._cluster.query_indexes().create_primary_index(bucket_name)
        return cb



    def createDataUpdateStateBucketIfNotExists(self):
        bucket_name = "data_update_state"
        try:
            bucket = self._cluster.bucket(bucket_name)
            bucket = self._cluster
            ## The CREATE PRIMARY INDEX step is only needed the first time you run this script
            self._cluster.query_indexes().create_primary_index(bucket_name)
            return bucket
        except BucketDoesNotExistException:

            return bucket


    def createCluster(self, couchbaseConfig):
        """
        Create a client and connect to Couchbase bucket
        :return: {Couchbase.Clien}

        """
        host = couchbaseConfig['cluster']['host']
        port = couchbaseConfig['cluster']['port']
        password = couchbaseConfig['cluster']['password']
        username = couchbaseConfig['cluster']['username']
        cluster = Cluster.connect("http://" + host + ":" + port,
                                  ClusterOptions(PasswordAuthenticator(username, password)))
        return cluster

    def addUser(self, uid, user):
        self._userBucket.upsert(uid, user.__dict__())

    def addEmail(self, uid, email):
        self._emailBucket.upsert(uid, email.__dict__())


if __name__ == "__main__":
    config = CreateConfig(path='../config/config.json')
    db = DB(config=config['couchbase'])

