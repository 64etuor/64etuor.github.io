# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 18:54:54 2024

@author: LSH_Notebook
"""



# VIP 고객 시각화
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

# VIP 고객 식별 쿼리
vip_customers_query = """
SELECT 
    o.customerNumber, 
    COUNT(DISTINCT o.orderNumber) AS order_count, 
    SUM(p.amount) AS total_spent
FROM 
    orders o
JOIN 
    payments p ON o.customerNumber = p.customerNumber
GROUP BY 
    o.customerNumber
ORDER BY 
    total_spent DESC
LIMIT 10;
"""

# VIP 고객 데이터를 DataFrame으로 로딩
vip_df = pd.read_sql_query(vip_customers_query, conn)

# 구매 빈도 시각화
plt.figure(figsize=(10, 6))
plt.bar(vip_df['customerNumber'].astype(str), vip_df['order_count'], color='skyblue')
plt.xlabel('Customer Number')
plt.ylabel('Order Count')
plt.title('VIP Customers Order Frequency')
plt.xticks(rotation=45)
plt.show()

# 구매 금액 시각화
plt.figure(figsize=(10, 6))
plt.bar(vip_df['customerNumber'].astype(str), vip_df['total_spent'], color='lightgreen')
plt.xlabel('Customer Number')
plt.ylabel('Total Spent ($)')
plt.title('VIP Customers Total Spending')
plt.xticks(rotation=45)
plt.show()





# 변화

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



# 시간대별 구매 금액 변화 분석 쿼리 실행
purchase_change_query = """
SELECT 
    p.customerNumber, 
    SUM(CASE 
        WHEN p.paymentDate BETWEEN '2004-01-01' AND '2004-12-30' THEN p.amount 
        ELSE 0 
    END) AS previous_period_total,
    SUM(CASE 
        WHEN p.paymentDate BETWEEN '2004-12-30' AND '2005-12-31' THEN p.amount 
        ELSE 0 
    END) AS recent_period_total
FROM 
    payments p
INNER JOIN (
    SELECT customerNumber
    FROM payments
    GROUP BY customerNumber
    ORDER BY SUM(amount) DESC
    
) AS vip_customers ON p.customerNumber = vip_customers.customerNumber
GROUP BY 
    p.customerNumber;
"""

# SQL 쿼리 실행 및 결과 DataFrame으로 변환
purchase_change_df = pd.read_sql_query(purchase_change_query, conn)

# 구매 금액 변화 계산
purchase_change_df['change_in_spending'] = purchase_change_df['recent_period_total'] - purchase_change_df['previous_period_total']

# 변화량의 절대값에 따라 상위 10개 고객 선택
top_10_customers_change = purchase_change_df.assign(
    abs_change_in_spending=purchase_change_df['change_in_spending'].abs()
).nlargest(10, 'abs_change_in_spending')

# 상위 10개 고객의 원래 변화량 시각화
plt.figure(figsize=(10, 6))

# 여기서는 .loc을 사용해 원래 DataFrame에서 상위 10명 고객의 데이터를 가져옵니다.
plt.bar(top_10_customers_change['customerNumber'].astype(str),
    purchase_change_df.loc[top_10_customers_change.index, 'change_in_spending'],
    color='orange'
)
plt.xlabel('Customer Number')
plt.ylabel('Change in Total Spent ($)')
plt.title('Top 10 VIP Customers with Largest Changes in Spending')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 구매 금액 변화량이 증가한 상위 10명의 고객을 찾습니다.
increased_spending_top10 = purchase_change_df[purchase_change_df['change_in_spending'] > 0] \
                                .nlargest(10, 'change_in_spending')

# 구매 금액 변화량이 감소한 상위 10명의 고객을 찾습니다.
decreased_spending_top10 = purchase_change_df[purchase_change_df['change_in_spending'] < 0] \
                                .nsmallest(10, 'change_in_spending') \
                                .sort_values(by='change_in_spending', ascending=True)  # 감소한 금액이 큰 순서대로 정렬

# 증가한 고객의 변화량 시각화
plt.figure(figsize=(10, 6))
plt.bar(increased_spending_top10['customerNumber'].astype(str), increased_spending_top10['change_in_spending'], color='green')
plt.xlabel('Customer Number')
plt.ylabel('Increase in Total Spent ($)')
plt.title('Top 10 Customers with Increased Spending')
plt.xticks(rotation=90);plt.tight_layout();plt.show()

# 감소한 고객의 변화량 시각화
plt.figure(figsize=(10, 6))
plt.bar(decreased_spending_top10['customerNumber'].astype(str), decreased_spending_top10['change_in_spending'], color='red')
plt.xlabel('Customer Number')
plt.ylabel('Decrease in Total Spent ($)')
plt.title('Top 10 Customers with Decreased Spending')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()



# 연결 종료
conn.close()

