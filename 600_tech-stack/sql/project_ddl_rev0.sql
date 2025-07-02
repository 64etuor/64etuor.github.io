CREATE DATABASE billon_db;
-- 외래 키 체크 해제
SET FOREIGN_KEY_CHECKS = 0;

-- 1. authority
CREATE TABLE `authority` (
  `authority_id` INT NOT NULL AUTO_INCREMENT,
  `authority_name` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`authority_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. category
CREATE TABLE `category` (
  `category_id` BIGINT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(60) NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `modified_at` TIMESTAMP NOT NULL,
  `deleted_at` TIMESTAMP NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. user
CREATE TABLE `user` (
  `user_id` VARCHAR(30) NOT NULL,
  `authority_id` INT NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `contact_number` VARCHAR(11) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  `age` INT NOT NULL,
  `gender` ENUM('M','W') NOT NULL,
  -- TEXT 컬럼에 DEFAULT 설정 제거
  `profile_image` TEXT NOT NULL,
  `is_alarm_enabled` TINYINT(1) NOT NULL,
  `is_consent_provided` TINYINT(1) NOT NULL,
  `account_status` ENUM('휴먼','탈퇴','정지') NOT NULL,
  `reported_count` INT NOT NULL DEFAULT 0,
  `created_at` TIMESTAMP NOT NULL,
  `modified_at` TIMESTAMP NOT NULL,
  `deleted_at` TIMESTAMP NULL,
  `remaining_point` DECIMAL(10,2) NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `FK_AUTHORITY` FOREIGN KEY (`authority_id`) REFERENCES `authority`(`authority_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. store
CREATE TABLE `store` (
  `store_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(30) NOT NULL,
  `category_id` BIGINT NOT NULL,
  `business_registration_number` VARCHAR(255) NOT NULL,
  `business_operation_certificate` VARCHAR(255) NOT NULL,
  `store_name` VARCHAR(150) NOT NULL,
  `contact_number` VARCHAR(11) NOT NULL,
  `address` VARCHAR(100) NOT NULL,
  `address_detail` VARCHAR(90) NOT NULL,
  `business_hours` TIMESTAMP NOT NULL,
  `average_rating` DECIMAL(2, 1) NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `modified_at` TIMESTAMP NOT NULL,
  `deleted_at` TIMESTAMP NULL,
  PRIMARY KEY (`store_id`),
  CONSTRAINT `FK_USER_STORE` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  CONSTRAINT `FK_CATEGORY_STORE` FOREIGN KEY (`category_id`) REFERENCES `category`(`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. notification_type
CREATE TABLE `notification_type` (
  `notification_type_id` BIGINT NOT NULL AUTO_INCREMENT,
  `notification_message` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`notification_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. report_type
CREATE TABLE `report_type` (
  `report_type_id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `modified_at` TIMESTAMP NOT NULL,
  `deleted_at` TIMESTAMP NULL,
  PRIMARY KEY (`report_type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. card_company
CREATE TABLE `card_company` (
  `card_company_id` BIGINT NOT NULL AUTO_INCREMENT,
  `card_company_name` VARCHAR(50) NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `modified_at` TIMESTAMP NOT NULL,
  `deleted_at` TIMESTAMP NULL,
  PRIMARY KEY (`card_company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8. receipt
-- JSON → LONGTEXT로 변경
CREATE TABLE `receipt` (
  `receipt_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(30) NOT NULL,
  `store_id` BIGINT NOT NULL,
  `card_company_id` BIGINT NULL,
  `receipt_body` LONGTEXT NOT NULL,
  `amount` INT NOT NULL,
  `payment_method` ENUM('신용','체크','현금') NOT NULL,
  `transaction_status` ENUM('승인','취소') NOT NULL,
  `is_canceled` ENUM('Y','N') NULL,
  `created_at` TIMESTAMP NOT NULL,
  `deleted_at` TIMESTAMP NULL,
  PRIMARY KEY (`receipt_id`),
  CONSTRAINT `FK_USER_RECEIPT` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  CONSTRAINT `FK_STORE_RECEIPT` FOREIGN KEY (`store_id`) REFERENCES `store`(`store_id`),
  CONSTRAINT `FK_CARD_COMPANY` FOREIGN KEY (`card_company_id`) REFERENCES `card_company`(`card_company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. transaction_status_code
CREATE TABLE `transaction_status_code` (
  `transaction_status_code` INT NOT NULL,
  `code_description` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`transaction_status_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 10. point_product
CREATE TABLE `point_product` (
  `point_product_id` BIGINT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(100) NOT NULL,
  `price` INT NOT NULL,
  `quantity` INT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `modified_at` TIMESTAMP NOT NULL,
  `deleted_at` TIMESTAMP NULL,
  PRIMARY KEY (`point_product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 11. review
CREATE TABLE `review` (
  `review_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(30) NOT NULL,
  `store_id` BIGINT NOT NULL,
  `content` VARCHAR(255) NOT NULL,
  `rating` INT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `modified_at` TIMESTAMP NOT NULL,
  `deleted_at` TIMESTAMP NULL,
  PRIMARY KEY (`review_id`),
  CONSTRAINT `FK_USER_REVIEW` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  CONSTRAINT `FK_STORE_REVIEW` FOREIGN KEY (`store_id`) REFERENCES `store`(`store_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 12. comment
CREATE TABLE `comment` (
  `comment_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(30) NOT NULL,
  `review_id` BIGINT NOT NULL,
  `content` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `modified_at` TIMESTAMP NOT NULL,
  `deleted_at` TIMESTAMP NULL,
  PRIMARY KEY (`comment_id`),
  CONSTRAINT `FK_USER_COMMENT` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  CONSTRAINT `FK_REVIEW_COMMENT` FOREIGN KEY (`review_id`) REFERENCES `review`(`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 13. like
-- like는 예약어이므로 백틱(`)으로 감싸야 함
CREATE TABLE `like` (
  `like_id` BIGINT NOT NULL AUTO_INCREMENT,
  `review_id` BIGINT NOT NULL,
  `user_id` VARCHAR(30) NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`like_id`),
  CONSTRAINT `FK_REVIEW_LIKE` FOREIGN KEY (`review_id`) REFERENCES `review`(`review_id`),
  CONSTRAINT `FK_USER_LIKE` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 14. review_image
CREATE TABLE `review_image` (
  `review_image_id` BIGINT NOT NULL AUTO_INCREMENT,
  `review_id` BIGINT NOT NULL,
  `review_image_url` VARCHAR(255) NULL,
  PRIMARY KEY (`review_image_id`),
  CONSTRAINT `FK_REVIEW_IMAGE` FOREIGN KEY (`review_id`) REFERENCES `review`(`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 15. point
CREATE TABLE `point` (
  `point_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(30) NOT NULL,
  `reference_point_id` BIGINT NULL,
  `receipt_id` BIGINT NOT NULL,
  `transaction_type` VARCHAR(10) NULL,
  `point` INT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `is_canceled` ENUM('Y','N') NOT NULL,
  PRIMARY KEY (`point_id`),
  CONSTRAINT `FK_USER_POINT` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  CONSTRAINT `FK_RECEIPT_POINT` FOREIGN KEY (`receipt_id`) REFERENCES `receipt`(`receipt_id`),
  CONSTRAINT `FK_REFERENCE_POINT` FOREIGN KEY (`reference_point_id`) REFERENCES `point`(`point_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 16. transaction_error_history
CREATE TABLE `transaction_error_history` (
  `point_transaction_id` BIGINT NOT NULL AUTO_INCREMENT,
  `transaction_status_code` INT NOT NULL,
  `receipt_id` BIGINT NULL,
  `point_product_id` BIGINT NULL,
  `transaction_type` VARCHAR(10) NOT NULL,
  `created_at` DATETIME NOT NULL,
  PRIMARY KEY (`point_transaction_id`),
  CONSTRAINT `FK_RECEIPT` FOREIGN KEY (`receipt_id`) REFERENCES `receipt`(`receipt_id`),
  CONSTRAINT `FK_POINT_PRODUCT` FOREIGN KEY (`point_product_id`) REFERENCES `point_product`(`point_product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 17. favorite
CREATE TABLE `favorite` (
  `favorite_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(30) NOT NULL,
  `store_id` BIGINT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  `deleted_at` TIMESTAMP NULL,
  PRIMARY KEY (`favorite_id`),
  CONSTRAINT `FK_USER_FAVORITE` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  CONSTRAINT `FK_STORE_FAVORITE` FOREIGN KEY (`store_id`) REFERENCES `store`(`store_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 18. store_image
CREATE TABLE `store_image` (
  `store_image_id` BIGINT NOT NULL AUTO_INCREMENT,
  `store_id` BIGINT NOT NULL,
  `store_image_url` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`store_image_id`),
  CONSTRAINT `FK_STORE_IMAGE` FOREIGN KEY (`store_id`) REFERENCES `store`(`store_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 19. login_history
CREATE TABLE `login_history` (
  `login_history_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(30) NOT NULL,
  `login_at` TIMESTAMP NOT NULL,
  `ip_address` TEXT NOT NULL,
  `device_type` TEXT NOT NULL,
  PRIMARY KEY (`login_history_id`),
  CONSTRAINT `FK_USER_LOGIN` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 20. report
CREATE TABLE `report` (
  `report_id` BIGINT NOT NULL AUTO_INCREMENT,
  `report_type_id` BIGINT NOT NULL,
  `user_id` VARCHAR(30) NOT NULL,
  `comment_id` BIGINT NULL,
  `review_id` BIGINT NULL,
  `report_comment` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`report_id`),
  CONSTRAINT `FK_REPORT_TYPE` FOREIGN KEY (`report_type_id`) REFERENCES `report_type`(`report_type_id`),
  CONSTRAINT `FK_USER_REPORT` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  CONSTRAINT `FK_COMMENT_REPORT` FOREIGN KEY (`comment_id`) REFERENCES `comment`(`comment_id`),
  CONSTRAINT `FK_REVIEW_REPORT` FOREIGN KEY (`review_id`) REFERENCES `review`(`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 21. penalty_history
CREATE TABLE `penalty_history` (
  `penalty_history_id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(30) NOT NULL,
  `admin_id` VARCHAR(30) NOT NULL,
  `penalty_reason` VARCHAR(255) NOT NULL,
  `start_penalty_at` TIMESTAMP NOT NULL,
  `end_penalty_at` TIMESTAMP NOT NULL,
  PRIMARY KEY (`penalty_history_id`),
  CONSTRAINT `FK_USER` FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  CONSTRAINT `FK_ADMIN` FOREIGN KEY (`admin_id`) REFERENCES `user`(`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 외래 키 체크 다시 활성화
SET FOREIGN_KEY_CHECKS = 1;
