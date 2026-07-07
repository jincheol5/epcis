from fastapi import APIRouter,Request
from module import DBInterface

query_bizSteps_router=APIRouter(prefix="/bizSteps",tags=["bizSteps"])

@query_bizSteps_router.get("/")
def get_bizSteps(request:Request):
    db:DBInterface=request.app.state.db

@query_bizSteps_router.get("/{bizStep}")
def get_resources_of_bizStep(
        bizStep:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db

@query_bizSteps_router.get("/{bizStep}/events")
def get_events_of_bizStep(
        bizStep:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db
