import mysql.connector
from mysql.connector import Error
from config import db_config

def create_connection():
    try:
        connection = mysql.connector.connect(**db_config.DATABASE_CONFIG)
        # connection = mysql.connector.connect(
        #     host='localhost',
        #     user='root',
        #     database='데이터베이스 이름',
        #     password='비밀번호'
        # )
        if connection.is_connected():
            print('연결 성공')
            return connection
    
    except Error as e:
        print(f"에러 발생: {e}")
        return None
    
connection = create_connection()
connection.close()