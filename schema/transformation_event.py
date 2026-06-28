from typing import Literal,Optional

from pydantic import Field,model_validator

try:
    from . import field_element as FE
    from .epcis_event import EPCISEvent
except ImportError:
    import field_element as FE
    from epcis_event import EPCISEvent


class TransformationEvent(EPCISEvent):
    type: Literal["TransformationEvent"]="TransformationEvent"
    inputEPCList: Optional[list[FE.URI]]=Field(default=None,min_length=1)
    inputQuantityList: Optional[list[FE.QuantityElement]]=Field(default=None,min_length=1)
    outputEPCList: Optional[list[FE.URI]]=Field(default=None,min_length=1)
    outputQuantityList: Optional[list[FE.QuantityElement]]=Field(default=None,min_length=1)
    transformationID: Optional[FE.URI]=None
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
    def validate_epcis_rules(self)->"TransformationEvent":
        has_input=bool(self.inputEPCList) or bool(self.inputQuantityList)
        has_output=bool(self.outputEPCList) or bool(self.outputQuantityList)

        if (has_input and has_output) or (self.transformationID is not None and (has_input or has_output)):
            return self
        raise ValueError(
            "TransformationEvent requires both input and output lists, or transformationID with at least one input/output list."
        )
