import streamlit as st
import pandas as pd
from pykrx import stock

def new():
    #코스피 종목데이터 추출
    stock_list = []
    stock_code = []
    for ticker in stock.get_market_ticker_list():
        종목 = stock.get_market_ticker_name(ticker)
        print(종목)
        stock_list.append(종목)
        stock_code.append(ticker)

    df1 = pd.DataFrame(stock_list, columns=['종목명'])
    df2 = pd.DataFrame(stock_code, columns=['종목코드'])
    final_df1 = pd.concat([df1, df2], axis=1) # 열 방향으로 통합

    #코스닥 종목데이터 추출
    stock_list = []
    stock_code = []
    for ticker in stock.get_market_ticker_list(market="KOSDAQ"):
        종목 = stock.get_market_ticker_name(ticker)
        print(종목)
        stock_list.append(종목)
        stock_code.append(ticker)

    df1 = pd.DataFrame(stock_list, columns=['종목명'])
    df2 = pd.DataFrame(stock_code, columns=['종목코드'])
    final_df2 = pd.concat([df1, df2], axis=1) # 열 방향으로 통합

    #코넥스 종목데이터 추출
    stock_list = []
    stock_code = []
    for ticker in stock.get_market_ticker_list(market="KONEX"):
        종목 = stock.get_market_ticker_name(ticker)
        print(종목)
        stock_list.append(종목)
        stock_code.append(ticker)

    df1 = pd.DataFrame(stock_list, columns=['종목명'])
    df2 = pd.DataFrame(stock_code, columns=['종목코드'])
    final_df3 = pd.concat([df1, df2], axis=1) # 열 방향으로 통합


    last_df = pd.concat([final_df1, final_df2, final_df3], axis=0)
    last_df.to_csv('한국 주식 리스트.csv', index=False)

    st.sidebar.write('종목 리스트 최신화를 마쳤습니다.')

def index_new():
    tickers = stock.get_index_ticker_list(market='KRX')
    index_number = []
    index_name = []
    for ticker in tickers:
        index_number.append(ticker)
        index_name.append(stock.get_index_ticker_name(ticker))

    df1 = pd.DataFrame(index_number, columns=['인덱스 티커'])
    df2 = pd.DataFrame(index_name, columns=['인덱스 이름'])
    final_index_df = pd.concat([df1, df2], axis=1)
    final_index_df.to_csv('KRX 인덱스 리스트.csv', index=False)

    st.sidebar.write('인덱스 리스트 최신화를 마쳤습니다.')