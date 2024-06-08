from time import sleep
import streamlit as st
import pandas as pd
from pykrx import stock
from pykrx import bond
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def in_stock(total_df, total_index_df):
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader('인덱스를 분석합니다.')
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.write('기간이 아닌 특정한 날짜 선택의 경우 종료 날짜를 기준으로 합니다.')
    st.write('특정한 날짜가 주말일 경우, 마지막 영업일로 계산합니다.')
    st.write('특정 인덱스를 분석할때는 KRX 인덱스를 기준으로 합니다.')

    def get_last_business_day(date_str):
        # 주어진 날짜를 datetime 객체로 변환
        date = pd.to_datetime(date_str)
    
        # 주어진 날짜가 주말(토요일=5, 일요일=6)인 경우 마지막 영업일 찾기
        while date.weekday() >= 5:
            date -= timedelta(days=1)
        return date.strftime("%Y%m%d")
    
    def formatted_date(day): # 날짜 형식으로 변환
        date_obj = datetime.strptime(day, '%Y%m%d')
        formatted_date = date_obj.strftime('%Y-%m-%d')

        return formatted_date

    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    four_years_ago = today - timedelta(days=4*365)

    st.sidebar.write('분석할 기간, 인덱스를 선택하시오')
    start_date = st.sidebar.date_input("시작 날짜", value=yesterday - timedelta(days=14), min_value=four_years_ago, max_value=yesterday)
    end_date = st.sidebar.date_input("종료 날짜(특정 날짜)", value=yesterday, min_value=four_years_ago, max_value=yesterday)

    selected_index = st.sidebar.selectbox('KRX 인덱스', total_index_df['인덱스 이름'])
    if selected_index:
        selected_index_ticker = total_index_df[total_index_df['인덱스 이름'] == selected_index]['인덱스 티커'].iloc[0]
        spdf = stock.get_index_portfolio_deposit_file(str(selected_index_ticker))
        
    with st.expander('인덱스 종류'):
        tab1, tab2, tab3 = st.tabs(['KOSPI', 'KOSDAQ', 'KRX'])
        with tab1:
            for ticker in stock.get_index_ticker_list(market='KOSPI'):
                st.write(ticker, stock.get_index_ticker_name(ticker))
        with tab2:
            for ticker in stock.get_index_ticker_list(market='KOSDAQ'):
                st.write(ticker, stock.get_index_ticker_name(ticker))
        with tab3:
            for ticker in stock.get_index_ticker_list(market='KRX'):
                st.write(ticker, stock.get_index_ticker_name(ticker))

    sleep(0.2)
    with st.expander('인덱스 상장 정보'):
        tab1, tab2, tab3 = st.tabs(['KOSPI', 'KOSDAQ', 'KRX'])
        with tab1:
            df = stock.get_index_listing_date("KOSPI")
            st.markdown(f"##### KOSPI 각 인덱스별 상장일 및 기준비수 정보")
            st.dataframe(df)
        with tab2:
            df = stock.get_index_listing_date("KOSDAQ")
            st.markdown(f"##### KOSDAQ 각 인덱스별 상장일 및 기준비수 정보")
            st.dataframe(df)
        with tab3:
            df = stock.get_index_listing_date("KRX")
            st.markdown(f"##### KRX 각 인덱스별 상장일 및 기준비수 정보")
            st.dataframe(df)

    if st.sidebar.button('데이터 조회'):
        progress_bar = st.progress(0)
        progress_step = 0

        st.markdown("<hr>", unsafe_allow_html=True)
        with st.spinner('데이터 불러오는 중...'):
            with st.expander(f'{selected_index}에 포함되어있는 종목'):
                st.write(f'{selected_index} 인덱스에는 총 {len(spdf)}개의 종목이 있습니다.')
                df = pd.DataFrame(spdf, columns=['종목코드'])
                merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='종목코드', right_on='종목코드')

                cols = merge_df.columns.tolist()
                cols.insert(0, cols.pop(cols.index('종목명')))
                merge_df = merge_df[cols]

                st.dataframe(merge_df)
                progress_step += 1
                progress_bar.progress(progress_step / 3)

            # 마지막 영업일 찾기
            last_business_day = get_last_business_day(end_date)
            st.sidebar.write('데이터가 조회되었습니다.')
            st.sidebar.write('오른쪽에서 보고싶은 정보를 선택하십시오.')
        
            sleep(0.2)
            with st.expander(f'{selected_index} 인덱스 OHLCV'):
                st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                df = stock.get_index_ohlcv(str(start_date), formatted_date(last_business_day), str(selected_index_ticker))
                df.index = df.index.date 
                df = df.loc[::-1]
                df = df.dropna()

                fig = go.Figure()
                fig.add_trace(go.Bar(x=df.index, y=df['거래량'], name='거래량', yaxis='y2'))
                fig.add_trace(go.Scatter(x=df.index, y=df['시가'], mode='lines+markers', name='시가'))
                fig.add_trace(go.Scatter(x=df.index, y=df['고가'], mode='lines+markers', name='고가'))
                fig.add_trace(go.Scatter(x=df.index, y=df['저가'], mode='lines+markers', name='저가'))
                fig.add_trace(go.Scatter(x=df.index, y=df['종가'], mode='lines+markers', name='종가'))
                fig.add_trace(go.Scatter(x=df.index, y=df['고가'] - (df['고가'] - df['저가'])/2, mode='lines+markers', name='중위값'))
                fig.update_layout(
                    title=f'{selected_index}의 OHLCV',
                    xaxis_title='날짜',
                    yaxis_title='지수',
                    yaxis2=dict(
                        title='거래량',
                        overlaying='y',
                        side='right',
                        range=[0, df['거래량'].max()*5]
                    ),
                    xaxis=dict(tickmode='linear'),
                    template='plotly_white'
                )
                st.plotly_chart(fig)
                progress_step += 1
                progress_bar.progress(progress_step / 3)

            sleep(0.2)
            
            with st.expander('인덱스 등락률'):
                tab1, tab2, tab3 = st.tabs(['KOSPI', 'KOSDAQ', 'KRX'])
                with tab1:
                    st.markdown(f"##### KOSPI 각 인덱스별 등락률")
                    df = stock.get_index_price_change(str(start_date), formatted_date(last_business_day), "KOSPI")
                    st.dataframe(df)
                with tab2:
                    st.markdown(f"##### KOSDAQ 각 인덱스별 등락률")
                    df = stock.get_index_price_change(str(start_date), formatted_date(last_business_day), "KOSDAQ")
                    st.dataframe(df)
                with tab3:
                    st.markdown(f"##### KRX 각 인덱스별 등락률")
                    df = stock.get_index_price_change(str(start_date), formatted_date(last_business_day), "KRX")
                    st.dataframe(df)
                progress_step += 1
                progress_bar.progress(progress_step / 3)

            













