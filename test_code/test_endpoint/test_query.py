import pytest


def event_list(response):
    return response.json()["epcisBody"]["queryResults"]["resultsBody"]["eventList"]


def test_get_all_events(query_client):
    response=query_client.get("/events/")

    assert response.status_code==200
    assert response.json()["type"]=="EPCISQueryDocument"
    assert len(event_list(response))==3
    assert all("_id" not in event for event in event_list(response))


@pytest.mark.parametrize(
    ("path","expected"),
    [
        ("/eventTypes/",{"ObjectEvent","AggregationEvent"}),
        ("/epcs/",{
            "urn:epc:id:sgtin:8801234.100001.1",
            "urn:epc:id:sscc:8801234.0000000010",
            "urn:epc:class:lgtin:8801234.100001.lot1"
        }),
        ("/bizSteps/",{"shipping","packing"}),
        ("/bizLocations/",{
            "urn:epc:id:sgln:8801234.00001.0",
            "urn:epc:id:sgln:8801234.00002.0"
        }),
        ("/readPoints/",{
            "urn:epc:id:sgln:8801234.00001.1",
            "urn:epc:id:sgln:8801234.00002.1"
        }),
        ("/dispositions/",{"in_transit","container_closed"})
    ]
)
def test_get_top_level_collections(query_client,path,expected):
    response=query_client.get(path)

    assert response.status_code==200
    assert response.json()["type"]=="Collection"
    assert set(response.json()["member"])==expected


@pytest.mark.parametrize(
    ("resource_path","expected_event_count"),
    [
        ("/eventTypes/AggregationEvent",1),
        ("/epcs/urn:epc:id:sscc:8801234.0000000010",1),
        ("/bizSteps/shipping",1),
        ("/bizLocations/urn:epc:id:sgln:8801234.00001.0",1),
        ("/readPoints/urn:epc:id:sgln:8801234.00002.1",1),
        ("/dispositions/container_closed",1)
    ]
)
def test_get_resource_and_its_events(query_client,resource_path,expected_event_count):
    resource_response=query_client.get(resource_path)
    events_response=query_client.get(f"{resource_path}/events")

    assert resource_response.status_code==200
    assert resource_response.json()["member"]==[f"http://testserver{resource_path}/events"]
    assert events_response.status_code==200
    assert len(event_list(events_response))==expected_event_count


def test_get_event_by_id_includes_error_declaration(query_client):
    event_id="urn:uuid:00000000-0000-0000-0000-000000000001"
    response=query_client.get(f"/events/{event_id}")

    assert response.status_code==200
    assert {event["eventID"] for event in event_list(response)}=={
        event_id,
        "urn:uuid:00000000-0000-0000-0000-000000000003"
    }


def test_unknown_resources_return_not_found(query_client):
    assert query_client.get("/bizSteps/unknown").status_code==404
    assert query_client.get("/bizSteps/unknown/events").status_code==404
    assert query_client.get("/events/urn:uuid:unknown").status_code==404


def test_post_event_captures_single_event(query_client,query_db):
    event={
        "type":"ObjectEvent",
        "eventTime":"2026-07-13T12:00:00+09:00",
        "eventTimeZoneOffset":"+09:00",
        "epcList":["urn:epc:id:sgtin:8801234.100001.99"],
        "action":"OBSERVE"
    }

    response=query_client.post("/events/",json=event)

    assert response.status_code==201
    assert response.json()["eventID"].startswith("urn:uuid:")
    assert "_id" not in response.json()
    assert len(query_db.events)==4
