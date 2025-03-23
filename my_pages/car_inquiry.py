import streamlit as st 
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt 
import seaborn as sns
import datetime
from module.data_processing import *
from module.sql_query import search_city_do_gender, get_vehicle_count
import altair as alt
from module import config

# 작성자: 허한결결
# 지역별 차종별 비교
def region_comparsion(year, month):
    try:
        car_type_col, col1, col2 = st.columns(3)
        # 데이터 쿼리 불러오기 
        vehicle_data_list = get_vehicle_count(config.DATABASE_CONFIG, year, month)
        vehicle_data_list.sort(key = lambda x : x['city_do'])

        data = {
            '지역': list(vd['city_do'] for vd in vehicle_data_list),
            '승용': list(map(int, [vd['sedan'] for vd in vehicle_data_list])),
            '승합': list(map(int, [vd['van'] for vd in vehicle_data_list])),
            '화물': list(map(int, [vd['truck'] for vd in vehicle_data_list])),
            '특수': list(map(int, [vd['special'] for vd in vehicle_data_list])),
            '총계': list(map(int, [sum((vd['sedan'], vd['van'], vd['truck'], vd['special'])) for vd in vehicle_data_list]))
        }

        df_data = pd.DataFrame(data)

        # 지역 선택 도시명 만 받아오기 

        with car_type_col:
            car_type = st.selectbox('차 종류를 선택하세요', ['승용', '승합', '화물', '특수', '총계'])
        with col1:
            지역1 = st.selectbox('첫 번째 지역을 선택하세요', df_data['지역'])
        with col2: 
            지역2 = st.selectbox('두 번째 지역을 선택하세요', df_data['지역'])
        

        # 두 지역 선택된 데이터 필터링
        지역1_data = df_data[df_data['지역'] == 지역1].iloc[0]
        지역2_data = df_data[df_data['지역'] == 지역2].iloc[0]

        chart_data = pd.DataFrame(
            {
                "지역": [지역1_data['지역'], 지역2_data['지역']],
                car_type: [지역1_data[car_type], 지역2_data[car_type]]
            }
        )
        # Altair 차트 생성 (막대 너비 조절)
        chart = alt.Chart(chart_data).mark_bar(size=20).encode(  
                x=alt.X("지역:N", title="지역", sort=None),  # 막대 간격 자동 조정
                y=alt.Y(f"{car_type}:Q", title=f"{car_type} 차량 수"),
                color="지역:N"
            ).properties(
                width=300,  # 전체 그래프 너비
                height=300  # 전체 그래프 높이
            )
        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.write('조회결과가 없습니다.')

def region_age_gendercomparsion(city_name, gender=None):
    sns.set_style("whitegrid")
    sns.set_theme(font="AppleGothic")  # Seaborn에서 한글 폰트 적용
    colums = ['gender', 'age', 'registers']
    df_city = pd.DataFrame(search_city_do_gender(config.DATABASE_CONFIG, city_name, gender), columns=colums)
    fig = plt.figure(figsize=(12, 9))
    # 선택된 도시 데이터의 선 그래프
    sns.barplot(x="age", y="registers", hue="gender", data=df_city)
    # 그래프 제목과 레이블 설정
    plt.title(f'{city_name} 성별/연령대별 차량 등록대수')
    plt.xlabel('연령대')
    plt.ylabel('차량 등록대수')
    plt.grid(True)

    # Streamlit에 그래프 출력
    st.pyplot(fig)
    st.subheader(f'{city_name} 지역 데이터')
    st.dataframe(df_city)
    
def make_year_month_selector():
    col1, col2 = st.columns(2)
    with col1:
        years = list(range(2023, 2026))
        current_year = datetime.datetime.now().year
        # 현재 연도가 리스트에 있다면 해당 인덱스를 기본값으로 설정
        default_year = years.index(current_year) if current_year in years else min(years) 
        year = st.selectbox("연도 선택", years, index=default_year)
        
    with col2:
        months = list(range(1, 13))
        current_month = datetime.datetime.now().month
        default_month = months.index(current_month)-1 if current_month in months else min(months) # 현재값이 25년2월까지 있어서.. 바로 데이터가 안나올수 있음.. 
        month = st.selectbox("월 선택", months, index= default_month)
        
    st.write(f"선택한 날짜: {year}년 {month}월")
    return year, month

def visual_map_chart(year, month):
    # year month selector 만들기 
    df = merge_dataframe(year, month)
    if df is None :
        st.write('조회결과가 없습니다.')
    else:
        st.write("전국 자동차등록 현황 지도")
        # 2D 마커를 위한 ScatterplotLayer
        layer = pdk.Layer(
            'ScatterplotLayer',
            df,
            get_position='[lon, lat]',  # 'lon'과 'lat'를 사용하여 위치 지정
            get_color=[254, 233,4, 140],  # 마커의 색상 (빨간색)
            get_radius=5000,  # 마커의 반경 (각각의 점 크기)
            pickable=True,  # 클릭 가능하게 설정
            auto_highlight=True,  # 마우스를 올렸을 때 하이라이트 효과
        )

        # ViewState 설정 (2D 지도)
        view_state = pdk.ViewState(
            longitude=127.87,  # 중심 경도
            latitude=36.52,  # 중심 위도
            zoom=7  # 확대 수준
        )

            # 마우스를 올렸을 때 tooltip 표시 
        tooltip = {
                "html": "<b>City:</b> {docity} <br> <b>Count:</b> {count}",  # 표시할 내용
                "style": {"backgroundColor": "rgba(0, 0, 0, 0.5)", "color": "white", "fontSize": "12px"}
            }

            # PyDeck을 사용하여 2D 지도 렌더링
        st.pydeck_chart(pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip=tooltip  # tooltip을 설정하여 마우스를 대면 값이 표시되도록 설정
        ))

def show():
    st.title("전국차량등록현황")
    # 날짜 선택 탭 
    year, month = make_year_month_selector()
    df = processing_datafame(year, month)

    # 네비게이션 바 (탭)
    tabs = ["전국차량등록 현황", "전국차량등록", "지역별 비교", "성별/연령별 비교"]
    tab1, tab2, tab3, tab4 = st.tabs(tabs)
    
    with tab1:
        st.subheader("📊 전국차량등록 현황") 
        st.write(f'{year}년 {month}월기준') 
        if df is not None:
            st.dataframe(df)
        else: 
            st.write('조회되는 결과가 없습니다.')
            
    with tab2:
        st.subheader("🚗 전국차량등록 현황")
        visual_map_chart(year, month)
    with tab3: 
        st.subheader("지역간 차량등록 대수 비교")
        region_comparsion(year, month)
    with tab4:
        st.subheader("지역간 차량등록 대수 비교")
        col1, col2 = st.columns(2)
        with col1:
            city_do_lst = ['서울', '부산', '대구', '인천', '광주', '대전','울산',
                       '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북',
                       '경남', '제주']
            city_location = st.selectbox('지역을 선택하세요', city_do_lst)
        with col2:
            gender_lst = ['모두', '남성', '여성','기타']  
            gender = st.selectbox('성별을 선택하세요', gender_lst)
            
            if gender == '모두':
                gender = None # 선택할 필요없음 

        st.write(f"### {city_location}  성별/연령별 차량등록대수 데이터 분석")
        region_age_gendercomparsion(city_location, gender)
