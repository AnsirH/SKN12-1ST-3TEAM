"""
데이터 처리 및 전처리 모듈
========================

이 모듈은 차량 등록 현황 데이터의 전처리와 지역별 데이터 통합을 담당합니다.
주요 기능으로는 광역시 구역 통합, 데이터 집계, 위치 정보 병합 등이 있습니다.

주요 함수:
- define_region: 시군구 정보를 기반으로 광역시 단위로 지역 통합
- processing_datafame: 차량 등록 현황 데이터 전처리 및 집계
- merge_dataframe: 차량 데이터와 위치 정보(위도/경도) 병합

주성 작성일: 2025.09.01
"""

import pandas as pd 
import openpyxl 
# from sql_query import import_dataset
from module.sql_query import import_dataset
from module import config

# 광역시별 구역 목록 정의
# 각 광역시에 속하는 구/군들을 리스트로 정의하여 지역 통합에 사용

# 부산광역시에 속하는 구/군들
busan = ['중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','강서구','연제구','수영구','사상구','기장군']

# 인천광역시에 속하는 구/군들
incheon = ['중구', '동구', '미추홀구', '연수구', '남동구', '부평구', '계양구', '서구', '강화군', '옹진군']

# 대구광역시에 속하는 구/군들
daegu = ['중구', '동구', '서구', '남구', '북구', '수성구', '달서구', '달성군', '군위군']

# 대전광역시에 속하는 구/군들
daejeon = ['동구','중구', '서구', '유성구', '대덕구']

# 울산광역시에 속하는 구/군들
ulsan = ['중구', '남구', '동구', '북구', '울주군']

# 광주광역시에 속하는 구/군들
gwangju  = ['광산구', '동구', '서구','남구','북구']

# 제주특별자치도에 속하는 시들
jeju = ['제주시', '서귀포시']

def define_region(row):
    """
    시군구 정보를 기반으로 광역시 단위로 지역을 통합하는 함수
    
    Args:
        row (pandas.Series): 시도(city_do)와 시군구(city_gun_gu) 정보가 포함된 행
        
    Returns:
        str: 통합된 지역명 (예: "서울특별시", "부산광역시", "강남구" 등)
        
    로직:
        1. 서울특별시는 별도 처리
        2. 광역시들은 해당 구/군 목록에 포함되는지 확인하여 통합
        3. 그 외 지역은 시군구명의 첫 번째 단어 반환
    """
    if row["city_do"] == "서울":
        return "서울특별시"
    elif row["city_do"] == "부산" and row["city_gun_gu"] in busan:
        return "부산광역시"
    elif row["city_do"] == "대전" and row["city_gun_gu"] in daejeon:
        return "대전광역시"
    elif row["city_do"] == "인천" and row["city_gun_gu"] in incheon:
        return "인천광역시"
    elif row["city_do"] == "대구" and row["city_gun_gu"] in daegu:
        return "대구광역시"
    elif row["city_do"] == "울산" and row["city_gun_gu"] in ulsan:
        return "울산광역시"
    elif row["city_do"] == "광주" and row["city_gun_gu"] in gwangju:
        return "광주광역시"
    elif row["city_do"] == "제주" and row["city_gun_gu"] in jeju:
        return "제주시"
    else:
        # 광역시가 아닌 일반 시/군의 경우 시군구명의 첫 번째 단어 반환
        return row["city_gun_gu"].split(" ")[0] 
    
def processing_datafame(year, month):
    """
    특정 연월의 차량 등록 현황 데이터를 전처리하고 지역별로 집계하는 함수
    
    Args:
        year (int): 조회할 연도
        month (int): 조회할 월
        
    Returns:
        pandas.DataFrame: 전처리 및 집계가 완료된 차량 등록 현황 데이터
                         실패 시 None 반환
        
    처리 과정:
        1. 데이터베이스에서 해당 연월의 차량 등록 현황 데이터 조회
        2. 차종별(van, sedan, truck, special) 데이터 합계 계산
        3. '계'가 포함된 요약 행 제거
        4. 지역별로 그룹화하여 총합 계산
        5. 등록 대수 기준 내림차순 정렬
        6. 3자리 단위 콤마 포맷팅 적용
    """
    try: 
        # 데이터베이스에서 해당 연월의 차량 등록 현황 데이터 조회
        national_vehicles = import_dataset(config.DATABASE_CONFIG, year, month)
        
        # 데이터가 없는 경우 None 반환
        if len(national_vehicles) == 0:
            return None 
        
        # 리스트를 데이터프레임으로 변환
        df_national_vehicles = pd.DataFrame(national_vehicles)
        
        # 차종별 컬럼 존재 여부 확인 (van, sedan, truck, special)
        required_columns = ['van', 'sedan', 'truck', 'special']
        
        # 각 행별로 차종별 등록 대수 총합 계산
        df_national_vehicles['count'] = df_national_vehicles[required_columns].sum(axis=1)
        
        # '계'가 포함된 요약 행 제거 (전체 합계 행 등)
        df_national_vehicles = df_national_vehicles[~df_national_vehicles.apply(lambda row: row.astype(str).str.contains('계').any(), axis=1)]
        
        # 지역 정보 정의 (광역시 단위로 통합)
        df_national_vehicles['region'] = df_national_vehicles.apply(define_region, axis=1)
        
        # 'region' 기준으로 그룹화하여 지역별 총합 계산
        national_vehicle_register = pd.DataFrame(df_national_vehicles.groupby('region', as_index=False)['count'].sum())
        
        # 'count' 기준으로 내림차순 정렬 (등록 대수가 많은 지역 순)
        national_vehicle_register.sort_values(by='count', ascending=False, inplace=True)
        
        # 인덱스 초기화 및 순위 ID 생성
        national_vehicle_register.reset_index(drop=True, inplace=True)
        national_vehicle_register.insert(0, 'id', national_vehicle_register.index + 1)
        
        # 'count' 값을 3자리 단위 콤마로 포맷팅 (예: 1,234,567)
        national_vehicle_register['count'] = national_vehicle_register['count'].apply(lambda x: f"{x:,}")
        
        return national_vehicle_register
    
    except Exception as e:
        # 예외 발생 시 에러 메시지 출력 및 None 반환
        print(f"Error: {e}")
        return None


def merge_dataframe(year, month):
    """
    차량 등록 현황 데이터와 위치 정보(위도/경도)를 병합하는 함수
    
    Args:
        year (int): 조회할 연도
        month (int): 조회할 월
        
    Returns:
        pandas.DataFrame: 위치 정보가 병합된 차량 등록 현황 데이터
                         실패 시 None 반환
        
    처리 과정:
        1. 한국 지역별 위도/경도 정보가 담긴 엑셀 파일 로드
        2. 데이터베이스에서 해당 연월의 차량 등록 현황 데이터 조회
        3. 차종별 데이터 합계 계산 및 지역 통합
        4. 위치 정보와 차량 데이터를 지역명 기준으로 병합
        5. 불필요한 컬럼 제거하여 지도 시각화에 필요한 데이터만 반환
    """
    try: 
        # 한국 지역별 위도/경도 정보가 담긴 엑셀 파일 로드
        df_location = pd.read_excel('./data/korea_lat_lon.xlsx', engine='openpyxl')
        
        # 데이터베이스에서 해당 연월의 차량 등록 현황 데이터 조회
        national_vehicles = import_dataset(config.DATABASE_CONFIG, year, month)
        
        # 차량 데이터를 데이터프레임으로 변환
        df_national_vehicles = pd.DataFrame(national_vehicles)
        
        # 각 행별로 차종별 등록 대수 총합 계산
        df_national_vehicles['count'] = df_national_vehicles[['van', 'sedan', 'truck', 'special']].sum(axis=1)
        
        # '계'가 포함된 요약 행 제거
        df_national_vehicles = df_national_vehicles[~df_national_vehicles.apply(lambda row: row.astype(str).str.contains('계').any(), axis=1)]
        
        # 지역 정보 정의 (광역시 단위로 통합)
        df_national_vehicles['region'] = df_national_vehicles.apply(define_region, axis=1)
        
        # 시도 + 시군구 첫 번째 단어로 병합 키 생성 (위치 정보와 매칭용)
        df_national_vehicles['docity'] = df_national_vehicles.apply(lambda row: row['city_do'] + row['city_gun_gu'].split(' ')[0], axis=1)
        
        # 차량 데이터와 위치 정보를 'docity' 기준으로 병합 (left join)
        df_vehicles_loc = pd.DataFrame(pd.merge(df_national_vehicles, df_location, how='left', on='docity'))
        
        # 지도 시각화에 불필요한 컬럼들 제거
        # id, city_do, city_gun_gu, van, sedan, truck, special, update_time, region, do, city 컬럼 삭제
        df_vehicles_loc = df_vehicles_loc.drop(columns=['id', 'city_do', 'city_gun_gu', 'van',
                                                        'sedan', 'truck', 'special', 'update_time', 'region', 'do', 'city'])
    
        return df_vehicles_loc
        
    except Exception as e:
        # 예외 발생 시 None 반환
        return None 