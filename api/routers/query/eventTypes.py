from fastapi import APIRouter,Request
from module import DBInterface

query_eventTypes_router=APIRouter(prefix="/eventTypes",tags=["eventTypes"])

@query_eventTypes_router.post("/")
def get_eventTypes(request:Request):
    """
    DB 내의 eventTypes을 조회
    """
    # request를 통해 FastAPI app 객체에 접근해서 db를 꺼내는 것
    db:DBInterface=request.app.state.db

@query_eventTypes_router.get("/{eventType}")
def get_resources_of_eventType(
        eventType:str,
        request:Request
    ):
    """
    eventType의 resources를 조회
    """
    # request를 통해 FastAPI app 객체에 접근해서 db를 꺼내는 것
    db:DBInterface=request.app.state.db

@query_eventTypes_router.get("/{eventType}/events")
def get_events_of_eventType(
        eventType:str,
        request:Request
    ):
    """
    eventType의 events를 조회
    """
    # request를 통해 FastAPI app 객체에 접근해서 db를 꺼내는 것
    db:DBInterface=request.app.state.db