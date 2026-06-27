from typing import Literal, Optional

from pydantic import Field, model_validator

try:
    from . import field_element as FE
    from .epcis_event import EPCISEvent
except ImportError:
    import field_element as FE
    from epcis_event import EPCISEvent


class TransactionEvent(EPCISEvent):
    type: Literal["TransactionEvent"] = "TransactionEvent"
    bizTransactionList: list[FE.BizTransaction] = Field(min_length=1)
    parentID: Optional[FE.Uri] = None
    epcList: Optional[list[FE.Uri]] = None
    quantityList: Optional[list[FE.QuantityElement]] = Field(default=None, min_length=1)
    action: FE.Action
    bizStep: Optional[FE.BizStepValue] = None
    disposition: Optional[FE.DispositionValue] = None
    readPoint: Optional[FE.ReadPoint] = None
    bizLocation: Optional[FE.BizLocation] = None
    sourceList: Optional[list[FE.Source]] = None
    destinationList: Optional[list[FE.Destination]] = None
    sensorElementList: Optional[list[FE.SensorElement]] = None

    @model_validator(mode="after")
    def validate_epcis_rules(self) -> "TransactionEvent":
        has_epc_list = self.epcList is not None
        has_quantity_list = bool(self.quantityList)
        if not (has_epc_list or has_quantity_list) and self.action != FE.Action.DELETE:
            raise ValueError(
                "TransactionEvent requires epcList or quantityList unless action is DELETE."
            )
        return self
