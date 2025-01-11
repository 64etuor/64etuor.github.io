USE testdb;
CREATE TABLE testtable (
    id INT AUTO_INCREMENT,        -- AUTO_INCREMENT를 사용해 id 자동 증가
    name VARCHAR(50),             -- 이름 필드, 최대 50자
    age INT,                      -- 나이 필드
    email VARCHAR(100),           -- 이메일 필드, 최대 100자
    PRIMARY KEY (id)              -- id 필드를 PRIMARY KEY로 설정
);

USE testdb;
SELECT * FROM testtable;

SELECT * FROM testdb.testtable;

INSERT INTO testtable (name, age, email)
VALUES
('김철수', 28, 'cheolsu.kim@example.com'),
('박영희', 32, 'younghee.park@example.com'),
('이민준', 24, 'minjun.lee@example.com');