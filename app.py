"""
전국 차량 등록 현황 분석 대시보드 - 메인 애플리케이션
====================================================

이 파일은 Streamlit 기반의 차량 정보 분석 대시보드의 메인 진입점입니다.
사이드바를 통해 사용자가 원하는 페이지로 이동할 수 있도록 구성되어 있습니다.

주요 기능:
- 페이지 기본 설정 (제목, 사이드바 상태)
- 페이지 라우팅 및 네비게이션
- 동적 모듈 로딩을 통한 페이지 관리

주석 작성일: 2025.09.01
"""

import streamlit as st
import importlib

# 페이지 기본 설정
# page_title: 브라우저 탭에 표시될 제목
# initial_sidebar_state: 사이드바 초기 상태 (collapsed: 접힘)
st.set_page_config(
    page_title="전국 차량 등록 현황 분석 대시보드", 
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 페이지 목록 정의
# 각 페이지의 이름과 해당 모듈 경로를 매핑
# 사용자가 사이드바에서 선택할 수 있는 메뉴 항목들
PAGES = {
    "🏠 홈": "my_pages.home",                    # 메인 홈페이지
    "📊 전국차량등록현황": "my_pages.car_inquiry", # 차량 등록 현황 분석 페이지
    "❓ 차량 FAQ": "my_pages.faq"                # 자주 묻는 질문 페이지
}

# 사이드바에서 페이지 선택
# st.sidebar.selectbox: 사이드바에 드롭다운 메뉴 생성
# 사용자가 선택한 페이지 이름을 selection 변수에 저장
selection = st.sidebar.selectbox("메뉴", list(PAGES.keys()))

# 선택한 페이지 불러오기
# importlib.import_module: 동적으로 모듈을 import
# PAGES[selection]: 선택된 페이지에 해당하는 모듈 경로
# module.show(): 해당 모듈의 show() 함수 호출하여 페이지 렌더링
module = importlib.import_module(PAGES[selection])
module.show()
