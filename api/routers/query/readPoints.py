from fastapi import APIRouter,Request
from module import DBInterface

query_readPoints_router=APIRouter(prefix="/readPoints",tags=["readPoints"])

@query_readPoints_router.get("/")
def get_readPoints(request:Request):
    db:DBInterface=request.app.state.db

@query_readPoints_router.get("/{readPoint}")
def get_resources_of_readPoint(
        readPoint:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db

@query_readPoints_router.get("/{readPoint}/events")
def get_events_of_readPoint(
        readPoint:str,
        request:Request
    ):
    db:DBInterface=request.app.state.db
