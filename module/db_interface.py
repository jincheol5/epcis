from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Literal

class DBInterface:
    """
    Collections:
        - event
        - vocab
    """
    def __init__(self,port:int=27017):
        try:
            self.client=MongoClient(f"mongodb://127.0.0.1:{port}/")
            self.db=self.client["epcis"]
            self.event_collection=self.db["event"]
            self.vocab_collection=self.db["vocab"]
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
    
    def connect_db(self,port:int=27017):
        try:
            self.client=MongoClient(f"mongodb://127.0.0.1:{port}/")
            self.db=self.client["epcis"]
            self.event_collection=self.db["event"]
            self.vocab_collection=self.db["vocab"]
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
    
    def insert_data_list(self,
            data_list:list,
            data_type:Literal["event","vocab"]
        ):
        """
        """
        if self.client is None:
            self.connect_db()
        data_collection=(
            self.event_collection
            if data_type=="event"
            else self.vocab_collection
        )
        try:
            data_collection.insert_many(
                data_list,
                ordered=False
            ) # ordered=False: 중복 _id 있으면 skip
        except PyMongoError as e:
            print(f"{data_type} type data list insert error: {e}")

    def find_events(self):
        """
        """
        events=self.event_collection.find() # find()는 cursor를 반환
        return list(events)

    def find_event_by_id(self,event_id:str):
        """
        """
        event=self.event_collection.find_one({"_id":event_id}) # dict
        if event is None:
            return None
        return event