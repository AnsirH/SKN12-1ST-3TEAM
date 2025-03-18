import pandas as pd 
import openpyxl 
# from sql_query import import_dataset
from module.sql_query import import_dataset


args = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'root1234',
    'port' : 3306
}

# 광역시 합치기
busan = ['중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','강서구','연제구','수영구','사상구','기장군']
incheon = ['중구', '동구', '미추홀구', '연수구', '남동구', '부평구', '계양구', '서구', '강화군', '옹진군']
daegu = ['중구', '동구', '서구', '남구', '북구', '수성구', '달서구', '달성군', '군위군']
daejeon = ['동구','중구', '서구', '유성구', '대덕구']
ulsan = ['중구', '남구', '동구', '북구', '울주군']
gwangju  = ['광산구', '동구', '서구','남구','북구']
jeju = ['제주시', '서귀포시']

def define_region(row):
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
        return row["city_gun_gu"].split(" ")[0] 
    
def processing_datafame(year, month):
    try: 
        # 데이터셋 가져오기
        national_vehicles = import_dataset(args, year, month)
        if len(national_vehicles) == 0:
            return None 
        
        df_national_vehicles = pd.DataFrame(national_vehicles)
        # 'van', 'sedan', 'truck', 'special' 컬럼이 데이터프레임에 존재하는지 확인
        required_columns = ['van', 'sedan', 'truck', 'special']
        
        # 각 행별로 총합 구하기
        df_national_vehicles['count'] = df_national_vehicles[required_columns].sum(axis=1)
        
        # '계' 포함된 데이터 삭제
        df_national_vehicles = df_national_vehicles[~df_national_vehicles.apply(lambda row: row.astype(str).str.contains('계').any(), axis=1)]
        
        # 지역 정보 정의
        df_national_vehicles['region'] = df_national_vehicles.apply(define_region, axis=1)
        
        # 'region' 기준으로 그룹화 및 총합 계산
        national_vehicle_register = pd.DataFrame(df_national_vehicles.groupby('region', as_index=False)['count'].sum())
        
        # 'count' 기준으로 내림차순 정렬
        national_vehicle_register.sort_values(by='count', ascending=False, inplace=True)
        
        # 인덱스 초기화 및 id 생성
        national_vehicle_register.reset_index(drop=True, inplace=True)
        national_vehicle_register.insert(0, 'id', national_vehicle_register.index + 1)
        
        # 'count' 값을 3자리 단위로 포맷팅
        national_vehicle_register['count'] = national_vehicle_register['count'].apply(lambda x: f"{x:,}")
        
        return national_vehicle_register
    
    except Exception as e:
        # 다른 예외 처리
        print(f"Error: {e}")
        return None


def merge_dataframe(year, month):
    try: 
        df_location = pd.read_excel('./data/korea_lat_lon.xlsx', engine='openpyxl')
        national_vehicles = import_dataset(args, year, month)
        # 각행별로 총합 구하기 
        df_national_vehicles = pd.DataFrame(national_vehicles)
        df_national_vehicles['count'] = df_national_vehicles[['van', 'sedan', 'truck', 'special']].sum(axis= 1)
        # 계가 포함된 데이터 삭제 
        df_national_vehicles = df_national_vehicles[~df_national_vehicles.apply(lambda row: row.astype(str).str.contains('계').any(), axis=1)]
        df_national_vehicles['region'] = df_national_vehicles.apply(define_region, axis=1)
        df_national_vehicles['docity']= df_national_vehicles.apply(lambda row: row['city_do'] + row['city_gun_gu'].split(' ')[0] , axis=1)
        df_vehicles_loc = pd.DataFrame(pd.merge(df_national_vehicles, df_location, how='left', on ='docity')) 
        df_vehicles_loc =  df_vehicles_loc.drop(columns=['id', 'city_do', 'city_gun_gu', 'van',
                                                        'sedan', 'truck', 'special', 'update_time', 'region', 'do', 'city'])
    
        return df_vehicles_loc
    except Exception as e:
        return None 