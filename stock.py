import streamlit as st
from utils import load_data, load_data2
from one_stock import one
from market_stock import market
from home import home
from newest import new, index_new
from index_stock import in_stock
from rec import recommand
import pandas as pd
import os

def main():
    file_path = 'KRX 인덱스 리스트.csv'
    file_path2 = '한국 주식 리스트.csv'

    if not os.path.exists(file_path):
        df = pd.DataFrame()
        df.to_csv('KRX 인덱스 리스트.csv')
    
    if not os.path.exists(file_path2):
        df = pd.DataFrame()
        df.to_csv('한국 주식 리스트.csv')

    total_df = load_data() # 종목 리스트
    total_index_df = load_data2() # 인덱스 리스트

    st.title('간단 주식 분석')

    if st.sidebar.button('리스트 최신화'):
        new()
        index_new()
    st.sidebar.title('분석 방법 선택')

    analysis_method = st.sidebar.radio("분석 방법을 선택하세요", ("홈 화면",
                                                        "특정 종목 분석",
                                                        "인덱스 분석",
                                                        "시장 전체 분석",
                                                        "인덱스 기반 종목 추천"))
    if analysis_method == "특정 종목 분석":
        one(total_df)
    elif analysis_method == "인덱스 분석":
        in_stock(total_df, total_index_df)
    elif analysis_method == "시장 전체 분석":
        market(total_df)
    elif analysis_method == "홈 화면":
        home()
    elif analysis_method == "인덱스 기반 종목 추천":
        recommand(total_index_df, total_df)

if __name__ == "__main__":
    main()
