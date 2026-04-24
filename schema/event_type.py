from datetime import datetime
from typing import Optional
from pydantic import BaseModel,Field,model_validator
import field_element as FE

class EPCISEvent(BaseModel):
    eventTime:datetime=Field()
    eventTimeZoneOffset:str=Field(default="+00:00",pattern=r"^[+-]\d{2}:\d{2}$")
    recordTime:Optional[datetime]=Field(default=None)
    eventID:Optional[str]=Field(default=None)

class ObjectEvent(EPCISEvent):
    eventType:str=Field(default="ObjectEvent")
    epcList:list[str]=Field(default_factory=list)
    quantityList:list[FE.QuantityElement]=Field(default_factory=list)
    action:FE.Action=Field(default=FE.Action.OBSERVE)
    bizStep:Optional[FE.BizStep]=Field(default=None)
    disposition:Optional[FE.Disposition]=Field(default=None)
    persistentDisposition:Optional[FE.PersistentDisposition]=Field(default=None)
    readPoint:Optional[str]=Field(default=None)
    bizLocation:Optional[str]=Field(default=None)
    bizTransactionList:list[FE.BizTransaction]=Field(default_factory=list)
    sourceList:list[FE.Source]=Field(default_factory=list)
    destinationList:list[FE.Destination]=Field(default_factory=list)

    ### 검증 코드 추가
    # pydantic의 @model_validator 사용
    # 공식 문서 기준으로 ObjectEvent는 EPCISEvent를 상속하고, epcList 또는 quantityList 중 하나 이상을 가져야 함
    # ilmd는 action=ADD일 때만 허용