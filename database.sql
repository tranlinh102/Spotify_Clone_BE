CREATE DATABASE  IF NOT EXISTS `spotify` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `spotify`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: spotify
-- ------------------------------------------------------
-- Server version	9.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `album_favorites`
--

DROP TABLE IF EXISTS `album_favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `album_favorites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `album_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `album_favorites_user_id_album_id_54110d29_uniq` (`user_id`,`album_id`),
  KEY `album_favorites_album_id_99824288_fk_albums_album_id` (`album_id`),
  CONSTRAINT `album_favorites_album_id_99824288_fk_albums_album_id` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`),
  CONSTRAINT `album_favorites_user_id_cc87370a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `album_favorites`
--

LOCK TABLES `album_favorites` WRITE;
/*!40000 ALTER TABLE `album_favorites` DISABLE KEYS */;
/*!40000 ALTER TABLE `album_favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `album_songs`
--

DROP TABLE IF EXISTS `album_songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `album_songs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `added_at` datetime(6) NOT NULL,
  `album_id` int NOT NULL,
  `song_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `album_songs_album_id_song_id_4cff9aec_uniq` (`album_id`,`song_id`),
  KEY `album_songs_song_id_49167b9d_fk_songs_song_id` (`song_id`),
  CONSTRAINT `album_songs_album_id_3250027a_fk_albums_album_id` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`),
  CONSTRAINT `album_songs_song_id_49167b9d_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `album_songs`
--

LOCK TABLES `album_songs` WRITE;
/*!40000 ALTER TABLE `album_songs` DISABLE KEYS */;
INSERT INTO `album_songs` VALUES (1,'2025-05-03 08:31:35.575750',1,1),(2,'2025-05-03 08:31:44.027036',1,2),(3,'2025-05-03 08:31:53.040752',1,3),(4,'2025-05-03 08:33:09.841804',7,8),(5,'2025-05-03 08:33:45.195437',7,9),(6,'2025-05-03 08:34:11.767867',2,1),(7,'2025-05-03 08:34:20.305061',2,4),(8,'2025-05-03 08:34:58.731984',6,5),(9,'2025-05-03 08:35:02.721663',6,6),(10,'2025-05-03 08:35:06.311568',6,7),(11,'2025-05-04 13:44:26.255261',1,4);
/*!40000 ALTER TABLE `album_songs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `albums`
--

DROP TABLE IF EXISTS `albums`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `albums` (
  `album_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `artist_id` int NOT NULL,
  PRIMARY KEY (`album_id`),
  KEY `albums_artist_id_8a9e6bb4_fk_artists_artist_id` (`artist_id`),
  CONSTRAINT `albums_artist_id_8a9e6bb4_fk_artists_artist_id` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `albums`
--

LOCK TABLES `albums` WRITE;
/*!40000 ALTER TABLE `albums` DISABLE KEYS */;
INSERT INTO `albums` VALUES (1,'SKY','image/Có_chắc_yêu_là_đây.jpg','2025-05-03 07:03:34.208126',1),(2,'SKY_TOUR','image/Chúng_ta_của_tương_lai.jpg','2025-05-03 07:04:05.335561',1),(3,'SƠN TÙNG','image/Sơn_Tùng_MTP_rKpgTuk.jpg','2025-05-03 07:04:28.901814',1),(4,'Bật nó lên','image/Ai_mà_biết_được.jpg','2025-05-03 07:07:12.320351',2),(5,'Soobin','image/Giá_như.jpg','2025-05-03 07:08:01.114215',2),(6,'PMQ','image/Phan_mạnh_quỳnh_rBXLQ4y.jpg','2025-05-03 07:08:34.779460',3),(7,'Bắc Bling','image/Hòa_Minzy_xxjUR7w.jpg','2025-05-03 07:08:52.357422',4);
/*!40000 ALTER TABLE `albums` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artist_songs`
--

DROP TABLE IF EXISTS `artist_songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `artist_songs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `main_artist` tinyint(1) NOT NULL,
  `added_at` datetime(6) NOT NULL,
  `artist_id` int NOT NULL,
  `song_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `artist_songs_artist_id_song_id_893d0a8e_uniq` (`artist_id`,`song_id`),
  KEY `artist_songs_song_id_32762766_fk_songs_song_id` (`song_id`),
  CONSTRAINT `artist_songs_artist_id_e8c6135e_fk_artists_artist_id` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`),
  CONSTRAINT `artist_songs_song_id_32762766_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artist_songs`
--

LOCK TABLES `artist_songs` WRITE;
/*!40000 ALTER TABLE `artist_songs` DISABLE KEYS */;
INSERT INTO `artist_songs` VALUES (1,1,'2025-05-03 07:46:20.620654',1,1),(2,1,'2025-05-03 07:52:52.641606',1,2),(3,1,'2025-05-03 07:55:17.961919',1,3),(4,1,'2025-05-03 07:56:36.299024',1,4),(5,1,'2025-05-03 07:58:23.609655',3,5),(6,1,'2025-05-03 08:00:31.401702',3,6),(7,1,'2025-05-03 08:01:21.222974',3,7),(8,1,'2025-05-03 08:03:14.706133',4,8),(9,0,'2025-05-03 08:03:14.747658',5,8),(10,0,'2025-05-03 08:03:14.769922',6,8),(11,1,'2025-05-03 08:05:39.830427',4,9),(12,1,'2025-05-03 08:06:31.360421',4,10),(13,0,'2025-05-03 08:06:31.384104',6,10),(14,1,'2025-05-03 08:36:47.957241',2,11);
/*!40000 ALTER TABLE `artist_songs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artists`
--

DROP TABLE IF EXISTS `artists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `artists` (
  `artist_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `bio` longtext COLLATE utf8mb4_general_ci,
  `image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`artist_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artists`
--

LOCK TABLES `artists` WRITE;
/*!40000 ALTER TABLE `artists` DISABLE KEYS */;
INSERT INTO `artists` VALUES (1,'Sơn Tùng MTP','Welcome to bio Sơn Tùng MTP','image/Sơn_Tùng_MTP.jpg','2025-05-03 06:26:46.942922'),(2,'Soobin Hoàng Sơn','Welcome  to my bio','image/Soobin.jpg','2025-05-03 06:57:13.500311'),(3,'Phan Mạnh Quỳnh','My bio','image/Phan_mạnh_quỳnh.jpg','2025-05-03 06:58:18.036075'),(4,'Hòa minzy','Welcome to my bio','image/Hòa_Minzy.jpg','2025-05-03 06:59:00.620450'),(5,'NS Xuân Hinh','Nghệ sĩ nhân dân','image/NS_Xuân_Hinh.jpg','2025-05-03 06:59:30.009388'),(6,'Masew','Nhạc sĩ','image/Masew.jpg','2025-05-03 07:00:21.802233');
/*!40000 ALTER TABLE `artists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add user',3,'add_user'),(10,'Can change user',3,'change_user'),(11,'Can delete user',3,'delete_user'),(12,'Can view user',3,'view_user'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add log entry',5,'add_logentry'),(18,'Can change log entry',5,'change_logentry'),(19,'Can delete log entry',5,'delete_logentry'),(20,'Can view log entry',5,'view_logentry'),(21,'Can add artist',6,'add_artist'),(22,'Can change artist',6,'change_artist'),(23,'Can delete artist',6,'delete_artist'),(24,'Can view artist',6,'view_artist'),(25,'Can add song',7,'add_song'),(26,'Can change song',7,'change_song'),(27,'Can delete song',7,'delete_song'),(28,'Can view song',7,'view_song'),(29,'Can add album',8,'add_album'),(30,'Can change album',8,'change_album'),(31,'Can delete album',8,'delete_album'),(32,'Can view album',8,'view_album'),(33,'Can add message',9,'add_message'),(34,'Can change message',9,'change_message'),(35,'Can delete message',9,'delete_message'),(36,'Can view message',9,'view_message'),(37,'Can add playlist',10,'add_playlist'),(38,'Can change playlist',10,'change_playlist'),(39,'Can delete playlist',10,'delete_playlist'),(40,'Can view playlist',10,'view_playlist'),(41,'Can add follower',11,'add_follower'),(42,'Can change follower',11,'change_follower'),(43,'Can delete follower',11,'delete_follower'),(44,'Can view follower',11,'view_follower'),(45,'Can add playlist song',12,'add_playlistsong'),(46,'Can change playlist song',12,'change_playlistsong'),(47,'Can delete playlist song',12,'delete_playlistsong'),(48,'Can view playlist song',12,'view_playlistsong'),(49,'Can add favorite',13,'add_favorite'),(50,'Can change favorite',13,'change_favorite'),(51,'Can delete favorite',13,'delete_favorite'),(52,'Can view favorite',13,'view_favorite'),(53,'Can add download',14,'add_download'),(54,'Can change download',14,'change_download'),(55,'Can delete download',14,'delete_download'),(56,'Can view download',14,'view_download'),(57,'Can add artist song',15,'add_artistsong'),(58,'Can change artist song',15,'change_artistsong'),(59,'Can delete artist song',15,'delete_artistsong'),(60,'Can view artist song',15,'view_artistsong'),(61,'Can add album song',16,'add_albumsong'),(62,'Can change album song',16,'change_albumsong'),(63,'Can delete album song',16,'delete_albumsong'),(64,'Can view album song',16,'view_albumsong'),(65,'Can add chat room',17,'add_chatroom'),(66,'Can change chat room',17,'change_chatroom'),(67,'Can delete chat room',17,'delete_chatroom'),(68,'Can view chat room',17,'view_chatroom'),(69,'Can add chat message',18,'add_chatmessage'),(70,'Can change chat message',18,'change_chatmessage'),(71,'Can delete chat message',18,'delete_chatmessage'),(72,'Can view chat message',18,'view_chatmessage'),(73,'Can add album favorite',19,'add_albumfavorite'),(74,'Can change album favorite',19,'change_albumfavorite'),(75,'Can delete album favorite',19,'delete_albumfavorite'),(76,'Can view album favorite',19,'view_albumfavorite'),(77,'Can add playlist favorite',20,'add_playlistfavorite'),(78,'Can change playlist favorite',20,'change_playlistfavorite'),(79,'Can delete playlist favorite',20,'delete_playlistfavorite'),(80,'Can view playlist favorite',20,'view_playlistfavorite');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$MfCZiazVVskGo083Oq7luL$xTU+FSVWrnPv1pMppwE4m34gAO59Tx/RxLKtIY7dD7o=',NULL,1,'admin','','','admin@gmail.com',1,1,'2025-04-21 15:34:16.582349'),(2,'pbkdf2_sha256$1000000$dzM2GoStTqrXRiBozaf6f2$TCaqmHBUcmnEytjKTUYP0W3SLr5LpvAALFvxenxDzaI=',NULL,0,'linh','','','linhtranvo2003@gmail.com',0,1,'2025-04-24 14:04:16.657189'),(3,'pbkdf2_sha256$1000000$8wGcfIXNIB13iHdhwn1goP$RH9C+27eL8mO463B5lYrbLijlhRwZ2VQ0nDReMBDqQ4=',NULL,1,'DuyKhanh','','','khanh@gmail.com',1,1,'2025-05-03 06:24:38.970464'),(4,'pbkdf2_sha256$1000000$0X7sU7G9FSeZ4IlBpCf7ox$Cv2JsY/GmS/veVAb4yfAoHq5TDU6vbMDV4gJYS6pFDw=',NULL,0,'user1','','','user1@example.com',0,1,'2025-05-03 08:22:02.416299'),(5,'pbkdf2_sha256$1000000$g9ufBnnMFPAs55XYsCXDnA$f2P4QYZ9de4aym8YzJGJhUUniJ2ZOqlYA0dnNtpT4gM=',NULL,0,'user2','','','user2@example.com',0,1,'2025-05-03 08:22:03.282481'),(6,'pbkdf2_sha256$1000000$mubzWkT6wqlZZDNZO64pNT$3hFA5Ss8pUpJH1IlWg82oI9mcpTWSVNEmlKQu6Nq7Sw=',NULL,0,'user3','','','user3@example.com',0,1,'2025-05-03 08:22:04.098884'),(7,'pbkdf2_sha256$1000000$bIWML6b24UmIQ5RrE1grJp$5yqeSlR9EDIvfLoN/TOvyDe57kVQOzYuTvGulh7Bo5Q=',NULL,0,'user4','','','user4@example.com',0,1,'2025-05-03 08:22:04.919377'),(8,'pbkdf2_sha256$1000000$zDPVfkPOrF0mFsd2LLkKpT$6LsA9U4WLQL9eOWTmrzM24etr4o+oLCYgUqX5j9J1Yc=',NULL,0,'user5','','','user5@example.com',0,1,'2025-05-03 08:22:05.768692'),(9,'pbkdf2_sha256$1000000$snY0mUU7k67pRiEAJAjXFz$R6JHTL+lvexnfVOfUs4qWjaylGrV41+OOWZCW8GWdnY=',NULL,0,'user6','','','user6@example.com',0,1,'2025-05-03 08:22:06.624969'),(10,'pbkdf2_sha256$1000000$zg30mI9vCA6DB8uGFK0TZR$6QlCkvbYoJQJU8ygunvJ9q4qQ3PUAKvmtu3mrA1P6mk=',NULL,0,'user7','','','user7@example.com',0,1,'2025-05-03 08:22:07.431870'),(11,'pbkdf2_sha256$1000000$YSp5IVB9qahHhFfB2R2GtU$trIlhJHRxOmqZ/hfKzq6rVk2Sxr8NrAeD95G2tJLX5U=',NULL,0,'user8','','','user8@example.com',0,1,'2025-05-03 08:22:08.257816'),(12,'pbkdf2_sha256$1000000$1pDXKWYAC20lTIIYv3iFnr$JS/6Garhls3atfDv/w1T5f9QhaTAJU6SmC9dhtEmD2Q=',NULL,0,'user9','','','user9@example.com',0,1,'2025-05-03 08:22:09.073330'),(13,'pbkdf2_sha256$1000000$p35EhyM5zx5WnII8baOxrU$krdSQCcsLPuJjMxjUfZwagaHPsGa4j5llWRDNivdH7I=',NULL,0,'user10','','','user10@example.com',0,1,'2025-05-03 08:22:09.891981'),(14,'pbkdf2_sha256$1000000$D8EGwsCA6svdhuBEUS0VLW$EeDkdsrTGZ0T4b6kG+vK8EX7QtOSK3MO3C1cjSx/pDg=',NULL,0,'user11','','','user11@example.com',0,1,'2025-05-03 08:22:10.704700'),(15,'pbkdf2_sha256$1000000$JOp4y8TO9rHstdN9CX73bC$ixiLJ+OGlSZ0xXyj5BVXftD5GaSx1Wbxj/koM39p+Gc=',NULL,0,'user12','','','user12@example.com',0,1,'2025-05-03 08:22:11.526503'),(16,'pbkdf2_sha256$1000000$SYrazyofM7t2BU8yhTWd7B$FICSgmVMNGkWtB91HIpefpdx0EVPV3MOITxp+3DzWm0=',NULL,0,'user13','','','user13@example.com',0,1,'2025-05-03 08:22:12.368288'),(17,'pbkdf2_sha256$1000000$RF9hOM3KHmxZPL74IbOLvN$O6Yz7pW4IsKMg55nM9U12Zs5k+1JRAC4N2BQGvjHxYs=',NULL,0,'user14','','','user14@example.com',0,1,'2025-05-03 08:22:13.201504'),(18,'pbkdf2_sha256$1000000$nmBtMtkkBt7WX0MUICg3lR$epZVDLdqISkVPQ5jW3RFOMvc7Vupg1dVVffrMkg1Vo4=',NULL,0,'user15','','','user15@example.com',0,1,'2025-05-03 08:22:14.035673');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chatmessages`
--

DROP TABLE IF EXISTS `chatmessages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chatmessages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `srcfile` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sender_id` int NOT NULL,
  `song_id` int DEFAULT NULL,
  `chatroom_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chatmessages_sender_id_950a0f14_fk_auth_user_id` (`sender_id`),
  KEY `chatmessages_song_id_74a4bcae_fk_songs_song_id` (`song_id`),
  KEY `chatmessages_chatroom_id_f3f72455_fk_chatrooms_id` (`chatroom_id`),
  CONSTRAINT `chatmessages_chatroom_id_f3f72455_fk_chatrooms_id` FOREIGN KEY (`chatroom_id`) REFERENCES `chatrooms` (`id`),
  CONSTRAINT `chatmessages_sender_id_950a0f14_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `chatmessages_song_id_74a4bcae_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatmessages`
--

LOCK TABLES `chatmessages` WRITE;
/*!40000 ALTER TABLE `chatmessages` DISABLE KEYS */;
/*!40000 ALTER TABLE `chatmessages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chatrooms`
--

DROP TABLE IF EXISTS `chatrooms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chatrooms` (
  `id` int NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `user1_id` int NOT NULL,
  `user2_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `chatrooms_user1_id_2e325bba_fk_auth_user_id` (`user1_id`),
  KEY `chatrooms_user2_id_61d31a3d_fk_auth_user_id` (`user2_id`),
  CONSTRAINT `chatrooms_user1_id_2e325bba_fk_auth_user_id` FOREIGN KEY (`user1_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `chatrooms_user2_id_61d31a3d_fk_auth_user_id` FOREIGN KEY (`user2_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatrooms`
--

LOCK TABLES `chatrooms` WRITE;
/*!40000 ALTER TABLE `chatrooms` DISABLE KEYS */;
/*!40000 ALTER TABLE `chatrooms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_general_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_general_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (5,'admin','logentry'),(2,'auth','group'),(1,'auth','permission'),(3,'auth','user'),(4,'contenttypes','contenttype'),(8,'manager','album'),(19,'manager','albumfavorite'),(16,'manager','albumsong'),(6,'manager','artist'),(15,'manager','artistsong'),(18,'manager','chatmessage'),(17,'manager','chatroom'),(14,'manager','download'),(13,'manager','favorite'),(11,'manager','follower'),(9,'manager','message'),(10,'manager','playlist'),(20,'manager','playlistfavorite'),(12,'manager','playlistsong'),(7,'manager','song');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-21 14:40:02.832630'),(2,'auth','0001_initial','2025-04-21 14:40:03.294836'),(3,'admin','0001_initial','2025-04-21 14:40:03.410691'),(4,'admin','0002_logentry_remove_auto_add','2025-04-21 14:40:03.415513'),(5,'admin','0003_logentry_add_action_flag_choices','2025-04-21 14:40:03.426243'),(6,'contenttypes','0002_remove_content_type_name','2025-04-21 14:40:03.492897'),(7,'auth','0002_alter_permission_name_max_length','2025-04-21 14:40:03.533241'),(8,'auth','0003_alter_user_email_max_length','2025-04-21 14:40:03.556562'),(9,'auth','0004_alter_user_username_opts','2025-04-21 14:40:03.564566'),(10,'auth','0005_alter_user_last_login_null','2025-04-21 14:40:03.604335'),(11,'auth','0006_require_contenttypes_0002','2025-04-21 14:40:03.606334'),(12,'auth','0007_alter_validators_add_error_messages','2025-04-21 14:40:03.614367'),(13,'auth','0008_alter_user_username_max_length','2025-04-21 14:40:03.642272'),(14,'auth','0009_alter_user_last_name_max_length','2025-04-21 14:40:03.665007'),(15,'auth','0010_alter_group_name_max_length','2025-04-21 14:40:03.685546'),(16,'auth','0011_update_proxy_permissions','2025-04-21 14:40:03.694550'),(17,'auth','0012_alter_user_first_name_max_length','2025-04-21 14:40:03.716237'),(18,'manager','0001_initial','2025-04-21 14:40:04.618186'),(19,'manager','0002_song_duration_alter_album_image_alter_artist_image_and_more','2025-05-04 13:41:54.398248');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `downloads`
--

DROP TABLE IF EXISTS `downloads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `downloads` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `downloaded_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `song_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `downloads_user_id_song_id_e246188a_uniq` (`user_id`,`song_id`),
  KEY `downloads_song_id_4177d846_fk_songs_song_id` (`song_id`),
  CONSTRAINT `downloads_song_id_4177d846_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`),
  CONSTRAINT `downloads_user_id_2b9b2559_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `downloads`
--

LOCK TABLES `downloads` WRITE;
/*!40000 ALTER TABLE `downloads` DISABLE KEYS */;
/*!40000 ALTER TABLE `downloads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `added_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `song_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `favorites_user_id_song_id_703788fc_uniq` (`user_id`,`song_id`),
  KEY `favorites_song_id_b4ee1f74_fk_songs_song_id` (`song_id`),
  CONSTRAINT `favorites_song_id_b4ee1f74_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`),
  CONSTRAINT `favorites_user_id_d60eb79f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
INSERT INTO `favorites` VALUES (1,'2025-05-03 15:28:59.000000',4,1),(2,'2025-05-03 15:28:59.000000',4,3),(3,'2025-05-03 15:28:59.000000',4,5),(4,'2025-05-03 15:28:59.000000',5,2),(5,'2025-05-03 15:28:59.000000',5,4),(6,'2025-05-03 15:28:59.000000',5,6),(7,'2025-05-03 15:28:59.000000',6,1),(8,'2025-05-03 15:28:59.000000',6,7),(9,'2025-05-03 15:28:59.000000',6,9),(10,'2025-05-03 15:28:59.000000',7,3),(11,'2025-05-03 15:28:59.000000',7,6),(12,'2025-05-03 15:28:59.000000',7,10),(13,'2025-05-03 15:28:59.000000',8,2),(14,'2025-05-03 15:28:59.000000',8,5),(15,'2025-05-03 15:28:59.000000',8,8),(16,'2025-05-03 15:28:59.000000',4,10),(17,'2025-05-03 15:28:59.000000',5,7),(18,'2025-05-03 15:28:59.000000',6,4),(19,'2025-05-03 15:28:59.000000',7,8),(20,'2025-05-03 15:28:59.000000',8,6),(21,'2025-05-03 15:28:59.000000',4,2),(22,'2025-05-03 15:28:59.000000',5,1),(23,'2025-05-03 15:28:59.000000',6,5),(24,'2025-05-03 15:28:59.000000',7,1),(25,'2025-05-03 15:28:59.000000',8,3),(26,'2025-05-03 15:28:59.000000',4,6),(27,'2025-05-03 15:28:59.000000',5,9),(28,'2025-05-03 15:28:59.000000',6,10),(29,'2025-05-03 15:28:59.000000',7,2),(30,'2025-05-03 15:28:59.000000',8,4);
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `followers`
--

DROP TABLE IF EXISTS `followers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `followers` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `followed_at` datetime(6) NOT NULL,
  `artist_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `followers_user_id_artist_id_fb1f7902_uniq` (`user_id`,`artist_id`),
  KEY `followers_artist_id_560f1ea7_fk_artists_artist_id` (`artist_id`),
  CONSTRAINT `followers_artist_id_560f1ea7_fk_artists_artist_id` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`),
  CONSTRAINT `followers_user_id_556252d5_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `followers`
--

LOCK TABLES `followers` WRITE;
/*!40000 ALTER TABLE `followers` DISABLE KEYS */;
INSERT INTO `followers` VALUES (1,'2025-05-03 15:30:39.000000',1,4),(2,'2025-05-03 15:30:39.000000',2,4),(3,'2025-05-03 15:30:39.000000',3,5),(4,'2025-05-03 15:30:39.000000',4,5),(5,'2025-05-03 15:30:39.000000',5,6),(6,'2025-05-03 15:30:39.000000',6,6),(7,'2025-05-03 15:30:39.000000',1,7),(8,'2025-05-03 15:30:39.000000',2,7),(9,'2025-05-03 15:30:39.000000',3,8),(10,'2025-05-03 15:30:39.000000',4,8),(11,'2025-05-03 15:30:39.000000',5,4),(12,'2025-05-03 15:30:39.000000',6,4),(13,'2025-05-03 15:30:39.000000',1,5),(14,'2025-05-03 15:30:39.000000',2,5),(15,'2025-05-03 15:30:39.000000',3,6),(16,'2025-05-03 15:30:39.000000',4,6),(17,'2025-05-03 15:30:39.000000',5,7),(18,'2025-05-03 15:30:39.000000',6,7),(19,'2025-05-03 15:30:39.000000',1,8),(20,'2025-05-03 15:30:39.000000',2,8),(21,'2025-05-03 15:30:39.000000',3,4),(22,'2025-05-03 15:30:39.000000',4,4),(23,'2025-05-03 15:30:39.000000',5,5),(24,'2025-05-03 15:30:39.000000',6,5),(25,'2025-05-03 15:30:39.000000',1,6),(26,'2025-05-03 15:30:39.000000',2,6),(27,'2025-05-03 15:30:39.000000',3,7),(28,'2025-05-03 15:30:39.000000',4,7),(29,'2025-05-03 15:30:39.000000',5,8),(30,'2025-05-03 15:30:39.000000',6,8);
/*!40000 ALTER TABLE `followers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `message_text` longtext COLLATE utf8mb4_general_ci,
  `sent_at` datetime(6) NOT NULL,
  `receiver_id` int NOT NULL,
  `sender_id` int NOT NULL,
  PRIMARY KEY (`message_id`),
  KEY `messages_receiver_id_874b4e0a_fk_auth_user_id` (`receiver_id`),
  KEY `messages_sender_id_dc5a0bbd_fk_auth_user_id` (`sender_id`),
  CONSTRAINT `messages_receiver_id_874b4e0a_fk_auth_user_id` FOREIGN KEY (`receiver_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `messages_sender_id_dc5a0bbd_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlist_favorites`
--

DROP TABLE IF EXISTS `playlist_favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playlist_favorites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `playlist_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `playlist_favorites_user_id_playlist_id_c00ffe24_uniq` (`user_id`,`playlist_id`),
  KEY `playlist_favorites_playlist_id_317889bc_fk_playlists_playlist_id` (`playlist_id`),
  CONSTRAINT `playlist_favorites_playlist_id_317889bc_fk_playlists_playlist_id` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`playlist_id`),
  CONSTRAINT `playlist_favorites_user_id_484e828c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlist_favorites`
--

LOCK TABLES `playlist_favorites` WRITE;
/*!40000 ALTER TABLE `playlist_favorites` DISABLE KEYS */;
/*!40000 ALTER TABLE `playlist_favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlist_songs`
--

DROP TABLE IF EXISTS `playlist_songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playlist_songs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `added_at` datetime(6) NOT NULL,
  `playlist_id` int NOT NULL,
  `song_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `playlist_songs_playlist_id_song_id_0289700d_uniq` (`playlist_id`,`song_id`),
  KEY `playlist_songs_song_id_1f2a4faa_fk_songs_song_id` (`song_id`),
  CONSTRAINT `playlist_songs_playlist_id_99c5daf1_fk_playlists_playlist_id` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`playlist_id`),
  CONSTRAINT `playlist_songs_song_id_1f2a4faa_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlist_songs`
--

LOCK TABLES `playlist_songs` WRITE;
/*!40000 ALTER TABLE `playlist_songs` DISABLE KEYS */;
INSERT INTO `playlist_songs` VALUES (1,'2025-05-03 08:09:44.979790',1,4),(2,'2025-05-03 08:09:44.979790',1,2),(3,'2025-05-03 08:09:44.982791',1,1),(4,'2025-05-03 08:09:44.986789',1,3),(5,'2025-05-03 08:15:00.974478',2,8),(6,'2025-05-03 08:15:00.975353',2,9),(7,'2025-05-03 08:15:00.975353',2,10),(8,'2025-05-03 08:40:46.451433',3,2),(9,'2025-05-03 08:40:46.452432',3,1),(10,'2025-05-03 08:40:46.461434',3,5),(11,'2025-05-03 08:40:46.462435',3,3),(12,'2025-05-03 08:40:46.462435',3,4),(13,'2025-05-03 08:40:46.465430',3,6);
/*!40000 ALTER TABLE `playlist_songs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlists`
--

DROP TABLE IF EXISTS `playlists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `playlists` (
  `playlist_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` int NOT NULL,
  PRIMARY KEY (`playlist_id`),
  KEY `playlists_created_by_id_e6261091_fk_auth_user_id` (`created_by_id`),
  CONSTRAINT `playlists_created_by_id_e6261091_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlists`
--

LOCK TABLES `playlists` WRITE;
/*!40000 ALTER TABLE `playlists` DISABLE KEYS */;
INSERT INTO `playlists` VALUES (1,'Nhạc của Sơn Tùng','image/Sơn_Tùng_MTP_7WzesGh.jpg','2025-05-03 08:09:44.929922',1),(2,'Nhạc của Hòa minzy','image/Hòa_Minzy_5MvT4no.jpg','2025-05-03 08:15:00.906677',1),(3,'Nhạc của tôi','image/Giá_như_kpUvfb6.jpg','2025-05-03 08:40:46.395381',2);
/*!40000 ALTER TABLE `playlists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `songs`
--

DROP TABLE IF EXISTS `songs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `songs` (
  `song_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `file_path` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `video_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `content_type` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `duration` varchar(5) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`song_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `songs`
--

LOCK TABLES `songs` WRITE;
/*!40000 ALTER TABLE `songs` DISABLE KEYS */;
INSERT INTO `songs` VALUES (1,'Nơi này có anh','image/Nơi_này_có_anh.jpg','songs/NƠI_NÀY_CÓ_ANH_-_OFFICIAL_MUSIC_VIDEO_-_SƠN_TÙNG_M-TP.mp3','video/NƠI_NÀY_CÓ_ANH_-_OFFICIAL_MUSIC_VIDEO_-_SƠN_TÙNG_M-TP.mp4','Music','2025-05-03 07:46:20.576209',NULL),(2,'Đừng làm trái tim anh đau','image/Đừng_làm_trái_tim_anh_đau.jpg','songs/SƠN_TÙNG_M-TP_-_ĐỪNG_LÀM_TRÁI_TIM_ANH_ĐAU_-_OFFICIAL_MUSIC_VIDEO.mp3','video/SƠN_TÙNG_M-TP_-_ĐỪNG_LÀM_TRÁI_TIM_ANH_ĐAU_-_OFFICIAL_MUSIC_VIDEO.mp4','Music','2025-05-03 07:52:52.618502',NULL),(3,'Chúng ta của tương lai','image/Chúng_ta_của_tương_lai_x8qFUjf.jpg','songs/SƠN_TÙNG_M-TP_-_CHÚNG_TA_CỦA_TƯƠNG_LAI_-_OFFICIAL_MUSIC_VIDEO.mp3','video/SƠN_TÙNG_M-TP_-_CHÚNG_TA_CỦA_TƯƠNG_LAI_-_OFFICIAL_MUSIC_VIDEO.mp4','Music','2025-05-03 07:55:17.902794',NULL),(4,'Có chắc yêu là đây','image/Có_chắc_yêu_là_đây_dB6Ovws.jpg','songs/SƠN_TÙNG_M-TP_-_CÓ_CHẮC_YÊU_LÀ_ĐÂY_-_OFFICIAL_MUSIC_VIDEO.mp3','video/SƠN_TÙNG_M-TP_-_CÓ_CHẮC_YÊU_LÀ_ĐÂY_-_OFFICIAL_MUSIC_VIDEO.mp4','Music','2025-05-03 07:56:36.246160',NULL),(5,'Đưa anh về','image/Đưa_anh_về.jpg','songs/ĐƯA_ANH_VỀ_-_Phan_Mạnh_Quỳnh_-_Official_MV.mp3','video/ĐƯA_ANH_VỀ_-_Phan_Mạnh_Quỳnh_-_Official_MV.mp4','Music','2025-05-03 07:58:23.559424',NULL),(6,'Lời hẹn','image/Lời_hẹn.jpg','songs/Lời_hẹn_OST_Thám_Tử_Kiên_-_Phan_Mạnh_Quỳnh_Lyrics.mp3','video/Lời_hẹn_OST_Thám_Tử_Kiên_-_Phan_Mạnh_Quỳnh_Lyrics.mp4','Music','2025-05-03 08:00:31.349986',NULL),(7,'Từ bàn tay này','image/Từ_bàn_tay_này.jpg','songs/TỪ_BÀN_TAY_NÀY_-_PHAN_MẠNH_QUỲNH_-_OFFICIAL_MV.mp3','video/TỪ_BÀN_TAY_NÀY_-_PHAN_MẠNH_QUỲNH_-_OFFICIAL_MV.mp4','Music','2025-05-03 08:01:21.159136',NULL),(8,'Bắc Bling','image/Bắc_Bling.jpg','songs/BẮC_BLING_BẮC_NINH_-_OFFICIAL_MV_-_HOÀ_MINZY_ft_NS_XUÂN_HINH_x_MASEW_x_TUẤN_CRY.mp3','video/BẮC_BLING_BẮC_NINH_-_OFFICIAL_MV_-_HOÀ_MINZY_ft_NS_XUÂN_HINH_x_MASEW_x_TUẤN_CRY.mp4','Music','2025-05-03 08:03:14.667687',NULL),(9,'Kén cá chọn canh','image/Kén_cá_chọn_canh.jpg','songs/Kén_Cá_Chọn_Canh_-_Hòa_Minzy_x_Tuấn_Cry_x_Masew_-_Official_Music_Video_Genshin_Impact.mp3','video/Kén_Cá_Chọn_Canh_-_Hòa_Minzy_x_Tuấn_Cry_x_Masew_-_Official_Music_Video_Genshin_Impact.mp4','Music','2025-05-03 08:05:39.797233',NULL),(10,'Thị Mầu','image/Thị_Mầu.jpg','songs/Thị_Mầu_-_Hòa_Minzy_x_Masew_-_Official_Music_Video.mp3','video/Thị_Mầu_-_Hòa_Minzy_x_Masew_-_Official_Music_Video.mp4','Music','2025-05-03 08:06:31.317178',NULL),(11,'Giá như','image/Giá_như_XkzyPdC.jpg','songs/SOOBIN_-_giá_như_-_Karaoke.mp3','video/SOOBIN_-_giá_như_-_Karaoke.mp4','Music','2025-05-03 08:36:47.915094',NULL);
/*!40000 ALTER TABLE `songs` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-05  0:48:01
