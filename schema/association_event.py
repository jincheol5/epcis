from typing import Literal,Optional

from pydantic import Field,model_validator

try:
    from . import field_element as FE
    from .epcis_event import EPCISEvent
except ImportError:
    import field_element as FE
    from epcis_event import EPCISEvent


class AssociationEvent(EPCISEvent):
    type: Literal["AssociationEvent"]="AssociationEvent"
    parentID: FE.URI
    childEPCs: Optional[list[FE.URI]]=Field(default=None,min_length=1)
    childQuantityList: Optional[list[FE.QuantityElement]]=Field(default=None,min_length=1)
    action: FE.Action
    bizStep: Optional[FE.BizStepValue]=None
    disposition: Optional[FE.DispositionValue]=None
    readPoint: Optional[FE.ReadPoint]=None
    bizLocation: Optional[FE.BizLocation]=None
    bizTransactionList: Optional[list[FE.BizTransaction]]=None
    sourceList: Optional[list[FE.Source]]=None
    destinationList: Optional[list[FE.Destination]]=None
    sensorElementList: Optional[list[FE.SensorElement]]=None

    @model_validator(mode="after")
    def validate_epcis_rules(self)->"AssociationEvent":
        has_child_list=bool(self.childEPCs) or bool(self.childQuantityList)
        if not has_child_list and self.action!=FE.Action.DELETE:
            raise ValueError(
                "AssociationEvent requires childEPCs or childQuantityList unless action is DELETE."
            )
        return self
