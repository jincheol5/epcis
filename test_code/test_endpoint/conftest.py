import copy
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.main import app
from module import CaptureModule
from schema import EPCISDocument


TEST_DATA_DIR=Path(__file__).parents[1]/"test_data"


def load_test_data(file_name:str):
    with (TEST_DATA_DIR/file_name).open(encoding="utf-8") as file:
        return json.load(file)


def get_values(document:dict,path:str):
    values=[document]
    for key in path.split("."):
        next_values=[]
        for value in values:
            if isinstance(value,dict) and key in value:
                child=value[key]
                next_values.extend(child if isinstance(child,list) else [child])
        values=next_values
    return values


class MemoryDB:
    def __init__(self):
        self.events=[]
        self.vocabularies=[]

    def insert_data_list(self,data_list:list,data_type:str):
        target=self.events if data_type=="event" else self.vocabularies
        target.extend(copy.deepcopy(data_list))

    def find_events(self):
        return copy.deepcopy(self.events)

    def find_events_by_filter(self,query:dict):
        if "$or" in query:
            return [
                copy.deepcopy(event)
                for event in self.events
                if any(expected in get_values(event,path) for condition in query["$or"] for path,expected in condition.items())
            ]
        path,expected=next(iter(query.items()))
        return [copy.deepcopy(event) for event in self.events if expected in get_values(event,path)]

    def find_distinct_event_values(self,field_name:str):
        values={value for event in self.events for value in get_values(event,field_name) if value is not None}
        return sorted(values)

    def find_event_types(self):
        return self.find_distinct_event_values("type")

    def find_biz_steps(self):
        return self.find_distinct_event_values("bizStep")

    def find_biz_locations(self):
        return self.find_distinct_event_values("bizLocation.id")

    def find_read_points(self):
        return self.find_distinct_event_values("readPoint.id")

    def find_dispositions(self):
        return self.find_distinct_event_values("disposition")

    def find_epcs(self):
        fields=(
            "parentID","epcList","childEPCs","inputEPCList","outputEPCList",
            "quantityList.epcClass","childQuantityList.epcClass",
            "inputQuantityList.epcClass","outputQuantityList.epcClass"
        )
        values={value for event in self.events for field in fields for value in get_values(event,field)}
        return sorted(values)

    def find_events_by_event_type(self,event_type:str):
        return self.find_events_by_filter({"type":event_type})

    def find_events_by_biz_step(self,biz_step:str):
        return self.find_events_by_filter({"bizStep":biz_step})

    def find_events_by_biz_location(self,biz_location:str):
        return self.find_events_by_filter({"bizLocation.id":biz_location})

    def find_events_by_read_point(self,read_point:str):
        return self.find_events_by_filter({"readPoint.id":read_point})

    def find_events_by_disposition(self,disposition:str):
        return self.find_events_by_filter({"disposition":disposition})

    def find_events_by_epc(self,epc:str):
        fields=(
            "parentID","epcList","childEPCs","inputEPCList","outputEPCList",
            "quantityList.epcClass","childQuantityList.epcClass",
            "inputQuantityList.epcClass","outputQuantityList.epcClass"
        )
        return self.find_events_by_filter({"$or":[{field:epc} for field in fields]})

    def find_events_by_event_id(self,event_id:str):
        return self.find_events_by_filter({
            "$or":[
                {"eventID":event_id},
                {"errorDeclaration.correctiveEventIDs":event_id}
            ]
        })


@pytest.fixture
def memory_db():
    return MemoryDB()


@pytest.fixture
def client(memory_db):
    app.state.db=memory_db
    return TestClient(app)


@pytest.fixture
def query_db(memory_db):
    document=EPCISDocument.model_validate(load_test_data("query_document.json"))
    events,_=CaptureModule.extract_from_epcis_document(document=document)
    memory_db.insert_data_list(CaptureModule.transform_events(event_list=events),"event")
    return memory_db


@pytest.fixture
def query_client(client,query_db):
    return client
