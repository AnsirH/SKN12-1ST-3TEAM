"""
차량 등록 현황 분석 및 시각화 페이지 모듈
========================================

이 모듈은 전국 차량 등록 현황을 분석하고 다양한 형태로 시각화하는 기능을 제공합니다.
지역별 비교, 성별/연령별 분석, 지도 시각화 등 다양한 분석 도구를 포함합니다.

주요 기능:
- 지역별 차종별 차량 등록 현황 비교
- 성별/연령별 차량 등록 현황 분석
- 연도/월 선택기
- 전국 지도 기반 차량 등록 현황 시각화
- 탭 기반 네비게이션

주석 작성일: 2025.09.01
"""

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

def region_comparsion(year, month):
    """
    지역별 차종별 차량 등록 현황을 비교하는 함수
    
    Args:
        year (int): 조회할 연도
        month (int): 조회할 월
        
    기능:
        1. 데이터베이스에서 해당 연월의 차량 등록 현황 데이터 조회
        2. 차종별(승용, 승합, 화물, 특수, 총계) 데이터 정리
        3. 사용자가 선택한 두 지역의 특정 차종별 등록 현황 비교
        4. Altair를 사용한 인터랙티브 막대 차트 생성
    """
    try:
        # 3개 컬럼으로 레이아웃 분할 (차종 선택, 지역1 선택, 지역2 선택)
        car_type_col, col1, col2 = st.columns(3)
        
        # 데이터베이스에서 해당 연월의 차량 등록 현황 데이터 조회
        vehicle_data_list = get_vehicle_count(config.DATABASE_CONFIG, year, month)
        vehicle_data_list.sort(key=lambda x: x['city_do'])  # 지역명 기준으로 정렬

        # 차종별 데이터를 데이터프레임으로 구성
        data = {
            '지역': list(vd['city_do'] for vd in vehicle_data_list),
            '승용': list(map(int, [vd['sedan'] for vd in vehicle_data_list])),
            '승합': list(map(int, [vd['van'] for vd in vehicle_data_list])),
            '화물': list(map(int, [vd['truck'] for vd in vehicle_data_list])),
            '특수': list(map(int, [vd['special'] for vd in vehicle_data_list])),
            '총계': list(map(int, [sum((vd['sedan'], vd['van'], vd['truck'], vd['special'])) for vd in vehicle_data_list]))
        }

        df_data = pd.DataFrame(data)

        # 사용자 입력 컨트롤 생성
        with car_type_col:
            # 차종 선택 (승용, 승합, 화물, 특수, 총계)
            car_type = st.selectbox('차 종류를 선택하세요', ['승용', '승합', '화물', '특수', '총계'])
        with col1:
            # 첫 번째 비교 지역 선택
            지역1 = st.selectbox('첫 번째 지역을 선택하세요', df_data['지역'])
        with col2: 
            # 두 번째 비교 지역 선택
            지역2 = st.selectbox('두 번째 지역을 선택하세요', df_data['지역'])
        
        # 선택된 두 지역의 데이터 필터링
        지역1_data = df_data[df_data['지역'] == 지역1].iloc[0]
        지역2_data = df_data[df_data['지역'] == 지역2].iloc[0]

        # 차트 데이터 구성 (선택된 차종과 두 지역의 데이터)
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
        
        # 차트를 Streamlit에 표시
        st.altair_chart(chart, use_container_width=True)
        
    except Exception as e:
        # 예외 발생 시 사용자에게 안내 메시지 표시
        st.write('조회결과가 없습니다.')

def region_age_gendercomparsion(city_name, gender=None):
    """
    특정 도시의 성별/연령별 차량 등록 현황을 분석하는 함수
    
    Args:
        city_name (str): 분석할 도시명
        gender (str, optional): 특정 성별만 분석 (None인 경우 전체 성별)
        
    기능:
        1. 데이터베이스에서 해당 도시의 성별/연령별 차량 등록 현황 조회
        2. Seaborn을 사용한 막대 차트 생성
        3. 원본 데이터를 테이블 형태로 표시
    """
    # Seaborn 스타일 설정
    sns.set_style("whitegrid")
    sns.set_theme(font="AppleGothic")  # Seaborn에서 한글 폰트 적용
    
    # 데이터베이스에서 성별/연령별 차량 등록 현황 조회
    colums = ['gender', 'age', 'registers']
    df_city = pd.DataFrame(search_city_do_gender(config.DATABASE_CONFIG, city_name, gender), columns=colums)
    
    # matplotlib을 사용한 차트 생성
    fig = plt.figure(figsize=(12, 9))
    
    # 선택된 도시 데이터의 막대 그래프 (성별을 구분하여 표시)
    sns.barplot(x="age", y="registers", hue="gender", data=df_city)
    
    # 그래프 제목과 레이블 설정
    plt.title(f'{city_name} 성별/연령대별 차량 등록대수')
    plt.xlabel('연령대')
    plt.ylabel('차량 등록대수')
    plt.grid(True)

    # Streamlit에 그래프 출력
    st.pyplot(fig)
    
    # 원본 데이터를 테이블 형태로 표시
    st.subheader(f'{city_name} 지역 데이터')
    st.dataframe(df_city)
    
def make_year_month_selector():
    """
    연도와 월을 선택할 수 있는 컨트롤을 생성하는 함수
    
    Returns:
        tuple: (선택된 연도, 선택된 월)
        
    기능:
        1. 2023년부터 2025년까지 연도 선택 가능
        2. 1월부터 12월까지 월 선택 가능
        3. 현재 연도/월을 기본값으로 설정
        4. 선택된 날짜 정보를 화면에 표시
    """
    col1, col2 = st.columns(2)
    
    with col1:
        # 연도 선택 (2023-2025)
        years = list(range(2023, 2026))
        current_year = datetime.datetime.now().year
        
        # 현재 연도가 리스트에 있다면 해당 인덱스를 기본값으로 설정
        default_year = years.index(current_year) if current_year in years else min(years) 
        year = st.selectbox("연도 선택", years, index=default_year)
        
    with col2:
        # 월 선택 (1-12)
        months = list(range(1, 13))
        current_month = datetime.datetime.now().month
        
        # 현재값이 25년2월까지 있어서.. 바로 데이터가 안나올수 있음.. 
        # 기본값을 현재 월보다 1 작게 설정하여 데이터가 있는 월을 기본값으로 설정
        default_month = months.index(current_month)-1 if current_month in months else min(months)
        month = st.selectbox("월 선택", months, index=default_month)
        
    # 선택된 날짜 정보를 화면에 표시
    st.write(f"선택한 날짜: {year}년 {month}월")
    
    return year, month

def visual_map_chart(year, month):
    """
    전국 지도 기반 차량 등록 현황을 시각화하는 함수
    
    Args:
        year (int): 조회할 연도
        month (int): 조회할 월
        
    기능:
        1. 해당 연월의 차량 등록 현황 데이터와 위치 정보 병합
        2. PyDeck을 사용한 2D 지도 시각화
        3. 각 지역별 차량 등록 현황을 지도상에 마커로 표시
        4. 마우스 호버 시 지역명과 차량 수 표시
    """
    # year month selector 만들기 
    df = merge_dataframe(year, month)
    
    if df is None:
        # 데이터가 없는 경우 안내 메시지 표시
        st.write('조회결과가 없습니다.')
    else:
        st.write("전국 자동차등록 현황 지도")
        
        # 2D 마커를 위한 ScatterplotLayer 설정
        layer = pdk.Layer(
            'ScatterplotLayer',
            df,
            get_position='[lon, lat]',  # 'lon'과 'lat'를 사용하여 위치 지정
            get_color=[254, 233, 4, 140],  # 마커의 색상 (노란색, 투명도 140)
            get_radius=5000,  # 마커의 반경 (각각의 점 크기)
            pickable=True,  # 클릭 가능하게 설정
            auto_highlight=True,  # 마우스를 올렸을 때 하이라이트 효과
        )

        # ViewState 설정 (2D 지도)
        view_state = pdk.ViewState(
            longitude=127.87,  # 중심 경도 (한국 중앙부)
            latitude=36.52,    # 중심 위도 (한국 중앙부)
            zoom=7             # 확대 수준
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
    """
    차량 등록 현황 분석 페이지의 메인 함수
    
    이 함수는 페이지의 모든 요소를 렌더링하며, 다음과 같은 기능을 제공합니다:
    1. 연도/월 선택기
    2. 탭 기반 네비게이션 (전국 현황, 지도 시각화, 지역 비교, 성별/연령별 비교)
    3. 각 탭별 상세 분석 기능
    """
    # 페이지 제목
    st.title("전국차량등록현황")
    
    # 날짜 선택 탭 
    year, month = make_year_month_selector()
    df = processing_datafame(year, month)

    # 네비게이션 바 (탭)
    tabs = ["전국차량등록 현황", "전국차량등록", "지역별 비교", "성별/연령별 비교"]
    tab1, tab2, tab3, tab4 = st.tabs(tabs)
    
    # 탭 1: 전국차량등록 현황 (테이블 형태)
    with tab1:
        st.subheader("📊 전국차량등록 현황") 
        st.write(f'{year}년 {month}월기준') 
        if df is not None:
            st.dataframe(df)
        else: 
            st.write('조회되는 결과가 없습니다.')
            
    # 탭 2: 전국차량등록 (지도 시각화)
    with tab2:
        st.subheader("🚗 전국차량등록 현황")
        visual_map_chart(year, month)
        
    # 탭 3: 지역간 차량등록 대수 비교
    with tab3: 
        st.subheader("지역간 차량등록 대수 비교")
        region_comparsion(year, month)
        
    # 탭 4: 성별/연령별 차량등록 대수 비교
    with tab4:
        st.subheader("지역간 차량등록 대수 비교")
        col1, col2 = st.columns(2)
        
        with col1:
            # 분석할 지역 선택 (전국 17개 시도)
            city_do_lst = ['서울', '부산', '대구', '인천', '광주', '대전','울산',
                       '세종', '경기', '강원', '충북', '충남', '전북', '전남', '경북',
                       '경남', '제주']
            city_location = st.selectbox('지역을 선택하세요', city_do_lst)
            
        with col2:
            # 성별 선택 (모두, 남성, 여성, 기타)
            gender_lst = ['모두', '남성', '여성','기타']  
            gender = st.selectbox('성별을 선택하세요', gender_lst)
            
            if gender == '모두':
                gender = None  # '모두' 선택 시 성별 구분 없이 전체 데이터 분석

        # 선택된 지역과 성별에 대한 분석 결과 표시
        st.write(f"### {city_location}  성별/연령별 차량등록대수 데이터 분석")
        region_age_gendercomparsion(city_location, gender)
