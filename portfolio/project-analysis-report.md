# 프로젝트 상세 분석 보고서
## 전국 차량 등록 현황 분석 대시보드

> **📊 분석 목적**: 포트폴리오 작성을 위한 프로젝트 코드베이스 상세 분석 및 기술적 인사이트 도출

---

## 🔍 **프로젝트 개요**

### **프로젝트 정보**
- **프로젝트명**: 전국 차량 등록 현황 분석 대시보드
- **개발 기간**: 2025.03.17 - 2025.03.18 (2일)
- **개발 인원**: 4명 (팀 프로젝트)
- **프로젝트 타입**: 웹 기반 데이터 분석 대시보드

### **핵심 가치**
- **데이터 기반 의사결정**: 전국 차량 등록 현황을 통한 지역별, 차종별 분석
- **정책 수립 지원**: 자동차 산업 정책 및 시장 분석에 활용 가능한 인사이트 제공
- **사용자 친화적 인터페이스**: 복잡한 데이터를 직관적으로 시각화

---

## 🏗️ **아키텍처 및 시스템 구조**

### **전체 시스템 아키텍처**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Streamlit)   │◄──►│   (Python)      │◄──►│   (MySQL)       │
│                 │    │                 │    │                 │
│ - 홈페이지      │    │ - 데이터 처리    │    │ - 차량 정보     │
│ - 대시보드      │    │ - SQL 쿼리      │    │ - 지역 정보     │
│ - FAQ          │    │ - 크롤링        │    │ - 인구 통계     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **모듈 구조 분석**
```
SKN12_First/
├── app.py                    # 메인 애플리케이션 진입점
├── my_pages/                 # 페이지별 모듈
│   ├── home.py              # 홈페이지 (19줄)
│   ├── car_inquiry.py       # 차량 등록 현황 분석 (182줄)
│   └── faq.py               # FAQ 시스템 (23줄)
├── module/                   # 핵심 기능 모듈
│   ├── sql_query.py         # 데이터베이스 연동 (211줄)
│   ├── data_processing.py   # 데이터 처리 로직 (95줄)
│   ├── config.py            # 데이터베이스 설정 (6줄)
│   ├── merge_excel.ipynb    # 데이터 병합 노트북 (870줄)
│   └── crawling.ipynb       # 웹 크롤링 노트북 (556줄)
├── data/                     # 데이터 파일 저장소
├── images/                   # 이미지 리소스
└── requirements.txt          # 의존성 관리
```

---

## 💻 **기술 스택 상세 분석**

### **프로그래밍 언어**
- **Python 3.x**: 메인 개발 언어, 데이터 처리 및 웹 애플리케이션 구축

### **웹 프레임워크**
- **Streamlit 1.43.2**: 
  - 빠른 프로토타이핑과 데이터 시각화에 특화
  - Python 코드만으로 인터랙티브 웹 앱 구축
  - 실시간 데이터 업데이트 및 반응형 UI 제공

### **데이터 처리 및 분석**
- **Pandas 2.2.2**: 
  - 대용량 데이터 처리 및 조작
  - 데이터 그룹화, 집계, 병합 등 고급 데이터 처리
- **OpenPyXL 3.1.5**: Excel 파일 읽기/쓰기 지원
- **NumPy**: 수치 계산 및 배열 처리

### **데이터 시각화**
- **Seaborn 0.13.2**: 통계적 데이터 시각화
- **Matplotlib**: 기본 차트 및 그래프 생성
- **Altair**: 인터랙티브 차트 생성
- **PyDeck 0.9.1**: 지리적 데이터 시각화

### **데이터베이스**
- **MySQL**: 관계형 데이터베이스
  - 차량 정보, 지역 정보, 인구 통계 저장
  - JOIN을 활용한 복합 쿼리 처리

### **웹 크롤링**
- **Selenium**: 동적 웹 페이지 크롤링
  - 국토교통부 통계 데이터 자동 수집
  - JavaScript 렌더링된 콘텐츠 처리

---

## 🔧 **핵심 기능 및 알고리즘 분석**

### **1. 데이터 수집 및 처리 시스템**

#### **웹 크롤링 엔진**
```python
# 크롤링 데이터 구조
crawling_data = {
    'upload_time': date.today(),
    'city_do': '서울',           # 시/도
    'city_gun_gu': '강남구',     # 시/군/구
    '승용': 123456,              # 승용차 등록 대수
    '승합': 23456,               # 승합차 등록 대수
    '화물': 34567,               # 화물차 등록 대수
    '특수': 4567,                # 특수차 등록 대수
    'total_count': 0             # 총계
}
```

#### **데이터 전처리 알고리즘**
```python
def processing_datafame(year, month):
    # 1. 데이터셋 가져오기
    national_vehicles = import_dataset(config.DATABASE_CONFIG, year, month)
    
    # 2. 데이터프레임 변환
    df_national_vehicles = pd.DataFrame(national_vehicles)
    
    # 3. 각 행별로 총합 계산
    df_national_vehicles['count'] = df_national_vehicles[['van', 'sedan', 'truck', 'special']].sum(axis=1)
    
    # 4. '계' 포함된 데이터 삭제 (중복 제거)
    df_national_vehicles = df_national_vehicles[~df_national_vehicles.apply(lambda row: row.astype(str).str.contains('계').any(), axis=1)]
    
    # 5. 지역 정보 정의 및 그룹화
    df_national_vehicles['region'] = df_national_vehicles.apply(define_region, axis=1)
    national_vehicle_register = df_national_vehicles.groupby('region', as_index=False)['count'].sum()
    
    return national_vehicle_register
```

### **2. 지역별 데이터 분석 시스템**

#### **지역 매핑 알고리즘**
```python
def define_region(row):
    # 광역시별 구역 통합 로직
    if row["city_do"] == "서울":
        return "서울특별시"
    elif row["city_do"] == "부산" and row["city_gun_gu"] in busan:
        return "부산광역시"
    elif row["city_do"] == "대전" and row["city_gun_gu"] in daejeon:
        return "대전광역시"
    # ... 기타 광역시 처리
    else:
        return row["city_gun_gu"].split(" ")[0]
```

#### **통계 분석 엔진**
```python
def region_comparsion(year, month):
    # 1. 데이터 쿼리 및 정렬
    vehicle_data_list = get_vehicle_count(config.DATABASE_CONFIG, year, month)
    vehicle_data_list.sort(key=lambda x: x['city_do'])
    
    # 2. 데이터프레임 구성
    data = {
        '지역': [vd['city_do'] for vd in vehicle_data_list],
        '승용': [int(vd['sedan']) for vd in vehicle_data_list],
        '승합': [int(vd['van']) for vd in vehicle_data_list],
        '화물': [int(vd['truck']) for vd in vehicle_data_list],
        '특수': [int(vd['special']) for vd in vehicle_data_list],
        '총계': [sum((vd['sedan'], vd['van'], vd['truck'], vd['special'])) for vd in vehicle_data_list]
    }
    
    # 3. 인터랙티브 차트 생성
    chart = alt.Chart(chart_data).mark_bar(size=20).encode(
        x=alt.X("지역:N", title="지역", sort=None),
        y=alt.Y(f"{car_type}:Q", title=f"{car_type} 차량 수"),
        color="지역:N"
    )
```

### **3. 데이터베이스 연동 시스템**

#### **SQL 쿼리 최적화**
```sql
-- 지역별 차량 등록 현황 조회
SELECT vt.id, rn.city_do, rn.city_gun_gu,
       vt.van, vt.sedan, vt.truck, vt.special,
       vt.update_time
FROM national_vehicle.vehicle_type vt  
JOIN national_vehicle.region_name rn 
ON vt.region_id = rn.id
WHERE vt.update_time BETWEEN '2024-01-01' AND %s
```

#### **데이터 무결성 보장**
```python
def insert_vehicle_type(args):
    # 1. CSV 파일 읽기
    with open(csv_file_path, newline='', encoding='cp949') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 헤더값 제외
        
        for row in reader:
            # 2. 데이터 타입 변환 및 검증
            try:
                van = int(van.replace(',', ''))
                sedan = int(sedan.replace(',', ''))
                truck = int(truck.replace(',', ''))
                special = int(special.replace(',', ''))
            except ValueError:
                print(f"⚠ Warning: Invalid data detected in row: {row}")
                break  # 잘못된 데이터 건너뛰기
            
            # 3. 지역 ID 조회 및 데이터 삽입
            search_region_id = '''SELECT rn.id FROM national_vehicle.region_name AS rn
                                WHERE rn.city_do = %s AND rn.city_gun_gu = %s'''
            cursor.execute(search_region_id, (city_do, city_gun_gu))
            result = cursor.fetchone()
            
            if result:
                region_id = result[0]
                query = '''INSERT INTO national_vehicle.vehicle_type
                           (region_id, van, sedan, truck, special, update_time) 
                           VALUES (%s, %s, %s, %s, %s, %s)'''
                cursor.execute(query, (region_id, van, sedan, truck, special, update_date))
```

---

## 📊 **데이터 모델 및 구조**

### **데이터베이스 스키마**
```
national_vehicle/
├── region_name (지역 정보)
│   ├── id (PK)
│   ├── city_do (시/도)
│   └── city_gun_gu (시/군/구)
├── vehicle_type (차량 정보)
│   ├── id (PK)
│   ├── region_id (FK → region_name.id)
│   ├── van (승합차)
│   ├── sedan (승용차)
│   ├── truck (화물차)
│   ├── special (특수차)
│   └── update_time (업데이트 시간)
└── gender_age (성별/연령별 정보)
    ├── id (PK)
    ├── gender (성별)
    ├── age_group (연령대)
    ├── region_id (FK → region_name.id)
    └── population (인구수)
```

### **데이터 처리 파이프라인**
```
1. 웹 크롤링 → 2. CSV 파일 생성 → 3. 데이터 검증 → 4. DB 저장 → 5. 분석 처리 → 6. 시각화
```

---

## 🎯 **핵심 성과 및 기술적 성취**

### **정량적 성과**
- **데이터 처리 규모**: 전국 17개 시도, 250개 이상 시군구 차량 등록 현황 분석
- **데이터 수집 자동화**: 웹 크롤링을 통한 자동화된 데이터 수집 시스템 구축
- **사용자 인터페이스**: 3개 주요 페이지로 구성된 직관적인 웹 대시보드

### **기술적 성취**
- **모듈화 설계**: 기능별 모듈 분리로 유지보수성 향상
- **데이터 무결성**: CSV 데이터 검증 및 예외 처리로 안정성 확보
- **성능 최적화**: 효율적인 SQL 쿼리와 데이터 처리 알고리즘
- **확장성**: 새로운 지역이나 차종 추가 시 유연한 확장 가능

### **사용자 경험 개선**
- **인터랙티브 시각화**: Altair를 활용한 동적 차트 생성
- **반응형 UI**: Streamlit의 컴포넌트를 활용한 사용자 친화적 인터페이스
- **데이터 접근성**: 복잡한 통계 데이터를 직관적으로 이해할 수 있는 시각화

---

## 🔮 **향후 개선 방향**

### **기술적 개선점**
1. **테스트 코드 작성**: 단위 테스트 및 통합 테스트로 코드 품질 향상
2. **성능 모니터링**: 로깅 시스템 구축 및 성능 지표 측정
3. **에러 핸들링**: 더욱 견고한 예외 처리 및 사용자 피드백 시스템
4. **API 설계**: RESTful API로 확장하여 다양한 클라이언트 지원

### **기능적 개선점**
1. **실시간 데이터 업데이트**: 자동화된 데이터 수집 및 실시간 처리
2. **고급 분석 기능**: 머신러닝을 활용한 예측 분석 및 트렌드 분석
3. **사용자 커스터마이징**: 개인화된 대시보드 및 알림 시스템
4. **모바일 최적화**: 반응형 디자인 및 모바일 앱 개발

### **데이터 품질 개선**
1. **데이터 검증 강화**: 더욱 정교한 데이터 품질 검증 알고리즘
2. **데이터 백업**: 자동화된 데이터 백업 및 복구 시스템
3. **데이터 버전 관리**: 데이터 변경 이력 추적 및 롤백 기능

---

## 📈 **포트폴리오 작성 가이드**

### **강조할 기술적 요소**
1. **데이터 엔지니어링**: 웹 크롤링부터 데이터베이스 설계까지의 전체 파이프라인
2. **웹 개발**: Streamlit을 활용한 현대적인 웹 애플리케이션 개발
3. **데이터 시각화**: 다양한 라이브러리를 활용한 효과적인 데이터 표현
4. **시스템 설계**: 모듈화된 아키텍처와 확장 가능한 구조 설계

### **구체적 성과 지표**
- **개발 효율성**: 2일간 4명이 협업하여 완성된 프로젝트
- **기술적 깊이**: Python, MySQL, 웹 크롤링, 데이터 시각화 등 다양한 기술 스택 활용
- **실용성**: 실제 정부 데이터를 활용한 실용적인 분석 도구
- **사용자 중심**: 복잡한 데이터를 직관적으로 이해할 수 있는 인터페이스

### **학습 및 성장 포인트**
1. **팀 협업**: 4명이 협업하여 단기간에 완성한 프로젝트 관리 경험
2. **기술 통합**: 다양한 라이브러리와 기술을 통합하여 완성된 시스템 구축
3. **문제 해결**: 데이터 처리부터 시각화까지의 전체 과정에서 발생한 문제 해결 경험
4. **사용자 경험**: 복잡한 데이터를 사용자가 쉽게 이해할 수 있도록 설계한 경험

---

## 🏆 **결론**

이 프로젝트는 **데이터 기반 의사결정을 위한 현대적인 웹 애플리케이션**으로, 다음과 같은 가치를 제공합니다:

1. **기술적 가치**: Python 생태계를 활용한 풀스택 웹 개발 경험
2. **비즈니스 가치**: 실제 정부 데이터를 활용한 실용적인 분석 도구
3. **사용자 가치**: 복잡한 통계 데이터를 직관적으로 이해할 수 있는 인터페이스
4. **확장 가치**: 모듈화된 구조로 향후 기능 확장이 용이한 시스템

이러한 분석 결과를 바탕으로 포트폴리오를 작성하면, 단순한 프로젝트 소개를 넘어서 **기술적 깊이와 실용적 가치**를 효과적으로 전달할 수 있을 것입니다.
