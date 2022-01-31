-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 31, 2022 at 08:29 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fms`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `getCategoryTypeInflow` (IN `inp` VARCHAR(50))  SELECT catname,catdesc FROM category WHERE cattype=inp$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `getCategoryTypeOutflow` (IN `inp` VARCHAR(50))  SELECT catname,catdesc FROM category WHERE cattype=inp$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `getUsers` ()  SELECT * FROM USER$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `catid` int(11) NOT NULL,
  `catname` varchar(50) NOT NULL,
  `catdesc` varchar(100) NOT NULL,
  `cattype` varchar(50) NOT NULL,
  `catparentid` int(11) DEFAULT NULL,
  `userid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`catid`, `catname`, `catdesc`, `cattype`, `catparentid`, `userid`) VALUES
(2, 'INCOME', 'INCOME', 'INFLOW', NULL, 1),
(6, 'EMPLOYMENT', 'EMPLOYMENT', 'INFLOW', NULL, 1),
(8, 'SALARY', 'SALARY', 'INFLOW', 6, 1),
(9, 'PROPERTY', 'PROPERTY', 'INFLOW', NULL, 1),
(10, 'BUSINESS', 'BUSINESS', 'INFLOW', NULL, 1),
(11, 'RENT', 'RENT', 'INFLOW', 9, 1),
(12, 'CHARITY', 'CHARITY', 'OUTFLOW', NULL, 1),
(13, 'COMMUNICATION', 'COMMUNICATION', 'OUTFLOW', NULL, 1),
(14, 'INTERNET', 'INTERNET', 'OUTFLOW', 13, 1),
(15, 'UTILITY', 'UTILITY', 'OUTFLOW', NULL, 1),
(16, 'GAS', 'GAS', 'OUTFLOW', 15, 1),
(17, 'MILK', 'MILK', 'OUTFLOW', 15, 1),
(30, 'WATERBILL', 'WATERBILL', 'OUTFLOW', 15, 1),
(32, 'ENTERTAINMENT', 'ENTERTAINMENT', 'OUTFLOW', NULL, 2),
(33, 'CINEMA', 'CINEMA', 'OUTFLOW', 32, 2),
(34, 'AUTOMOBILE', 'AUTOMOBILE', 'OUTFLOW', 15, 1),
(39, 'CINEMA', 'CINEMA', 'OUTFLOW', 38, 1);

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `paymentid` int(11) NOT NULL,
  `paymenttype` varchar(50) NOT NULL,
  `paymentmode` varchar(50) NOT NULL,
  `paymentdescription` varchar(50) NOT NULL,
  `userid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`paymentid`, `paymenttype`, `paymentmode`, `paymentdescription`, `userid`) VALUES
(3, 'WALLET/UPI', 'PHONE PAY', 'UTR', 1),
(4, 'WALLET/UPI', 'GPAY', 'UTR', 2),
(5, 'WALLET/UPI', 'PHONE PAY', 'UTR', 1);

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `transid` int(11) NOT NULL,
  `catid` int(11) NOT NULL,
  `venid` int(11) NOT NULL,
  `paymentid` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `transdate` date NOT NULL,
  `transdetails` varchar(100) NOT NULL,
  `particulars` varchar(100) NOT NULL,
  `remarks` varchar(100) NOT NULL,
  `createdon` datetime DEFAULT NULL,
  `modifiedon` datetime DEFAULT NULL,
  `userid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`transid`, `catid`, `venid`, `paymentid`, `amount`, `transdate`, `transdetails`, `particulars`, `remarks`, `createdon`, `modifiedon`, `userid`) VALUES
(3, 33, 4, 3, 150, '2022-01-20', 'MOVIE', 'MOVIE', 'GOOD', '2022-01-20 13:00:55', '0000-00-00 00:00:00', 1),
(5, 33, 7, 3, 160, '2022-01-28', 'movie', 'movie', 'movie', '2022-01-28 23:29:55', NULL, 1),
(6, 15, 3, 3, 20, '2022-01-28', 'utility', 'utility', 'utility', '2022-01-28 23:31:34', NULL, 1),
(7, 17, 3, 3, 50, '2022-01-28', 'milk', 'milk', 'milk', '2022-01-28 23:32:07', NULL, 1),
(8, 17, 3, 3, 10, '2022-01-28', 'milk', 'milk', 'milk', '2022-01-28 23:33:09', '2022-01-31 22:27:10', 1),
(10, 16, 3, 3, 900, '2022-01-31', 'GAS', 'GAS', 'GAS', '2022-01-31 22:02:50', '2022-01-31 22:27:06', 1),
(11, 39, 7, 3, 350, '2022-02-01', 'MOVIE', 'CINEMA', 'CINEMA', '2022-02-01 00:53:15', '2022-02-01 00:53:24', 1);

-- --------------------------------------------------------

--
-- Table structure for table `trigr`
--

CREATE TABLE `trigr` (
  `tid` int(11) NOT NULL,
  `venid` int(11) NOT NULL,
  `venname` varchar(50) NOT NULL,
  `venloc` varchar(50) NOT NULL,
  `action` varchar(50) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `trigr`
--

INSERT INTO `trigr` (`tid`, `venid`, `venname`, `venloc`, `action`, `timestamp`) VALUES
(1, 9, 'AMAZON', 'INDIA', 'VENDOR INSERTED', '2022-02-01 00:09:41'),
(2, 9, 'FLIPKART', 'INDIA', 'VENDOR UPDATED', '2022-02-01 00:13:33'),
(3, 9, 'FLIPKART', 'INDIA', 'VENDOR DELETED', '2022-02-01 00:17:08'),
(4, 10, 'BOOK MY SHOW', 'MYSORE', 'VENDOR INSERTED', '2022-02-01 00:50:45'),
(5, 10, 'BOOK MY SHOW', 'INDIA', 'VENDOR UPDATED', '2022-02-01 00:50:54'),
(6, 10, 'BOOK MY SHOW', 'INDIA', 'VENDOR DELETED', '2022-02-01 00:50:57'),
(7, 2, 'MYNTRA', 'INDIA', 'VENDOR UPDATED', '2022-02-01 00:51:20');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`) VALUES
(1, 'sachin', 'hmsachin13@gmail.com', 'pbkdf2:sha256:260000$C4KhWQEr9kUubBcG$fe885c28f7d029d1c645e17788a3f196a29a610181a4af678046f7912b61bc66'),
(2, 'abcd', 'abcd@gmail.com', 'pbkdf2:sha256:260000$PbKRFHGVb7R1YG79$de48d63da1c4b9d1b9c0523f106ddbff14989eb47faa8259c099b22c6d03037e'),
(4, '123', '123@gmail.com', 'pbkdf2:sha256:260000$UusUWHXLAcqZEcKT$dc2c71bb00d4736c098091978aed98cf185ac681b049748afb204303a8554193');

-- --------------------------------------------------------

--
-- Table structure for table `vendor`
--

CREATE TABLE `vendor` (
  `venid` int(11) NOT NULL,
  `venname` varchar(50) NOT NULL,
  `venloc` varchar(50) NOT NULL,
  `createdon` datetime DEFAULT NULL,
  `modifiedon` datetime DEFAULT NULL,
  `userid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `vendor`
--

INSERT INTO `vendor` (`venid`, `venname`, `venloc`, `createdon`, `modifiedon`, `userid`) VALUES
(2, 'MYNTRA', 'INDIA', '2022-01-17 01:02:00', '2022-02-01 00:51:20', 1),
(3, 'LOYAL WORLD', 'INDIA', '2022-01-17 01:02:09', '2022-01-17 01:02:19', 1),
(4, 'BOOK MY SHOW', 'INDIA', '2022-01-17 22:56:13', NULL, 2),
(5, 'BIGBASKET', 'INDIA', '2022-01-19 00:02:13', '2022-01-19 00:02:22', 1),
(7, 'BOOK MY SHOW', 'MYSORE', '2022-01-20 17:44:51', '2022-01-20 17:47:32', 1);

--
-- Triggers `vendor`
--
DELIMITER $$
CREATE TRIGGER `vendor deleted` BEFORE DELETE ON `vendor` FOR EACH ROW INSERT INTO `trigr` VALUES(null,OLD.venid,OLD.venname,OLD.venloc,'VENDOR DELETED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `vendor insertion` AFTER INSERT ON `vendor` FOR EACH ROW INSERT INTO `trigr` VALUES(null,NEW.venid,NEW.venname,NEW.venloc,'VENDOR INSERTED',NOW())
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `vendor updation` AFTER UPDATE ON `vendor` FOR EACH ROW INSERT INTO `trigr` VALUES(null,NEW.venid,NEW.venname,NEW.venloc,'VENDOR UPDATED',NOW())
$$
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`catid`),
  ADD KEY `cat parent relation` (`catparentid`),
  ADD KEY `user cat` (`userid`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`paymentid`),
  ADD KEY `userpay relation` (`userid`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
  ADD PRIMARY KEY (`transid`),
  ADD KEY `cat trans` (`catid`),
  ADD KEY `ven trans` (`venid`),
  ADD KEY `pay trans` (`paymentid`),
  ADD KEY `user trans` (`userid`);

--
-- Indexes for table `trigr`
--
ALTER TABLE `trigr`
  ADD PRIMARY KEY (`tid`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `vendor`
--
ALTER TABLE `vendor`
  ADD PRIMARY KEY (`venid`),
  ADD KEY `user ven relation` (`userid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `catid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `paymentid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `transid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `trigr`
--
ALTER TABLE `trigr`
  MODIFY `tid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `vendor`
--
ALTER TABLE `vendor`
  MODIFY `venid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
