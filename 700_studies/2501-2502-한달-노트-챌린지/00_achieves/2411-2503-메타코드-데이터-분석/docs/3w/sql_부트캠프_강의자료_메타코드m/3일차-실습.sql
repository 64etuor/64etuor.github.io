SELECT productline, count(productline)
FROM products
GROUP BY productline
HAVING COUNT(productline) >20
;

SELECT  avg(buyprice)
FROM products
WHERE  avg(BUYPRICE) > 50
GROUP BY productline
;
SELECT *
FROM products 
;
SELECT productcode, SUM(quantityordered)
FROM orderdetails
WHERE orderlinenumber = 1
group BY productcode
HAVING PRODUCTCODE LIKE 'S10%'
; 

SELECT productline, MAX(msrp)
FROM products
GROUP BY productline
having productline = 'planes'
;

#문제 1: 'orders' 테이블에서 연도별 주문 건수가 100건을 초과하는 연도를 조회하세요. (orderDate와 orderNumber 컬럼 사용)
SELECT YEAR(orderDate) AS OrderYear, COUNT(orderNumber) AS TotalOrders
FROM orders
GROUP BY YEAR(orderDate)
HAVING TotalOrders > 100
;

# 문제 2: 'orderdetails' 테이블에서 상품별  총 주문량이 500개 이상인 상품 코드를 조회하세요. (productCode와 quantityOrdered 컬럼 사용)

SELECT productCode, SUM(quantityOrdered) AS TotalQuantity
FROM orderdetails
GROUP BY productCode
HAVING TotalQuantity >= 500
;

# 문제 3: 'payments' 테이블에서 고객별 총 결제 금액이 $10,000을 초과하는 고객 번호를 조회하세요. (customerNumber와 amount 컬럼 사용)
SELECT customerNumber, SUM(amount) AS TotalAmount
FROM payments
GROUP BY customerNumber
HAVING TotalAmount > 150000
;

#문제 4: 'customers' 테이블에서 국가별 고객 수가 10명 이상인 국가를 조회하세요. (country와 customerNumber 컬럼 사용)

SELECT country, COUNT(customerNumber) AS TotalCustomers
FROM customers
GROUP BY country
HAVING TotalCustomers >= 10
;

SELECT checkNumber, amount, IF(amount > 50000, 'Large', 'Small') AS orderSize 
FROM payments
;

# 문제 5. products' 테이블을 사용하여, 상품별로 가격이 $100을 초과하면 'Expensive'로, 그렇지 않으면 'Cheap'으로 표시하는 쿼리를 작성하세요. (products.productName, products.buyPrice 컬럼 사용)

SELECT productName, buyprice, IF(buyPrice > 100, 'Expensive', 'Cheap') AS PriceCategory
FROM products
ORDER BY buyprice desc;


SELECT productName, buyPrice,
CASE 
    WHEN buyPrice < 20 THEN 'Cheap'
    WHEN buyPrice BETWEEN 20 AND 50 THEN 'Moderate'
    ELSE 'Expensive'
END AS priceCategory

FROM products;


--  문제 6. employees' 테이블을 사용하여, 각 직원의 직책(jobTitle)에 따라 다음과 같이 분류하세요:
-- 'Sales Rep': 'Sales Team'
-- 'VP Sales': 'Management'
-- 'VP Marketing': 'Management'
-- 그 외: 'Other Positions'

SELECT firstName, lastName, jobTitle,
       CASE jobTitle
           WHEN 'Sales Rep' THEN 'Sales Team'
           WHEN 'VP Sales' THEN 'Management'
           WHEN 'VP Marketing' THEN 'Management'
           ELSE 'Other Positions'
       END AS PositionCategory
FROM employees;

SELECT firstName, lastName, jobTitle,
       CASE jobTitle
           WHEN  'Sales Rep' THEN 'Sales Team'
           WHEN  IN ('VP Sales','VP Marketing') THEN 'Management'
           
           ELSE 'Other Positions'
       END AS PositionCategory
FROM employees;


# 조인을 위한 데이터 생성
CREATE TABLE ex3(
	`id` TINYINT,
	`NAME` VARCHAR(10),
	`age` TINYINT
)
;
INSERT INTO ex3
	(`id`, `name`, `age`)
VALUES
	(1,'이상훈',34),
	(2,'박상훈',30),
	(3,'최상훈',20)
;
CREATE TABLE ex4(
	`id` TINYINT,
	`region` VARCHAR(10)
)
;
INSERT INTO ex4
	(`id`, `region`)
VALUES
	(1,'서울'),
	(4,'대구'),
	(5,'부산')
;



#inner join
SELECT * 
FROM ex3
JOIN ex4 ON ex3.id = ex4.id
;

#left join
SELECT * 
FROM ex3
left JOIN ex4 ON ex3.id = ex4.id
;

#left join2
SELECT * 
FROM ex3
left JOIN ex4 ON ex3.id = ex4.id
WHERE ex4.id IS null
;

#RIGHT join
SELECT * 
FROM ex3
RIGHT JOIN ex4 ON ex3.id = ex4.id
;

#RIGHT join2
SELECT * 
FROM ex3
RIGHT JOIN ex4 ON ex3.id = ex4.id
WHERE ex3.id IS NULL;


SELECT ex4.id
FROM ex3
RIGHT JOIN ex4 ON ex3.id = ex4.id
WHERE ex3.id IS NULL;


SELECT id FROM ex3
UNION
SELECT id FROM ex4;

SELECT id FROM ex3
UNION ALL
SELECT id FROM ex4;

#FULL OUTER JOIN
SELECT ex3.id, ex3.name, ex3.age, ex4.id, ex4.region
FROM ex3
left JOIN ex4 ON ex3.id = ex4.id
union
SELECT ex3.id, ex3.name, ex3.age, ex4.id, ex4.region
FROM ex3
RIGHT JOIN ex4 ON ex3.id = ex4.id
WHERE ex3.id IS NULL;


#JOIN 문제 7 'customers' 테이블과 'orders' 테이블을 사용하여, 모든 고객의 이름과 주문 번호를 조회하세요.
SELECT c.customerName, o.orderNumber
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber;

# 문제 8 'products' 테이블과 'orderdetails' 테이블을 사용하여, 상품 이름과 주문된 수량을 조회하세요.
SELECT p.productName, od.quantityOrdered
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode;

# 문제 9. 'employees' 테이블과 'customers' 테이블을 사용하여, 'Leslie'이라는 이름을 가진 직원이 담당하는 모든 고객의 이름을 조회하세요.
SELECT c.customerName
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
WHERE e.firstName = 'Leslie';

# 문제 10.'employees' 테이블과 'offices' 테이블을 사용하여, San Francisco 사무실에서 근무하는 모든 직원의 이름을 조회하세요.

SELECT e.firstName, e.lastName
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'San Francisco';

# 문제 11. 'orderdetails' 테이블과 'products' 테이블을 사용하여, 주문 가격이 상품의 구매 가격보다 2.5배 높은 상품의 이름, 코드, 판매가격, 주문가격, 주문 수량을 조회하세요.
SELECT p.productcode, p.productName, od.priceEach, p.buyPrice, od.quantityOrdered
FROM orderdetails od
JOIN products p ON od.productCode = p.productCode
WHERE od.priceEach > 2.5 * p.buyPrice;

# 문제 12. 'customers' 테이블과 'orders' 테이블을 JOIN하여, 2003년에 주문한 고객의 이름과 주문 번호를 조회하세요.
SELECT c.customerName, o.orderNumber
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
WHERE YEAR(o.orderDate) = 2003;

# 문제 13. 'customers' 테이블과 'payments' 테이블을 JOIN하여, 2004년에 결제한 고객의 이름과 결제 금액을 조회하세요.

SELECT c.customerName, p.amount
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
WHERE YEAR(p.paymentDate) = 2004;


# 문제 14. 'employees' 테이블과 'customers' 테이블을 JOIN하여, 각 직원별로 담당한 고객의 수를 조회하세요.
SELECT CONCAT(e.firstName, ' ', e.lastName) AS EmployeeName, COUNT(c.customerNumber) AS NumberOfCustomers
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber;


#문제 15. 'orders' 테이블, 'orderdetails' 테이블, 'products' 테이블을 JOIN하여, 2003년에 주문된 상품 이름과 해당 주문의 수량을 조회하세요.
SELECT p.productName, od.quantityOrdered
FROM orders o
JOIN orderdetails od ON o.orderNumber = od.orderNumber
JOIN products p ON od.productCode = p.productCode
WHERE YEAR(o.orderDate) = 2003;


# 문제 16. 'customers' 테이블, 'orders' 테이블, 'orderdetails' 테이블을 JOIN하여, 각 고객별 총 주문 금액을 조회하세요.
SELECT c.customerName, SUM(od.priceEach * od.quantityOrdered) AS TotalOrderValue
FROM customers c
JOIN orders o ON c.customerNumber = o.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
GROUP BY c.customerName;


# 문제 17. 'employees' 테이블, 'customers' 테이블, 'payments' 테이블을 JOIN하여, 각 직원별로 담당한 고객들의 총 결제 금액을 조회하세요.
SELECT CONCAT(e.firstName, ' ', e.lastName) AS EmployeeName, SUM(p.amount) AS TotalPayments
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN payments p ON c.customerNumber = p.customerNumber
GROUP BY e.employeeNumber;

#문제 18. 'products' 테이블, 'orderdetails' 테이블, 'productlines' 테이블을 JOIN하여, 각 상품 라인별로 주문된 상품의 총 수량을 조회하세요.
SELECT pl.productLine, SUM(od.quantityOrdered) AS TotalQuantity
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN productlines pl ON p.productLine = pl.productLine
GROUP BY pl.productLine;

# 문제 19. 'orders' 테이블, 'orderdetails' 테이블, 'products' 테이블을 JOIN하여, 2004년에 가장 많이 판매된 상품 이름과 해당 상품의 총 판매 수량을 조회하세요.
SELECT p.productName, SUM(od.quantityOrdered) AS TotalQuantity
FROM orders o
JOIN orderdetails od ON o.orderNumber = od.orderNumber
JOIN products p ON od.productCode = p.productCode
WHERE YEAR(o.orderDate) = 2004
GROUP BY p.productName
ORDER BY TotalQuantity DESC
LIMIT 5;

# SUM OVER 예제1
SELECT customernumber,paymentdate, amount,  sum(amount) OVER( PARTITION BY CUSTOMERNUMBER ORDER BY PAYMENTDATE) AS total_amount
FROM payments;

SELECT customernumber,paymentdate, amount,  sum(amount) OVER( PARTITION BY CUSTOMERNUMBER) AS total_amount
FROM payments;

SELECT customernumber,paymentdate, amount,  sum(amount) OVER(ORDER BY PAYMENTDATE) AS total_amount
FROM payments;

SELECT customernumber,paymentdate, amount,  sum(amount) OVER( ) AS total_amount
FROM payments;

#문제20: "orderdetails" 테이블에서 각 주문별로 주문된 제품의 평균 수량("quantityOrdered")을 계산하세요.
SELECT orderNumber, productCode, 
       AVG(quantityOrdered) OVER (PARTITION BY orderNumber) AS avg_quantity_per_order
FROM orderdetails;


#문제21: "orders" 테이블에서 각 고객별로 주문 날짜에 따라서 지금까지의 주문 횟수를 계산하세요.
SELECT o.customerNumber, o.orderNumber, o.orderDate,
       COUNT(o.orderNumber) OVER (PARTITION BY o.customerNumber ORDER BY o.orderDate) AS order_count_so_far
FROM orders o;


# LEAD / LAG 예제
SELECT orderNumber, customerNumber, orderDate,
       LAG(orderDate) OVER (PARTITION BY customerNumber ORDER BY orderDate) AS prev_order_date,
       LEAD(orderDate) OVER (PARTITION BY customerNumber ORDER BY orderDate) AS next_order_date
FROM orders;

SELECT orderNumber, customerNumber, orderDate,
       LAG(orderDate) OVER ( ORDER BY orderDate) AS prev_order_date,
       LEAD(orderDate) OVER ( ORDER BY orderDate) AS next_order_date
FROM orders;

SELECT orderNumber, customerNumber, orderDate,
       LAG(orderDate) OVER ( PARTITION BY customerNumber) AS prev_order_date,
       LEAD(orderDate) OVER ( PARTITION BY customerNumber) AS next_order_date
FROM orders;

SELECT orderNumber, customerNumber, orderDate,
       LAG(orderDate) OVER ( ) AS prev_order_date,
       LEAD(orderDate) OVER ( ) AS next_order_date
FROM orders;


# 문제 22 : "orderdetails" 테이블에서 각 제품 코드별로 주문된 수량(ORDERNUMBER)을 기준으로 정렬했을 때, 주문 수량의 증분을 계산하시오..
SELECT orderNumber, productCode,  quantityOrdered,
       quantityOrdered - LAG(quantityOrdered) OVER (PARTITION BY productCode ORDER BY ORDERNUMBER)  AS quantity_difference
FROM orderdetails;



SELECT customername, creditlimit,
       ROW_NUMBER() OVER ( ORDER BY creditlimit DESC) AS row_number_,
       RANK() OVER ( ORDER BY creditlimit DESC) AS rank_,
       DENSE_RANK() OVER ( ORDER BY creditlimit DESC) AS dense_rank_
FROM customers
ORDER BY creditlimit DESC;




#문제 23: "products" 테이블에서 각 제품 라인별로 가장 비싼 제품의 이름과 가장 싼 제품의 이름을 조회하세요.
#오답
SELECT productLine, productName, buyPrice,
       FIRST_VALUE(productName) OVER (PARTITION BY productLine ORDER BY buyPrice ASC) AS cheapest_product,
       LAST_VALUE(productName) OVER (PARTITION BY productLine ORDER BY buyPrice ASC ) AS most_expensive_product
FROM products
ORDER BY productLine, buyPrice ASC;




#정답1
SELECT productLine, productname, buyprice, 
       FIRST_VALUE(productName) OVER (PARTITION BY productLine ORDER BY buyPrice ASC) AS cheapest_product,
       FIRST_VALUE(productName) OVER (PARTITION BY productLine ORDER BY buyPrice DESC) AS most_expensive_product
FROM products;
#정답2
SELECT productLine, productName, buyPrice,
       FIRST_VALUE(productName) OVER (PARTITION BY productLine ORDER BY buyPrice ASC) AS cheapest_product,
       LAST_VALUE(productName) OVER (PARTITION BY productLine ORDER BY buyPrice ASC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS most_expensive_product
FROM products
ORDER BY productLine, buyPrice ASC;





#예제
SELECT orderNumber, productCode, quantityOrdered,
       AVG(quantityOrdered) OVER (ORDER BY orderNumber ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg_quantity_1,
       AVG(quantityOrdered) OVER (ORDER BY orderNumber ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) AS moving_avg_quantity_2,
       AVG(quantityOrdered) OVER (ORDER BY orderNumber ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS moving_avg_quantity_3,
       AVG(quantityOrdered) OVER (ORDER BY orderNumber RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg_quantity_4
FROM orderdetails
;

SELECT t.orderNumber, t.quantityOrdered,
       AVG(t.quantityOrdered) OVER (ORDER BY t.orderNumber ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg_quantity_1,
       AVG(t.quantityOrdered) OVER (ORDER BY t.orderNumber ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) AS moving_avg_quantity_2,
       AVG(t.quantityOrdered) OVER (ORDER BY t.orderNumber ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS moving_avg_quantity_3,
       AVG(t.quantityOrdered) OVER (ORDER BY t.orderNumber RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg_quantity_4

FROM (
SELECT ordernumber, SUM(quantityordered) AS quantityOrdered
FROM ORDERDETAILS
GROUP BY ordernumber
) AS t

;





#문제 24 "employees" 테이블과 "customers" 테이블을 JOIN하여 각 직원별로 담당하는 고객 수를 계산하고, 각 직원별 담당 고객 수의 누적 합계를 계산하세요.
SELECT 
    e.employeeNumber, 
    e.firstName, 
    e.lastName, 
    COUNT(c.customerNumber) AS customerCount,
    SUM(COUNT(c.customerNumber)) OVER (ORDER BY e.employeeNumber) AS cumulativeCustomerCount
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
ORDER BY e.employeeNumber;






# 요기 아래는 무시

WITH RECURSIVE EmployeeHierarchy AS (
    -- Base Case
    SELECT employeeNumber, reportsTo, firstName, lastName
    FROM employees
    WHERE employeeNumber = 1166  -- 특정 직원 번호

    UNION ALL

    -- Recursive Case
    SELECT e.employeeNumber, e.reportsTo, e.firstName, e.lastName
    FROM employees e
    JOIN EmployeeHierarchy eh ON e.employeeNumber = eh.reportsTo
)

SELECT * FROM EmployeeHierarchy;








# 파티션 활용 예제
SELECT sub.OrderYear, p.productName, sub.TotalQuantity
FROM (
    SELECT YEAR(o.orderDate) AS OrderYear, od.productCode, SUM(od.quantityOrdered) AS TotalQuantity,
           RANK() OVER(PARTITION BY YEAR(o.orderDate) ORDER BY SUM(od.quantityOrdered) DESC) as rnk
    FROM orders o
    JOIN orderdetails od ON o.orderNumber = od.orderNumber
    WHERE YEAR(o.orderDate) BETWEEN 2003 AND 2005
    GROUP BY YEAR(o.orderDate), od.productCode
) AS sub
JOIN products p ON sub.productCode = p.productCode
WHERE sub.rnk = 1;

SELECT YEAR(o.orderDate) AS OrderYear, od.productCode, SUM(od.quantityOrdered) AS TotalQuantity,
           RANK() OVER(PARTITION BY YEAR(o.orderDate) ORDER BY SUM(od.quantityOrdered) DESC) as rnk
    FROM orders o
    JOIN orderdetails od ON o.orderNumber = od.orderNumber
    WHERE YEAR(o.orderDate) BETWEEN 2003 AND 2005
    GROUP BY YEAR(o.orderDate), od.productCode;
    
SELECT orderNumber, productCode, quantityOrdered,
       SUM(quantityOrdered) OVER (ORDER BY orderNumber) AS OrderCumulativeTotal
FROM orderdetails;




SELECT orderDate,
       AVG(sumQuantity) OVER (
           ORDER BY orderDate 
           ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
       ) AS rolling_avg_3days
FROM (
    SELECT orderDate, SUM(quantityOrdered) as sumQuantity
    FROM orderdetails
    JOIN orders ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY orderDate
) AS subquery
ORDER BY orderDate;