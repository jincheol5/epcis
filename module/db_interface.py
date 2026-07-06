from pymongo import MongoClient
from pymongo.errors import PyMongoError

class DBInterface:
    def __init__(self,port:int=27017):
        try:
            self.client=MongoClient(f"mongodb://127.0.0.1:{port}/")
            self.db=self.client["epcis"]
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
    
    def connect_db(self,port:int=27017):
        try:
            self.client=MongoClient(f"mongodb://127.0.0.1:{port}/")
            self.db=self.client["epcis"]
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
    
    def disconnect_db(self):
        self.client.close()
    
    def delete_collection(self,collection_name:str):
        if self.client is None:
            self.connect_db()
        collection=self.db[collection_name]
        try:
            collection.delete_many({})
            print(f"{collection_name} collection is deleted!")
        except PyMongoError as e:
            print(f"MongoDB delete collection error: {e}")
    
    def insert_event_data(self,event_list:list):
        """
        """
        if self.client is None:
            self.connect_db()
        event_data_collection=self.db["event_data"]

    def insert_master_data(self,vocabulary_list:list):
        """
        """
        master_data_collection=self.db["master_data"]