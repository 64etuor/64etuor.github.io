SELECT DISTINCT productLine FROM productlines ; 

SELECT customerName AS ClientName FROM customers;

SELECT DISTINCT orderDate FROM orders;

SELECT lastName, firstName AS GivenName FROM employees;

SELECT DISTINCT productCode FROM orderdetails LIMIT 15; 

SELECT checkNumber AS Check_ID FROM payments;

SELECT DISTINCT productName FROM products LIMIT 9, 5;

SELECT officeCode AS Office_ID FROM offices;

SELECT productCode, quantityOrdered AS TotalOrdered FROM orderdetails;

SELECT DISTINCT customerName FROM customers LIMIT 10;   