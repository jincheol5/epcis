import os
import argparse
import json
import pandas as pd
import numpy as np

"""
<< Test >> 
Check Dataset.
"""
def test_fn(**kwargs):
    # dataset_name=kwargs["dataset_name"]
    dataset_dir_name=f"synthetic-food-supply-chain-dataset"
    dataset_file_name=f"synthetic-food-supply-chain-dataset.json"
    dataset_path=os.path.join("..","data","epcis",dataset_dir_name,dataset_file_name)
    match kwargs['test_num']:
        case 1:
            """
            Test. 
            """
            with open(dataset_path,"r",encoding="utf-8") as f:
                epcis_doc=json.load(f)
            epcis_header=epcis_doc["epcisHeader"]
            epcis_body=epcis_doc["epcisBody"]
            print(f"epcis_doc keys: {epcis_doc.keys()}",end="\n\n")
            print(f"epcis header keys: {epcis_header.keys()}",end="\n\n")
            print(f"epcis body keys: {epcis_body.keys()}",end="\n\n")

            master_data=epcis_header["epcisMasterData"]
            print(f"master data keys: {master_data.keys()}",end="\n\n")

            vocabulary_list=master_data["vocabularyList"]
            print(f"length of vocabulary list: {len(vocabulary_list)}",end="\n\n")
            for vocabulary in vocabulary_list:
                print(f"vocabulary keys: {vocabulary.keys()}",end="\n\n")
                print(f"vocabulary type: {vocabulary['type']}",end="\n\n")
                vocabulary_element_list=vocabulary["vocabularyElementList"]
                print(f"length of vocabulary elements: {len(vocabulary_element_list)}",end="\n\n")
                for element in vocabulary_element_list:
                    print(json.dumps(element,indent=2,ensure_ascii=False))
                    print()
                    break
                break

            event_list=epcis_body["eventList"]
            print(f"length of event list: {len(event_list)}",end="\n\n")
            for idx,event in enumerate(event_list):
                if idx==1:
                    break
                print(json.dumps(event,indent=2,ensure_ascii=False))
                print()

if __name__=="__main__":
    """
    Check Dataset.
    """
    parser=argparse.ArgumentParser()
    parser.add_argument("--test_num",type=int,default=1)
    parser.add_argument("--dataset_name",type=str,default=f"enron")
    args=parser.parse_args()
    test_config={
        "test_num":args.test_num,
        "dataset_name":args.dataset_name
    }
    test_fn(**test_config)