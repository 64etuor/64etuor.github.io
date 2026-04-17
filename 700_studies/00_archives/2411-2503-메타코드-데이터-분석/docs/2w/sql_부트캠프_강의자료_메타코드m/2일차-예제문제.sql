SELECT *
FROM orderdetails
WHERE orderlinenumber = 10
; 








SELECT *
FROM orderdetails
WHERE productcode = 's24_3969'
; 




SELECT *
FROM orderdetails
WHERE quantityordered > 70
; 


SELECT *
FROM orderdetails
WHERE quantityordered >= 70
; 

SELECT *
FROM orderdetails
WHERE quantityordered = 46 AND 
productcode = 's24_3969';




SELECT *
FROM orderdetails
WHERE quantityordered = 46 OR 
productcode = 's24_3969'
;


SELECT *
FROM orderdetails
WHERE priceEach = 35.29 AND 
productcode = 's24_3969' 
OR 
quantityordered = 46 
;
SELECT *
FROM orderdetails
WHERE (priceEach = 35.29 AND 
productcode = 's24_3969' 
)OR 
quantityordered = 46 
;
SELECT *
FROM orderdetails
WHERE priceEach = 35.29 AND 
(productcode = 's24_3969' 
OR 
quantityordered = 46 )
;

SELECT DISTINCT productline
FROM products
;

SELECT *
FROM products
WHERE productline = 'vintage cars' OR productline = 'classic cars'
;

SELECT *
FROM products
WHERE productline LIKE "%cars%"
;

SELECT *
FROM orders
WHERE orderdate 
BETWEEN '2003-01-01' AND '2003-01-31'
;

SELECT *
FROM orders
WHERE orderdate BETWEEN '2003-01-01' AND '2003-01-31'
;
SELECT *
FROM orders
WHERE orderdate >= '2003-01-01' AND orderdate <= '2003-01-31'
;

SELECT *
FROM orders
WHERE orderdate NOT BETWEEN '2003-01-01' AND '2003-01-31'
;

SELECT *
FROM orders
WHERE orderdate < '2003-01-01' OR orderdate > '2003-01-31'
;

SELECT *
FROM orders
WHERE orderdate IN ('2003-02-11','2003-02-17')
;

SELECT *
FROM employees
WHERE officecode not IN (1,2,3)
;
SELECT *
FROM employees
WHERE officecode <> 1 and officecode <> 2 and officecode <>3
;

SELECT *
FROM orders
WHERE comments IS NULL 
;
SELECT *
FROM orders
WHERE comments IS not NULL 
;

SELECT LASTNAME, FIRSTNAME, OFFICECODE
FROM employees
ORDER BY OFFICECODE
LIMIT 8;



SELECT LASTNAME, FIRSTNAME, OFFICECODE
FROM employees
ORDER BY OFFICECODE DESC
LIMIT 8;

SELECT *
FROM orderdetails
ORDER BY 
quantityordered DESC , priceEach asc
;

SELECT *
FROM orderdetails
ORDER BY 
quantityordered DESC , priceEach desc
;

SELECT productline, count(productline)
FROM products
GROUP BY productline
;

SELECT productline, avg(buyprice)
FROM products
GROUP BY productline
;

SELECT productcode, SUM(quantityordered)
FROM orderdetails
WHERE orderlinenumber = 1
group BY productcode
; 

SELECT productline, MAX(msrp)
FROM products
GROUP BY productline
;


