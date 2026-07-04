from datetime import datetime
from typing import Annotated,Any,Literal,Optional,Union

from pydantic import BaseModel,ConfigDict,Field

from .aggregation_event import AggregationEvent
from .association_event import AssociationEvent
from .object_event import ObjectEvent
from .transaction_event import TransactionEvent
from .transformation_event import TransformationEvent


EPCISEventType=Annotated[
    Union[
        ObjectEvent,
        AggregationEvent,
        TransactionEvent,
        TransformationEvent,
        AssociationEvent,
    ],
    Field(discriminator="type"),
]

class EPCISBaseDocumentElement(BaseModel):
    model_config=ConfigDict(
        extra="allow",
        populate_by_name=True,
        validate_assignment=True,
    )

class EPCISHeader(EPCISBaseDocumentElement):
    epcisMasterData: Optional[dict[str,Any]]=None

class EPCISBody(EPCISBaseDocumentElement):
    eventList: list[EPCISEventType]=Field(default_factory=list)

class EPCISDocument(EPCISBaseDocumentElement):
    context: Any=Field(
        default="https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
        alias="@context",
    )
    type: Literal["EPCISDocument"]="EPCISDocument"
    schemaVersion: str="2.0"
    creationDate: datetime
    epcisHeader: Optional[EPCISHeader]=None
    epcisBody: EPCISBody
    id: Optional[str]=Field(default=None,alias="@id")

