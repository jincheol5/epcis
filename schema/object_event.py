from typing import Literal,Optional

from pydantic import Field,model_validator

from . import field_element as FE
from .epcis_event import EPCISEvent


class ObjectEvent(EPCISEvent):
    type: Literal["ObjectEvent"]="ObjectEvent"
    epcList: Optional[list[FE.URI]]=None
    quantityList: Optional[list[FE.QuantityElement]]=Field(default=None,min_length=1)
    action: FE.Action
    bizStep: Optional[FE.BizStepValue]=None
    disposition: Optional[FE.DispositionValue]=None
    persistentDisposition: Optional[FE.PersistentDisposition]=None
    readPoint: Optional[FE.ReadPoint]=None
    bizLocation: Optional[FE.BizLocation]=None
    bizTransactionList: Optional[list[FE.BizTransaction]]=None
    sourceList: Optional[list[FE.Source]]=None
    destinationList: Optional[list[FE.Destination]]=None
    sensorElementList: Optional[list[FE.SensorElement]]=None
    ilmd: Optional[FE.ILMD]=None

    @model_validator(mode="after")
    def validate_epcis_rules(self)->"ObjectEvent":
        has_epc_list=self.epcList is not None
        has_quantity_list=bool(self.quantityList)
        has_sensor_reading=bool(self.sensorElementList) and self.readPoint is not None

        if not (has_epc_list or has_quantity_list or has_sensor_reading):
            raise ValueError(
                "ObjectEvent requires epcList, quantityList, or sensorElementList with readPoint."
            )
        if self.ilmd is not None and self.action!=FE.Action.ADD:
            raise ValueError("ObjectEvent ilmd is only allowed when action is ADD.")
        return self
