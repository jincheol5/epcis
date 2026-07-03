import os
import argparse
import pandas as pd
import numpy as np

"""
<< Test >> 
Check Dataset.
"""
def test_fn(**kwargs):
    dataset_name=kwargs["dataset_name"]
    dataset_path=os.path.join("..","data","epcis",dataset_name)
    match kwargs['test_num']:
        case 1:
            """
            Test. 
            """
            


if __name__=="__main__":
    """
    Execute test_fn
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