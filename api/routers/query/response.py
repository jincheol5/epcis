from datetime import datetime,timezone

from fastapi import HTTPException,Request


EPCIS_CONTEXT="https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld"


def uri_collection(members:list[str]):
    return {"@context":EPCIS_CONTEXT,"type":"Collection","member":members}


def event_query_document(events:list[dict]):
    cleaned_events=[]
    for event in events:
        cleaned_event=dict(event)
        cleaned_event.pop("_id",None)
        cleaned_events.append(cleaned_event)
    return {
        "@context": EPCIS_CONTEXT,
        "type": "EPCISQueryDocument",
        "schemaVersion": "2.0",
        "creationDate": datetime.now(timezone.utc).isoformat(),
        "epcisBody": {"queryResults": {
            "queryName": "SimpleEventQuery",
            "resultsBody": {"eventList": cleaned_events},
        }},
    }


def event_subresource(request:Request,exists:bool):
    if not exists:
        raise HTTPException(status_code=404,detail="Resource not found")
    return uri_collection([f'{str(request.url).rstrip("/")}/events'])


def require_events(events:list[dict]):
    if not events:
        raise HTTPException(status_code=404,detail="Resource not found")
    return events
