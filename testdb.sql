-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: baykeshopdb
-- ------------------------------------------------------
-- Server version	8.0.32-0ubuntu0.22.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykebanner`
--

DROP TABLE IF EXISTS `baykeshop_baykebanner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykebanner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `img` varchar(200) NOT NULL,
  `target_url` varchar(200) NOT NULL,
  `desc` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykemenu`
--

DROP TABLE IF EXISTS `baykeshop_baykemenu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykemenu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  `sort` smallint unsigned NOT NULL,
  `parent_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `baykeshop_baykemenu_parent_id_221134be_fk_baykeshop_baykemenu_id` (`parent_id`),
  CONSTRAINT `baykeshop_baykemenu_parent_id_221134be_fk_baykeshop_baykemenu_id` FOREIGN KEY (`parent_id`) REFERENCES `baykeshop_baykemenu` (`id`),
  CONSTRAINT `baykeshop_baykemenu_chk_1` CHECK ((`sort` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeorderinfocomments`
--

DROP TABLE IF EXISTS `baykeshop_baykeorderinfocomments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeorderinfocomments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `object_id` int unsigned NOT NULL,
  `content` varchar(200) NOT NULL,
  `comment_choices` smallint unsigned NOT NULL,
  `content_type_id` int NOT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baykeshop_b_content_386eed_idx` (`content_type_id`,`object_id`),
  KEY `baykeshop_baykeorder_owner_id_40933517_fk_auth_user` (`owner_id`),
  CONSTRAINT `baykeshop_baykeorder_content_type_id_67462782_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `baykeshop_baykeorder_owner_id_40933517_fk_auth_user` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `baykeshop_baykeorderinfocomments_chk_1` CHECK ((`object_id` >= 0)),
  CONSTRAINT `baykeshop_baykeorderinfocomments_chk_2` CHECK ((`comment_choices` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykepermission`
--

DROP TABLE IF EXISTS `baykeshop_baykepermission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykepermission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `url` varchar(150) NOT NULL,
  `icon` varchar(50) NOT NULL,
  `is_show` tinyint(1) NOT NULL,
  `menus_id` bigint NOT NULL,
  `permission_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permission_id` (`permission_id`),
  KEY `baykeshop_baykepermi_menus_id_0f07b3dd_fk_baykeshop` (`menus_id`),
  CONSTRAINT `baykeshop_baykepermi_menus_id_0f07b3dd_fk_baykeshop` FOREIGN KEY (`menus_id`) REFERENCES `baykeshop_baykemenu` (`id`),
  CONSTRAINT `baykeshop_baykepermi_permission_id_0dbf62fe_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshopaddress`
--

DROP TABLE IF EXISTS `baykeshop_baykeshopaddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshopaddress` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  `phone` varchar(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `province` varchar(150) NOT NULL,
  `city` varchar(150) NOT NULL,
  `county` varchar(150) NOT NULL,
  `address` varchar(150) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baykeshop_baykeshopaddress_owner_id_1c0c863a_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `baykeshop_baykeshopaddress_owner_id_1c0c863a_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshopcategory`
--

DROP TABLE IF EXISTS `baykeshop_baykeshopcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshopcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  `icon` varchar(50) NOT NULL,
  `img_map` varchar(200) DEFAULT NULL,
  `desc` varchar(150) NOT NULL,
  `is_home` tinyint(1) NOT NULL,
  `parent_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `baykeshop_baykeshopc_parent_id_e15e8fec_fk_baykeshop` (`parent_id`),
  CONSTRAINT `baykeshop_baykeshopc_parent_id_e15e8fec_fk_baykeshop` FOREIGN KEY (`parent_id`) REFERENCES `baykeshop_baykeshopcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshopingcart`
--

DROP TABLE IF EXISTS `baykeshop_baykeshopingcart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshopingcart` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `num` int unsigned NOT NULL,
  `owner_id` int NOT NULL,
  `sku_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_owner_sku` (`owner_id`,`sku_id`),
  KEY `baykeshop_baykeshopi_sku_id_ae2f75c8_fk_baykeshop` (`sku_id`),
  CONSTRAINT `baykeshop_baykeshopi_sku_id_ae2f75c8_fk_baykeshop` FOREIGN KEY (`sku_id`) REFERENCES `baykeshop_baykeshopsku` (`id`),
  CONSTRAINT `baykeshop_baykeshopingcart_owner_id_9d8be953_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `baykeshop_baykeshopingcart_chk_1` CHECK ((`num` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshoporderinfo`
--

DROP TABLE IF EXISTS `baykeshop_baykeshoporderinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshoporderinfo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `order_sn` varchar(32) NOT NULL,
  `trade_sn` varchar(64) DEFAULT NULL,
  `pay_status` int NOT NULL,
  `pay_method` int DEFAULT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `order_mark` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  `phone` varchar(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `address` varchar(200) NOT NULL,
  `pay_time` datetime(6) DEFAULT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_sn` (`order_sn`),
  UNIQUE KEY `trade_sn` (`trade_sn`),
  KEY `baykeshop_baykeshoporderinfo_owner_id_ae55cd62_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `baykeshop_baykeshoporderinfo_owner_id_ae55cd62_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshopordersku`
--

DROP TABLE IF EXISTS `baykeshop_baykeshopordersku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshopordersku` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `title` varchar(200) NOT NULL,
  `desc` varchar(200) NOT NULL,
  `spec` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `count` int NOT NULL,
  `price` decimal(18,2) NOT NULL,
  `is_commented` tinyint(1) NOT NULL,
  `order_id` bigint NOT NULL,
  `sku_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `baykeshop_baykeshopo_order_id_cb850175_fk_baykeshop` (`order_id`),
  KEY `baykeshop_baykeshopo_sku_id_b2f6c7fe_fk_baykeshop` (`sku_id`),
  CONSTRAINT `baykeshop_baykeshopo_order_id_cb850175_fk_baykeshop` FOREIGN KEY (`order_id`) REFERENCES `baykeshop_baykeshoporderinfo` (`id`),
  CONSTRAINT `baykeshop_baykeshopo_sku_id_b2f6c7fe_fk_baykeshop` FOREIGN KEY (`sku_id`) REFERENCES `baykeshop_baykeshopsku` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshopsku`
--

DROP TABLE IF EXISTS `baykeshop_baykeshopsku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshopsku` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `cover_pic` varchar(200) NOT NULL,
  `price` decimal(8,2) NOT NULL,
  `cost_price` decimal(8,2) NOT NULL,
  `org_price` decimal(8,2) NOT NULL,
  `stock` int NOT NULL,
  `sales` int unsigned NOT NULL,
  `numname` varchar(50) NOT NULL,
  `weight` double NOT NULL,
  `vol` double NOT NULL,
  `spu_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baykeshop_baykeshops_spu_id_99e66bd6_fk_baykeshop` (`spu_id`),
  CONSTRAINT `baykeshop_baykeshops_spu_id_99e66bd6_fk_baykeshop` FOREIGN KEY (`spu_id`) REFERENCES `baykeshop_baykeshopspu` (`id`),
  CONSTRAINT `baykeshop_baykeshopsku_chk_1` CHECK ((`sales` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshopsku_options`
--

DROP TABLE IF EXISTS `baykeshop_baykeshopsku_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshopsku_options` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `baykeshopsku_id` bigint NOT NULL,
  `baykeshopspecoption_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `baykeshop_baykeshopsku_o_baykeshopsku_id_baykesho_9ae1006d_uniq` (`baykeshopsku_id`,`baykeshopspecoption_id`),
  KEY `baykeshop_baykeshops_baykeshopspecoption__6ac951c4_fk_baykeshop` (`baykeshopspecoption_id`),
  CONSTRAINT `baykeshop_baykeshops_baykeshopsku_id_b77612f9_fk_baykeshop` FOREIGN KEY (`baykeshopsku_id`) REFERENCES `baykeshop_baykeshopsku` (`id`),
  CONSTRAINT `baykeshop_baykeshops_baykeshopspecoption__6ac951c4_fk_baykeshop` FOREIGN KEY (`baykeshopspecoption_id`) REFERENCES `baykeshop_baykeshopspecoption` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshopspec`
--

DROP TABLE IF EXISTS `baykeshop_baykeshopspec`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshopspec` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshopspecoption`
--

DROP TABLE IF EXISTS `baykeshop_baykeshopspecoption`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshopspecoption` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `name` varchar(50) NOT NULL,
  `spec_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `baykeshop_baykeshops_spec_id_904bdb5b_fk_baykeshop` (`spec_id`),
  CONSTRAINT `baykeshop_baykeshops_spec_id_904bdb5b_fk_baykeshop` FOREIGN KEY (`spec_id`) REFERENCES `baykeshop_baykeshopspec` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshopspu`
--

DROP TABLE IF EXISTS `baykeshop_baykeshopspu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshopspu` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `title` varchar(150) NOT NULL,
  `keywords` varchar(150) NOT NULL,
  `desc` varchar(200) NOT NULL,
  `unit` varchar(50) NOT NULL,
  `cover_pic` varchar(200) NOT NULL,
  `freight` decimal(5,2) NOT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeshopspu_category`
--

DROP TABLE IF EXISTS `baykeshop_baykeshopspu_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeshopspu_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `baykeshopspu_id` bigint NOT NULL,
  `baykeshopcategory_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `baykeshop_baykeshopspu_c_baykeshopspu_id_baykesho_8f541fd8_uniq` (`baykeshopspu_id`,`baykeshopcategory_id`),
  KEY `baykeshop_baykeshops_baykeshopcategory_id_5ec1deb6_fk_baykeshop` (`baykeshopcategory_id`),
  CONSTRAINT `baykeshop_baykeshops_baykeshopcategory_id_5ec1deb6_fk_baykeshop` FOREIGN KEY (`baykeshopcategory_id`) REFERENCES `baykeshop_baykeshopcategory` (`id`),
  CONSTRAINT `baykeshop_baykeshops_baykeshopspu_id_0a24caaf_fk_baykeshop` FOREIGN KEY (`baykeshopspu_id`) REFERENCES `baykeshop_baykeshopspu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykespucarousel`
--

DROP TABLE IF EXISTS `baykeshop_baykespucarousel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykespucarousel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `img` varchar(200) NOT NULL,
  `target_url` varchar(200) NOT NULL,
  `desc` varchar(150) NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baykeshop_baykespuca_product_id_2ca53137_fk_baykeshop` (`product_id`),
  CONSTRAINT `baykeshop_baykespuca_product_id_2ca53137_fk_baykeshop` FOREIGN KEY (`product_id`) REFERENCES `baykeshop_baykeshopspu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeupload`
--

DROP TABLE IF EXISTS `baykeshop_baykeupload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeupload` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `img` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeuserbalancelog`
--

DROP TABLE IF EXISTS `baykeshop_baykeuserbalancelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeuserbalancelog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `amount` decimal(15,2) NOT NULL,
  `change_status` smallint unsigned DEFAULT NULL,
  `change_way` smallint unsigned NOT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `baykeshop_baykeuserbalancelog_owner_id_7de12bb5_fk_auth_user_id` (`owner_id`),
  CONSTRAINT `baykeshop_baykeuserbalancelog_owner_id_7de12bb5_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `baykeshop_baykeuserbalancelog_chk_1` CHECK ((`change_status` >= 0)),
  CONSTRAINT `baykeshop_baykeuserbalancelog_chk_2` CHECK ((`change_way` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `baykeshop_baykeuserinfo`
--

DROP TABLE IF EXISTS `baykeshop_baykeuserinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `baykeshop_baykeuserinfo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `add_date` datetime(6) NOT NULL,
  `pub_date` datetime(6) NOT NULL,
  `is_del` tinyint(1) NOT NULL,
  `avatar` varchar(200) NOT NULL,
  `nickname` varchar(30) NOT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `balance` decimal(8,2) NOT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `owner_id` (`owner_id`),
  UNIQUE KEY `phone` (`phone`),
  CONSTRAINT `baykeshop_baykeuserinfo_owner_id_0a438220_fk_auth_user_id` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-03-16 10:06:59
