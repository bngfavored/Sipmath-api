from PySIP import PySIP3library as PySIP
import numpy as np
import pandas as pd
from fastapi import FastAPI
from typing import Optional, List, Union
from pydantic import BaseModel
import json

app = FastAPI()

class SIPDataModel(BaseModel):
    data: List[List[Union[int, float]]]
    variable_name: List[str]
    filename: str
    author: str
    dependence: Optional[str] = 'independent'
    boundedness: List[str]
    bounds: List[List[int]]
    term_saved: List[int]
    probs: List[List[float]]

@app.post("/sipmath-json")
def sipmath_json(sip_data: SIPDataModel):
    # Convert data into correct format
    df = pd.DataFrame(sip_data.data).T
    df.columns = sip_data.variable_name
    filename = f"{sip_data.filename}.SIPmath"
    data_dict_for_JSON = dict(boundedness=sip_data.boundedness,
                    bounds=sip_data.bounds,
                    term_saved=sip_data.term_saved)
    PySIP.Json(SIPdata=df,
                    file_name=filename,
                    author=sip_data.author,
                    dependence=sip_data.dependence,
                    setupInputs=data_dict_for_JSON,
                    probs=sip_data.probs)
    with open(filename, 'rb') as f:
        return json.load(f)