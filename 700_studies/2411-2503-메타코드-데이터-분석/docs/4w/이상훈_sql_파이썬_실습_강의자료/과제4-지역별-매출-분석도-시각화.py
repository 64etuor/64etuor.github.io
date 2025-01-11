import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# MySQL 데이터베이스 연결 설정
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='2tkdgns@',  # 실제 비밀번호로 변경하세요
    database='classicmodels'
)

# 지역별 매출 분석 쿼리 실행
sales_by_country_query = """
SELECT 
    c.country, 
    SUM(od.quantityOrdered * od.priceEach) AS total_sales,
    AVG(od.quantityOrdered * od.priceEach) AS average_sales
FROM 
    customers c
JOIN 
    orders o ON c.customerNumber = o.customerNumber
JOIN 
    orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY 
    c.country
ORDER BY 
    total_sales DESC;
"""

# SQL 쿼리 실행 및 결과 DataFrame으로 변환
sales_by_country_df = pd.read_sql_query(sales_by_country_query, conn)

# 연결 종료
conn.close()

# 총 매출 시각화
plt.figure(figsize=(12, 8))
plt.barh(sales_by_country_df['country'], sales_by_country_df['total_sales'], color='skyblue')
plt.xlabel('Total Sales ($)')
plt.ylabel('Country')
plt.title('Total Sales by Country')
plt.show()

# 평균 매출 시각화
plt.figure(figsize=(12, 8))
plt.barh(sales_by_country_df['country'], sales_by_country_df['average_sales'], color='lightgreen')
plt.xlabel('Average Sales ($)')
plt.ylabel('Country')
plt.title('Average Sales by Country')
plt.show()