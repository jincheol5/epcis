from datetime import datetime
from enum import Enum
from typing import List,Optional,Union
from pydantic import BaseModel,ConfigDict,Field

"""
Field
"""
class Action(str,Enum):
    ADD="ADD"
    OBSERVE="OBSERVE"
    DELETE="DELETE"

class UOM(str,Enum):
    MTR="MTR" # metre
    CMT="CMT" # centimetre
    MMT="MMT" # millimetre
    KMT="KMT" # kilometre
    KGM="KGM" # kilogram
    GRM="GRM" # gram
    MGM="MGM" # milligram
    # 이후 추가 

class QuantityElement(BaseModel):
    epcClass: str
    quantity: Optional[float]
    uom: Optional[UOM]


class ErrorDeclaration(BaseModel):
    declarationTime: datetime
    reason: str
    correctiveEventIDs: List[datetime]

"""
Event
"""
class EventBase(BaseModel):
    model_config=ConfigDict(
        populate_by_name=True, # alias와 실제 필드명 둘 다 입력 가능
        validate_assignment=True, # 객체 생성 후 값 변경 시에도 검증 수행
        extra="forbid" # 정의되지 않은 필드 허용 X (임시)
    )

class EPCISEvent(EventBase):
    # Required
    eventTime: datetime
    eventTimeZoneOffset: str

    # Optional
    recordTime: Optional[datetime]
    eventID: Optional[str]
    errorDeclaration: Optional[ErrorDeclaration]
    certificationInfo: Optional[str]


class ObjectEvent(EPCISEvent):
    # Required
    action: Action




"""
Document
"""