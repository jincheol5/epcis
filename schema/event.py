from datetime import datetime
from typing import Optional,Union,List,Dict,Any
from pydantic import BaseModel,Field,ConfigDict,field_validator








class EPCISEvent(BaseModel):
    """
    """
    # Pydantic 설정
    model_config = ConfigDict(
        populate_by_name=True,   # alias(@context) 사용 가능
        extra="allow",           # 정의되지 않은 필드 허용 (EPCIS 확장 대응)
        validate_assignment=True # 값 변경 시 검증
    )

    # JSON-LD context
    context: Union[str, List[Union[str, Dict[str, Any]]]] = Field(
        default="https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
        alias="@context"
    )

    # 이벤트 타입 (ObjectEvent 등에서 override)
    type: str

    # 필수 필드
    eventTime: datetime
    eventTimeZoneOffset: str

    # 선택 필드
    recordTime: Optional[datetime] = None
    eventID: Optional[str] = None

    # (간단 버전) errorDeclaration / certificationInfo는 일단 생략 가능

    @field_validator("eventTimeZoneOffset")
    @classmethod
    def validate_timezone(cls, v: str) -> str:
        """
        형식: +09:00, -05:00
        """
        if len(v) != 6 or v[0] not in "+-" or v[3] != ":":
            raise ValueError("eventTimeZoneOffset must be in format ±HH:MM")
        return v