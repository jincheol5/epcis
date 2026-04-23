from typing import Optional
from enum import Enum
from pydantic import BaseModel

class QuantityElement(BaseModel):
    epcClass:str
    quantity:Optional[float]=None
    uom:Optional[str]=None

class Action(str,Enum):
    ADD="ADD"
    OBSERVE="OBSERVE"
    DELETE="DELETE"

class BizStep(str,Enum):
    ACCEPTING="accepting"
    ARRIVING="arriving"
    ASSEMBLING="assembling"
    COMMISSIONING="commissioning"
    CONSIGNING="consigning"
    CREATING_CLASS_INSTANCE="creating_class_instance"
    CYCLE_COUNTING="cycle_counting"
    DECOMMISSIONING="decommissioning"
    DEPARTING="departing"
    DESTROYING="destroying"
    DISASSEMBLING="disassembling"
    DISPENSING="dispensing"
    ENCODING="encoding"
    ENTERING_EXITING="entering_exiting"
    HOLDING="holding"
    INSPECTING="inspecting"
    INSTALLING="installing"
    KILLING="killing"
    LOADING="loading"
    OTHER="other"
    PACKING="packing"
    PICKING="picking"
    RECEIVING="receiving"
    REMOVING="removing"
    REPACKING="repacking"
    REPAIRING="repairing"
    REPLACING="replacing"
    RESERVING="reserving"
    RETAIL_SELLING="retail_selling"
    SHIPPING="shipping"
    STAGING_OUTBOUND="staging_outbound"
    STOCK_TAKING="stock_taking"
    STORING="storing"
    TRANSPORTING="transporting"
    UNLOADING="unloading"
    UNPACKING="unpacking"
    VOID_SHIPPING="void_shipping"

class Disposition(str, Enum):
    ACTIVE="active"
    ALIVE="alive"
    CONSUMED="consumed"
    DAMAGED="damaged"
    DESTROYED="destroyed"
    DISPENSED="dispensed"
    ENCODED="encoded"
    EXPIRED="expired"
    IN_PROGRESS="in_progress"
    IN_TRANSIT="in_transit"
    INACTIVE="inactive"
    NO_PEDIGREE_MATCH="no_pedigree_match"
    NON_SELLABLE_OTHER="non_sellable_other"
    PARTIALLY_DISPENSED="partially_dispensed"
    PROCESSING="processing"
    RECALLED="recalled"
    RESERVED="reserved"
    RETAIL_SOLD="retail_sold"

class PersistentDisposition(BaseModel):
    set:Optional[list[str]]=None
    unset:Optional[list[str]]=None

class BizTransaction(BaseModel):
    type:Optional[str]=None
    bizTransaction:str

class Source(BaseModel):
    type:Optional[str]=None
    source:str

class Destination(BaseModel):
    type:Optional[str]=None
    destination:str
