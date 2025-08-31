# 전국 차량 등록 현황 분석 대시보드 - Hugging Face Spaces

> **📊 프로젝트 소개**: 전국 차량 등록 현황을 분석하고 시각화하는 Streamlit 기반 대시보드

## 🚀 **배포 정보**

### **Hugging Face Spaces**
- **Space URL**: [차량등록현황분석](https://huggingface.co/spaces/[username]/vehicle-analysis-dashboard)
- **배포 상태**: ![Deploy Status](https://huggingface.co/spaces/[username]/vehicle-analysis-dashboard/badge)
- **실행 방법**: Space 페이지에서 직접 실행하거나 API로 호출

### **GitHub Actions CI/CD**
- **자동 배포**: main 브랜치에 push 시 자동으로 Hugging Face Spaces에 배포
- **테스트 자동화**: 코드 변경 시 자동 테스트 실행
- **배포 상태**: ![Deploy](https://github.com/[username]/SKN12_First/workflows/Deploy%20to%20Hugging%20Face/badge.svg)

## 📋 **프로젝트 개요**

### **주제**
전국 차량 등록 현황 분석 및 시각화 대시보드

### **목적**
- 지역별/차종별 차량 등록 현황 시각화
- 성별/연령별 차량 소유 현황 분석
- 인터랙티브 지도 기반 데이터 탐색

### **사용 언어/기술 스택**
- **Backend**: Python 3.9+
- **Frontend**: Streamlit
- **Database**: MySQL
- **Data Processing**: Pandas, NumPy
- **Visualization**: PyDeck, Matplotlib, Seaborn, Altair
- **Web Scraping**: Selenium
- **Deployment**: Hugging Face Spaces

## 🔧 **주요 기능**

### **1. 데이터 수집 및 처리**
- 웹 크롤링을 통한 실시간 차량 등록 현황 데이터 수집
- MySQL 데이터베이스 기반 데이터 저장 및 관리
- 지역별 데이터 통합 및 전처리

### **2. 시각화 및 분석**
- **지도 시각화**: PyDeck 기반 전국 지도에 차량 등록 현황 표시
- **차트 분석**: 지역별, 차종별, 성별/연령별 차량 등록 현황 분석
- **인터랙티브 대시보드**: 사용자 선택에 따른 동적 데이터 표시

### **3. 사용자 인터페이스**
- **탭 기반 네비게이션**: 전국 현황, 지도 시각화, 지역 비교, 성별/연령별 비교
- **연도/월 선택기**: 특정 기간 데이터 조회
- **지역 선택기**: 원하는 지역 데이터 분석

## 🏗️ **시스템 아키텍처**

```
웹 크롤링 → 데이터 전처리 → MySQL 저장 → Streamlit 앱 → 사용자 인터페이스
    ↓              ↓            ↓           ↓
Selenium      Pandas      Database    Streamlit
크롤러      데이터처리     저장소      웹앱
```

## 📊 **데이터 모델**

### **주요 테이블**
- **region_name**: 지역 정보 (시도, 시군구)
- **vehicle_type**: 차량 타입별 등록 현황 (승용, 승합, 화물, 특수)
- **gender_age**: 성별/연령별 차량 소유 현황

### **데이터 흐름**
1. **수집**: 국토교통통계누리에서 차량 등록 현황 데이터 크롤링
2. **처리**: 지역별 데이터 통합 및 차종별 집계
3. **저장**: MySQL 데이터베이스에 구조화된 데이터 저장
4. **분석**: Streamlit 앱에서 데이터 시각화 및 분석

## 🚀 **로컬 실행 방법**

### **1. 환경 설정**
```bash
# 저장소 클론
git clone https://github.com/[username]/SKN12_First.git
cd SKN12_First

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### **2. 데이터베이스 설정**
```bash
# MySQL 데이터베이스 생성
CREATE DATABASE national_vehicle;

# 테이블 생성 (module/sql_query.py 참조)
# 데이터 삽입 (CSV 파일 기반)
```

### **3. 애플리케이션 실행**
```bash
# Streamlit 앱 실행
streamlit run app.py
```

## 🌐 **Hugging Face Spaces 배포**

### **자동 배포**
- GitHub main 브랜치에 push 시 자동으로 Hugging Face Spaces에 배포
- GitHub Actions 워크플로우로 CI/CD 파이프라인 구축

### **수동 배포**
1. Hugging Face에서 Space 생성
2. Space 설정에서 GitHub 저장소 연결
3. 필요한 파일들 업로드

## 🔄 **CI/CD 파이프라인**

### **GitHub Actions 워크플로우**
```yaml
name: Deploy to Hugging Face
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Hugging Face
        uses: huggingface/huggingface_hub@main
        with:
          token: ${{ secrets.HF_TOKEN }}
          space: ${{ secrets.HF_SPACE }}
```

## 📈 **성과 및 배운 점**

### **성과**
- **데이터 수집**: 250개 이상 시군구 차량 등록 현황 데이터 수집 완료
- **시각화**: 인터랙티브 지도 기반 데이터 시각화 구현
- **사용자 경험**: 직관적이고 사용하기 쉬운 대시보드 구축

### **배운 점**
- **웹 크롤링**: Selenium을 활용한 동적 콘텐츠 수집 기술
- **데이터 처리**: 대용량 데이터의 효율적인 전처리 및 집계 방법
- **시각화**: 다양한 차트 라이브러리를 활용한 데이터 시각화 기법
- **배포**: Hugging Face Spaces를 활용한 클라우드 배포 경험

## 🔮 **향후 개선 계획**

### **기능 개선**
- [ ] 실시간 데이터 업데이트 시스템 구축
- [ ] 머신러닝 기반 차량 등록 현황 예측 분석
- [ ] 모바일 최적화 및 반응형 디자인 개선

### **기술 개선**
- [ ] 테스트 코드 자동화 및 CI/CD 파이프라인 고도화
- [ ] 성능 모니터링 및 로깅 시스템 구축
- [ ] 마이크로서비스 아키텍처로 전환 검토

## 👥 **팀 구성**

- **김승학**: 프로젝트 기획 및 데이터베이스 설계
- **허한결**: 웹 크롤링 및 데이터 수집 시스템
- **윤권**: 데이터 처리 및 분석 알고리즘
- **오진우**: Streamlit UI 및 시각화

## 📄 **라이선스**

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 **기여 방법**

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**문의사항**: [GitHub Issues](https://github.com/[username]/SKN12_First/issues) 또는 [Hugging Face Space](https://huggingface.co/spaces/[username]/vehicle-analysis-dashboard)를 통해 연락주세요.
