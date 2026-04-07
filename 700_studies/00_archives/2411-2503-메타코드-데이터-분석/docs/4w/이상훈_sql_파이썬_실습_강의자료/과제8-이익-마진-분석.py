# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 21:30:13 2024

@author: lshls
"""

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
cursor = conn.cursor()

# 이익 마진 분석 SQL 쿼리 실행
query = """
SELECT 
    p.productName, 
    p.buyPrice, 
    AVG(od.priceEach) AS averageSalePrice,
    (AVG(od.priceEach) - p.buyPrice) AS profitMargin
FROM 
    products p
JOIN 
    orderdetails od ON p.productCode = od.productCode
GROUP BY 
    p.productCode
ORDER BY 
    profitMargin DESC;
"""

cursor.execute(query)

# 결과를 DataFrame으로 변환
columns = [desc[0] for desc in cursor.description]
profit_margin_df = pd.DataFrame(cursor.fetchall(), columns=columns)

# 연결 종료
cursor.close()
conn.close()

# 이익 마진 시각화
plt.figure(figsize=(12, 8))
# 상위 20개 제품만 시각화
top_20_products = profit_margin_df.head(20)
plt.barh(top_20_products['productName'], top_20_products['profitMargin'], color='skyblue')
plt.xlabel('Profit Margin ($)')
plt.title('Top 20 Products by Profit Margin')
plt.tight_layout()
plt.show()


# 각 제품의 카테고리를  추가해주는 코드
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
cursor = conn.cursor()

# 이익 마진 및 productLine 포함한 SQL 쿼리 실행
query = """
SELECT 
    p.productName, 
    p.productLine,
    p.buyPrice, 
    AVG(od.priceEach) AS averageSalePrice,
    (AVG(od.priceEach) - p.buyPrice) AS profitMargin
FROM 
    products p
JOIN 
    orderdetails od ON p.productCode = od.productCode
GROUP BY 
    p.productCode
ORDER BY 
    profitMargin DESC
LIMIT 20;
"""

cursor.execute(query)

# 결과를 DataFrame으로 변환
columns = [desc[0] for desc in cursor.description]
profit_margin_df = pd.DataFrame(cursor.fetchall(), columns=columns)

# 연결 종료
cursor.close()
conn.close()

# 이익 마진 및 productLine 시각화
plt.figure(figsize=(12, 8))
# 상위 20개 제품 시각화
# 제품 이름과 productLine을 결합하여 y축 레이블 생성
y_labels = [f"{row['productName']} ({row['productLine']})" for index, row in profit_margin_df.iterrows()]
plt.barh(y_labels, profit_margin_df['profitMargin'], color='skyblue')
plt.xlabel('Profit Margin ($)')
plt.title('Top 20 Products by Profit Margin and Product Line')
plt.tight_layout()
plt.show()