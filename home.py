import streamlit as st

def home():
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('#### 국내 주식을 분석하는 사이트입니다.')
    st.write('pykrx를 사용하여 증권시장의 주식 정보를 스크래핑합니다.')
    st.write('처음 들어오시거나, 어제 이후 오늘 처음 들어오셨다면 리스트 최신화 버튼을 눌러주시기 바랍니다.')
    st.write('왼쪽 사이드바에서 분석 방법을 선택하면 됩니다.')
    st.write(' - 특정 종목 분석은 말 그대로 특정한 하나의 종목을 분석하는 것입니다.')
    st.write(' - 인덱스 분석은 특정한 인덱스를 분석합니다.')
    st.write(' - 시장 전체 분석은 주식 시장을 전체적으로 분석합니다.')
    st.write(' - 인덱스 기반 종목 추천은 투자자별 순매수 종목 데이터를 기반으로 종목을 추천합니다.')
    st.write('조회하는 날짜 기준 4년 전부터 어제까지의 데이터를 가져올 수 있습니다. 실시간으로는 가져오지 않습니다.')
    st.write('서버에 과도한 부담을 줄 수 없으므로 정보 사이사이에 지연시간을 두었습니다.')
    st.write('ETF, ETN, ELW, 채권은 제외하였습니다.')
    st.markdown('##### ※ 모든 투자의 책임은 본인에게 있습니다.')

    with st.expander('주요 용어 설명'):
        st.markdown('##### 인덱스')
        st.write('특정 분야, 산업 또는 주식 시장의 성과와 가치를 평가하여 나타내는 지표')
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### KOSPI (Korea Composite Stock Price Index, 코스피)')
        st.write('한국거래소(KRX)에서 운영하는 주식시장 중 하나로, 주로 대형 기업들이 상장되어 있음')
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### KOSDAQ (Korean Securities Dealers Automated Quotations, 코스닥)')
        st.write('벤처기업과 중소기업들이 주로 상장된 주식시장')

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### KONEX (Korea New Exchange, 코넥스)')
        st.write('창업 초기 단계의 중소기업을 위한 주식시장')

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### KRX (Korea Exchange, 한국거래소)')
        st.write('한국의 유가증권 시장을 운영하는 통합 거래소, KOSPI, KOSDAQ, KONEX 등의 시장을 통합 운영하는 기관')
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### OHLCV')
        st.write('open, high, low, close, volume을 나타내는 것으로 각각 시가, 고가, 저가, 종가, 거래량을 의미함')
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### BPS (Book Value Per Share, 주당순자산가치)')
        st.write('기업의 자산 가치에서 부채를 뺀 순자산을 발행 주식 수로 나눈 값')
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### PER (Price to Earnings Ratio, 주가수익비율)')
        st.write('주가를 주당순이익(EPS)으로 나눈 값')

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### PBR (Price to Book Ratio, 주가순자산비율)')
        st.write('주가를 주당순자산가치(BPS)로 나눈 값')

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### EPS (Earnings Per Share, 주당순이익)')
        st.write('기업의 순이익을 발행 주식 수로 나눈 값')

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### DIV (Dividend, 배당)')
        st.write('기업이 주주에게 분배하는 이익의 일부분')

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### DPS (Dividend Per Share, 주당배당금)')
        st.write('주식 한 주당 지급되는 배당금의 금액')
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('##### 공매도')
        st.write('주식시장에서 투자자가 주식을 실제로 소유하지 않은 상태에서 주식을 매도하는 행위')
        