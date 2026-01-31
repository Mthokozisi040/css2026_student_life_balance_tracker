# -*- coding: utf-8 -*-
"""
Created on Sat Jan 31 11:17:25 2026

@author: mbuya
"""

import pandas as pd
import os

FILE_NAME = "life_balance_data.csv"

def save_data(data):
    if os.path.exists(FILE_NAME):
        old = pd.read_csv(FILE_NAME)
        new = pd.DataFrame([data])
        df = pd.concat([old, new], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_csv(FILE_NAME, index=False)
    return df


def load_user_data(name):
    if not os.path.exists(FILE_NAME):
        return None

    df = pd.read_csv(FILE_NAME)
    return df[df["Student"] == name]
