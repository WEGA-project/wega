SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';
SET NAMES utf8mb4;
DROP TABLE IF EXISTS `devices`;
CREATE TABLE `devices` (
    `id` int NOT NULL AUTO_INCREMENT,
    `db` varchar(255) NOT NULL,
    `name` varchar(255) NOT NULL,
    `userid` int NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
INSERT INTO `devices` (`id`, `db`, `name`, `userid`)
VALUES (1, '2esp32', '2esp32', 1),
    (3, 'esp32wega', 'esp32wega', 1);