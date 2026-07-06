from fastapi import FastAPI,HTTPException
from schema import EPCISDocument
from module import CaptureModule,DBInterface

app=FastAPI()

@app.post("/capture")
def epcis_capture(doc:EPCISDocument):
    db=None
    try:
        # 1. EPCIS Document 전처리
        event_list,vocabulary_list=CaptureModule.preprocess_epcis_document(doc=doc)

        # 2. MongoDB 저장 형태로 변환
        event_dict_list=CaptureModule.convert_events_for_mongoDB(
            event_list=event_list
        )
        vocabulary_element_list=CaptureModule.convert_vocabularies_for_mongoDB(
            vocabulary_list=vocabulary_list
        )

        # 3. DB 저장
        db=DBInterface()
        if event_dict_list:
            db.insert_event_data(
                event_list=event_dict_list
            )

        if vocabulary_element_list:
            db.insert_master_data(
                vocabulary_element_list=vocabulary_element_list
            )

        # 4. 응답 반환
        return {
            "message": "EPCIS document captured successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to capture EPCIS document: {str(e)}"
        )
    finally:
        if db is not None:
            db.disconnect_db()