from fastapi import APIRouter,Request
from module import DBInterface

query_bizLocations_router=APIRouter(prefix="/bizLocations",tags=["bizLocations"])

@query_bizLocations_router.get("/")
def get_bizLocations(request:Request):
    db:DBInterface=request.app.state.db

@query_bizLocations_router.get("/{bizLocation}")
def get_resources_of_bizLocation(
        bizLocation:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db

@query_bizLocations_router.get("/{bizLocation}/events")
def get_events_of_bizLocation(
        bizLocation:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db
