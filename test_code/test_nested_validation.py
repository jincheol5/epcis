"""
EPCISDocument를 통한 nested validation 검증
EventList 안의 event 데이터들이 자동으로 해당 class에 대해 검증되는지 확인
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from pydantic import ValidationError

# 상위 디렉토리를 path에 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from schema.epcis_document import EPCISDocument, EPCISHeader, EPCISBody
from schema.field_element import Action


def test_nested_event_validation_success():
    """정상적인 event 데이터들이 자동으로 검증되는지 확인"""
    data = {
        "creationDate": datetime.now().isoformat(),
        "epcisBody": {
            "eventList": [
                {
                    "type": "ObjectEvent",
                    "eventTime": datetime.now().isoformat(),
                    "eventTimeZoneOffset": "+00:00",
                    "epcList": ["urn:epc:id:sgtin:0000001.000001.123456"],
                    "action": "ADD",
                }
            ]
        }
    }
    
    # EPCISDocument로 검증
    doc = EPCISDocument(**data)
    assert len(doc.epcisBody.eventList) == 1
    assert doc.epcisBody.eventList[0].type == "ObjectEvent"
    print("✓ 정상 event 검증 성공")


def test_nested_event_invalid_type():
    """잘못된 event type - discriminator 검증"""
    data = {
        "creationDate": datetime.now().isoformat(),
        "epcisBody": {
            "eventList": [
                {
                    "type": "InvalidEventType",  # 존재하지 않는 타입
                    "eventTime": datetime.now().isoformat(),
                    "eventTimeZoneOffset": "+00:00",
                    "epcList": ["urn:epc:id:sgtin:0000001.000001.123456"],
                    "action": "ADD",
                }
            ]
        }
    }
    
    # EPCISDocument 검증 실패
    try:
        EPCISDocument(**data)
        raise AssertionError("ValidationError가 발생해야 함")
    except ValidationError as e:
        print(f"✓ 잘못된 event type 감지됨")


def test_nested_event_missing_required_field():
    """필수 필드 누락 - nested 검증"""
    data = {
        "creationDate": datetime.now().isoformat(),
        "epcisBody": {
            "eventList": [
                {
                    "type": "ObjectEvent",
                    "eventTime": datetime.now().isoformat(),
                    "eventTimeZoneOffset": "+00:00",
                    # epcList, quantityList, 또는 sensorElementList 모두 누락
                    "action": "ADD",
                }
            ]
        }
    }
    
    # ObjectEvent의 model_validator에서 검증 실패
    try:
        EPCISDocument(**data)
        raise AssertionError("ValidationError가 발생해야 함")
    except ValidationError as e:
        print(f"✓ 필수 필드 누락 감지됨")


def test_nested_aggregation_event_validation():
    """AggregationEvent도 정상 검증되는지 확인"""
    data = {
        "creationDate": datetime.now().isoformat(),
        "epcisBody": {
            "eventList": [
                {
                    "type": "AggregationEvent",
                    "eventTime": datetime.now().isoformat(),
                    "eventTimeZoneOffset": "+00:00",
                    "parentID": "urn:epc:id:sgtin:0000002.000001.000001",
                    "childEPCs": ["urn:epc:id:sgtin:0000001.000001.000001"],
                    "action": "ADD",
                }
            ]
        }
    }
    
    # EPCISDocument로 검증
    doc = EPCISDocument(**data)
    assert len(doc.epcisBody.eventList) == 1
    assert doc.epcisBody.eventList[0].type == "AggregationEvent"
    print("✓ AggregationEvent 검증 성공")


def test_nested_aggregation_invalid_rules():
    """AggregationEvent의 business rules 검증"""
    data = {
        "creationDate": datetime.now().isoformat(),
        "epcisBody": {
            "eventList": [
                {
                    "type": "AggregationEvent",
                    "eventTime": datetime.now().isoformat(),
                    "eventTimeZoneOffset": "+00:00",
                    "parentID": "urn:epc:id:sgtin:0000002.000001.000001",
                    # childEPCs와 childQuantityList 모두 없고 action이 DELETE가 아님
                    "action": "ADD",
                }
            ]
        }
    }
    
    # AggregationEvent의 model_validator에서 검증 실패
    try:
        EPCISDocument(**data)
        raise AssertionError("ValidationError가 발생해야 함")
    except ValidationError as e:
        print(f"✓ AggregationEvent 검증 규칙 위반 감지됨")


def test_multiple_events_partial_failure():
    """여러 event 중 하나만 유효하지 않은 경우"""
    data = {
        "creationDate": datetime.now().isoformat(),
        "epcisBody": {
            "eventList": [
                {
                    "type": "ObjectEvent",
                    "eventTime": datetime.now().isoformat(),
                    "eventTimeZoneOffset": "+00:00",
                    "epcList": ["urn:epc:id:sgtin:0000001.000001.123456"],
                    "action": "ADD",
                },
                {
                    "type": "AggregationEvent",
                    "eventTime": datetime.now().isoformat(),
                    "eventTimeZoneOffset": "+00:00",
                    # 필수 필드 누락
                    "action": "ADD",
                }
            ]
        }
    }
    
    # 두 번째 event에서 검증 실패
    try:
        EPCISDocument(**data)
        raise AssertionError("ValidationError가 발생해야 함")
    except ValidationError as e:
        print(f"✓ 부분 실패 감지됨")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("EPCISDocument Nested Validation 테스트")
    print("="*70 + "\n")
    
    print("[테스트 1] 정상 event 데이터 검증")
    try:
        test_nested_event_validation_success()
    except Exception as e:
        print(f"✗ 실패: {e}")
    
    print("\n[테스트 2] 잘못된 event type")
    try:
        test_nested_event_invalid_type()
    except Exception as e:
        print(f"✗ 예상과 다른 결과: {e}")
    
    print("\n[테스트 3] 필수 필드 누락")
    try:
        test_nested_event_missing_required_field()
    except Exception as e:
        print(f"✗ 예상과 다른 결과: {e}")
    
    print("\n[테스트 4] AggregationEvent 검증")
    try:
        test_nested_aggregation_event_validation()
    except Exception as e:
        print(f"✗ 실패: {e}")
    
    print("\n[테스트 5] AggregationEvent 규칙 검증")
    try:
        test_nested_aggregation_invalid_rules()
    except Exception as e:
        print(f"✗ 예상과 다른 결과: {e}")
    
    print("\n[테스트 6] 여러 event 중 부분 실패")
    try:
        test_multiple_events_partial_failure()
    except Exception as e:
        print(f"✗ 예상과 다른 결과: {e}")
    
    print("\n" + "="*70)
    print("테스트 완료")
    print("="*70)
