import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pykrx import stock
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from prophet import Prophet
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, USFederalHolidayCalendar
from time import sleep

class KRHolidayCalendar(AbstractHolidayCalendar):
    rules = [
    Holiday("New Year's Day", month=1, day=1, observance=nearest_workday),
    Holiday("Independence Movement Day", month=3, day=1, observance=nearest_workday),
    Holiday("Labor Day", month=5, day=1, observance=nearest_workday),
    Holiday("Children's Day", month=5, day=5, observance=nearest_workday),
    Holiday("Memorial Day", month=6, day=6, observance=nearest_workday),
    Holiday("Liberation Day", month=8, day=15, observance=nearest_workday),
    Holiday("National Foundation Day", month=10, day=3, observance=nearest_workday),
    Holiday("Hangul Proclamation Day", month=10, day=9, observance=nearest_workday),
    Holiday("Christmas Day", month=12, day=25, observance=nearest_workday),
    # You can add more holidays as needed
    ]

def one(total_df):
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader('특정 종목을 분석합니다.')
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    # 검색 입력
    search_term = st.sidebar.text_input("종목 검색", "")

    # 검색 결과 필터링
    filtered_stocks = total_df[total_df['종목명'].str.contains(search_term, case=False, na=False)]

    # 종목 선택 위젯
    selected_stock = st.sidebar.selectbox('종목을 선택하시오', filtered_stocks['종목명'])

    if selected_stock:
        selected_stock_code = total_df[total_df['종목명'] == selected_stock]['종목코드'].iloc[0]
        today = datetime.now()

        st.markdown(f'#### {selected_stock} 종목 분석')
        st.write('조회 버튼을 누른 후 보고 싶은 정보를 선택하시면 됩니다.')

        yesterday = today - timedelta(days=1)
        four_years_ago = today - timedelta(days=4*365)

        # 사이드바에 날짜 넣는 것 배치
        start_date = st.sidebar.date_input("시작 날짜", value=yesterday - timedelta(days=30), min_value=four_years_ago, max_value=yesterday)
        end_date = st.sidebar.date_input("종료 날짜", value=yesterday, min_value=four_years_ago, max_value=yesterday)


        if st.sidebar.button('데이터 조회'):
            progress_bar = st.progress(0)
            progress_step = 0

            with st.spinner('데이터 불러오는 중...'):

                st.sidebar.write('데이터가 조회되었습니다.')
                st.sidebar.write('오른쪽에서 보고싶은 정보를 선택하십시오.')

                with st.expander("OHLCV (open, high, low, close, volume)"):
                    st.markdown("##### OHLCV 분석")
                    df = stock.get_market_ohlcv(str(start_date), str(end_date), str(selected_stock_code))
                    df.index = pd.to_datetime(df.index)
                    df.index = df.index.date

                    df = df.loc[::-1]  # 최신 날짜부터 나타내도록 역순하기
                    st.dataframe(df)
                    progress_step += 1
                    progress_bar.progress(progress_step / 10)
                sleep(0.2)

                with st.expander("가격 변동 그래프"):
                    st.markdown("##### 가격 변동 분석")
                    df = stock.get_market_ohlcv(str(start_date), str(end_date), str(selected_stock_code))
                    df.index = df.index.date # 날짜 표시에서 시간은 지우기
                    df = df.dropna()

                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df.index, y=df['거래량'], name='거래량', yaxis='y2'))
                    fig.add_trace(go.Scatter(x=df.index, y=df['시가'], mode='lines+markers', name='시가'))
                    fig.add_trace(go.Scatter(x=df.index, y=df['고가'], mode='lines+markers', name='고가'))
                    fig.add_trace(go.Scatter(x=df.index, y=df['저가'], mode='lines+markers', name='저가'))
                    fig.add_trace(go.Scatter(x=df.index, y=df['종가'], mode='lines+markers', name='종가'))
                    fig.add_trace(go.Scatter(x=df.index, y=df['고가'] - (df['고가'] - df['저가'])/2, mode='lines+markers', name='중위값'))

                    fig.update_layout(
                        title=f'{selected_stock}의 가격 변동 그래프',
                        xaxis_title='날짜',
                        yaxis_title='가격',
                        yaxis2=dict(
                            title='거래량',
                            overlaying='y',
                            side='right',
                            range=[0, df['거래량'].max()*5]
                        ),
                        xaxis=dict(tickmode='linear'),
                        template='plotly_white'
                    )

                    # Streamlit에 그래프 표시
                    st.plotly_chart(fig)
                    progress_step += 1
                    progress_bar.progress(progress_step / 10)
                sleep(0.2)

                with st.expander("일자별 BPS, PER, PBR, EPS, DIV, DPS"):
                    st.markdown(f"##### {selected_stock}의 일자별 BPS, PER, PBR, EPS, DIV, DPS")
                    df = stock.get_market_fundamental(str(start_date), str(end_date), str(selected_stock_code))
                    st.dataframe(df)
                    df.index = pd.to_datetime(df.index)
                    
                    df = df.dropna()
                    df = df.loc[::-1]  # 최신 날짜부터 나타내도록 역순하기
                    st.dataframe(df)

                    st.markdown("<hr>", unsafe_allow_html=True)

                    fig = make_subplots(rows=2, cols=3, shared_xaxes=True,
                                        subplot_titles=('BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS'),
                                        horizontal_spacing=0.15)
                    fig.add_trace(go.Scatter(x=df.index, y=df['BPS'], mode='lines+markers', name='BPS'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=df['PER'], mode='lines+markers', name='PER'), row=1, col=2)
                    fig.add_trace(go.Scatter(x=df.index, y=df['PBR'], mode='lines+markers', name='PBR'), row=1, col=3)
                    fig.add_trace(go.Scatter(x=df.index, y=df['EPS'], mode='lines+markers', name='EPS'), row=2, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=df['DIV'], mode='lines+markers', name='DIV'), row=2, col=2)
                    fig.add_trace(go.Scatter(x=df.index, y=df['DPS'], mode='lines+markers', name='DPS'), row=2, col=3)

                    fig.update_layout(xaxis=dict(tickmode='linear'),template='plotly_white')

                    # Streamlit에 그래프 표시
                    st.plotly_chart(fig)
                    progress_step += 1
                    progress_bar.progress(progress_step / 10)
                sleep(0.2)

                with st.expander("일자별 거래실적 추이"):
                    st.markdown(f"##### {selected_stock}의 일자별 거래량 추이")
                    st.write('거래량이 양수면 매수, 음수면 매도입니다.')
                    df = stock.get_market_trading_volume_by_date(str(start_date), str(end_date), str(selected_stock_code))
                    df.index = df.index.date # 날짜 표시에서 시간은 지우기
                    df = df.dropna()
                    df = df.loc[::-1]  # 최신 날짜부터 나타내도록 역순하기

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df.index, y=df['기관합계'], mode='lines+markers', name='기관합계'))
                    fig.add_trace(go.Scatter(x=df.index, y=df['기타법인'], mode='lines+markers', name='기타법인'))
                    fig.add_trace(go.Scatter(x=df.index, y=df['개인'], mode='lines+markers', name='개인'))
                    fig.add_trace(go.Scatter(x=df.index, y=df['외국인합계'], mode='lines+markers', name='외국인합계'))

                    fig.update_layout(
                        xaxis_title='날짜',
                        yaxis_title='거래량',
                        legend_title='투자자 종류',
                        xaxis=dict(tickmode='linear'),
                        template='plotly_white'
                    )

                    # Streamlit에 그래프 표시
                    st.plotly_chart(fig)
                    progress_step += 1
                    progress_bar.progress(progress_step / 10)
                sleep(0.2)

                with st.expander("투자자별 거래실적 추이"):
                    st.markdown(f"##### {start_date}부터 {end_date}까지의 투자자별 거래량 추이")
                    df = stock.get_market_trading_volume_by_investor(str(start_date), str(end_date), str(selected_stock_code))
                    df = df.dropna()

                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=df.index, y=df['매도'], name='매도'))
                    fig.add_trace(go.Bar(x=df.index, y=df['매수'], name='매수'))
                    fig.add_trace(go.Bar(x=df.index, y=df['순매수'], name='순매수'))

                    fig.update_layout(
                        xaxis_title='투자자 구분',
                        yaxis_title='수량',
                        barmode='group',
                        xaxis={'categoryorder':'total descending'}
                    )

                    st.plotly_chart(fig)
                    progress_step += 1
                    progress_bar.progress(progress_step / 10)
                sleep(0.2)

                with st.expander("일자별 시가 총액"):
                    st.markdown(f"##### {selected_stock}의 일자별 시가 총액")
                    df = stock.get_market_cap(str(start_date), str(end_date), str(selected_stock_code))
                    df.index = df.index.date # 날짜 표시에서 시간은 지우기
                    df = df.dropna()
                    df = df.loc[::-1]  # 최신 날짜부터 나타내도록 역순하기

                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=df.index, y=df['시가총액'], mode='lines+markers', name='시가총액'))
                    fig.update_layout(
                        xaxis_title='날짜',
                        yaxis_title='시가총액',
                        xaxis=dict(tickmode='linear'),
                        template='plotly_white'
                    )
                    st.plotly_chart(fig)
                    progress_step += 1
                    progress_bar.progress(progress_step / 10)
                sleep(0.2)

                with st.expander("일자별 외국인 보유량 및 외국인 한도소진률"):
                    st.markdown("##### 일자별 외국인 보유량 및 외국인 한도소진률")
                    df = stock.get_exhaustion_rates_of_foreign_investment(str(start_date), str(end_date), str(selected_stock_code))
                    df.index = df.index.date # 날짜 표시에서 시간은 지우기
                    df = df.dropna()
                    df = df.loc[::-1]  # 최신 날짜부터 나타내도록 역순하기
                    st.dataframe(df)
                    progress_step += 1
                    progress_bar.progress(progress_step / 10)
                sleep(0.2)

                with st.expander("공매도 상황"):
                    st.markdown(f"##### {selected_stock}의 공매도 상황")
                    df = stock.get_shorting_status_by_date(str(start_date), str(end_date), str(selected_stock_code))
                    df.index = df.index.date # 날짜 표시에서 시간은 지우기
                    df = df.loc[::-1]  # 최신 날짜부터 나타내도록 역순하기
                    st.dataframe(df)
                    progress_step += 1
                    progress_bar.progress(progress_step / 10)
                sleep(0.2)

                with st.expander("기업의 주요 변동사항"):
                    st.markdown(f"##### {selected_stock} 기업의 주요 변동사항")
                    st.write('이 항목은 선택한 날짜가 아닌 전체 기간을 고려합니다.')
                    df = stock.get_stock_major_changes(str(selected_stock_code))
                    df.index = df.index.date # 날짜 표시에서 시간은 지우기
                    df = df.loc[::-1]  # 최신 날짜부터 나타내도록 역순하기
                    st.dataframe(df)
                    progress_step += 1
                    progress_bar.progress(progress_step / 10)
                sleep(0.2)

                with st.expander("단순 미래 주가 예측"):
                    st.markdown(f"##### {selected_stock} 종목 단순 미래 주가 예측")
                    st.write('입력한 기간의 1/3까지만 예측합니다.')
                    df = stock.get_market_ohlcv(str(start_date), str(end_date), str(selected_stock_code))
                    df.index = pd.to_datetime(df.index).date # 시간제거
                    df = df.loc[::-1]  # 최신 날짜부터 나타내도록 역순하기
                    df['y'] = df['고가'] - (df['고가'] - df['저가'])/2
                    df = df.dropna()
                    df.index.name = 'ds'

                    bdates = pd.bdate_range(start=start_date, end=end_date, freq='C', holidays=KRHolidayCalendar().holidays()).date
                    df = df[df.index.isin(bdates)]

                    df2 = df.reset_index()[['ds', 'y']]
                
                    model = Prophet()
                    model.fit(df2)

                    future_periods = (end_date - start_date).days // 3
                    future = model.make_future_dataframe(periods=future_periods)

                    future = future[future['ds'].dt.dayofweek < 5] # 주말 제거

                    # 공휴일 제거
                    holidays = KRHolidayCalendar().holidays(start=future['ds'].min(), end=future['ds'].max())
                    future = future[~future['ds'].isin(holidays)]

                    forecast = model.predict(future)

                    fig = go.Figure()

                    # 실제 데이터
                    fig.add_trace(go.Scatter(x=df2['ds'], y=df2['y'], mode='lines+markers', name='실제 가격'))

                    # 예측 데이터
                    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines+markers', name='예측 가격'))

                    fig.add_trace(go.Scatter(
                        x=forecast['ds'], y=forecast['yhat_upper'],
                        mode='lines', name='상위 신뢰구간',
                        line=dict(width=0),
                        showlegend=False
                    ))
                    fig.add_trace(go.Scatter(
                        x=forecast['ds'], y=forecast['yhat_lower'],
                        mode='lines', name='하위 신뢰구간',
                        line=dict(width=0),
                        fill='tonexty',
                        fillcolor='rgba(157, 220, 235, 0.3)',
                        showlegend=False
                    ))

                    fig.update_layout(
                        title=f'{selected_stock}의 미래 가격 예측',
                        xaxis_title='날짜',
                        yaxis_title='가격',
                        template='plotly_white'
                    )

                    # Display the plot in Streamlit
                    st.plotly_chart(fig)
                    progress_step += 1
                    progress_bar.progress(progress_step / 10)

