import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# MySQL 데이터베이스 연결 설정
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='2tkdgns@',  # 여기서 비밀번호, 호스트, 사용자 이름을 실제 정보로 변경해야 함
    database='classicmodels'
)

# 제품군별 연도별 매출 추세 쿼리 실행
query = """
SELECT 
    p.productLine,
    YEAR(o.orderDate) AS orderYear, 
    SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM 
    orders o
JOIN 
    orderdetails od ON o.orderNumber = od.orderNumber
JOIN 
    products p ON od.productCode = p.productCode
GROUP BY 
    p.productLine, orderYear
ORDER BY 
    p.productLine, orderYear;
"""

# SQL 쿼리 실행 및 결과 DataFrame으로 변환
df = pd.read_sql_query(query, conn)

# 연결 종료
conn.close()

# 모든 제품군의 연도별 매출 추세를 하나의 그래프에 표시
plt.figure(figsize=(14, 8))
product_lines = df['productLine'].unique()

for product_line in product_lines:
    subset = df[df['productLine'] == product_line]
    plt.plot(subset['orderYear'], subset['total_sales'], marker='o', linestyle='-', label=product_line)

plt.title('Yearly Sales Trend by Product Line')
plt.xlabel('Year')
plt.ylabel('Total Sales ($)')
plt.legend(title='Product Line', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout(rect=[0, 0, 0.85, 1])  # 범례가 그래프 영역 밖에 위치하도록 조정
plt.show()


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

# 모든 제품군의 제품별 연도별 매출 추세 쿼리 실행
query = """
SELECT 
    p.productLine,
    p.productName,
    YEAR(o.orderDate) AS orderYear, 
    SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM 
    orders o
JOIN 
    orderdetails od ON o.orderNumber = od.orderNumber
JOIN 
    products p ON od.productCode = p.productCode
GROUP BY 
    p.productLine, p.productName, orderYear
ORDER BY 
    p.productLine, p.productName, orderYear;
"""

# SQL 쿼리 실행 및 결과 DataFrame으로 변환
df = pd.read_sql_query(query, conn)

# 연결 종료
conn.close()

# 제품군별로 시각화
product_lines = [
    "Classic Cars", "Motorcycles", "Planes", 
    "Ships", "Trains", "Trucks and Buses", "Vintage Cars"
]

for product_line in product_lines:
    plt.figure(figsize=(14, 6))
    subset = df[df['productLine'] == product_line]
    products = subset['productName'].unique()
    for product in products:
        product_subset = subset[subset['productName'] == product]
        plt.plot(product_subset['orderYear'], product_subset['total_sales'], marker='o', linestyle='-', label=product)
    
    plt.title(f'Yearly Sales Trend for {product_line}')
    plt.xlabel('Year')
    plt.ylabel('Total Sales ($)')
    plt.legend(title='Product Name', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout(rect=[0, 0, 0.75, 1])  # 범례가 그래프 영역 밖에 위치하도록 조정
    plt.show()