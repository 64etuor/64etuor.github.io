#문제 1: customers 테이블에서 creditLimit이 10000보다 큰 고객들의 이름(customerName)을 조회하세요.
SELECT customerName
FROM customers
WHERE creditLimit > 10000;









#문제 2: orders 테이블에서 status가 'Shipped' 이거나 'In Process'인 주문의 orderNumber를 조회하세요.
SELECT orderNumber
FROM orders
WHERE status = 'Shipped' OR status = 'In Process';





# 문제 3: products 테이블에서 재고(quantityInStock)가 100개 미만이거나 500개 초과인 제품의 productName을 조회하세요.
SELECT productName
FROM products
WHERE quantityInStock < 100 OR quantityInStock > 500;



# 문제 4: products 테이블에서 제품의 가격(buyPrice)이 50보다 크고 재고(quantityInStock)가 100보다 작은 제품의 productName을 조회하세요.
SELECT productName
FROM products
WHERE buyPrice > 50 AND quantityInStock < 100;




# 문제 5: employees 테이블에서 jobTitle에 'Sales'라는 단어가 포함된 직원의 firstName와 lastName을 조회하세요.
SELECT firstName, lastName
FROM employees
WHERE jobTitle LIKE '%Sales%';




#문제 6: orderdetails 테이블에서 주문 수량(quantityOrdered)이 10개 이상 50개 이하인 주문의 orderNumber를 조회하세요.
SELECT orderNumber
FROM orderdetails
WHERE quantityOrdered BETWEEN 10 AND 50;

# 문제 7: customers 테이블에서 국가(country)가 'USA', 'Canada', 'France' 중 하나인 고객의 customerName을 조회하세요.
SELECT customerName
FROM customers
WHERE country IN ('USA', 'Canada', 'France');



# 문제 8: employees 테이블에서 상사(reportsTo)가 지정되지 않은 직원의 firstName와 lastName을 조회하세요.
SELECT firstName, lastName
FROM employees
WHERE reportsTo IS NULL;

# 문제 9: products 테이블에서 제품 이름(productName)을 조회하되, 가격(buyPrice)을 기준으로 내림차순으로 정렬하세요.
SELECT productName
FROM products
ORDER BY buyPrice DESC;



# 문제 10: orders 테이블에서 각 상태(status)별로 주문 개수를 구하세요.
SELECT status, COUNT(orderNumber) AS OrderCount
FROM orders
GROUP BY status;

#문제 11: orderdetails 테이블에서 각 제품 코드(productCode)별로 주문된 총 수량(quantityOrdered)을 구하세요.
SELECT productCode, SUM(quantityOrdered) AS TotalOrdered
FROM orderdetails
GROUP BY productCode;

# 문제 12: products 테이블에서 제품 라인(productLine)별 제품 개수를 조회하세요.
SELECT productLine, COUNT(productCode) AS ProductCount
FROM products
GROUP BY productLine;








# 문제 13. "products" 테이블에서 각 제품 라인("productLine")별로 제품의 최대 가격("buyPrice")과 최소 가격("buyPrice")을 계산하세요.
SELECT productLine, MAX(buyPrice) as maxPrice, MIN(buyPrice) as minPrice 
FROM products 
GROUP BY productLine;

# 문제 14. "customers" 테이블에서 각 고객 도시("city")별로 평균 크레딧 한도("creditLimit") 상위 5개를 조회하세요.
SELECT city, AVG(creditLimit) as averageCreditLimit 
FROM customers 
GROUP BY city 
ORDER BY averageCreditLimit DESC
LIMIT 5;

# 문제 15. "orderdetails" 테이블에서 주문 번호("orderNumber")별로 총 주문 총액 ("priceEach" * "quantityOrdered") 상위 5개를 계산하세요.
SELECT orderNumber, SUM(priceEach * quantityOrdered) as totalOrderPrice 
FROM orderdetails 
GROUP BY orderNumber 
ORDER BY totalOrderPrice DESC
LIMIT 5
;

# 문제 16. "customers" 테이블에서 각 국가("country")별로 고객 수가 많은 상위 5개를 조회하세요.
SELECT country, COUNT(customerNumber) as numberOfCustomers 
FROM customers 
GROUP BY country 
ORDER BY numberOfCustomers DESC
LIMIT 5;

# 문제 17. "products" 테이블에서 productScale이 '1:10'인 제품 라인("productLine")별로 제품의 평균 가격("buyPrice")을 계산하세요.
SELECT productLine, AVG(buyPrice) as averagePrice 
FROM products 
WHERE productScale = '1:10'
GROUP BY productLine;

# 문제 18. "orders" 테이블에서 2004년에 주문된 주문 상태("status")별로 평균 주문 금액("amount")을 계산하세요.
SELECT status, AVG(amount) 
FROM orders 
WHERE YEAR(orderDate) = 2004 
GROUP BY status;