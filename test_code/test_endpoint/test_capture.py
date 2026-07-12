from .conftest import load_test_data


def test_capture_stores_event_and_vocabulary(client,memory_db):
    response=client.post("/capture/",json=load_test_data("capture_document.json"))

    assert response.status_code==200
    assert response.json()=={"message":"EPCIS document captured successfully"}
    assert len(memory_db.events)==1
    assert len(memory_db.vocabularies)==1
    assert memory_db.events[0]["eventID"].startswith("urn:uuid:")
    assert memory_db.events[0]["_id"]==memory_db.events[0]["eventID"]
    assert memory_db.vocabularies[0]["elementID"]=="urn:epc:id:sgln:8801234.00001.0"


def test_capture_rejects_invalid_document(client):
    document=load_test_data("capture_document.json")
    document["epcisBody"]["eventList"][0].pop("eventTime")

    response=client.post("/capture/",json=document)

    assert response.status_code==422
