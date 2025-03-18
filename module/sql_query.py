from mysql import connector 
from datetime import datetime
import csv 
import time 

def import_dataset(args, year=None, month=None, day=1):
    try:
        conn = connector.connect(**args)
        cursor = conn.cursor() 
        nation_vehicles = []
        
        if (year is not None) and (month is not None): 
            input_date = datetime(year=year, month=month, day=day).strftime('%Y-%m-%d')
            sql = """
                SELECT vt.id, rn.city_do, rn.city_gun_gu,
                vt.van, vt.sedan, vt.truck, vt.special,
                vt.update_time
                FROM national_vehicle.vehicle_type vt  
                JOIN national_vehicle.region_name rn 
                ON vt.region_id = rn.id
                WHERE vt.update_time BETWEEN '2024-01-01' AND %s;
            """
            cursor.execute(sql, (input_date,))
        else:
            sql = """
            select vt.id, rn.city_do, rn.city_gun_gu,
                vt.van, vt.sedan, vt.truck, vt.special,
                vt.update_time
            from national_vehicle.vehicle_type vt
            join national_vehicle.region_name rn on vt.region_id = rn.id;
            """
            cursor.execute(sql)
            
        for idx_id, city_do, city_gun_gu, van, sedan, truck, special, update_time in cursor.fetchall():
            nation_vehicles_dict = {'id' :idx_id, 'city_do':city_do,
                                    'city_gun_gu': city_gun_gu,
                                    'van' : van,
                                    'sedan': sedan,
                                    'truck': truck,
                                    'special': special,
                                    'update_time' : update_time}
            nation_vehicles.append(nation_vehicles_dict)
            
    except Exception as e :
        print(e)
        return None
    
    finally:
        if conn:
            cursor.close()
            conn.close()
    return nation_vehicles

def insert_region(args):
    conn = connector.connect(**args)
    cursor = conn.cursor()
    
    # csv 파일 경로 
    csv_file_path = './data/vehicle_data.csv'
    
    # csv 파일 읽기 및 데이터 삽입 
    with open(csv_file_path, newline='', encoding='cp949') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) # 헤더값 제외
        for row in reader:
            _, update_date, city_do, city_gun_gu, van, sedan, truck, special, _ = row 
            query = 'INSERT IGNORE INTO national_vehicle.region_name(city_do, city_gun_gu) VALUES (%s, %s)'
            cursor.execute(query, (city_do, city_gun_gu))
    conn.commit()
    cursor.close()
    conn.close()


def insert_vehicle_type(args):
    conn = connector.connect(**args)
    cursor = conn.cursor()
    
    # CSV 파일 경로
    csv_file_path = './data/vehicle_data.csv'
    
    # CSV 파일 읽기 및 데이터 삽입
    with open(csv_file_path, newline='', encoding='cp949') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # 헤더값 제외

        for row in reader:
            _, update_date, city_do, city_gun_gu, van, sedan, truck, special, _ = row 
            # Convert numeric fields to integers, replacing invalid values with 0       
            try:
                van =  int(van.replace(',', ''))
                sedan =  int(sedan.replace(',', ''))
                truck =   int(truck.replace(',', ''))
                special =  int(special.replace(',', ''))
            
            except ValueError:
                print(f"⚠ Warning: Invalid data detected in row: {row}")
                break  # Skip this row to avoid inserting invalid data
            
            # region_id 조회
            search_region_id = '''SELECT rn.id FROM national_vehicle.region_name AS rn
                                WHERE rn.city_do = %s AND rn.city_gun_gu = %s'''
            cursor.execute(search_region_id, (city_do, city_gun_gu))
            
            result = cursor.fetchone()  # 반드시 결과를 가져와야 함
            
            if result:  # 결과가 있을 경우만 진행
                region_id = result[0]  # 튜플에서 값 추출

                # INSERT 실행
                query = '''INSERT INTO national_vehicle.vehicle_type
                           (region_id, van, sedan, truck, special, update_time) 
                           VALUES (%s, %s, %s, %s, %s, %s);'''
                cursor.execute(query, (region_id, van, sedan, truck, special, update_date))
            else:
                print(f"⚠ No region_id found for {city_do}, {city_gun_gu}")

    conn.commit()
    cursor.close()
    conn.close()
    
# 작성자: 허한결
# sql에서 특정 날짜, 지역에 따른 차종별 수 가져오기기
def get_vehicle_count(args, year, month, day=1):
    try:
        conn = connector.connect(**args)
        cursor = conn.cursor() 
        nation_vehicles = []

        input_date = datetime(year=year, month=month, day=day).strftime('%Y-%m-%d')
        sql = """
            SELECT rn.city_do, vt.update_time, sum(vt.van), sum(vt.sedan), sum(vt.truck), sum(vt.special)
                    FROM national_vehicle.vehicle_type vt  
                    JOIN national_vehicle.region_name rn 
                    ON vt.region_id = rn.id
                    WHERE vt.update_time = %s
                    GROUP BY rn.city_do;
        """
        cursor.execute(sql, (input_date,))
            
        for city_do, update_time, van, sedan, truck, special in cursor.fetchall():
            nation_vehicles_dict = {'city_do':city_do,
                                    'update_time' : update_time,
                                    'van' : van,
                                    'sedan': sedan,
                                    'truck': truck,
                                    'special': special
                                    }
            nation_vehicles.append(nation_vehicles_dict)
            
    except Exception as e :
        print(e)
    finally:
        if conn:
            cursor.close()
            conn.close()
    return nation_vehicles


def insert_gender_age(args, df):
    conn = connector.connect(**args)  
    cursor = conn.cursor(buffered=True)
    # 도시별 데이터 삽입 
    for idx, row in df.iterrows():
        for city in df.columns[2:]:
            sql = """
                select id from national_vehicle.region_name
                where city_do = %s
            """
            cursor.execute(sql, (city,))
            region_id = cursor.fetchone()[0]
            insert_query = """
                    insert into national_vehicle.gender_age(gender, age_group, 
                                        region_id, population) values(%s, %s, %s, %s)
            """        
            cursor.execute(insert_query, (row['성별'], row['연령/시도'], region_id, row[city]))
    conn.commit()
    conn.close   
    cursor.close() 
    
def search_city_do_gender(args, city_do, gender = None):
    conn = connector.connect(**args)  
    cursor = conn.cursor(buffered=True)
    if gender is not None:
        query = """SELECT ga.gender, ga.age_group, ga.population
	            From national_vehicle.gender_age ga
	            JOIN national_vehicle.region_name rn  on rn.id  = ga.region_id
	            where rn.city_do  = %s and ga.gender = %s;"""
        cursor.execute(query, (city_do, gender))
        time.sleep(2)
        result = cursor.fetchall()
        
    else: 
        query = """SELECT ga.gender, ga.age_group, ga.population
	            From national_vehicle.gender_age ga
	            JOIN national_vehicle.region_name rn  on rn.id  = ga.region_id
	            where rn.city_do  = %s;"""
        cursor.execute(query, (city_do,))
        time.sleep(2)
        result = cursor.fetchall()
    conn.close   
    cursor.close() 
    return result 

    
if __name__ == '__main__':
    args = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'root1234',
    'port' : 3306
    }
    
    insert_region(args) # 데이터가 없을 경우실행
    insert_vehicle_type(args) # 데이터가 없을 경우실행