from datetime import datetime
from typing import Optional,Union,List,Dict
from pydantic import BaseModel,ConfigDict,Field

class EPCISEvent(BaseModel):
    """
    """
    model_config=ConfigDict(
        populate_by_name=True, # alias(@context) 사용 가능
        extra="allow", # 정의되지 않은 필드 허용 (EPCIS 확장 대응)
        validate_assignment=True # 값 변경 시 검증
    )

    # JSON-LD context
    context: Union[str,List[str]]=Field(
        default="https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
        alias="@context"
    )

    # 이벤트 타입 (ObjectEvent 등에서 override)
    eventType: str

    # 필수 필드
    eventTime: datetime
    eventTimeZoneOffset: str

    # 선택 필드
    recordTime: Optional[datetime] = None
    eventID: Optional[str] = None
