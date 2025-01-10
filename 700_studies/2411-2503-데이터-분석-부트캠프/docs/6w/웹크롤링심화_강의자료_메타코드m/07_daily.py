import requests
from bs4 import BeautifulSoup
from config import DECODING_KEY

import mysql.connector
from mysql.connector import Error
from config import db_config

def fetch_data(schDate, schAirport='GMP') : # schDate = '20240831', schAirport =  'GMP'
    url = 'http://openapi.airport.co.kr/service/rest/dailyExpectPassenger/dailyExpectPassenger'
    params ={'serviceKey' : DECODING_KEY, 'schDate' : {schDate}, 'schAirport' : {schAirport}, 'numOfRows':'100'}

    # requests 이용한 url에 데이터 요청
    response = requests.get(url, params=params)
    xml_content = response.content

    # BeautifulSoup을 사용해서 XML 파싱
    soup = BeautifulSoup(xml_content, 'html')

    # items 내의 모든 item 요소들을 찾기
    items = soup.find_all('item')

    datas = []

    for item in items:
        item_data = {data.name : data.text for data in item.find_all()}
        datas.append(item_data)

    return datas

def create_connection():
    try:
        connection = mysql.connector.connect(**db_config.DATABASE_CONFIG)
        if connection.is_connected():
            print('연결 성공')
            return connection
    
    except Error as e:
        print(f"에러 발생: {e}")
        return None
    
def insert_data_fromlist(datas, connection) :
    cursor = connection.cursor()

    insert_query_withvalues = """
        INSERT INTO AIRPORT.DAILY_PSG
        (ARR_OR_DEP, AIRPORT_NAME, YYYYMMDD, HH_HOUR, PASSENGER_AMT, PASSENGER_TEAM_AMT, TYPE_OF_FLIGHT, CONGETST_YN)
        VALUES
        (%(ARR_OR_DEP)s, %(AIRPORT_NAME)s, %(YYYYMMDD)s, %(HH_HOUR)s, %(PASSENGER_AMT)s, %(PASSENGER_TEAM_AMT)s, %(TYPE_OF_FLIGHT)s, %(CONGETST_YN)s)
        """
    
    for item in datas : 
        data_withvalues = {
            'ARR_OR_DEP' : item['aod'],
            'AIRPORT_NAME' : item['arp'],
            'YYYYMMDD' : item['sdt'],
            'HH_HOUR' : item['hh'],
            'PASSENGER_AMT' : item['pct'],
            'PASSENGER_TEAM_AMT' : item['pcg'],
            'CONGETST_YN' : item['congestyn'],
            'TYPE_OF_FLIGHT' : item['tof']
        }
        cursor.execute(insert_query_withvalues, data_withvalues)
    
    connection.commit()
    connection.close()
    print("데이터 INSERT 완료")


datas = fetch_data(schDate = '20240831', schAirport='GMP')
connection = create_connection()

insert_data_fromlist(datas=datas, connection=connection)
