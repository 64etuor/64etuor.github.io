CREATE TABLE customers(
customer_number INT,
customer_name VARCHAR(50),
phone VARCHAR(50)
);

CREATE TABLE customers2(
customer_number INT NOT NULL,
customer_name VARCHAR(50) NOT NULL,
phone VARCHAR(50) NOT NULL
);
insert into customers
   (customer_number,customer_name,phone) 
values 
   (1,'이상훈','010-1234-5678'),
   (2,'김상훈','010-1234-5679'),
   (3,'박상훈','010-1234-5679')
;

ALTER TABLE customers rename newcustomers;

ALTER TABLE newcustomers ADD 지역 VARCHAR(50);

ALTER TABLE newcustomers MODIFY 지역 INT;

ALTER TABLE newcustomers CHANGE 지역 REGION VARCHAR(10);

ALTER TABLE newcustomers DROP REGION ;




SHOW GLOBAL VARIABLES LIKE 'LOCAL_INFILE';







SET GLOBAL LOCAL_INFILE=TRUE;





SHOW GLOBAL VARIABLES LIKE 'LOCAL_INFILE';






SELECT customer_name, phone FROM `newcustomers`
;




SELECT customer_name, phone FROM customers
;
SELECT 이름,영어, 수학, 수학+영어 
FROM exercise1
;


SELECT 이름,영어, 수학, 수학+영어 AS 영수
FROM exercise1
;





SELECT * FROM exercise1 LIMIT 10
;





SELECT * FROM exercise1 LIMIT 5, 3
;




SELECT * FROM exercise1 LIMIT 3 OFFSET 5
;




SELECT DISTINCT 수학 FROM exercise1
;





#문제 1: customers 테이블에서 customerName을 가져오되, 중복 없이 가져오세요.

SELECT DISTINCT customerName
FROM customers;





#문제 2: products 테이블에서 제품 이름(productName)만 5개만 가져오세요.

SELECT productName
FROM products
LIMIT 5;



#문제 3: orders 테이블에서 주문 상태(status)의 종류를 모두 나열하세요. 중복은 제거하세요.

SELECT DISTINCT status
FROM orders;




#문제 4: employees 테이블에서 직원의 성(lastName)을 10개만 가져오되, 5번째부터 시작하세요.

SELECT lastName
FROM employees
LIMIT 4, 10;



#문제 5: products 테이블의 productVendor를 별칭(alias) Vendor로 조회하세요.

SELECT productVendor AS Vendor
FROM products;
#문제 6: orders 테이블에서 고객 번호(customerNumber)의 중복 없는 값을 7개만 가져오세요.

SELECT DISTINCT customerNumber
FROM orders
LIMIT 7;
#문제 7: employees 테이블에서 employeeNumber를 별칭 Employee_ID로 조회하되, 3번째부터 6개만 가져오세요.

SELECT employeeNumber AS Employee_ID
FROM employees
LIMIT 2, 6;
#문제 8: offices 테이블에서 국가(country)의 종류를 중복 없이 나열하세요.

SELECT DISTINCT country
FROM offices;
#문제 9: orderdetails 테이블에서 제품 코드(productCode)를 Code라는 별칭으로, 주문 수량(quantityOrdered)를 Quantity라는 별칭으로 조회하세요.

SELECT productCode AS CODE , quantityOrdered AS Quantity
FROM orderdetails;



#문제 10: payments 테이블에서 체크 번호(checkNumber)의 중복 없는 값을 10개만 가져오세요.

SELECT DISTINCT checkNumber
FROM payments
LIMIT 10;


