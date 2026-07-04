import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from schema.aggregation_event import AggregationEvent
from schema.association_event import AssociationEvent
from schema.epcis_document import EPCISDocument
from schema.object_event import ObjectEvent
from schema.transaction_event import TransactionEvent
from schema.transformation_event import TransformationEvent


SAMPLE_DIR = Path(__file__).parent / "samples"


def load_sample(name: str):
    with (SAMPLE_DIR / name).open(encoding="utf-8") as sample_file:
        return json.load(sample_file)


def test_valid_epcis_document_sample_validates_all_event_types():
    sample = load_sample("valid_epcis_document.json")

    document = EPCISDocument.model_validate(sample)

    assert document.type == "EPCISDocument"
    assert document.schemaVersion == "2.0"
    assert document.id == "urn:uuid:12345678-1234-5678-1234-567812345678"
    assert len(document.epcisBody.eventList) == 5
    assert [type(event) for event in document.epcisBody.eventList] == [
        ObjectEvent,
        AggregationEvent,
        TransactionEvent,
        TransformationEvent,
        AssociationEvent,
    ]


@pytest.mark.parametrize(
    "invalid_sample",
    load_sample("invalid_epcis_documents.json"),
    ids=lambda invalid_sample: invalid_sample["name"],
)
def test_invalid_epcis_document_samples_raise_validation_error(invalid_sample):
    with pytest.raises(ValidationError):
        EPCISDocument.model_validate(invalid_sample["document"])
