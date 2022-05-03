from __future__ import annotations

import uuid
import numpy as np
import pandas as pd

def assign_uuids_to_new_entries(df) -> DataFrame:
    
    for i in range(len(df)):
        if pd.isna(df.loc[i,"UUID"]):
            df.loc[i,"UUID"]=uuid.uuid4()
    return df