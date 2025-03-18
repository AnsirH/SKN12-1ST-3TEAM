import streamlit as st 


def show():
    st.title('Welcome !')
    st.write("""
        이 사이트는 전국차량등록 현황 및 별 비교를 위해 만들어졌습니다. \n
        자료 제공 : 국토교통통계누리 자동차등록현황보고 (Total Registered Motor Vehicles) \n

        자료수집기간: 2024.01. ~ 2025.02.
    """)
    
    # 이미지 추가 (옵션)
    st.image('https://www.molit.go.kr/images/infog/card_230117_01_02.jpg')
    st.write('출처: 국토교통부')

    

