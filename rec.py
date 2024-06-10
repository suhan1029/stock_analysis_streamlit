import streamlit as st
import pandas as pd
from pykrx import stock
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday
from time import sleep
from datetime import datetime, timedelta

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
    ]

def recommand(total_index_df, total_df):
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader('인덱스를 기반으로 투자할만한 종목을 추천합니다.')
    st.write('추천 기준은 주관적인 것이므로 결과를 100% 신뢰해서는 안됩니다.')
    st.write('종료 날짜가 주말일 경우, 마지막 영업일로 계산합니다.')
    st.write('KRX 서버 부담을 줄이기 위한 지연시간으로 인해 추천 종목 로딩까지의 시간이 제법 걸립니다.')

    def get_last_business_day(date_str):
        date = pd.to_datetime(date_str)
        while date.weekday() >= 5:
            date -= timedelta(days=1)
        return date.strftime("%Y%m%d")

    def formatted_date(day):
        date_obj = datetime.strptime(day, '%Y%m%d')
        return date_obj.strftime('%Y-%m-%d')

    follow_method = st.sidebar.radio('따라갈 투자자를 선택하시오', ('기관 따라가기', '기타법인 따라가기', '개인 따라가기', '외국인 따라가기'))
    if follow_method == '기관 따라가기':
        follower = '기관합계'
    elif follow_method == '기타법인 따라가기':
        follower = '기타법인'
    elif follow_method == '개인 따라가기':
        follower = '개인'
    elif follow_method == '외국인 따라가기':
        follower = '외국인'

    selected_market = st.sidebar.radio('시장을 선택하시오', ('KOSPI', 'KOSDAQ', 'KONEX'))
    
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    four_years_ago = today - timedelta(days=4*365)

    st.sidebar.write('분석 기간을 선택하시오')
    start_date = st.sidebar.date_input("시작 날짜", value=yesterday - timedelta(days=30), min_value=four_years_ago, max_value=yesterday)
    end_date = st.sidebar.date_input("종료 날짜", value=yesterday, min_value=four_years_ago, max_value=yesterday)

    last_business_day = get_last_business_day(end_date)

    if st.sidebar.button('데이터 조회'):
        with st.spinner('데이터 불러오는 중...'):
            st.markdown(f'##### 조회 기간: {start_date} ~ {formatted_date(last_business_day)}')
            st.markdown(f'###### {selected_market}에서 {follower}의 순매수 상위 종목 25개를 나타낸 데이터프레임(순매수거래대금 기준)')

            df = stock.get_market_net_purchases_of_equities(str(start_date), str(last_business_day), selected_market, follower)
            df = df.sort_values(by='순매수거래대금', ascending=False)
            df25 = df.head(25)

            df25 = df25.merge(total_df, left_on='종목명', right_on='종목명', how='left')

            st.dataframe(df25)

        index_name_count = {}
        progress_bar = st.progress(0)

        # 인덱스 조사
        with st.spinner('인덱스 조사 중...'):
            index_components = {}
            i = 0
            for index_ticker in total_index_df['인덱스 티커']:
                try:
                    pdf = stock.get_index_portfolio_deposit_file(str(index_ticker))
                    sleep(0.1)
                    index_name = total_index_df[total_index_df['인덱스 티커'] == index_ticker]['인덱스 이름'].iloc[0]
                    for component in pdf:
                        if component in index_components:
                            index_components[component].append(index_name)
                        else:
                            index_components[component] = [index_name]
                except Exception as e:
                    st.write(f"Error for index_ticker {index_ticker}: {e}")
                i += 1
                progress = i / len(total_index_df)  # 진행률 계산
                progress_bar.progress(progress)  # 진행률 업데이트


            for check_ticker in df25['종목코드']:
                st.write(f"Checking ticker: {check_ticker} - {df25[df25['종목코드'] == check_ticker]['종목명'].iloc[0]}")
                if check_ticker in index_components:
                    for index_name in index_components[check_ticker]:
                        if index_name in index_name_count:
                            index_name_count[index_name] += 1
                        else:
                            index_name_count[index_name] = 1
                

        index_count_df = pd.DataFrame(list(index_name_count.items()), columns=['인덱스 이름', '종목 수'])
        index_count_df = index_count_df.sort_values(by='종목 수', ascending=False)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('#### 종목이 많이 포함된 인덱스 순위 top5')
        st.write('한 종목이 여러 인덱스에 포함되어있는 경우가 많습니다.')
        st.dataframe(index_count_df.head(5))
            
        st.markdown("<hr>", unsafe_allow_html=True)

        progress_bar = st.progress(0)
        with st.spinner('추천 종목 선정 중...'):
            # 성과 데이터 수집
            def get_stock_performance(stock_code):
                sleep(0.1)
                df = stock.get_market_ohlcv_by_date(str(start_date), str(last_business_day), str(stock_code))
                if not df.empty:
                    start_price = df.iloc[0]['종가']
                    end_price = df.iloc[-1]['종가']
                    return (end_price - start_price) / start_price * 100  # 변동률 계산
                return None

            stock_performance = {}
            i = 0
            j = 0
            total_iterations = len(df25) * 2
            for stock_code in df25['종목코드']:
                performance = get_stock_performance(str(stock_code))
                i += 1
                progress_bar.progress(i / total_iterations)  # 진행률 업데이트

                if performance is not None:
                    stock_performance[stock_code] = performance

            # PER, BPS, PBR 데이터 수집
            def get_fundamental_data(stock_code):
                sleep(0.1)
                try:
                    financial_data = stock.get_market_fundamental_by_date(str(start_date), str(last_business_day), str(stock_code))
                    if not financial_data.empty:
                        per = financial_data['PER'].iloc[-1]
                        bps = financial_data['BPS'].iloc[-1]
                        pbr = financial_data['PBR'].iloc[-1]
                        return per, bps, pbr
                except Exception as e:
                    st.write(f"Error fetching fundamental data for {stock_code}: {e}")
                return None, None, None

            stock_fundamentals = {}
            for stock_code in df25['종목코드']:
                per, bps, pbr = get_fundamental_data(str(stock_code))
                j += 1
                progress_bar.progress((i + j)/ total_iterations)  # 진행률 업데이트

                if per is not None and bps is not None and pbr is not None:
                    stock_fundamentals[stock_code] = {'PER': per, 'BPS': bps, 'PBR': pbr}

            # 종목의 성장 잠재력 평가
            def evaluate_growth_potential(stock_code):
                performance = stock_performance[stock_code]
                fundamentals = stock_fundamentals.get(stock_code, {})
                per = fundamentals.get('PER', float('inf'))
                bps = fundamentals.get('BPS', 0)
                pbr = fundamentals.get('PBR', float('inf'))

                return performance > 5 and per < 15 and bps > 1000 and pbr < 1.5

            # 추천 종목 리스트 작성 및 정렬
            filtered_stocks = [stock_code for stock_code in stock_performance.keys() if evaluate_growth_potential(stock_code)]

            # 상위 4개 종목 선택
            recommended_stocks = sorted(filtered_stocks, key=lambda x: stock_performance[x], reverse=True)[:4]

            st.markdown('#### 추천 종목')
            st.write(f'{start_date} ~ {formatted_date(last_business_day)} 기간동안의 데이터를 바탕으로 추천된 종목은 다음과 같습니다.')
            st.write('추천의 기준은 분석 기간동안 종가기준 상승률 5% 초과, PER 15 미만, BPS 1000 이상, PBR 1.5 미만입니다.')

            recommended_stocks_df = df25[df25['종목코드'].isin(recommended_stocks)]
            st.dataframe(recommended_stocks_df)
            if len(recommended_stocks_df) == 0:
                st.write('이런! 추천 조건에 맞는 종목이 없습니다! 따라갈 투자자나 시장을 변경하시는 것을 추천드립니다.')
            else:
                st.write('최대 4개까지의 종목을 추천합니다.')
                st.write('다운 받기 버튼을 누르면 분석 결과는 사라집니다.')
                st.download_button(
                    label='csv로 다운 받기',
                    data=recommended_stocks_df.to_csv(index=False).encode('utf-8'),
                    file_name=f'recommanded_stocks_{today}.csv',
                    mime='text/csv'
                )