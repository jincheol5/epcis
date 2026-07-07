from uuid import uuid4
from typing import Any
from schema import EPCISDocument

class CaptureModule:
    """
    """
    @staticmethod
    def extract_from_epcis_document(document:EPCISDocument):
        """
        Extract event list and vocabulary list from a validated EPCISDocument.
        """
        event_list=document.epcisBody.eventList
        vocabulary_list=[]
        if document.epcisHeader and document.epcisHeader.epcisMasterData:
            vocabulary_list=document.epcisHeader.epcisMasterData.vocabularyList
        return event_list,vocabulary_list

    @staticmethod
    def transform_events(event_list:list):
        """
        Input:
            event_list
        Output:
            transformed_event_list 
        """
        transformed_event_list:list[dict[str,Any]]=[]
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
            transformed_event_list.append(event_dict)
        return transformed_event_list

    @staticmethod
    def transform_vocabularies(vocabulary_list:list):
        """
        EPCIS master data의 vocabularyList를 VocabularyElement 단위 dict list로 변환한다.
        각 VocabularyElement의 _id는 {vocabulary_type}_{element_id}로 구성한다.
        VocabularyElement의 Attributes는 key=id, value=attribute인 dict로 변환하여 저장한다.
        Input:
            vocabulary_list
        Output:
            preprocessed_vocab_element_list 
        """
        transformed_vocab_element_list:list[dict[str,Any]]=[]
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
                vocab_element_dict={
                    "_id": f"{vocabulary_type}_{element_id}",
                    "vocabularyType": vocabulary_type,
                    "elementID": element_id,
                    "attributes": attribute_dict,
                    "children": children
                }
                transformed_vocab_element_list.append(vocab_element_dict)
        return transformed_vocab_element_list
