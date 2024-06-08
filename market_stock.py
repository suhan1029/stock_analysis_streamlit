import streamlit as st
import pandas as pd
from pykrx import stock
from datetime import datetime, timedelta
import plotly.graph_objects as go
from time import sleep

def market(total_df):
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader('시장을 분석합니다.')
    st.write('기간이 아닌 특정한 날짜 선택의 경우 종료 날짜를 기준으로 합니다.')
    st.write('특정한 날짜가 주말일 경우, 마지막 영업일로 계산합니다.')
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

    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.write('분석할 기간을 선택하세요')
    start_date = st.sidebar.date_input("시작 날짜", value=yesterday - timedelta(days=14), min_value=four_years_ago, max_value=yesterday)
    end_date = st.sidebar.date_input("종료 날짜(특정 날짜)", value=yesterday, min_value=four_years_ago, max_value=yesterday)
    
    if st.sidebar.button('데이터 조회'):
        progress_bar = st.progress(0)
        progress_step = 0

        with st.spinner('데이터 불러오는 중...'):
            # 마지막 영업일 찾기
            last_business_day = get_last_business_day(end_date)
            st.sidebar.write('데이터가 조회되었습니다.')
            st.sidebar.write('오른쪽에서 보고싶은 정보를 선택하십시오.')
            with st.expander('전체 종목 시세'):
                tab1, tab2, tab3, tab4 = st.tabs(['KOSPI', 'KOSDAQ', 'KONEX', '전체'])
                with tab1:
                    st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                    st.markdown(f"##### KOSPI 종목 시세 조회")
                    df = stock.get_market_ohlcv(str(last_business_day), market='KOSPI')
                    merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                    merge_df.set_index('종목코드', inplace=True)

                    cols = merge_df.columns.tolist()
                    cols.insert(0, cols.pop(cols.index('종목명')))
                    merge_df = merge_df[cols]

                    st.dataframe(merge_df)
                with tab2:
                    st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                    st.markdown(f"##### KOSDAQ 종목 시세 조회")
                    df = stock.get_market_ohlcv(str(last_business_day), market='KOSDAQ')
                    merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                    merge_df.set_index('종목코드', inplace=True)

                    cols = merge_df.columns.tolist()
                    cols.insert(0, cols.pop(cols.index('종목명')))
                    merge_df = merge_df[cols]
                    
                    st.dataframe(merge_df)
                with tab3:
                    st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                    st.markdown(f"##### KONEX 종목 시세 조회")
                    df = stock.get_market_ohlcv(str(last_business_day), market='KONEX')
                    merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                    merge_df.set_index('종목코드', inplace=True)

                    cols = merge_df.columns.tolist()
                    cols.insert(0, cols.pop(cols.index('종목명')))
                    merge_df = merge_df[cols]
                    
                    st.dataframe(merge_df)
                with tab4:
                    st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                    st.markdown(f"##### 모든 종목 시세 조회")
                    df = stock.get_market_ohlcv(str(last_business_day), market='ALL')
                    merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                    merge_df.set_index('종목코드', inplace=True)

                    cols = merge_df.columns.tolist()
                    cols.insert(0, cols.pop(cols.index('종목명')))
                    merge_df = merge_df[cols]
                    
                    st.dataframe(merge_df)
                progress_step += 1
                progress_bar.progress(progress_step / 8)
            sleep(0.2)

            with st.expander('모든 종목의 가격 변동'):
                tab1, tab2, tab3, tab4 = st.tabs(['KOSPI', 'KOSDAQ', 'KONEX', '전체'])
                with tab1:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### KOSPI 종목들의 가격변동 조회")
                    df = stock.get_market_price_change(str(start_date), str(last_business_day), market='KOSPI')
                    st.dataframe(df)
                with tab2:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### KOSDAQ 종목들의 가격변동 조회")
                    df = stock.get_market_price_change(str(start_date), str(last_business_day), market='KOSDAQ')
                    st.dataframe(df)
                with tab3:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### KONEX 종목들의 가격변동 조회")
                    df = stock.get_market_price_change(str(start_date), str(last_business_day), market='KONEX')
                    st.dataframe(df)
                with tab4:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### 모든 종목들의 가격변동 조회")
                    df = stock.get_market_price_change(str(start_date), str(last_business_day), market='ALL')
                    st.dataframe(df)
                
                progress_step += 1
                progress_bar.progress(progress_step / 8)
            sleep(0.2)

            with st.expander('각 시장의 일자별 거래량, 거래대금'):
                st.write('양수면 매수, 음수면 매도입니다.')
                tab1, tab2, tab3, tab4 = st.tabs(['KOSPI', 'KOSDAQ', 'KONEX', '전체'])
                with tab1:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### KOSPI 일자별 거래량")
                    df = stock.get_market_trading_volume_by_date(str(start_date), str(last_business_day), 'KOSPI')
                    df2 = stock.get_market_trading_value_by_date(str(start_date), str(last_business_day), 'KOSPI')
                    df.index = df.index.date
                    df = df.loc[::-1] 
                    df2.index = df2.index.date 
                    df2 = df2.loc[::-1]  
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df.index, y=df['기관합계'], name='기관합계'))
                    fig.add_trace(go.Bar(x=df.index, y=df['기타법인'], name='기타법인'))
                    fig.add_trace(go.Bar(x=df.index, y=df['개인'], name='개인'))
                    fig.add_trace(go.Bar(x=df.index, y=df['외국인합계'], name='외국인합계'))
                    fig.update_layout(
                        xaxis_title='날짜',
                        yaxis_title='수량',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig)
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(f"##### KOSPI 일자별 거래대금")
                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['기관합계'], name='기관합계'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['기타법인'], name='기타법인'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['개인'], name='개인'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['외국인합계'], name='외국인합계'))
                    fig2.update_layout(
                        xaxis_title='날짜',
                        yaxis_title='금액',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig2)
                with tab2:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### KOSDAQ 일자별 거래량")
                    df = stock.get_market_trading_volume_by_date(str(start_date), str(last_business_day), 'KOSDAQ')
                    df2 = stock.get_market_trading_value_by_date(str(start_date), str(last_business_day), 'KOSDAQ')
                    df.index = df.index.date
                    df = df.loc[::-1] 
                    df2.index = df2.index.date 
                    df2 = df2.loc[::-1]
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df.index, y=df['기관합계'], name='기관합계'))
                    fig.add_trace(go.Bar(x=df.index, y=df['기타법인'], name='기타법인'))
                    fig.add_trace(go.Bar(x=df.index, y=df['개인'], name='개인'))
                    fig.add_trace(go.Bar(x=df.index, y=df['외국인합계'], name='외국인합계'))
                    fig.update_layout(
                        xaxis_title='날짜',
                        yaxis_title='수량',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig)
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(f"##### KOSDAQ 일자별 거래대금")
                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['기관합계'], name='기관합계'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['기타법인'], name='기타법인'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['개인'], name='개인'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['외국인합계'], name='외국인합계'))
                    fig2.update_layout(
                        xaxis_title='날짜',
                        yaxis_title='금액',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig2)
                with tab3:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### KONEX 일자별 거래량")
                    df = stock.get_market_trading_volume_by_date(str(start_date), str(last_business_day), 'KONEX')
                    df2 = stock.get_market_trading_value_by_date(str(start_date), str(last_business_day), 'KONEX')
                    df.index = df.index.date
                    df = df.loc[::-1] 
                    df2.index = df2.index.date 
                    df2 = df2.loc[::-1]
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df.index, y=df['기관합계'], name='기관합계'))
                    fig.add_trace(go.Bar(x=df.index, y=df['기타법인'], name='기타법인'))
                    fig.add_trace(go.Bar(x=df.index, y=df['개인'], name='개인'))
                    fig.add_trace(go.Bar(x=df.index, y=df['외국인합계'], name='외국인합계'))
                    fig.update_layout(
                        xaxis_title='날짜',
                        yaxis_title='수량',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig)
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(f"##### KONEX 일자별 거래대금")
                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['기관합계'], name='기관합계'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['기타법인'], name='기타법인'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['개인'], name='개인'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['외국인합계'], name='외국인합계'))
                    fig2.update_layout(
                        xaxis_title='날짜',
                        yaxis_title='금액',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig2)
                with tab4:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### 모든 종목들의 일자별 거래량")
                    df = stock.get_market_trading_volume_by_date(str(start_date), str(last_business_day), 'ALL')
                    df2 = stock.get_market_trading_value_by_date(str(start_date), str(last_business_day), 'ALL')
                    df.index = df.index.date
                    df = df.loc[::-1] 
                    df2.index = df2.index.date 
                    df2 = df2.loc[::-1]
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df.index, y=df['기관합계'], name='기관합계'))
                    fig.add_trace(go.Bar(x=df.index, y=df['기타법인'], name='기타법인'))
                    fig.add_trace(go.Bar(x=df.index, y=df['개인'], name='개인'))
                    fig.add_trace(go.Bar(x=df.index, y=df['외국인합계'], name='외국인합계'))
                    fig.update_layout(
                        xaxis_title='날짜',
                        yaxis_title='수량',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig)
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(f"##### 모든 종목들의 일자별 거래대금")
                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['기관합계'], name='기관합계'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['기타법인'], name='기타법인'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['개인'], name='개인'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['외국인합계'], name='외국인합계'))
                    fig2.update_layout(
                        xaxis_title='날짜',
                        yaxis_title='금액',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig2)
                progress_step += 1
                progress_bar.progress(progress_step / 8)
            sleep(0.2)

            with st.expander('각 시장의 투자자별 거래량, 거래대금'):
                tab1, tab2, tab3, tab4 = st.tabs(['KOSPI', 'KOSDAQ', 'KONEX', '전체'])
                with tab1:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### KOSPI 투자자별 거래량")
                    df = stock.get_market_trading_volume_by_investor(str(start_date), str(last_business_day), 'KOSPI')
                    df2 = stock.get_market_trading_value_by_investor(str(start_date), str(last_business_day), 'KOSPI')
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df.index, y=df['매도'], name='매도'))
                    fig.add_trace(go.Bar(x=df.index, y=df['매수'], name='매수'))
                    fig.add_trace(go.Bar(x=df.index, y=df['순매수'], name='순매수'))
                    fig.update_layout(
                        xaxis_title='투자자구분',
                            yaxis_title='수량',
                            barmode='group',
                            xaxis={'categoryorder':'total descending'}
                    )

                    st.plotly_chart(fig)
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(f"##### KOSPI 투자자별 거래대금")
                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['매도'], name='매도'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['매수'], name='매수'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['순매수'], name='순매수'))
                    fig2.update_layout(
                        xaxis_title='투자자구분',
                        yaxis_title='금액',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig2)
                with tab2:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### KOSDAQ 투자자별 거래량")
                    df = stock.get_market_trading_volume_by_investor(str(start_date), str(last_business_day), 'KOSDAQ')
                    df2 = stock.get_market_trading_value_by_investor(str(start_date), str(last_business_day), 'KOSDAQ')
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df.index, y=df['매도'], name='매도'))
                    fig.add_trace(go.Bar(x=df.index, y=df['매수'], name='매수'))
                    fig.add_trace(go.Bar(x=df.index, y=df['순매수'], name='순매수'))
                    fig.update_layout(
                        xaxis_title='투자자구분',
                        yaxis_title='수량',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig)
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(f"##### KOSDAQ 투자자별 거래대금")
                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['매도'], name='매도'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['매수'], name='매수'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['순매수'], name='순매수'))
                    fig2.update_layout(
                        xaxis_title='투자자구분',
                        yaxis_title='금액',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig2)

                with tab3:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### KONEX 투자자별 거래량, 거래대금")
                    df = stock.get_market_trading_volume_by_investor(str(start_date), str(last_business_day), 'KONEX')
                    df2 = stock.get_market_trading_value_by_investor(str(start_date), str(last_business_day), 'KONEX')
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df.index, y=df['매도'], name='매도'))
                    fig.add_trace(go.Bar(x=df.index, y=df['매수'], name='매수'))
                    fig.add_trace(go.Bar(x=df.index, y=df['순매수'], name='순매수'))
                    fig.update_layout(
                        xaxis_title='투자자구분',
                        yaxis_title='수량',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig)
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(f"##### KONEX 투자자별 거래대금")
                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['매도'], name='매도'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['매수'], name='매수'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['순매수'], name='순매수'))
                    fig2.update_layout(
                        xaxis_title='투자자구분',
                        yaxis_title='금액',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig2)
                with tab4:
                    st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                    st.markdown(f"##### 모든 종목에 대한 투자자별 거래량")
                    df = stock.get_market_trading_volume_by_investor(str(start_date), str(last_business_day), 'ALL')
                    df2 = stock.get_market_trading_value_by_investor(str(start_date), str(last_business_day), 'ALL')
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df.index, y=df['매도'], name='매도'))
                    fig.add_trace(go.Bar(x=df.index, y=df['매수'], name='매수'))
                    fig.add_trace(go.Bar(x=df.index, y=df['순매수'], name='순매수'))
                    fig.update_layout(
                        xaxis_title='투자자구분',
                        yaxis_title='수량',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig)
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown(f"##### 모든 종목에 대한 투자자별 거래대금")
                    fig2 = go.Figure()
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['매도'], name='매도'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['매수'], name='매수'))
                    fig2.add_trace(go.Bar(x=df2.index, y=df2['순매수'], name='순매수'))
                    fig2.update_layout(
                        xaxis_title='투자자구분',
                        yaxis_title='금액',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )
                    st.plotly_chart(fig2)
                progress_step += 1
                progress_bar.progress(progress_step / 8)
            sleep(0.2)

            with st.expander('투자자별 순매수 상위종목 50개'):
                tab1, tab2, tab3 = st.tabs(['KOSPI', 'KOSDAQ', 'KONEX'])
                with tab1:
                    tab11, tab22, tab33, tab44 = st.tabs(['기관합계', '기타법인', '개인', '외국인'])
                    with tab11:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KOSPI에서 기관의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KOSPI", "기관합계")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                    with tab22:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KOSPI에서 기타법인의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KOSPI", "기타법인")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                    with tab33:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KOSPI에서 개인의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KOSPI", "개인")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                    with tab44:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KOSPI에서 외국인의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KOSPI", "외국인")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)

                with tab2:
                    tab11, tab22, tab33, tab44 = st.tabs(['기관합계', '기타법인', '개인', '외국인'])
                    with tab11:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KOSDAQ에서 기관의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KOSDAQ", "기관합계")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                    with tab22:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KOSDAQ에서 기타법인의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KOSDAQ", "기타법인")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                    with tab33:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KOSDAQ에서 개인의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KOSDAQ", "개인")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                    with tab44:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KOSDAQ에서 외국인의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KOSDAQ", "외국인")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                with tab3:
                    tab11, tab22, tab33, tab44 = st.tabs(['기관합계', '기타법인', '개인', '외국인'])
                    with tab11:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KONEX에서 기관의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KONEX", "기관합계")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                    with tab22:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KONEX에서 기타법인의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KONEX", "기타법인")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                    with tab33:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KONEX에서 개인의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KONEX", "개인")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                    with tab44:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"###### KONEX에서 외국인의 순매수 상위 종목 50개")
                        df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), "KONEX", "외국인")
                        df = df.sort_values(by='순매수거래량', ascending=False)
                        df50 = df.head(50)
                        st.dataframe(df50)
                progress_step += 1
                progress_bar.progress(progress_step / 8)
            sleep(0.2)

            with st.expander('종목별 시가 총액'):
                st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                st.markdown(f"##### 종목별 시가 총액")
                df = stock.get_market_cap(formatted_date(last_business_day))
                merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                merge_df.set_index('종목코드', inplace=True)

                cols = merge_df.columns.tolist()
                cols.insert(0, cols.pop(cols.index('종목명')))
                merge_df = merge_df[cols]

                st.dataframe(merge_df)

                progress_step += 1
                progress_bar.progress(progress_step / 8)
            sleep(0.2)

            with st.expander('티커별 외국인 보유량 및 외국인 한도소진률'):
                tab1, tab2, tab3 = st.tabs(['KOSPI', 'KOSDAQ', 'KONEX'])
                with tab1:
                    st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                    df = stock.get_exhaustion_rates_of_foreign_investment(formatted_date(last_business_day), "KOSPI")
                    merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                    merge_df.set_index('종목코드', inplace=True)

                    cols = merge_df.columns.tolist()
                    cols.insert(0, cols.pop(cols.index('종목명')))
                    merge_df = merge_df[cols]

                    st.dataframe(merge_df)
                with tab2:
                    st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                    df = stock.get_exhaustion_rates_of_foreign_investment(formatted_date(last_business_day), "KOSDAQ")
                    merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                    merge_df.set_index('종목코드', inplace=True)

                    cols = merge_df.columns.tolist()
                    cols.insert(0, cols.pop(cols.index('종목명')))
                    merge_df = merge_df[cols]

                    st.dataframe(merge_df)
                with tab3:
                    st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                    df = stock.get_exhaustion_rates_of_foreign_investment(formatted_date(last_business_day), "KONEX")
                    merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                    merge_df.set_index('종목코드', inplace=True)

                    cols = merge_df.columns.tolist()
                    cols.insert(0, cols.pop(cols.index('종목명')))
                    merge_df = merge_df[cols]

                    st.dataframe(merge_df)
                progress_step += 1
                progress_bar.progress(progress_step / 8)
            sleep(0.2)

            with st.expander('공매도 정보'):
                tab1, tab2, tab3 = st.tabs(['시장별 공매도 거래 정보', '투자자별 공매도 거래량, 거래대금', '공매도 거래비중 상위 50개 종목'])
                with tab1:
                    tab11, tab22 = st.tabs(['KOSPI', 'KOSDAQ'])
                    with tab11:
                        st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                        st.markdown(f"##### KOSPI 공매도 거래 정보")
                        df = stock.get_shorting_volume_by_ticker(formatted_date(last_business_day), "KOSPI")
                        merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                        merge_df.set_index('종목코드', inplace=True)

                        cols = merge_df.columns.tolist()
                        cols.insert(0, cols.pop(cols.index('종목명')))
                        merge_df = merge_df[cols]

                        st.dataframe(merge_df)
                    with tab22:
                        st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                        st.markdown(f"##### KOSDAQ 공매도 거래 정보")
                        df = stock.get_shorting_volume_by_ticker(formatted_date(last_business_day), "KOSDAQ")
                        merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                        merge_df.set_index('종목코드', inplace=True)
    
                        cols = merge_df.columns.tolist()
                        cols.insert(0, cols.pop(cols.index('종목명')))
                        merge_df = merge_df[cols]
    
                        st.dataframe(merge_df)

                with tab2:
                    tab11, tab22 = st.tabs(['KOSPI', 'KOSDAQ'])
                    with tab11:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"##### 투자자별 KOSPI 공매도 거래량")
                        df = stock.get_shorting_investor_volume_by_date(str(start_date), formatted_date(last_business_day), "KOSPI")
                        df2 = stock.get_shorting_investor_value_by_date(str(start_date), formatted_date(last_business_day), "KOSPI")
                        df.index = df.index.date
                        df = df.loc[::-1] 
                        df2.index = df2.index.date 
                        df2 = df2.loc[::-1]

                        fig = go.Figure()
                        fig.add_trace(go.Bar(x=df.index, y=df['기관'], name='기관'))
                        fig.add_trace(go.Bar(x=df.index, y=df['개인'], name='개인'))
                        fig.add_trace(go.Bar(x=df.index, y=df['외국인'], name='외국인'))
                        fig.add_trace(go.Bar(x=df.index, y=df['기타'], name='기타'))
                        fig.add_trace(go.Bar(x=df.index, y=df['합계'], name='합계'))
                        fig.update_layout(
                            xaxis_title='날짜',
                            yaxis_title='수량',
                            barmode='group',
                            xaxis={'categoryorder':'total descending'}
                        )
                        st.plotly_chart(fig)

                        st.markdown("<hr>", unsafe_allow_html=True)
                        st.markdown(f"##### 투자자별 KOSPI 공매도 거래대금")
                        fig2 = go.Figure()
                        fig2.add_trace(go.Bar(x=df2.index, y=df2['기관'], name='기관'))
                        fig2.add_trace(go.Bar(x=df2.index, y=df2['개인'], name='개인'))
                        fig2.add_trace(go.Bar(x=df2.index, y=df2['외국인'], name='외국인'))
                        fig2.add_trace(go.Bar(x=df2.index, y=df2['기타'], name='기타'))
                        fig2.add_trace(go.Bar(x=df2.index, y=df2['합계'], name='합계'))
                        fig2.update_layout(
                            xaxis_title='날짜',
                            yaxis_title='금액',
                            barmode='group',
                            xaxis={'categoryorder':'total descending'}
                        )
                        st.plotly_chart(fig2)
                    with tab22:
                        st.write(f'조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
                        st.markdown(f"##### 투자자별 KOSDAQ 공매도 거래량")
                        df = stock.get_shorting_investor_volume_by_date(str(start_date), formatted_date(last_business_day), "KOSDAQ")
                        df2 = stock.get_shorting_investor_value_by_date(str(start_date), formatted_date(last_business_day), "KOSDAQ")
                        df.index = df.index.date
                        df = df.loc[::-1] 
                        df2.index = df2.index.date 
                        df2 = df2.loc[::-1]

                        fig = go.Figure()
                        fig.add_trace(go.Bar(x=df.index, y=df['기관'], name='기관'))
                        fig.add_trace(go.Bar(x=df.index, y=df['개인'], name='개인'))
                        fig.add_trace(go.Bar(x=df.index, y=df['외국인'], name='외국인'))
                        fig.add_trace(go.Bar(x=df.index, y=df['기타'], name='기타'))
                        fig.add_trace(go.Bar(x=df.index, y=df['합계'], name='합계'))
                        fig.update_layout(
                            xaxis_title='날짜',
                            yaxis_title='수량',
                            barmode='group',
                            xaxis={'categoryorder':'total descending'}
                        )
                        st.plotly_chart(fig)

                        st.markdown("<hr>", unsafe_allow_html=True)
                        st.markdown(f"##### 투자자별 KOSDAQ 공매도 거래대금")
                        fig2 = go.Figure()
                        fig2.add_trace(go.Bar(x=df2.index, y=df2['기관'], name='기관'))
                        fig2.add_trace(go.Bar(x=df2.index, y=df2['개인'], name='개인'))
                        fig2.add_trace(go.Bar(x=df2.index, y=df2['외국인'], name='외국인'))
                        fig2.add_trace(go.Bar(x=df2.index, y=df2['기타'], name='기타'))
                        fig2.add_trace(go.Bar(x=df2.index, y=df2['합계'], name='합계'))
                        fig2.update_layout(
                            xaxis_title='날짜',
                            yaxis_title='금액',
                            barmode='group',
                            xaxis={'categoryorder':'total descending'}
                        )
                        st.plotly_chart(fig2)

                with tab3:
                    tab11, tab22 = st.tabs(['KOSPI', 'KOSDAQ'])
                    with tab11:
                        st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                        st.markdown(f"##### KOSPI 공매도 거래비중 상위 50개")
                        df = stock.get_shorting_volume_top50(formatted_date(last_business_day), "KOSPI")
                        merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                        merge_df.set_index('종목코드', inplace=True)

                        cols = merge_df.columns.tolist()
                        cols.insert(0, cols.pop(cols.index('종목명')))
                        merge_df = merge_df[cols]

                        st.dataframe(merge_df)

                    with tab22:
                        st.write(f'조회 날짜: {formatted_date(last_business_day)}')
                        st.markdown(f"##### KOSDAQ 공매도 거래비중 상위 50개")
                        df = stock.get_shorting_volume_top50(formatted_date(last_business_day), "KOSDAQ")
                        merge_df = df.merge(total_df[['종목코드', '종목명']], left_on='티커', right_on='종목코드')
                        merge_df.set_index('종목코드', inplace=True)

                        cols = merge_df.columns.tolist()
                        cols.insert(0, cols.pop(cols.index('종목명')))
                        merge_df = merge_df[cols]

                        st.dataframe(merge_df)
                progress_step += 1
                progress_bar.progress(progress_step / 8)