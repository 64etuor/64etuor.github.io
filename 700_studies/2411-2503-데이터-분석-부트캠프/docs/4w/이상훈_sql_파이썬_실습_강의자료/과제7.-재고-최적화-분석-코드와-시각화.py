# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 21:21:30 2024

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

# 재고 최적화 분석 SQL 쿼리 실행
query = """
SELECT 
    p.productCode, 
    p.productName, 
    p.quantityInStock, 
    IFNULL(SUM(od.quantityOrdered), 0) AS totalSold,
    IFNULL(SUM(od.quantityOrdered), 0) / p.quantityInStock AS salesRate
FROM 
    products p
LEFT JOIN 
    orderdetails od ON p.productCode = od.productCode
GROUP BY 
    p.productCode
HAVING 
    p.quantityInStock > 0
ORDER BY 
    salesRate DESC
LIMIT 20;
"""
# pd.read_sql_query를 사용하여 SQL 쿼리 실행 및 결과 DataFrame으로 변환
inventory_df = pd.read_sql_query(query, conn)

# 판매 속도(재고 대비 판매 비율) 시각화
plt.figure(figsize=(10, 8))
plt.barh(inventory_df['productName'], inventory_df['salesRate'], color='skyblue')
plt.xlabel('Sales Rate (Total Sold / Quantity in Stock)')
plt.title('Top 20 Products by Sales Rate')
plt.tight_layout()
plt.show()

# 연결 종료
conn.close()


"""
이 코드는 제품별로 판매된 총 수량(totalSold)과 재고 수량(quantityInStock)을 기반으로 판매 속도(salesRate)를 계산하고, 이를 시각화합니다. LEFT JOIN을 사용하여 orderdetails 테이블과 조인하고, 판매 기록이 없는 제품의 경우 totalSold를 0으로 처리하여 모든 제품을 포함시킵니다. 또한, HAVING 절을 사용하여 재고 수량이 0보다 큰 제품만을 대상으로 합니다.

이 분석은 재고가 있는 제품 중에서 판매 속도가 높은 상위 20개 제품을 식별하여 보여줍니다. 판매 속도는 재고 대비 판매된 총 수량의 비율로 계산되며, 이 비율이 높은 제품은 재고 관리와 추가 주문 계획에 있어 우선적으로 고려해야 할 대상입니다.\
"""