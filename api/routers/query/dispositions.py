from fastapi import APIRouter,Request
from module import DBInterface

query_dispositions_router=APIRouter(prefix="/dispositions",tags=["dispositions"])

@query_dispositions_router.get("/")
def get_dispositions(request:Request):
    db:DBInterface=request.app.state.db

@query_dispositions_router.get("/{disposition}")
def get_resources_of_disposition(
        disposition:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db

@query_dispositions_router.get("/{disposition}/events")
def get_events_of_disposition(
        disposition:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db
