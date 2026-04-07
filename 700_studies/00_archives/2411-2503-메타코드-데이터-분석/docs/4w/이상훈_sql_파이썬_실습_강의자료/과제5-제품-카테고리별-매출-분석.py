# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:48:07 2024

@author: Check
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

# 제품 카테고리별 매출 분석 쿼리 실행
category_sales_query = """
SELECT 
    p.productLine, 
    SUM(od.quantityOrdered * od.priceEach) AS total_sales,
    AVG(od.quantityOrdered * od.priceEach) AS average_sales
FROM 
    products p
JOIN 
    orderdetails od ON p.productCode = od.productCode
GROUP BY 
    p.productLine
ORDER BY 
    total_sales DESC;
"""

# SQL 쿼리 실행 및 결과 DataFrame으로 변환
category_sales_df = pd.read_sql_query(category_sales_query, conn)

# 연결 종료
conn.close()

# 총 매출 시각화
plt.figure(figsize=(12, 8))
plt.bar(category_sales_df['productLine'], category_sales_df['total_sales'], color='skyblue')
plt.xlabel('Product Line')
plt.ylabel('Total Sales ($)')
plt.title('Total Sales by Product Category')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# 평균 매출 시각화
plt.figure(figsize=(12, 8))
plt.bar(category_sales_df['productLine'], category_sales_df['average_sales'], color='lightgreen')
plt.xlabel('Product Line')
plt.ylabel('Average Sales ($)')
plt.title('Average Sales by Product Category')
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()