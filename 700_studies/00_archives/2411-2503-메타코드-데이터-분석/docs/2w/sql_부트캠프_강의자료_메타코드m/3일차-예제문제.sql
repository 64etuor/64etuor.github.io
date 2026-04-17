SELECT productline, count(productline)
FROM products
GROUP BY productline
HAVING COUNT(productline) >20
;


SELECT productline, avg(buyprice)
FROM products
GROUP BY productline
HAVING AVG(BUYPRICE) < 50
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
HAVING productline = 'planes'
;

SELECT checkNumber, amount, IF(amount > 50000, 'Large', 'Small') AS orderSize 
FROM payments
;

SELECT productName, buyPrice,
CASE 
WHEN buyPrice < 20 THEN 'Cheap'
WHEN buyPrice BETWEEN 20 AND 50 THEN 'Moderate'
ELSE 'Expensive'
END AS priceCategory
FROM products;

SELECT firstName, lastName, jobTitle,
CASE jobTitle
WHEN 'Sales Rep' THEN 'Sales Team'
WHEN 'VP Sales' THEN 'Management'
WHEN 'VP Marketing' THEN 'Management'
ELSE 'Other Positions'
END AS PositionCategory
FROM employees;

SELECT * 
FROM ex3
JOIN ex4 ON ex3.id = ex4.id;

SELECT * 
FROM ex3
LEFT JOIN ex4 ON ex3.id = ex4.id;

SELECT * 
FROM ex3
left JOIN ex4 ON ex3.id = ex4.id
WHERE ex4.id IS null;

SELECT * 
FROM ex3
RIGHT JOIN ex4 ON ex3.id = ex4.id;

SELECT * 
FROM ex3
RIGHT JOIN ex4 ON ex3.id = ex4.id
WHERE ex3.id IS NULL;

SELECT id FROM ex3
UNION
SELECT id FROM ex4;

SELECT id FROM ex3
UNION ALL
SELECT id FROM ex4;

SELECT ex3.id, ex3.name, ex3.age, ex4.id, ex4.region
FROM ex3
left JOIN ex4 ON ex3.id = ex4.id
union
SELECT ex3.id, ex3.name, ex3.age, ex4.id, ex4.region
FROM ex3
RIGHT JOIN ex4 ON ex3.id = ex4.id
WHERE ex3.id IS NULL;



SELECT customernumber, paymentdate, amount, 
sum(amount) OVER(PARTITION BY CUSTOMERNUMBER ORDER BY PAYMENTDATE) AS total_amount
FROM payments;


SELECT customernumber,paymentdate, amount, sum(amount) OVER( PARTITION BY CUSTOMERNUMBER) AS total_amount
FROM payments;


SELECT customernumber,paymentdate, amount, sum(amount) OVER(ORDER BY PAYMENTDATE) AS total_amount
FROM payments;


SELECT customernumber,paymentdate, amount, sum(amount) OVER( ) AS total_amount
FROM payments;

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


SELECT customername, creditlimit,
ROW_NUMBER() OVER ( ORDER BY creditlimit ASC) AS row_number_,
RANK() OVER ( ORDER BY creditlimit ASC) AS rank_,
DENSE_RANK() OVER ( ORDER BY creditlimit ASC) AS dense_rank_
FROM customers
ORDER BY creditlimit ASC;

SELECT orderNumber, productCode, quantityOrdered,
AVG(quantityOrdered) OVER (ORDER BY orderNumber ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg_quantity_1,
AVG(quantityOrdered) OVER (ORDER BY orderNumber ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) AS moving_avg_quantity_2,
AVG(quantityOrdered) OVER (ORDER BY orderNumber ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS moving_avg_quantity_3,
AVG(quantityOrdered) OVER (ORDER BY orderNumber RANGE BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg_quantity_4
FROM orderdetails
;



