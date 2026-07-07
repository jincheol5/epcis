from fastapi import APIRouter,Request,HTTPException
from schema import EPCISDocument
from module import CaptureModule,DBInterface

capture_router=APIRouter(prefix="/capture",tags=["capture"])

@capture_router.post("/")
def capture(
        document:EPCISDocument,
        request:Request
    ):
    # request를 통해 FastAPI app 객체에 접근해서 db를 꺼내는 것
    db:DBInterface=request.app.state.db
    try:
        # 1. Extract event,vocabulary list from EPCIS Document
        event_list,vocabulary_list=CaptureModule.extract_from_epcis_document(document=document)

        # 2. Transform data for MongoDB load
        event_list=CaptureModule.transform_events(
            event_list=event_list
        )
        vocab_element_list=CaptureModule.transform_vocabularies(
            vocabulary_list=vocabulary_list
        )

        # 3. Load to MongoDB
        if event_list:
            db.insert_data_list(
                data_list=event_list,
                data_type=f"event"
            )
        if vocab_element_list:
            db.insert_data_list(
                data_list=vocab_element_list,
                data_type=f"vocab"
            )
        return {
            "message": "EPCIS document captured successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to capture EPCIS document: {str(e)}"
        )