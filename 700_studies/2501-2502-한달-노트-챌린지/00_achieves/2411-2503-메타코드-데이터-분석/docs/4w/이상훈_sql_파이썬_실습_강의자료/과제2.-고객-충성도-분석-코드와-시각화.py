# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 12:31:48 2024

@author: Check
"""

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# MySQL 데이터베이스 연결 설정
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='2tkdgns@',  # 실제 비밀번호로 변경하세요
    database='classicmodels'
)

# 고객 충성도 분석 쿼리 실행
loyalty_query = """
SELECT 
    customerNumber,
    COUNT(orderNumber) AS total_orders,
    MAX(orderDate) AS last_order_date
FROM 
    orders
GROUP BY 
    customerNumber
ORDER BY 
    total_orders DESC;
"""

# SQL 쿼리 실행 및 결과 DataFrame으로 변환
loyalty_df = pd.read_sql_query(loyalty_query, conn)

# 연결 종료
conn.close()

# 고객별 총 주문 수 시각화 (고객 번호 사용)
plt.figure(figsize=(12, 8))
# 여기서는 clarity를 위해 상위 20명의 고객만 표시합니다. 전체 데이터셋에서는 이 부분을 조정해야 할 수 있습니다.
top_20_customers = loyalty_df.head(20)
plt.bar(top_20_customers['customerNumber'].astype(str), top_20_customers['total_orders'], color='blue')
plt.xlabel('Customer Number')
plt.ylabel('Total Orders')
plt.title('Customer Loyalty: Total Orders per Customer')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 데이터셋 내의 최신 구매일을 기준으로 경과된 일수 계산
latest_order_date = loyalty_df['last_order_date'].max()
loyalty_df['days_since_last_order'] = (pd.to_datetime(latest_order_date) - pd.to_datetime(loyalty_df['last_order_date'])).dt.days

# 고객별 마지막 구매로부터 경과된 일수 시각화 (고객 번호 사용)
plt.figure(figsize=(12, 8))
# 상위 20명의 고객에 대해 시각화를 수행합니다. 전체 데이터셋에서는 이 부분을 조정해야 할 수 있습니다.
top_20_customers = loyalty_df.head(20)
plt.bar(top_20_customers['customerNumber'].astype(str), top_20_customers['days_since_last_order'], color='green')
plt.xlabel('Customer Number')
plt.ylabel('Days Since Last Order')
plt.title('Customer Loyalty: Days Since Last Order per Customer')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()