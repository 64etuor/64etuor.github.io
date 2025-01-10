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

# 각 productLine 별 시즌별 판매 추세 분석 쿼리
query = """
SELECT 
    p.productLine,
    YEAR(o.orderDate) AS orderYear,
    CASE 
        WHEN MONTH(o.orderDate) IN (12, 1, 2) THEN 'Winter'
        WHEN MONTH(o.orderDate) IN (3, 4, 5) THEN 'Spring'
        WHEN MONTH(o.orderDate) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Fall'
    END AS season,
    SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM 
    orders o
JOIN 
    orderdetails od ON o.orderNumber = od.orderNumber
JOIN 
    products p ON od.productCode = p.productCode
GROUP BY 
    p.productLine, orderYear, season
ORDER BY 
    p.productLine, orderYear, season;
"""

# SQL 쿼리 실행 및 결과 DataFrame으로 변환
df = pd.read_sql_query(query, conn)

# 연결 종료
conn.close()

# 제품군과 시즌별로 데이터를 분리하여 시각화
product_lines = df['productLine'].unique()
seasons = ['Winter', 'Spring', 'Summer', 'Fall']

for product_line in product_lines:
    plt.figure(figsize=(12, 6))
    for season in seasons:
        subset = df[(df['productLine'] == product_line) & (df['season'] == season)]
        if not subset.empty:
            plt.plot(subset['orderYear'].astype(str), subset['total_sales'], marker='o', linestyle='-', label=season)

    plt.title(f'Seasonal Sales Trend for {product_line}')
    plt.xlabel('Year')
    plt.ylabel('Total Sales ($)')
    plt.legend(title='Season')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()