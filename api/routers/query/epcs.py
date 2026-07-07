from fastapi import APIRouter,Request
from module import DBInterface

query_epcs_router=APIRouter(prefix="/epcs",tags=["epcs"])

@query_epcs_router.get("/")
def get_epcs(request:Request):
    db:DBInterface=request.app.state.db

@query_epcs_router.get("/{epc}")
def get_resources_of_epc(
        epc:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db

@query_epcs_router.get("/{epc}/events")
def get_events_of_epc(
        epc:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db
