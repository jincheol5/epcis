from datetime import datetime
from typing import Any,Optional,Union

from pydantic import BaseModel,ConfigDict,Field

from . import field_element as FE


class EPCISEvent(BaseModel):
    model_config=ConfigDict(
        extra="allow",
        populate_by_name=True,
        validate_assignment=True,
    )

    context: Optional[Any]=Field(default=None,alias="@context")
    eventTime: datetime
    eventTimeZoneOffset: str=Field(
        pattern=r"^([+-])((0[0-9]|1[0-3]):([0-5][0-9])|14:00)$"
    )
    recordTime: Optional[datetime]=None
    eventID: Optional[FE.URI]=None
    certificationInfo: Optional[Union[FE.URI,list[FE.URI]]]=None
    errorDeclaration: Optional[FE.ErrorDeclaration]=None
