from typing import Optional
from enum import Enum
from pydantic import BaseModel,Field

class UOM(str,Enum):
    EA="EA"
    KGM="KGM"
    GRM="GRM"
    LTR="LTR"
    MLT="MLT"

class BizTransactionType(str,Enum):
    po="po"
    inv="inv"

class SourceType(str,Enum):
    owning_party="owning_party"
    possessing_party="possessing_party"
    location="location"

class QuantityElement(BaseModel):
    epcClass:str=Field(default="")
    quantity:Optional[float]=Field(default=0.0)
    uom:Optional[UOM]=Field(default=UOM.EA)

class Action(str,Enum):
    ADD="ADD"
    OBSERVE="OBSERVE"
    DELETE="DELETE"

class BizStep(str,Enum):
    shipping="shipping"
    receiving="receiving"
    packing="packing"

class Disposition(str,Enum):
    in_progress="in_progress"
    in_transit="in_transit"

class PersistentDisposition(BaseModel):
    set:list[Disposition]=Field(default_factory=list)
    unset:list[Disposition]=Field(default_factory=list)

class BizTransaction(BaseModel):
    type:BizTransactionType=Field(default=BizTransactionType.po)
    bizTransaction:str

class Source(BaseModel):
    type:SourceType=Field(default=SourceType.location)
    source:str

class Destination(BaseModel):
    type:Optional[str]=None
    destination:str
