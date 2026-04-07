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

# 가장 잘 팔리는 제품 분석 쿼리 실행
top_products_query = """
SELECT 
    od.productCode, 
    p.productName, 
    SUM(od.quantityOrdered) AS total_quantity
FROM 
    orderdetails od
JOIN 
    products p ON od.productCode = p.productCode
GROUP BY 
    od.productCode
ORDER BY 
    total_quantity DESC
LIMIT 5;
"""

# 가장 안 팔리는 제품 분석 쿼리 실행
bottom_products_query = """
SELECT 
    od.productCode, 
    p.productName, 
    SUM(od.quantityOrdered) AS total_quantity
FROM 
    orderdetails od
JOIN 
    products p ON od.productCode = p.productCode
GROUP BY 
    od.productCode
ORDER BY 
    total_quantity ASC
LIMIT 5;
"""

# SQL 쿼리 실행 및 결과 DataFrame으로 변환
top_products_df = pd.read_sql_query(top_products_query, conn)
bottom_products_df = pd.read_sql_query(bottom_products_query, conn)

# 연결 종료
conn.close()

# 가장 잘 팔리는 제품 시각화
plt.figure(figsize=(10, 6))
plt.bar(top_products_df['productName'], top_products_df['total_quantity'], color='skyblue')
plt.xlabel('Product Name')
plt.ylabel('Total Quantity Ordered')
plt.title('Top 5 Best Selling Products')
plt.xticks(rotation=45)
plt.show()

# 가장 안 팔리는 제품 시각화
plt.figure(figsize=(10, 6))
plt.bar(bottom_products_df['productName'], bottom_products_df['total_quantity'], color='lightcoral')
plt.xlabel('Product Name')
plt.ylabel('Total Quantity Ordered')
plt.title('Top 5 Least Selling Products')
plt.xticks(rotation=45)
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

# 가장 많이 팔린 제품 분석 쿼리 실행
top_products_query = """
SELECT 
    od.productCode, 
    p.productName, 
    SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM 
    orderdetails od
JOIN 
    products p ON od.productCode = p.productCode
GROUP BY 
    od.productCode
ORDER BY 
    total_sales DESC
LIMIT 5;
"""

# 가장 적게 팔린 제품 분석 쿼리 실행
bottom_products_query = """
SELECT 
    od.productCode, 
    p.productName, 
    SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM 
    orderdetails od
JOIN 
    products p ON od.productCode = p.productCode
GROUP BY 
    od.productCode
ORDER BY 
    total_sales ASC
LIMIT 5;
"""

# SQL 쿼리 실행 및 결과 DataFrame으로 변환
top_products_df = pd.read_sql_query(top_products_query, conn)
bottom_products_df = pd.read_sql_query(bottom_products_query, conn)

# 연결 종료
conn.close()

# 가장 많이 팔린 제품 시각화
plt.figure(figsize=(10, 6))
plt.bar(top_products_df['productName'], top_products_df['total_sales'], color='skyblue')
plt.xlabel('Product Name')
plt.ylabel('Total Sales ($)')
plt.title('Top 5 Best Selling Products by Total Sales')
plt.xticks(rotation=45)
plt.show()

# 가장 적게 팔린 제품 시각화
plt.figure(figsize=(10, 6))
plt.bar(bottom_products_df['productName'], bottom_products_df['total_sales'], color='lightcoral')
plt.xlabel('Product Name')
plt.ylabel('Total Sales ($)')
plt.title('Top 5 Least Selling Products by Total Sales')
plt.xticks(rotation=45)
plt.show()