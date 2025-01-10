

# 필요한 라이브러리를 불러옵니다.
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# MySQL 데이터베이스 연결 설정
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='2tkdgns@',  # 실제 비밀번호로 변경하세요
    database='classicmodels'
)
cursor = conn.cursor()

# 고객 세분화 쿼리 실행
cursor.execute("""
SELECT 
    c.customerNumber, 
    COUNT(o.orderNumber) AS orderCount, 
    AVG(od.quantityOrdered * od.priceEach) AS avgOrderValue
FROM 
    customers c
JOIN 
    orders o ON c.customerNumber = o.customerNumber
JOIN 
    orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY 
    c.customerNumber
ORDER BY 
    orderCount DESC, avgOrderValue DESC;
""")

# 결과를 DataFrame으로 변환
columns = [desc[0] for desc in cursor.description]
customer_df = pd.DataFrame(cursor.fetchall(), columns=columns)

# 연결 종료
cursor.close()
conn.close()

# 세분화 기준 정의 (임의로 설정)
orderCount_median = customer_df['orderCount'].median()
avgOrderValue_median = customer_df['avgOrderValue'].median()

# 세분화 레이블링
customer_df['Segment'] = np.where((customer_df['orderCount'] >= orderCount_median) & (customer_df['avgOrderValue'] >= avgOrderValue_median), 'High Value - High Frequency',
                                  np.where((customer_df['orderCount'] < orderCount_median) & (customer_df['avgOrderValue'] >= avgOrderValue_median), 'High Value - Low Frequency',
                                           np.where((customer_df['orderCount'] >= orderCount_median) & (customer_df['avgOrderValue'] < avgOrderValue_median), 'Low Value - High Frequency',
                                                    'Low Value - Low Frequency')))

# 세그먼트별 색상 매핑
color_map = {
    'High Value - High Frequency': 'green',
    'High Value - Low Frequency': 'blue',
    'Low Value - High Frequency': 'orange',
    'Low Value - Low Frequency': 'red'
}

# 산점도 시각화
plt.figure(figsize=(10, 8))
sns.scatterplot(data=customer_df, x='orderCount', y='avgOrderValue', hue='Segment', palette=color_map, s=100)
plt.title('Customer Segmentation based on Order Count and Average Order Value')
plt.xlabel('Order Count')
plt.ylabel('Average Order Value')
plt.legend(title='Segment', title_fontsize='13', labelspacing=1.2)
plt.grid(True)
plt.show()