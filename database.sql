-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th5 04, 2025 lúc 03:45 PM
-- Phiên bản máy phục vụ: 11.7.2-MariaDB
-- Phiên bản PHP: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `spotify`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `albums`
--

CREATE TABLE `albums` (
  `album_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `artist_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `albums`
--

INSERT INTO `albums` (`album_id`, `title`, `image`, `created_at`, `artist_id`) VALUES
(1, 'SKY', 'image/Có_chắc_yêu_là_đây.jpg', '2025-05-03 07:03:34.208126', 1),
(2, 'SKY_TOUR', 'image/Chúng_ta_của_tương_lai.jpg', '2025-05-03 07:04:05.335561', 1),
(3, 'SƠN TÙNG', 'image/Sơn_Tùng_MTP_rKpgTuk.jpg', '2025-05-03 07:04:28.901814', 1),
(4, 'Bật nó lên', 'image/Ai_mà_biết_được.jpg', '2025-05-03 07:07:12.320351', 2),
(5, 'Soobin', 'image/Giá_như.jpg', '2025-05-03 07:08:01.114215', 2),
(6, 'PMQ', 'image/Phan_mạnh_quỳnh_rBXLQ4y.jpg', '2025-05-03 07:08:34.779460', 3),
(7, 'Bắc Bling', 'image/Hòa_Minzy_xxjUR7w.jpg', '2025-05-03 07:08:52.357422', 4);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `album_favorites`
--

CREATE TABLE `album_favorites` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `album_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `album_songs`
--

CREATE TABLE `album_songs` (
  `id` bigint(20) NOT NULL,
  `added_at` datetime(6) NOT NULL,
  `album_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `album_songs`
--

INSERT INTO `album_songs` (`id`, `added_at`, `album_id`, `song_id`) VALUES
(1, '2025-05-03 08:31:35.575750', 1, 1),
(2, '2025-05-03 08:31:44.027036', 1, 2),
(3, '2025-05-03 08:31:53.040752', 1, 3),
(4, '2025-05-03 08:33:09.841804', 7, 8),
(5, '2025-05-03 08:33:45.195437', 7, 9),
(6, '2025-05-03 08:34:11.767867', 2, 1),
(7, '2025-05-03 08:34:20.305061', 2, 4),
(8, '2025-05-03 08:34:58.731984', 6, 5),
(9, '2025-05-03 08:35:02.721663', 6, 6),
(10, '2025-05-03 08:35:06.311568', 6, 7),
(11, '2025-05-04 13:44:26.255261', 1, 4);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `artists`
--

CREATE TABLE `artists` (
  `artist_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `bio` longtext DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `artists`
--

INSERT INTO `artists` (`artist_id`, `name`, `bio`, `image`, `created_at`) VALUES
(1, 'Sơn Tùng MTP', 'Welcome to bio Sơn Tùng MTP', 'image/Sơn_Tùng_MTP.jpg', '2025-05-03 06:26:46.942922'),
(2, 'Soobin Hoàng Sơn', 'Welcome  to my bio', 'image/Soobin.jpg', '2025-05-03 06:57:13.500311'),
(3, 'Phan Mạnh Quỳnh', 'My bio', 'image/Phan_mạnh_quỳnh.jpg', '2025-05-03 06:58:18.036075'),
(4, 'Hòa minzy', 'Welcome to my bio', 'image/Hòa_Minzy.jpg', '2025-05-03 06:59:00.620450'),
(5, 'NS Xuân Hinh', 'Nghệ sĩ nhân dân', 'image/NS_Xuân_Hinh.jpg', '2025-05-03 06:59:30.009388'),
(6, 'Masew', 'Nhạc sĩ', 'image/Masew.jpg', '2025-05-03 07:00:21.802233');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `artist_songs`
--

CREATE TABLE `artist_songs` (
  `id` bigint(20) NOT NULL,
  `main_artist` tinyint(1) NOT NULL,
  `added_at` datetime(6) NOT NULL,
  `artist_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `artist_songs`
--

INSERT INTO `artist_songs` (`id`, `main_artist`, `added_at`, `artist_id`, `song_id`) VALUES
(1, 1, '2025-05-03 07:46:20.620654', 1, 1),
(2, 1, '2025-05-03 07:52:52.641606', 1, 2),
(3, 1, '2025-05-03 07:55:17.961919', 1, 3),
(4, 1, '2025-05-03 07:56:36.299024', 1, 4),
(5, 1, '2025-05-03 07:58:23.609655', 3, 5),
(6, 1, '2025-05-03 08:00:31.401702', 3, 6),
(7, 1, '2025-05-03 08:01:21.222974', 3, 7),
(8, 1, '2025-05-03 08:03:14.706133', 4, 8),
(9, 0, '2025-05-03 08:03:14.747658', 5, 8),
(10, 0, '2025-05-03 08:03:14.769922', 6, 8),
(11, 1, '2025-05-03 08:05:39.830427', 4, 9),
(12, 1, '2025-05-03 08:06:31.360421', 4, 10),
(13, 0, '2025-05-03 08:06:31.384104', 6, 10),
(14, 1, '2025-05-03 08:36:47.957241', 2, 11);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can view permission', 1, 'view_permission'),
(5, 'Can add group', 2, 'add_group'),
(6, 'Can change group', 2, 'change_group'),
(7, 'Can delete group', 2, 'delete_group'),
(8, 'Can view group', 2, 'view_group'),
(9, 'Can add user', 3, 'add_user'),
(10, 'Can change user', 3, 'change_user'),
(11, 'Can delete user', 3, 'delete_user'),
(12, 'Can view user', 3, 'view_user'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add log entry', 5, 'add_logentry'),
(18, 'Can change log entry', 5, 'change_logentry'),
(19, 'Can delete log entry', 5, 'delete_logentry'),
(20, 'Can view log entry', 5, 'view_logentry'),
(21, 'Can add artist', 6, 'add_artist'),
(22, 'Can change artist', 6, 'change_artist'),
(23, 'Can delete artist', 6, 'delete_artist'),
(24, 'Can view artist', 6, 'view_artist'),
(25, 'Can add song', 7, 'add_song'),
(26, 'Can change song', 7, 'change_song'),
(27, 'Can delete song', 7, 'delete_song'),
(28, 'Can view song', 7, 'view_song'),
(29, 'Can add album', 8, 'add_album'),
(30, 'Can change album', 8, 'change_album'),
(31, 'Can delete album', 8, 'delete_album'),
(32, 'Can view album', 8, 'view_album'),
(33, 'Can add message', 9, 'add_message'),
(34, 'Can change message', 9, 'change_message'),
(35, 'Can delete message', 9, 'delete_message'),
(36, 'Can view message', 9, 'view_message'),
(37, 'Can add playlist', 10, 'add_playlist'),
(38, 'Can change playlist', 10, 'change_playlist'),
(39, 'Can delete playlist', 10, 'delete_playlist'),
(40, 'Can view playlist', 10, 'view_playlist'),
(41, 'Can add follower', 11, 'add_follower'),
(42, 'Can change follower', 11, 'change_follower'),
(43, 'Can delete follower', 11, 'delete_follower'),
(44, 'Can view follower', 11, 'view_follower'),
(45, 'Can add playlist song', 12, 'add_playlistsong'),
(46, 'Can change playlist song', 12, 'change_playlistsong'),
(47, 'Can delete playlist song', 12, 'delete_playlistsong'),
(48, 'Can view playlist song', 12, 'view_playlistsong'),
(49, 'Can add favorite', 13, 'add_favorite'),
(50, 'Can change favorite', 13, 'change_favorite'),
(51, 'Can delete favorite', 13, 'delete_favorite'),
(52, 'Can view favorite', 13, 'view_favorite'),
(53, 'Can add download', 14, 'add_download'),
(54, 'Can change download', 14, 'change_download'),
(55, 'Can delete download', 14, 'delete_download'),
(56, 'Can view download', 14, 'view_download'),
(57, 'Can add artist song', 15, 'add_artistsong'),
(58, 'Can change artist song', 15, 'change_artistsong'),
(59, 'Can delete artist song', 15, 'delete_artistsong'),
(60, 'Can view artist song', 15, 'view_artistsong'),
(61, 'Can add album song', 16, 'add_albumsong'),
(62, 'Can change album song', 16, 'change_albumsong'),
(63, 'Can delete album song', 16, 'delete_albumsong'),
(64, 'Can view album song', 16, 'view_albumsong'),
(65, 'Can add chat room', 17, 'add_chatroom'),
(66, 'Can change chat room', 17, 'change_chatroom'),
(67, 'Can delete chat room', 17, 'delete_chatroom'),
(68, 'Can view chat room', 17, 'view_chatroom'),
(69, 'Can add chat message', 18, 'add_chatmessage'),
(70, 'Can change chat message', 18, 'change_chatmessage'),
(71, 'Can delete chat message', 18, 'delete_chatmessage'),
(72, 'Can view chat message', 18, 'view_chatmessage'),
(73, 'Can add album favorite', 19, 'add_albumfavorite'),
(74, 'Can change album favorite', 19, 'change_albumfavorite'),
(75, 'Can delete album favorite', 19, 'delete_albumfavorite'),
(76, 'Can view album favorite', 19, 'view_albumfavorite'),
(77, 'Can add playlist favorite', 20, 'add_playlistfavorite'),
(78, 'Can change playlist favorite', 20, 'change_playlistfavorite'),
(79, 'Can delete playlist favorite', 20, 'delete_playlistfavorite'),
(80, 'Can view playlist favorite', 20, 'view_playlistfavorite');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `auth_user`
--
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$1000000$MfCZiazVVskGo083Oq7luL$xTU+FSVWrnPv1pMppwE4m34gAO59Tx/RxLKtIY7dD7o=', NULL, 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2025-04-21 15:34:16.582349'),
(2, 'pbkdf2_sha256$1000000$dzM2GoStTqrXRiBozaf6f2$TCaqmHBUcmnEytjKTUYP0W3SLr5LpvAALFvxenxDzaI=', NULL, 0, 'linh', '', '', 'linhtranvo2003@gmail.com', 0, 1, '2025-04-24 14:04:16.657189'),
(3, 'pbkdf2_sha256$1000000$8wGcfIXNIB13iHdhwn1goP$RH9C+27eL8mO463B5lYrbLijlhRwZ2VQ0nDReMBDqQ4=', NULL, 1, 'DuyKhanh', '', '', 'khanh@gmail.com', 1, 1, '2025-05-03 06:24:38.970464'),
(4, 'pbkdf2_sha256$1000000$0X7sU7G9FSeZ4IlBpCf7ox$Cv2JsY/GmS/veVAb4yfAoHq5TDU6vbMDV4gJYS6pFDw=', NULL, 0, 'user1', '', '', 'user1@example.com', 0, 1, '2025-05-03 08:22:02.416299'),
(5, 'pbkdf2_sha256$1000000$g9ufBnnMFPAs55XYsCXDnA$f2P4QYZ9de4aym8YzJGJhUUniJ2ZOqlYA0dnNtpT4gM=', NULL, 0, 'user2', '', '', 'user2@example.com', 0, 1, '2025-05-03 08:22:03.282481'),
(6, 'pbkdf2_sha256$1000000$mubzWkT6wqlZZDNZO64pNT$3hFA5Ss8pUpJH1IlWg82oI9mcpTWSVNEmlKQu6Nq7Sw=', NULL, 0, 'user3', '', '', 'user3@example.com', 0, 1, '2025-05-03 08:22:04.098884'),
(7, 'pbkdf2_sha256$1000000$bIWML6b24UmIQ5RrE1grJp$5yqeSlR9EDIvfLoN/TOvyDe57kVQOzYuTvGulh7Bo5Q=', NULL, 0, 'user4', '', '', 'user4@example.com', 0, 1, '2025-05-03 08:22:04.919377'),
(8, 'pbkdf2_sha256$1000000$zDPVfkPOrF0mFsd2LLkKpT$6LsA9U4WLQL9eOWTmrzM24etr4o+oLCYgUqX5j9J1Yc=', NULL, 0, 'user5', '', '', 'user5@example.com', 0, 1, '2025-05-03 08:22:05.768692'),
(9, 'pbkdf2_sha256$1000000$snY0mUU7k67pRiEAJAjXFz$R6JHTL+lvexnfVOfUs4qWjaylGrV41+OOWZCW8GWdnY=', NULL, 0, 'user6', '', '', 'user6@example.com', 0, 1, '2025-05-03 08:22:06.624969'),
(10, 'pbkdf2_sha256$1000000$zg30mI9vCA6DB8uGFK0TZR$6QlCkvbYoJQJU8ygunvJ9q4qQ3PUAKvmtu3mrA1P6mk=', NULL, 0, 'user7', '', '', 'user7@example.com', 0, 1, '2025-05-03 08:22:07.431870'),
(11, 'pbkdf2_sha256$1000000$YSp5IVB9qahHhFfB2R2GtU$trIlhJHRxOmqZ/hfKzq6rVk2Sxr8NrAeD95G2tJLX5U=', NULL, 0, 'user8', '', '', 'user8@example.com', 0, 1, '2025-05-03 08:22:08.257816'),
(12, 'pbkdf2_sha256$1000000$1pDXKWYAC20lTIIYv3iFnr$JS/6Garhls3atfDv/w1T5f9QhaTAJU6SmC9dhtEmD2Q=', NULL, 0, 'user9', '', '', 'user9@example.com', 0, 1, '2025-05-03 08:22:09.073330'),
(13, 'pbkdf2_sha256$1000000$p35EhyM5zx5WnII8baOxrU$krdSQCcsLPuJjMxjUfZwagaHPsGa4j5llWRDNivdH7I=', NULL, 0, 'user10', '', '', 'user10@example.com', 0, 1, '2025-05-03 08:22:09.891981'),
(14, 'pbkdf2_sha256$1000000$D8EGwsCA6svdhuBEUS0VLW$EeDkdsrTGZ0T4b6kG+vK8EX7QtOSK3MO3C1cjSx/pDg=', NULL, 0, 'user11', '', '', 'user11@example.com', 0, 1, '2025-05-03 08:22:10.704700'),
(15, 'pbkdf2_sha256$1000000$JOp4y8TO9rHstdN9CX73bC$ixiLJ+OGlSZ0xXyj5BVXftD5GaSx1Wbxj/koM39p+Gc=', NULL, 0, 'user12', '', '', 'user12@example.com', 0, 1, '2025-05-03 08:22:11.526503'),
(16, 'pbkdf2_sha256$1000000$SYrazyofM7t2BU8yhTWd7B$FICSgmVMNGkWtB91HIpefpdx0EVPV3MOITxp+3DzWm0=', NULL, 0, 'user13', '', '', 'user13@example.com', 0, 1, '2025-05-03 08:22:12.368288'),
(17, 'pbkdf2_sha256$1000000$RF9hOM3KHmxZPL74IbOLvN$O6Yz7pW4IsKMg55nM9U12Zs5k+1JRAC4N2BQGvjHxYs=', NULL, 0, 'user14', '', '', 'user14@example.com', 0, 1, '2025-05-03 08:22:13.201504'),
(18, 'pbkdf2_sha256$1000000$nmBtMtkkBt7WX0MUICg3lR$epZVDLdqISkVPQ5jW3RFOMvc7Vupg1dVVffrMkg1Vo4=', NULL, 0, 'user15', '', '', 'user15@example.com', 0, 1, '2025-05-03 08:22:14.035673');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `chatmessages`
--

CREATE TABLE `chatmessages` (
  `id` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `srcfile` varchar(255) DEFAULT NULL,
  `sender_id` int(11) NOT NULL,
  `song_id` int(11) DEFAULT NULL,
  `chatroom_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `chatrooms`
--

CREATE TABLE `chatrooms` (
  `id` int(11) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user1_id` int(11) NOT NULL,
  `user2_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(5, 'admin', 'logentry'),
(2, 'auth', 'group'),
(1, 'auth', 'permission'),
(3, 'auth', 'user'),
(4, 'contenttypes', 'contenttype'),
(8, 'manager', 'album'),
(19, 'manager', 'albumfavorite'),
(16, 'manager', 'albumsong'),
(6, 'manager', 'artist'),
(15, 'manager', 'artistsong'),
(18, 'manager', 'chatmessage'),
(17, 'manager', 'chatroom'),
(14, 'manager', 'download'),
(13, 'manager', 'favorite'),
(11, 'manager', 'follower'),
(9, 'manager', 'message'),
(10, 'manager', 'playlist'),
(20, 'manager', 'playlistfavorite'),
(12, 'manager', 'playlistsong'),
(7, 'manager', 'song');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-04-21 14:40:02.832630'),
(2, 'auth', '0001_initial', '2025-04-21 14:40:03.294836'),
(3, 'admin', '0001_initial', '2025-04-21 14:40:03.410691'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-04-21 14:40:03.415513'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-04-21 14:40:03.426243'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-04-21 14:40:03.492897'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-04-21 14:40:03.533241'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-04-21 14:40:03.556562'),
(9, 'auth', '0004_alter_user_username_opts', '2025-04-21 14:40:03.564566'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-04-21 14:40:03.604335'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-04-21 14:40:03.606334'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-04-21 14:40:03.614367'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-04-21 14:40:03.642272'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-04-21 14:40:03.665007'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-04-21 14:40:03.685546'),
(16, 'auth', '0011_update_proxy_permissions', '2025-04-21 14:40:03.694550'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-04-21 14:40:03.716237'),
(18, 'manager', '0001_initial', '2025-04-21 14:40:04.618186'),
(19, 'manager', '0002_song_duration_alter_album_image_alter_artist_image_and_more', '2025-05-04 13:41:54.398248');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `downloads`
--

CREATE TABLE `downloads` (
  `id` bigint(20) NOT NULL,
  `downloaded_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `favorites`
--

CREATE TABLE `favorites` (
  `id` bigint(20) NOT NULL,
  `added_at` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `favorites`
--

INSERT INTO `favorites` (`id`, `added_at`, `user_id`, `song_id`) VALUES
(1, '2025-05-03 15:28:59.000000', 4, 1),
(2, '2025-05-03 15:28:59.000000', 4, 3),
(3, '2025-05-03 15:28:59.000000', 4, 5),
(4, '2025-05-03 15:28:59.000000', 5, 2),
(5, '2025-05-03 15:28:59.000000', 5, 4),
(6, '2025-05-03 15:28:59.000000', 5, 6),
(7, '2025-05-03 15:28:59.000000', 6, 1),
(8, '2025-05-03 15:28:59.000000', 6, 7),
(9, '2025-05-03 15:28:59.000000', 6, 9),
(10, '2025-05-03 15:28:59.000000', 7, 3),
(11, '2025-05-03 15:28:59.000000', 7, 6),
(12, '2025-05-03 15:28:59.000000', 7, 10),
(13, '2025-05-03 15:28:59.000000', 8, 2),
(14, '2025-05-03 15:28:59.000000', 8, 5),
(15, '2025-05-03 15:28:59.000000', 8, 8),
(16, '2025-05-03 15:28:59.000000', 4, 10),
(17, '2025-05-03 15:28:59.000000', 5, 7),
(18, '2025-05-03 15:28:59.000000', 6, 4),
(19, '2025-05-03 15:28:59.000000', 7, 8),
(20, '2025-05-03 15:28:59.000000', 8, 6),
(21, '2025-05-03 15:28:59.000000', 4, 2),
(22, '2025-05-03 15:28:59.000000', 5, 1),
(23, '2025-05-03 15:28:59.000000', 6, 5),
(24, '2025-05-03 15:28:59.000000', 7, 1),
(25, '2025-05-03 15:28:59.000000', 8, 3),
(26, '2025-05-03 15:28:59.000000', 4, 6),
(27, '2025-05-03 15:28:59.000000', 5, 9),
(28, '2025-05-03 15:28:59.000000', 6, 10),
(29, '2025-05-03 15:28:59.000000', 7, 2),
(30, '2025-05-03 15:28:59.000000', 8, 4);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `followers`
--

CREATE TABLE `followers` (
  `id` bigint(20) NOT NULL,
  `followed_at` datetime(6) NOT NULL,
  `artist_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `followers`
--

INSERT INTO `followers` (`id`, `followed_at`, `artist_id`, `user_id`) VALUES
(1, '2025-05-03 15:30:39.000000', 1, 4),
(2, '2025-05-03 15:30:39.000000', 2, 4),
(3, '2025-05-03 15:30:39.000000', 3, 5),
(4, '2025-05-03 15:30:39.000000', 4, 5),
(5, '2025-05-03 15:30:39.000000', 5, 6),
(6, '2025-05-03 15:30:39.000000', 6, 6),
(7, '2025-05-03 15:30:39.000000', 1, 7),
(8, '2025-05-03 15:30:39.000000', 2, 7),
(9, '2025-05-03 15:30:39.000000', 3, 8),
(10, '2025-05-03 15:30:39.000000', 4, 8),
(11, '2025-05-03 15:30:39.000000', 5, 4),
(12, '2025-05-03 15:30:39.000000', 6, 4),
(13, '2025-05-03 15:30:39.000000', 1, 5),
(14, '2025-05-03 15:30:39.000000', 2, 5),
(15, '2025-05-03 15:30:39.000000', 3, 6),
(16, '2025-05-03 15:30:39.000000', 4, 6),
(17, '2025-05-03 15:30:39.000000', 5, 7),
(18, '2025-05-03 15:30:39.000000', 6, 7),
(19, '2025-05-03 15:30:39.000000', 1, 8),
(20, '2025-05-03 15:30:39.000000', 2, 8),
(21, '2025-05-03 15:30:39.000000', 3, 4),
(22, '2025-05-03 15:30:39.000000', 4, 4),
(23, '2025-05-03 15:30:39.000000', 5, 5),
(24, '2025-05-03 15:30:39.000000', 6, 5),
(25, '2025-05-03 15:30:39.000000', 1, 6),
(26, '2025-05-03 15:30:39.000000', 2, 6),
(27, '2025-05-03 15:30:39.000000', 3, 7),
(28, '2025-05-03 15:30:39.000000', 4, 7),
(29, '2025-05-03 15:30:39.000000', 5, 8),
(30, '2025-05-03 15:30:39.000000', 6, 8);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `messages`
--

CREATE TABLE `messages` (
  `message_id` int(11) NOT NULL,
  `message_text` longtext DEFAULT NULL,
  `sent_at` datetime(6) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `playlists`
--

CREATE TABLE `playlists` (
  `playlist_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `playlists`
--

INSERT INTO `playlists` (`playlist_id`, `title`, `image`, `created_at`, `created_by_id`) VALUES
(1, 'Nhạc của Sơn Tùng', 'image/Sơn_Tùng_MTP_7WzesGh.jpg', '2025-05-03 08:09:44.929922', 1),
(2, 'Nhạc của Hòa minzy', 'image/Hòa_Minzy_5MvT4no.jpg', '2025-05-03 08:15:00.906677', 1),
(3, 'Nhạc của tôi', 'image/Giá_như_kpUvfb6.jpg', '2025-05-03 08:40:46.395381', 2);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `playlist_favorites`
--

CREATE TABLE `playlist_favorites` (
  `id` bigint(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `playlist_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `playlist_songs`
--

CREATE TABLE `playlist_songs` (
  `id` bigint(20) NOT NULL,
  `added_at` datetime(6) NOT NULL,
  `playlist_id` int(11) NOT NULL,
  `song_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Đang đổ dữ liệu cho bảng `playlist_songs`
--

INSERT INTO `playlist_songs` (`id`, `added_at`, `playlist_id`, `song_id`) VALUES
(1, '2025-05-03 08:09:44.979790', 1, 4),
(2, '2025-05-03 08:09:44.979790', 1, 2),
(3, '2025-05-03 08:09:44.982791', 1, 1),
(4, '2025-05-03 08:09:44.986789', 1, 3),
(5, '2025-05-03 08:15:00.974478', 2, 8),
(6, '2025-05-03 08:15:00.975353', 2, 9),
(7, '2025-05-03 08:15:00.975353', 2, 10),
(8, '2025-05-03 08:40:46.451433', 3, 2),
(9, '2025-05-03 08:40:46.452432', 3, 1),
(10, '2025-05-03 08:40:46.461434', 3, 5),
(11, '2025-05-03 08:40:46.462435', 3, 3),
(12, '2025-05-03 08:40:46.462435', 3, 4),
(13, '2025-05-03 08:40:46.465430', 3, 6);

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `songs`
--

CREATE TABLE `songs` (
  `song_id` int(11) NOT NULL,
  `title` varchar(100) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `file_path` varchar(255) NOT NULL,
  `video_url` varchar(255) DEFAULT NULL,
  `content_type` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `duration` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


--
-- Đang đổ dữ liệu cho bảng `songs`
--

INSERT INTO `songs` (`song_id`, `title`, `image`, `file_path`, `video_url`, `content_type`, `created_at`, `duration`) VALUES
(1, 'Nơi này có anh', 'image/Nơi_này_có_anh.jpg', 'songs/NƠI_NÀY_CÓ_ANH_-_OFFICIAL_MUSIC_VIDEO_-_SƠN_TÙNG_M-TP.mp3', 'video/NƠI_NÀY_CÓ_ANH_-_OFFICIAL_MUSIC_VIDEO_-_SƠN_TÙNG_M-TP.mp4', 'Music', '2025-05-03 07:46:20.576209', NULL),
(2, 'Đừng làm trái tim anh đau', 'image/Đừng_làm_trái_tim_anh_đau.jpg', 'songs/SƠN_TÙNG_M-TP_-_ĐỪNG_LÀM_TRÁI_TIM_ANH_ĐAU_-_OFFICIAL_MUSIC_VIDEO.mp3', 'video/SƠN_TÙNG_M-TP_-_ĐỪNG_LÀM_TRÁI_TIM_ANH_ĐAU_-_OFFICIAL_MUSIC_VIDEO.mp4', 'Music', '2025-05-03 07:52:52.618502', NULL),
(3, 'Chúng ta của tương lai', 'image/Chúng_ta_của_tương_lai_x8qFUjf.jpg', 'songs/SƠN_TÙNG_M-TP_-_CHÚNG_TA_CỦA_TƯƠNG_LAI_-_OFFICIAL_MUSIC_VIDEO.mp3', 'video/SƠN_TÙNG_M-TP_-_CHÚNG_TA_CỦA_TƯƠNG_LAI_-_OFFICIAL_MUSIC_VIDEO.mp4', 'Music', '2025-05-03 07:55:17.902794', NULL),
(4, 'Có chắc yêu là đây', 'image/Có_chắc_yêu_là_đây_dB6Ovws.jpg', 'songs/SƠN_TÙNG_M-TP_-_CÓ_CHẮC_YÊU_LÀ_ĐÂY_-_OFFICIAL_MUSIC_VIDEO.mp3', 'video/SƠN_TÙNG_M-TP_-_CÓ_CHẮC_YÊU_LÀ_ĐÂY_-_OFFICIAL_MUSIC_VIDEO.mp4', 'Music', '2025-05-03 07:56:36.246160', NULL),
(5, 'Đưa anh về', 'image/Đưa_anh_về.jpg', 'songs/ĐƯA_ANH_VỀ_-_Phan_Mạnh_Quỳnh_-_Official_MV.mp3', 'video/ĐƯA_ANH_VỀ_-_Phan_Mạnh_Quỳnh_-_Official_MV.mp4', 'Music', '2025-05-03 07:58:23.559424', NULL),
(6, 'Lời hẹn', 'image/Lời_hẹn.jpg', 'songs/Lời_hẹn_OST_Thám_Tử_Kiên_-_Phan_Mạnh_Quỳnh_Lyrics.mp3', 'video/Lời_hẹn_OST_Thám_Tử_Kiên_-_Phan_Mạnh_Quỳnh_Lyrics.mp4', 'Music', '2025-05-03 08:00:31.349986', NULL),
(7, 'Từ bàn tay này', 'image/Từ_bàn_tay_này.jpg', 'songs/TỪ_BÀN_TAY_NÀY_-_PHAN_MẠNH_QUỲNH_-_OFFICIAL_MV.mp3', 'video/TỪ_BÀN_TAY_NÀY_-_PHAN_MẠNH_QUỲNH_-_OFFICIAL_MV.mp4', 'Music', '2025-05-03 08:01:21.159136', NULL),
(8, 'Bắc Bling', 'image/Bắc_Bling.jpg', 'songs/BẮC_BLING_BẮC_NINH_-_OFFICIAL_MV_-_HOÀ_MINZY_ft_NS_XUÂN_HINH_x_MASEW_x_TUẤN_CRY.mp3', 'video/BẮC_BLING_BẮC_NINH_-_OFFICIAL_MV_-_HOÀ_MINZY_ft_NS_XUÂN_HINH_x_MASEW_x_TUẤN_CRY.mp4', 'Music', '2025-05-03 08:03:14.667687', NULL),
(9, 'Kén cá chọn canh', 'image/Kén_cá_chọn_canh.jpg', 'songs/Kén_Cá_Chọn_Canh_-_Hòa_Minzy_x_Tuấn_Cry_x_Masew_-_Official_Music_Video_Genshin_Impact.mp3', 'video/Kén_Cá_Chọn_Canh_-_Hòa_Minzy_x_Tuấn_Cry_x_Masew_-_Official_Music_Video_Genshin_Impact.mp4', 'Music', '2025-05-03 08:05:39.797233', NULL),
(10, 'Thị Mầu', 'image/Thị_Mầu.jpg', 'songs/Thị_Mầu_-_Hòa_Minzy_x_Masew_-_Official_Music_Video.mp3', 'video/Thị_Mầu_-_Hòa_Minzy_x_Masew_-_Official_Music_Video.mp4', 'Music', '2025-05-03 08:06:31.317178', NULL),
(11, 'Giá như', 'image/Giá_như_XkzyPdC.jpg', 'songs/SOOBIN_-_giá_như_-_Karaoke.mp3', 'video/SOOBIN_-_giá_như_-_Karaoke.mp4', 'Music', '2025-05-03 08:36:47.915094', NULL);


--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `albums`
--
ALTER TABLE `albums`
  ADD PRIMARY KEY (`album_id`),
  ADD KEY `albums_artist_id_8a9e6bb4_fk_artists_artist_id` (`artist_id`);

--
-- Chỉ mục cho bảng `album_favorites`
--
ALTER TABLE `album_favorites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `album_favorites_user_id_album_id_54110d29_uniq` (`user_id`,`album_id`),
  ADD KEY `album_favorites_album_id_99824288_fk_albums_album_id` (`album_id`);

--
-- Chỉ mục cho bảng `album_songs`
--
ALTER TABLE `album_songs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `album_songs_album_id_song_id_4cff9aec_uniq` (`album_id`,`song_id`),
  ADD KEY `album_songs_song_id_49167b9d_fk_songs_song_id` (`song_id`);

--
-- Chỉ mục cho bảng `artists`
--
ALTER TABLE `artists`
  ADD PRIMARY KEY (`artist_id`);

--
-- Chỉ mục cho bảng `artist_songs`
--
ALTER TABLE `artist_songs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `artist_songs_artist_id_song_id_893d0a8e_uniq` (`artist_id`,`song_id`),
  ADD KEY `artist_songs_song_id_32762766_fk_songs_song_id` (`song_id`);

--
-- Chỉ mục cho bảng `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Chỉ mục cho bảng `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Chỉ mục cho bảng `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Chỉ mục cho bảng `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Chỉ mục cho bảng `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Chỉ mục cho bảng `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Chỉ mục cho bảng `chatmessages`
--
ALTER TABLE `chatmessages`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chatmessages_sender_id_950a0f14_fk_auth_user_id` (`sender_id`),
  ADD KEY `chatmessages_song_id_74a4bcae_fk_songs_song_id` (`song_id`),
  ADD KEY `chatmessages_chatroom_id_f3f72455_fk_chatrooms_id` (`chatroom_id`);

--
-- Chỉ mục cho bảng `chatrooms`
--
ALTER TABLE `chatrooms`
  ADD PRIMARY KEY (`id`),
  ADD KEY `chatrooms_user1_id_2e325bba_fk_auth_user_id` (`user1_id`),
  ADD KEY `chatrooms_user2_id_61d31a3d_fk_auth_user_id` (`user2_id`);

--
-- Chỉ mục cho bảng `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Chỉ mục cho bảng `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Chỉ mục cho bảng `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Chỉ mục cho bảng `downloads`
--
ALTER TABLE `downloads`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `downloads_user_id_song_id_e246188a_uniq` (`user_id`,`song_id`),
  ADD KEY `downloads_song_id_4177d846_fk_songs_song_id` (`song_id`);

--
-- Chỉ mục cho bảng `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `favorites_user_id_song_id_703788fc_uniq` (`user_id`,`song_id`),
  ADD KEY `favorites_song_id_b4ee1f74_fk_songs_song_id` (`song_id`);

--
-- Chỉ mục cho bảng `followers`
--
ALTER TABLE `followers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `followers_user_id_artist_id_fb1f7902_uniq` (`user_id`,`artist_id`),
  ADD KEY `followers_artist_id_560f1ea7_fk_artists_artist_id` (`artist_id`);

--
-- Chỉ mục cho bảng `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`message_id`),
  ADD KEY `messages_receiver_id_874b4e0a_fk_auth_user_id` (`receiver_id`),
  ADD KEY `messages_sender_id_dc5a0bbd_fk_auth_user_id` (`sender_id`);

--
-- Chỉ mục cho bảng `playlists`
--
ALTER TABLE `playlists`
  ADD PRIMARY KEY (`playlist_id`),
  ADD KEY `playlists_created_by_id_e6261091_fk_auth_user_id` (`created_by_id`);

--
-- Chỉ mục cho bảng `playlist_favorites`
--
ALTER TABLE `playlist_favorites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `playlist_favorites_user_id_playlist_id_c00ffe24_uniq` (`user_id`,`playlist_id`),
  ADD KEY `playlist_favorites_playlist_id_317889bc_fk_playlists_playlist_id` (`playlist_id`);

--
-- Chỉ mục cho bảng `playlist_songs`
--
ALTER TABLE `playlist_songs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `playlist_songs_playlist_id_song_id_0289700d_uniq` (`playlist_id`,`song_id`),
  ADD KEY `playlist_songs_song_id_1f2a4faa_fk_songs_song_id` (`song_id`);

--
-- Chỉ mục cho bảng `songs`
--
ALTER TABLE `songs`
  ADD PRIMARY KEY (`song_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `albums`
--
ALTER TABLE `albums`
  MODIFY `album_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT cho bảng `album_favorites`
--
ALTER TABLE `album_favorites`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `album_songs`
--
ALTER TABLE `album_songs`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT cho bảng `artists`
--
ALTER TABLE `artists`
  MODIFY `artist_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT cho bảng `artist_songs`
--
ALTER TABLE `artist_songs`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT cho bảng `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=81;

--
-- AUTO_INCREMENT cho bảng `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT cho bảng `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `chatmessages`
--
ALTER TABLE `chatmessages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `chatrooms`
--
ALTER TABLE `chatrooms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT cho bảng `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT cho bảng `downloads`
--
ALTER TABLE `downloads`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `favorites`
--
ALTER TABLE `favorites`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT cho bảng `followers`
--
ALTER TABLE `followers`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT cho bảng `messages`
--
ALTER TABLE `messages`
  MODIFY `message_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `playlists`
--
ALTER TABLE `playlists`
  MODIFY `playlist_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT cho bảng `playlist_favorites`
--
ALTER TABLE `playlist_favorites`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT cho bảng `playlist_songs`
--
ALTER TABLE `playlist_songs`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT cho bảng `songs`
--
ALTER TABLE `songs`
  MODIFY `song_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `albums`
--
ALTER TABLE `albums`
  ADD CONSTRAINT `albums_artist_id_8a9e6bb4_fk_artists_artist_id` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`);

--
-- Các ràng buộc cho bảng `album_favorites`
--
ALTER TABLE `album_favorites`
  ADD CONSTRAINT `album_favorites_album_id_99824288_fk_albums_album_id` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`),
  ADD CONSTRAINT `album_favorites_user_id_cc87370a_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `album_songs`
--
ALTER TABLE `album_songs`
  ADD CONSTRAINT `album_songs_album_id_3250027a_fk_albums_album_id` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`),
  ADD CONSTRAINT `album_songs_song_id_49167b9d_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`);

--
-- Các ràng buộc cho bảng `artist_songs`
--
ALTER TABLE `artist_songs`
  ADD CONSTRAINT `artist_songs_artist_id_e8c6135e_fk_artists_artist_id` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`),
  ADD CONSTRAINT `artist_songs_song_id_32762766_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`);

--
-- Các ràng buộc cho bảng `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Các ràng buộc cho bảng `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Các ràng buộc cho bảng `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `chatmessages`
--
ALTER TABLE `chatmessages`
  ADD CONSTRAINT `chatmessages_chatroom_id_f3f72455_fk_chatrooms_id` FOREIGN KEY (`chatroom_id`) REFERENCES `chatrooms` (`id`),
  ADD CONSTRAINT `chatmessages_sender_id_950a0f14_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `chatmessages_song_id_74a4bcae_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`);

--
-- Các ràng buộc cho bảng `chatrooms`
--
ALTER TABLE `chatrooms`
  ADD CONSTRAINT `chatrooms_user1_id_2e325bba_fk_auth_user_id` FOREIGN KEY (`user1_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `chatrooms_user2_id_61d31a3d_fk_auth_user_id` FOREIGN KEY (`user2_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `downloads`
--
ALTER TABLE `downloads`
  ADD CONSTRAINT `downloads_song_id_4177d846_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`),
  ADD CONSTRAINT `downloads_user_id_2b9b2559_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `favorites`
--
ALTER TABLE `favorites`
  ADD CONSTRAINT `favorites_song_id_b4ee1f74_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`),
  ADD CONSTRAINT `favorites_user_id_d60eb79f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `followers`
--
ALTER TABLE `followers`
  ADD CONSTRAINT `followers_artist_id_560f1ea7_fk_artists_artist_id` FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`),
  ADD CONSTRAINT `followers_user_id_556252d5_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_receiver_id_874b4e0a_fk_auth_user_id` FOREIGN KEY (`receiver_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `messages_sender_id_dc5a0bbd_fk_auth_user_id` FOREIGN KEY (`sender_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `playlists`
--
ALTER TABLE `playlists`
  ADD CONSTRAINT `playlists_created_by_id_e6261091_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `playlist_favorites`
--
ALTER TABLE `playlist_favorites`
  ADD CONSTRAINT `playlist_favorites_playlist_id_317889bc_fk_playlists_playlist_id` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`playlist_id`),
  ADD CONSTRAINT `playlist_favorites_user_id_484e828c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Các ràng buộc cho bảng `playlist_songs`
--
ALTER TABLE `playlist_songs`
  ADD CONSTRAINT `playlist_songs_playlist_id_99c5daf1_fk_playlists_playlist_id` FOREIGN KEY (`playlist_id`) REFERENCES `playlists` (`playlist_id`),
  ADD CONSTRAINT `playlist_songs_song_id_1f2a4faa_fk_songs_song_id` FOREIGN KEY (`song_id`) REFERENCES `songs` (`song_id`);
COMMIT;


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- Dump completed on 2025-05-02 20:22:50
