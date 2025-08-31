"""
데이터베이스 쿼리 및 데이터 관리 모듈
====================================

이 모듈은 MySQL 데이터베이스와의 상호작용을 담당하며,
차량 등록 현황 데이터의 조회, 삽입, 수정 등의 작업을 수행합니다.

주요 기능:
- 차량 등록 현황 데이터 조회 (import_dataset)
- 지역 정보 데이터 삽입 (insert_region)
- 차량 타입별 데이터 삽입 (insert_vehicle_type)
- 특정 날짜/지역별 차량 수 조회 (get_vehicle_count)
- 성별/연령별 인구 데이터 삽입 (insert_gender_age)
- 도시별 성별 인구 데이터 검색 (search_city_do_gender)

주석 작성일: 2025.09.01
"""

from mysql import connector 
from datetime import datetime
import csv 
import time 
from module import config

def import_dataset(args, year=None, month=None, day=1):
    """
    특정 연월일의 차량 등록 현황 데이터를 데이터베이스에서 조회하는 함수
    
    Args:
        args (dict): 데이터베이스 연결 설정 정보
        year (int, optional): 조회할 연도
        month (int, optional): 조회할 월
        day (int, optional): 조회할 일 (기본값: 1)
        
    Returns:
        list: 차량 등록 현황 데이터 리스트 (실패 시 None)
        
    처리 과정:
        1. 데이터베이스 연결
        2. 입력된 날짜가 최신 업데이트 날짜보다 이후인지 검증
        3. 연월이 지정된 경우 해당 기간 데이터 조회, 아니면 전체 데이터 조회
        4. 조회된 데이터를 딕셔너리 형태로 변환하여 리스트에 저장
        5. 데이터베이스 연결 종료
    """
    # 나중에 데이터를 업데이트 했을 경우 업데이트 기간을 수정 해주면 됨 
    try:
        # 데이터베이스 연결
        conn = connector.connect(**args)
        cursor = conn.cursor() 
        nation_vehicles = []
        
        # 입력된 날짜를 YYYY-MM-DD 형식으로 변환
        input_date = datetime(year=year, month=month, day=day).strftime('%Y-%m-%d')
        
        # 최신 업데이트 날짜 (2025년 2월 1일)
        last_update_time = datetime(year=2025, month=2, day=1).strftime('%Y-%m-%d')
        
        # 입력된 날짜가 최신 업데이트 날짜보다 이후인 경우 None 반환
        if input_date > last_update_time:
            return None 
        
        # 연월이 모두 지정된 경우 해당 기간 데이터 조회
        elif (year is not None) and (month is not None): 
           
            sql = """
                SELECT vt.id, rn.city_do, rn.city_gun_gu,
                vt.van, vt.sedan, vt.truck, vt.special,
                vt.update_time
                FROM national_vehicle.vehicle_type vt  
                JOIN national_vehicle.region_name rn 
                ON vt.region_id = rn.id
                WHERE vt.update_time BETWEEN '2024-01-01' AND %s
            """
            cursor.execute(sql, (input_date,))
            
        # 연월이 지정되지 않은 경우 전체 데이터 조회
        else:
            sql = """
            select vt.id, rn.city_do, rn.city_gun_gu,
                vt.van, vt.sedan, vt.truck, vt.special,
                vt.update_time
            from national_vehicle.vehicle_type vt
            join national_vehicle.region_name rn on vt.region_id = rn.id;
            """
            cursor.execute(sql)
            
        # 조회된 데이터를 딕셔너리 형태로 변환하여 리스트에 저장
        for idx_id, city_do, city_gun_gu, van, sedan, truck, special, update_time in cursor.fetchall():
            nation_vehicles_dict = {'id': idx_id, 'city_do': city_do,
                                    'city_gun_gu': city_gun_gu,
                                    'van': van,
                                    'sedan': sedan,
                                    'truck': truck,
                                    'special': special,
                                    'update_time': update_time}
            nation_vehicles.append(nation_vehicles_dict)
            
    except Exception as e:
        # 예외 발생 시 에러 메시지 출력
        print(e)
        return None
    
    finally:
        # 데이터베이스 연결 종료 (예외 발생 여부와 관계없이 실행)
        if conn:
            cursor.close()
            conn.close()
            
    return nation_vehicles

def insert_region(args):
    """
    CSV 파일에서 지역 정보를 읽어 데이터베이스에 삽입하는 함수
    
    Args:
        args (dict): 데이터베이스 연결 설정 정보
        
    처리 과정:
        1. CSV 파일에서 지역 정보(시도, 시군구) 읽기
        2. region_name 테이블에 중복 없이 데이터 삽입 (INSERT IGNORE 사용)
        3. 데이터베이스 연결 종료
    """
    # 데이터베이스 연결
    conn = connector.connect(**args)
    cursor = conn.cursor()
    
    # CSV 파일 경로 
    csv_file_path = './data/vehicle_data.csv'
    
    # CSV 파일 읽기 및 데이터 삽입 
    with open(csv_file_path, newline='', encoding='cp949') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 헤더값 제외
        
        for row in reader:
            # CSV 행에서 시도, 시군구 정보 추출 (인덱스 2, 3번째 컬럼)
            _, update_date, city_do, city_gun_gu, van, sedan, truck, special, _ = row 
            
            # region_name 테이블에 지역 정보 삽입 (중복 시 무시)
            query = 'INSERT IGNORE INTO national_vehicle.region_name(city_do, city_gun_gu) VALUES (%s, %s)'
            cursor.execute(query, (city_do, city_gun_gu))
            
    # 변경사항 커밋 및 연결 종료
    conn.commit()
    cursor.close()
    conn.close()


def insert_vehicle_type(args):
    """
    CSV 파일에서 차량 타입별 등록 현황 데이터를 읽어 데이터베이스에 삽입하는 함수
    
    Args:
        args (dict): 데이터베이스 연결 설정 정보
        
    처리 과정:
        1. CSV 파일에서 차량 등록 현황 데이터 읽기
        2. 숫자 데이터 검증 및 변환 (콤마 제거, 정수 변환)
        3. 지역 ID 조회 후 vehicle_type 테이블에 데이터 삽입
        4. 데이터베이스 연결 종료
    """
    # 데이터베이스 연결
    conn = connector.connect(**args)
    cursor = conn.cursor()
    
    # CSV 파일 경로
    csv_file_path = './data/vehicle_data.csv'
    
    # CSV 파일 읽기 및 데이터 삽입
    with open(csv_file_path, newline='', encoding='cp949') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 헤더값 제외

        for row in reader:
            # CSV 행에서 필요한 데이터 추출
            _, update_date, city_do, city_gun_gu, van, sedan, truck, special, _ = row 
            
            # 숫자 필드를 정수로 변환 (콤마 제거, 잘못된 값은 0으로 대체)
            try:
                van = int(van.replace(',', ''))
                sedan = int(sedan.replace(',', ''))
                truck = int(truck.replace(',', ''))
                special = int(special.replace(',', ''))
            
            except ValueError:
                # 잘못된 데이터가 감지된 경우 경고 출력 후 해당 행 건너뛰기
                print(f"⚠ Warning: Invalid data detected in row: {row}")
                break  # 잘못된 데이터 삽입을 방지하기 위해 해당 행 건너뛰기
            
            # 지역 ID 조회 (city_do, city_gun_gu 기준)
            search_region_id = '''SELECT rn.id FROM national_vehicle.region_name AS rn
                                WHERE rn.city_do = %s AND rn.city_gun_gu = %s'''
            cursor.execute(search_region_id, (city_do, city_gun_gu))
            
            result = cursor.fetchone()  # 반드시 결과를 가져와야 함
            
            if result:  # 결과가 있을 경우만 진행
                region_id = result[0]  # 튜플에서 값 추출

                # vehicle_type 테이블에 데이터 삽입
                query = '''INSERT INTO national_vehicle.vehicle_type
                           (region_id, van, sedan, truck, special, update_time) 
                           VALUES (%s, %s, %s, %s, %s, %s);'''
                cursor.execute(query, (region_id, van, sedan, truck, special, update_date))
            else:
                # 해당 지역 정보가 없는 경우 경고 출력
                print(f"⚠ No region_id found for {city_do}, {city_gun_gu}")

    # 변경사항 커밋 및 연결 종료
    conn.commit()
    cursor.close()
    conn.close()
    
def get_vehicle_count(args, year, month, day=1):
    """
    특정 날짜와 지역에 따른 차종별 차량 등록 수를 조회하는 함수
    
    Args:
        args (dict): 데이터베이스 연결 설정 정보
        year (int): 조회할 연도
        month (int): 조회할 월
        day (int, optional): 조회할 일 (기본값: 1)
        
    Returns:
        list: 도시별 차종별 차량 등록 수 데이터
        
    처리 과정:
        1. 데이터베이스 연결
        2. 특정 날짜의 도시별 차종별 차량 등록 수 집계 조회
        3. 조회된 데이터를 딕셔너리 형태로 변환하여 리스트에 저장
        4. 데이터베이스 연결 종료
    """
    try:
        # 데이터베이스 연결
        conn = connector.connect(**args)
        cursor = conn.cursor() 
        nation_vehicles = []

        # 입력된 날짜를 YYYY-MM-DD 형식으로 변환
        input_date = datetime(year=year, month=month, day=day).strftime('%Y-%m-%d')
        
        # 특정 날짜의 도시별 차종별 차량 등록 수 집계 조회
        sql = """
            SELECT rn.city_do, vt.update_time, sum(vt.van), sum(vt.sedan), sum(vt.truck), sum(vt.special)
                    FROM national_vehicle.vehicle_type vt  
                    JOIN national_vehicle.region_name rn 
                    ON vt.region_id = rn.id
                    WHERE vt.update_time = %s
                    GROUP BY rn.city_do;
        """
        cursor.execute(sql, (input_date,))
            
        # 조회된 데이터를 딕셔너리 형태로 변환하여 리스트에 저장
        for city_do, update_time, van, sedan, truck, special in cursor.fetchall():
            nation_vehicles_dict = {'city_do': city_do,
                                    'update_time': update_time,
                                    'van': van,
                                    'sedan': sedan,
                                    'truck': truck,
                                    'special': special
                                    }
            nation_vehicles.append(nation_vehicles_dict)
            
    except Exception as e:
        # 예외 발생 시 에러 메시지 출력
        print(e)
        
    finally:
        # 데이터베이스 연결 종료 (예외 발생 여부와 관계없이 실행)
        if conn:
            cursor.close()
            conn.close()
            
    return nation_vehicles


def insert_gender_age(args, df):
    """
    성별/연령별 인구 데이터를 데이터베이스에 삽입하는 함수
    
    Args:
        args (dict): 데이터베이스 연결 설정 정보
        df (pandas.DataFrame): 성별/연령별 인구 데이터가 포함된 데이터프레임
        
    처리 과정:
        1. 데이터프레임의 각 행과 열을 순회하며 데이터 처리
        2. 지역 ID 조회 후 gender_age 테이블에 데이터 삽입
        3. 데이터베이스 연결 종료
    """
    # 데이터베이스 연결
    conn = connector.connect(**args)  
    cursor = conn.cursor(buffered=True)
    
    # 도시별 데이터 삽입 
    for idx, row in df.iterrows():
        for city in df.columns[2:]:  # 첫 번째 두 컬럼(성별, 연령/시도) 제외
            # 지역 ID 조회
            sql = """
                select id from national_vehicle.region_name
                where city_do = %s
            """
            cursor.execute(sql, (city,))
            region_id = cursor.fetchone()[0]
            
            # gender_age 테이블에 데이터 삽입
            insert_query = """
                    insert into national_vehicle.gender_age(gender, age_group, 
                                        region_id, population) values(%s, %s, %s, %s)
            """        
            cursor.execute(insert_query, (row['성별'], row['연령/시도'], region_id, row[city]))
            
    # 변경사항 커밋 및 연결 종료
    conn.commit()
    conn.close()   
    cursor.close() 
    
def search_city_do_gender(args, city_do, gender=None):
    """
    특정 도시의 성별/연령별 인구 데이터를 검색하는 함수
    
    Args:
        args (dict): 데이터베이스 연결 설정 정보
        city_do (str): 검색할 도시명
        gender (str, optional): 검색할 성별 (None인 경우 전체 성별)
        
    Returns:
        list: 검색된 성별/연령별 인구 데이터
        
    처리 과정:
        1. 데이터베이스 연결
        2. 성별이 지정된 경우 해당 성별만, 아니면 전체 성별 데이터 조회
        3. 조회된 결과 반환
        4. 데이터베이스 연결 종료
    """
    # 데이터베이스 연결
    conn = connector.connect(**args)  
    cursor = conn.cursor(buffered=True)
    
    if gender is not None:
        # 특정 성별 데이터만 조회
        query = """SELECT ga.gender, ga.age_group, ga.population
	            From national_vehicle.gender_age ga
	            JOIN national_vehicle.region_name rn  on rn.id  = ga.region_id
	            where rn.city_do  = %s and ga.gender = %s;"""
        cursor.execute(query, (city_do, gender))
        result = cursor.fetchall()
        
    else: 
        # 전체 성별 데이터 조회
        query = """SELECT ga.gender, ga.age_group, ga.population
	            From national_vehicle.gender_age ga
	            JOIN national_vehicle.region_name rn  on rn.id  = ga.region_id
	            where rn.city_do  = %s;"""
        cursor.execute(query, (city_do,))
        result = cursor.fetchall()
        
    # 데이터베이스 연결 종료
    conn.close()   
    cursor.close() 
    
    return result 

    
if __name__ == '__main__':   
    # 메인 실행 시 데이터가 없을 경우 실행할 함수들
    insert_region(config.DATABASE_CONFIG)      # 지역 정보 데이터 삽입
    insert_vehicle_type(config.DATABASE_CONFIG) # 차량 타입별 데이터 삽입