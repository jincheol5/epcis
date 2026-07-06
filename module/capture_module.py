from uuid import uuid4
from typing import Any
from schema import EPCISDocument

class CaptureModule:
    """
    """

    @staticmethod
    def preprocess_epcis_document(doc:EPCISDocument):
        """
        Extract event list and vocabulary list from a validated EPCISDocument.
        """
        event_list=doc.epcisBody.eventList
        vocabulary_list=[]
        if doc.epcisHeader and doc.epcisHeader.epcisMasterData:
            vocabulary_list=doc.epcisHeader.epcisMasterData.vocabularyList
        return event_list,vocabulary_list

    @staticmethod
    def convert_events_for_mongoDB(event_list:list):
        """
        """
        event_dict_list:list[dict[str,Any]]=[]
        for event in event_list:
            event_dict=event.model_dump(
                mode="json",
                by_alias=True,
                exclude_none=True,
            )
            event_id=event_dict.get("eventID")
            if event_id is None:
                event_id=f"urn:uuid:{uuid4()}"
                event_dict["eventID"]=event_id
            event_dict["_id"]=event_id
            event_dict_list.append(event_dict)
        return event_dict_list

    @staticmethod
    def convert_vocabularies_for_mongoDB(vocabulary_list:list):
        """
        EPCIS master data의 vocabularyList를 VocabularyElement 단위 dict list로 변환한다.
        각 VocabularyElement의 _id는 {vocabulary_type}_{element_id}로 구성한다.
        VocabularyElement의 Attributes는 key=id, value=attribute인 dict로 변환하여 저장한다.
        """
        element_dict_list:list[dict[str,Any]]=[]
        for vocabulary in vocabulary_list:
            vocabulary_type=vocabulary.type
            vocabulary_element_list=vocabulary.vocabularyElementList or []
            for vocabulary_element in vocabulary_element_list:
                element_id=vocabulary_element.id
                attribute_dict:dict[str,Any]={}
                attributes=vocabulary_element.attributes or []
                for attribute in attributes:
                    attribute_dict[attribute.id]=attribute.attribute
                children=vocabulary_element.children or []
                element_dict={
                    "_id": f"{vocabulary_type}_{element_id}",
                    "vocabularyType": vocabulary_type,
                    "elementID": element_id,
                    "attributes": attribute_dict,
                    "children": children
                }
                element_dict_list.append(element_dict)
        return element_dict_list
