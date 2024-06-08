# utils.py
# load_data

import pandas as pd

def load_data():
    data = pd.read_csv('한국 주식 리스트.csv')
    return data

def load_data2():
    index_data = pd.read_csv('KRX 인덱스 리스트.csv')
    return index_data