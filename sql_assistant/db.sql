-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 19, 2026 at 08:38 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sql_assistant_db`
--
CREATE DATABASE IF NOT EXISTS `sql_assistant_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `sql_assistant_db`;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
  `name` varchar(20) NOT NULL COMMENT 'Name of the category',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='List of categories';

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `name`) VALUES(1, 'Snacks');
INSERT INTO `category` (`id`, `name`) VALUES(2, 'Tools');
INSERT INTO `category` (`id`, `name`) VALUES(3, 'Gadgets');
INSERT INTO `category` (`id`, `name`) VALUES(4, 'Furnitures');

-- --------------------------------------------------------

--
-- Table structure for table `dtrans`
--

DROP TABLE IF EXISTS `dtrans`;
CREATE TABLE IF NOT EXISTS `dtrans` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
  `htrans_id` int(11) NOT NULL COMMENT 'The transaction where the detail belongs to (referencing to the table "htrans")',
  `item_id` int(11) NOT NULL COMMENT 'The item bought in the transaction (referencing to the table "item")',
  `quantity` int(11) NOT NULL COMMENT 'The quantity of the items bought',
  `subtotal` int(11) NOT NULL COMMENT 'The subtotal price (item price x quantity)',
  PRIMARY KEY (`id`),
  KEY `FK_DTRANS_HTRANS` (`htrans_id`),
  KEY `FK_DTRANS_ITEM` (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Transaction details';

--
-- Dumping data for table `dtrans`
--

INSERT INTO `dtrans` (`id`, `htrans_id`, `item_id`, `quantity`, `subtotal`) VALUES(1, 1, 1, 1, 1000);
INSERT INTO `dtrans` (`id`, `htrans_id`, `item_id`, `quantity`, `subtotal`) VALUES(2, 2, 2, 2, 100);
INSERT INTO `dtrans` (`id`, `htrans_id`, `item_id`, `quantity`, `subtotal`) VALUES(3, 2, 5, 1, 60);
INSERT INTO `dtrans` (`id`, `htrans_id`, `item_id`, `quantity`, `subtotal`) VALUES(4, 3, 3, 3, 150);
INSERT INTO `dtrans` (`id`, `htrans_id`, `item_id`, `quantity`, `subtotal`) VALUES(5, 3, 4, 2, 150);
INSERT INTO `dtrans` (`id`, `htrans_id`, `item_id`, `quantity`, `subtotal`) VALUES(6, 4, 6, 2, 1600);
INSERT INTO `dtrans` (`id`, `htrans_id`, `item_id`, `quantity`, `subtotal`) VALUES(7, 5, 6, 1, 800);

-- --------------------------------------------------------

--
-- Table structure for table `htrans`
--

DROP TABLE IF EXISTS `htrans`;
CREATE TABLE IF NOT EXISTS `htrans` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
  `user_id` int(11) NOT NULL COMMENT 'The user who does the transaction (referencing to the table "user")',
  `transaction_date` date NOT NULL COMMENT 'The date when the transaction is done',
  `total` int(11) NOT NULL COMMENT 'The total payment of the transaction done',
  PRIMARY KEY (`id`),
  KEY `FK_HTRANS_USER` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Transaction header';

--
-- Dumping data for table `htrans`
--

INSERT INTO `htrans` (`id`, `user_id`, `transaction_date`, `total`) VALUES(1, 1, '2026-07-01', 1000);
INSERT INTO `htrans` (`id`, `user_id`, `transaction_date`, `total`) VALUES(2, 3, '2026-05-14', 160);
INSERT INTO `htrans` (`id`, `user_id`, `transaction_date`, `total`) VALUES(3, 1, '2026-07-09', 300);
INSERT INTO `htrans` (`id`, `user_id`, `transaction_date`, `total`) VALUES(4, 1, '2026-07-05', 1600);
INSERT INTO `htrans` (`id`, `user_id`, `transaction_date`, `total`) VALUES(5, 3, '2026-07-06', 800);

-- --------------------------------------------------------

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
CREATE TABLE IF NOT EXISTS `item` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
  `name` varchar(30) NOT NULL COMMENT 'Name of the item',
  `category_id` int(11) NOT NULL COMMENT 'Category of the item (referencing to the table "category")',
  `price` int(11) NOT NULL COMMENT 'Price of the item',
  `stock` int(11) NOT NULL COMMENT 'Current stock of the item',
  PRIMARY KEY (`id`),
  KEY `FK_ITEM_CATEGORY` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='List of items';

--
-- Dumping data for table `item`
--

INSERT INTO `item` (`id`, `name`, `category_id`, `price`, `stock`) VALUES(1, 'Laptop', 3, 1000, 5);
INSERT INTO `item` (`id`, `name`, `category_id`, `price`, `stock`) VALUES(2, 'Crackers', 1, 50, 30);
INSERT INTO `item` (`id`, `name`, `category_id`, `price`, `stock`) VALUES(3, 'Screwdriver', 2, 50, 10);
INSERT INTO `item` (`id`, `name`, `category_id`, `price`, `stock`) VALUES(4, 'Drill', 2, 75, 24);
INSERT INTO `item` (`id`, `name`, `category_id`, `price`, `stock`) VALUES(5, 'Sofa', 4, 60, 7);
INSERT INTO `item` (`id`, `name`, `category_id`, `price`, `stock`) VALUES(6, 'Mobile Phone', 3, 800, 10);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Primary key',
  `name` varchar(30) NOT NULL COMMENT 'Name of the user',
  `gender` tinyint(1) NOT NULL COMMENT 'Gender of the user (0 = Male, 1 = Female)',
  `birthdate` date NOT NULL COMMENT 'Birthdate of the user',
  `address` varchar(255) NOT NULL COMMENT 'Physical address of the user',
  `username` varchar(20) NOT NULL COMMENT 'Username of the user',
  `email` varchar(30) NOT NULL COMMENT 'Email address of the user',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='List of users';

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `gender`, `birthdate`, `address`, `username`, `email`) VALUES(1, 'Jack', 0, '1996-04-02', 'Saint Avenue 19 No. 4, NY', 'jack111', 'jack65@gmail.com');
INSERT INTO `user` (`id`, `name`, `gender`, `birthdate`, `address`, `username`, `email`) VALUES(2, 'Sam', 0, '1980-09-27', 'Winconsin street 21 No. 1, Washington DC', 'sam.sung', 'samwitwicky@hotmail.com');
INSERT INTO `user` (`id`, `name`, `gender`, `birthdate`, `address`, `username`, `email`) VALUES(3, 'Anne', 1, '1997-07-15', 'Queenstown Park 10 No. 1, Columbia District', 'anneee', 'anne1@gmail.com');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dtrans`
--
ALTER TABLE `dtrans`
  ADD CONSTRAINT `FK_DTRANS_HTRANS` FOREIGN KEY (`htrans_id`) REFERENCES `htrans` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_DTRANS_ITEM` FOREIGN KEY (`item_id`) REFERENCES `item` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `htrans`
--
ALTER TABLE `htrans`
  ADD CONSTRAINT `FK_HTRANS_USER` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `item`
--
ALTER TABLE `item`
  ADD CONSTRAINT `FK_ITEM_CATEGORY` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
