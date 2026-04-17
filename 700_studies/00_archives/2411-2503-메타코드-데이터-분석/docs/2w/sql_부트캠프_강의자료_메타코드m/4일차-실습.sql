#실습1
SELECT productName, buyPrice 
FROM products 
WHERE buyPrice > (SELECT AVG(buyPrice) FROM products);

SELECT AVG(buyPrice) 
FROM products;




#실습2. 주문 개수가 5개 이상인 고객만 조회
SELECT customerNumber, order_count 
FROM (SELECT customerNumber, COUNT(orderNumber) AS order_count 
      FROM orders GROUP BY customerNumber) AS subquery 
WHERE order_count >= 5;


SELECT customerNumber, COUNT(orderNumber) AS order_count 
fROM orders GROUP BY customerNumber;



#문제1. 최대 주문 개수를 가진 고객의 ID를 조회
SELECT customerNumber 
FROM orders 
GROUP BY customerNumber 
HAVING COUNT(orderNumber) = (SELECT MAX(order_count) 
                             FROM (SELECT customerNumber, COUNT(orderNumber) AS order_count 
                                   FROM orders GROUP BY customerNumber) AS subquery);
                                   
                                   
SELECT customerNumber, COUNT(orderNumber) AS order_count 
FROM orders GROUP BY customerNumber;


#문제 2: products와 orderdetails 테이블을 이용하여, 각 제품별로 총 주문 금액(quantityOrdered * priceEach)을 계산하고, 그 결과를 기반으로 상위 5개의 제품만 조회하세요.

SELECT productCode, productName, totalAmount
FROM (
    SELECT p.productCode, p.productName, SUM(od.quantityOrdered * od.priceEach) AS totalAmount
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    GROUP BY p.productCode, p.productName
) AS inlineView
ORDER BY totalAmount DESC
LIMIT 5;

SELECT p.productCode, p.productName, SUM(od.quantityOrdered * od.priceEach) AS totalAmount
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalamount DESC
LIMIT 5;

#실습 3 각 고객별로 가장 최근의 주문일을 조회하세요
SELECT c.customerName, o.orderDate
FROM customers c, orders o
WHERE c.customerNumber = o.customerNumber 
AND o.orderDate = 
	(SELECT MAX(orderDate) FROM orders WHERE customerNumber = c.customerNumber);

SELECT c.customerName, o.orderDate
FROM customers c, orders o
WHERE c.customerNumber = o.customerNumber 
;
SELECT c.customerName, o.orderDate
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
;

#  문제3. 2003년에 주문한 모든 고객의 이름을 조회하세요.
SELECT customerName 
FROM customers 
WHERE customerNumber IN (SELECT customerNumber FROM orders WHERE YEAR(orderDate) = 2003);



#실습 4 orders 테이블에서 가장 최근 주문을 찾는 쿼리를 작성
WITH LatestOrders AS (
SELECT customerNumber, MAX(orderDate) AS MaxOrderDate
FROM orders
GROUP BY customerNumber
)
SELECT o.orderNumber, o.orderDate, o.customerNumber
FROM orders o
JOIN LatestOrders lo ON o.customerNumber = lo.customerNumber AND o.orderDate = lo.MaxOrderDate;



# 문제 5. products 테이블에서 각 제품 라인별로 평균 제품 가격을 계산하세요. 그리고 이 평균 가격보다 높은 가격을 가진 제품들만을 해당 제품 라인별로 조회하세요.
WITH AveragePrice AS (
    SELECT productLine, AVG(buyPrice) AS avgPrice
    FROM products
    GROUP BY productLine
)
SELECT p.productName, p.productLine, p.buyPrice, a.avgPrice
FROM products p
JOIN AveragePrice a ON p.productLine = a.productLine
WHERE p.buyPrice > a.avgPrice;


#문제 6 각 제품 라인별로 제품의 평균 가격과 전체 제품의 평균 가격을 비교하여 전체 평균 가격보다 높은 제품 라인만 조회하세요.
WITH ProductLineAvgPrice AS (
    SELECT productLine, AVG(buyPrice) AS avgPrice
    FROM products
    GROUP BY productLine
),
TotalAvgPrice AS (
    SELECT AVG(buyPrice) AS totalAvgPrice
    FROM products
)
SELECT plap.productLine, plap.avgPrice, tap.totalAvgPrice
FROM ProductLineAvgPrice plap, TotalAvgPrice tap
WHERE plap.avgPrice > tap.totalAvgPrice;


# 서브쿼리로도 가능
SELECT 
    pl.productLine, 
    AVG(pl.buyPrice) AS avgPrice,
    (SELECT AVG(buyPrice) FROM products) AS totalAvgPrice
FROM products pl
GROUP BY pl.productLine
HAVING avgPrice > (SELECT AVG(buyPrice) FROM products);


# 문제 7 각 직원별로 맡은 고객들의 평균 크레딧 한도를 계산하고, 크레딧 한도의 평균이 $100,000 이상인 직원만 조회하세요.
WITH EmployeeAvgCredit AS (
    SELECT salesRepEmployeeNumber, AVG(creditLimit) AS avgCredit
    FROM customers
    GROUP BY salesRepEmployeeNumber
)
SELECT e.employeeNumber, e.firstName, e.lastName, eac.avgCredit
FROM employees e
JOIN EmployeeAvgCredit eac ON e.employeeNumber = eac.salesRepEmployeeNumber
WHERE eac.avgCredit >= 100000;

# 서브쿼리로 가능
SELECT 
    e.employeeNumber, 
    e.firstName, 
    e.lastName, 
    eac.avgCredit
FROM employees e
JOIN (
    SELECT salesRepEmployeeNumber, AVG(creditLimit) AS avgCredit
    FROM customers
    GROUP BY salesRepEmployeeNumber
) eac ON e.employeeNumber = eac.salesRepEmployeeNumber
WHERE eac.avgCredit >= 100000;


# join으로 해결하기
SELECT e.employeeNumber, e.firstname, e.lastname, AVG(c.creditLimit) AS avgcredit
FROM customers c
JOIN employees e ON c.salesRepEmployeeNumber = e.employeeNumber
GROUP BY e.employeeNumber
HAVING avgcredit > 100000;