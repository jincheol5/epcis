from fastapi import APIRouter,Request
from module import DBInterface

query_events_router=APIRouter(prefix="/events",tags=["events"])

@query_events_router.get("/")
def get_all_events(request:Request):
    db:DBInterface=request.app.state.db

@query_events_router.post("/")
def get_queried_events(request:Request):
    """
    JSON Body로 Query 받음
    """
    db:DBInterface=request.app.state.db

@query_events_router.get("/{eventID}")
def get_event_of_eventID(
        eventID:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db
