from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any,Optional,Union
from pydantic import BaseModel,ConfigDict,Field,StrictFloat,StrictInt,StrictStr,model_validator


URI=str
VocabValue=str


class EPCISFieldElement(BaseModel):
    model_config=ConfigDict(extra="forbid",validate_assignment=True)


class EPCISExtensibleFieldElement(BaseModel):
    model_config=ConfigDict(extra="allow",validate_assignment=True)


class EventType(str,Enum):
    ObjectEvent="ObjectEvent"
    AggregationEvent="AggregationEvent"
    AssociationEvent="AssociationEvent"
    TransformationEvent="TransformationEvent"
    TransactionEvent="TransactionEvent"


class Action(str,Enum):
    ADD="ADD"
    OBSERVE="OBSERVE"
    DELETE="DELETE"


class BizStep(str,Enum):
    accepting="accepting"
    arriving="arriving"
    assembling="assembling"
    collecting="collecting"
    commissioning="commissioning"
    consigning="consigning"
    creating_class_instance="creating_class_instance"
    cycle_counting="cycle_counting"
    decommissioning="decommissioning"
    departing="departing"
    destroying="destroying"
    disassembling="disassembling"
    dispensing="dispensing"
    encoding="encoding"
    entering_exiting="entering_exiting"
    holding="holding"
    inspecting="inspecting"
    installing="installing"
    killing="killing"
    loading="loading"
    other="other"
    packing="packing"
    picking="picking"
    receiving="receiving"
    removing="removing"
    repackaging="repackaging"
    repairing="repairing"
    replacing="replacing"
    reserving="reserving"
    retail_selling="retail_selling"
    shipping="shipping"
    staging_outbound="staging_outbound"
    stock_taking="stock_taking"
    stocking="stocking"
    storing="storing"
    transporting="transporting"
    unloading="unloading"
    unpacking="unpacking"
    void_shipping="void_shipping"
    sensor_reporting="sensor_reporting"
    sampling="sampling"


class Disposition(str,Enum):
    active="active"
    container_closed="container_closed"
    damaged="damaged"
    destroyed="destroyed"
    dispensed="dispensed"
    disposed="disposed"
    encoded="encoded"
    expired="expired"
    in_progress="in_progress"
    in_transit="in_transit"
    inactive="inactive"
    no_pedigree_match="no_pedigree_match"
    non_sellable_other="non_sellable_other"
    partially_dispensed="partially_dispensed"
    recalled="recalled"
    reserved="reserved"
    retail_sold="retail_sold"
    returned="returned"
    sellable_accessible="sellable_accessible"
    sellable_not_accessible="sellable_not_accessible"
    stolen="stolen"
    unknown="unknown"
    available="available"
    completeness_verified="completeness_verified"
    completeness_inferred="completeness_inferred"
    conformant="conformant"
    container_open="container_open"
    mismatch_instance="mismatch_instance"
    mismatch_class="mismatch_class"
    mismatch_quantity="mismatch_quantity"
    needs_replacement="needs_replacement"
    non_conformant="non_conformant"
    unavailable="unavailable"


class BizTransactionType(str,Enum):
    bol="bol"
    cert="cert"
    desadv="desadv"
    inv="inv"
    pedigree="pedigree"
    po="po"
    poc="poc"
    prodorder="prodorder"
    recadv="recadv"
    rma="rma"
    testprd="testprd"
    testres="testres"
    upevt="upevt"


class SourceDestinationType(str,Enum):
    owning_party="owning_party"
    possessing_party="possessing_party"
    location="location"


class SourceType(str,Enum):
    owning_party=SourceDestinationType.owning_party.value
    possessing_party=SourceDestinationType.possessing_party.value
    location=SourceDestinationType.location.value


class SensorAlertType(str,Enum):
    ALARM_CONDITION="ALARM_CONDITION"
    ERROR_CONDITION="ERROR_CONDITION"


class MeasurementType(str,Enum):
    AbsoluteHumidity="AbsoluteHumidity"
    AbsorbedDose="AbsorbedDose"
    AbsorbedDoseRate="AbsorbedDoseRate"
    Acceleration="Acceleration"
    Radioactivity="Radioactivity"
    Altitude="Altitude"
    AmountOfSubstance="AmountOfSubstance"
    AmountOfSubstancePerUnitVolume="AmountOfSubstancePerUnitVolume"
    Angle="Angle"
    AngularAcceleration="AngularAcceleration"
    AngularMomentum="AngularMomentum"
    AngularVelocity="AngularVelocity"
    Area="Area"
    Capacitance="Capacitance"
    Conductance="Conductance"
    Conductivity="Conductivity"
    Count="Count"
    Density="Density"
    Dimensionless="Dimensionless"
    DoseEquivalent="DoseEquivalent"
    DoseEquivalentRate="DoseEquivalentRate"
    DynamicViscosity="DynamicViscosity"
    ElectricCharge="ElectricCharge"
    ElectricCurrent="ElectricCurrent"
    ElectricCurrentDensity="ElectricCurrentDensity"
    ElectricFieldStrength="ElectricFieldStrength"
    Energy="Energy"
    Exposure="Exposure"
    Force="Force"
    Frequency="Frequency"
    Illuminance="Illuminance"
    Inductance="Inductance"
    Irradiance="Irradiance"
    KinematicViscosity="KinematicViscosity"
    Length="Length"
    LinearMomentum="LinearMomentum"
    Luminance="Luminance"
    LuminousFlux="LuminousFlux"
    LuminousIntensity="LuminousIntensity"
    MagneticFlux="MagneticFlux"
    MagneticFluxDensity="MagneticFluxDensity"
    MagneticVectorPotential="MagneticVectorPotential"
    Mass="Mass"
    MassConcentration="MassConcentration"
    MassFlowRate="MassFlowRate"
    MassPerAreaTime="MassPerAreaTime"
    MemoryCapacity="MemoryCapacity"
    MolalityOfSolute="MolalityOfSolute"
    MolarEnergy="MolarEnergy"
    MolarMass="MolarMass"
    MolarVolume="MolarVolume"
    Power="Power"
    Pressure="Pressure"
    RadiantFlux="RadiantFlux"
    RadiantIntensity="RadiantIntensity"
    RelativeHumidity="RelativeHumidity"
    Resistance="Resistance"
    Resistivity="Resistivity"
    SolidAngle="SolidAngle"
    SpecificVolume="SpecificVolume"
    Speed="Speed"
    SurfaceDensity="SurfaceDensity"
    SurfaceTension="SurfaceTension"
    Temperature="Temperature"
    Time="Time"
    Torque="Torque"
    Voltage="Voltage"
    Volume="Volume"
    VolumeFlowRate="VolumeFlowRate"
    VolumeFraction="VolumeFraction"
    VolumetricFlux="VolumetricFlux"
    Wavenumber="Wavenumber"


class Component(str,Enum):
    x="x"
    y="y"
    z="z"
    axial_distance="axial_distance"
    azimuth="azimuth"
    height="height"
    spherical_radius="spherical_radius"
    polar_angle="polar_angle"
    elevation_angle="elevation_angle"
    easting="easting"
    northing="northing"
    latitude="latitude"
    longitude="longitude"
    altitude="altitude"


class ErrorReason(str,Enum):
    incorrect_data="incorrect_data"
    did_not_occur="did_not_occur"


BizStepValue=Union[BizStep,VocabValue]
DispositionValue=Union[Disposition,VocabValue]
BizTransactionTypeValue=Union[BizTransactionType,VocabValue]
SourceDestinationTypeValue=Union[SourceDestinationType,VocabValue]
MeasurementTypeValue=Union[MeasurementType,VocabValue]
SensorAlertTypeValue=Union[SensorAlertType,VocabValue]
ComponentValue=Union[Component,VocabValue]
MasterDataAttributeValue=Union[StrictInt,StrictFloat,StrictStr,dict[str,Any]]


class QuantityElement(EPCISFieldElement):
    epcClass: URI
    quantity: Optional[Decimal]=None
    uom: Optional[str]=Field(default=None,pattern=r"^[A-Z0-9]{2,3}$")


class PersistentDisposition(EPCISFieldElement):
    set: list[DispositionValue]=Field(default_factory=list)
    unset: list[DispositionValue]=Field(default_factory=list)

    @model_validator(mode="after")
    def require_set_or_unset(self) -> "PersistentDisposition":
        if not self.set and not self.unset:
            raise ValueError("PersistentDisposition requires at least one of set or unset.")
        return self


class BizTransaction(EPCISFieldElement):
    bizTransaction: URI
    type: Optional[BizTransactionTypeValue]=None


class ReadPoint(EPCISExtensibleFieldElement):
    id: URI


class BizLocation(EPCISExtensibleFieldElement):
    id: URI


class Source(EPCISFieldElement):
    type: SourceDestinationTypeValue
    source: URI


class Destination(EPCISFieldElement):
    type: SourceDestinationTypeValue
    destination: URI


class SensorMetadata(EPCISExtensibleFieldElement):
    time: Optional[datetime]=None
    deviceID: Optional[URI]=None
    deviceMetadata: Optional[URI]=None
    rawData: Optional[URI]=None
    startTime: Optional[datetime]=None
    endTime: Optional[datetime]=None
    dataProcessingMethod: Optional[URI]=None
    bizRules: Optional[URI]=None


class SensorReport(EPCISExtensibleFieldElement):
    type: MeasurementTypeValue
    exception: Optional[SensorAlertTypeValue]=None
    deviceID: Optional[URI]=None
    deviceMetadata: Optional[URI]=None
    rawData: Optional[URI]=None
    dataProcessingMethod: Optional[URI]=None
    bizRules: Optional[URI]=None
    time: Optional[datetime]=None
    microorganism: Optional[URI]=None
    chemicalSubstance: Optional[URI]=None
    coordinateReferenceSystem: Optional[URI]=None
    value: Optional[Decimal]=None
    component: Optional[ComponentValue]=None
    stringValue: Optional[str]=None
    booleanValue: Optional[bool]=None
    hexBinaryValue: Optional[str]=None
    uriValue: Optional[URI]=None
    minValue: Optional[Decimal]=None
    maxValue: Optional[Decimal]=None
    meanValue: Optional[Decimal]=None
    sDev: Optional[Decimal]=None
    percRank: Optional[Decimal]=None
    percValue: Optional[Decimal]=None
    uom: Optional[str]=None


class SensorElement(EPCISExtensibleFieldElement):
    sensorReport: list[SensorReport]=Field(min_length=1)
    sensorMetadata: Optional[SensorMetadata]=None


class ILMD(EPCISExtensibleFieldElement):
    pass


class ErrorDeclaration(EPCISExtensibleFieldElement):
    declarationTime: datetime
    reason: Optional[Union[ErrorReason,URI]]=None
    correctiveEventIDs: list[URI]=Field(default_factory=list)


class MasterDataAttribute(EPCISExtensibleFieldElement):
    id: URI
    attribute: Optional[MasterDataAttributeValue]=None


class VocabularyElement(EPCISExtensibleFieldElement):
    id: URI
    attributes: Optional[list[MasterDataAttribute]]=None
    children: Optional[list[URI]]=None


class Vocabulary(EPCISExtensibleFieldElement):
    type: URI
    vocabularyElementList: Optional[list[VocabularyElement]]=None


ExtensionFields=dict[str,Any]
