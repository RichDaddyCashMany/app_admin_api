# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.6.20)
# Database: easy_admin
# Generation Time: 2018-03-15 05:51:29 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table admin
# ------------------------------------------------------------

DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `create_at` int(11) DEFAULT NULL,
  `token` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;

INSERT INTO `admin` (`id`, `username`, `password`, `phone`, `email`, `create_at`, `token`)
VALUES
	(1,'admin','e10adc3949ba59abbe56e057f20f883e',NULL,NULL,NULL,'6e82873feecae44daaa46edd18c787ea');

/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table app_config
# ------------------------------------------------------------

DROP TABLE IF EXISTS `app_config`;

CREATE TABLE `app_config` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ios_ver` varchar(20) DEFAULT '' COMMENT 'iOS版本',
  `ios_force_update` tinyint(1) DEFAULT '0' COMMENT 'iOS强制更新',
  `ios_update_url` varchar(200) DEFAULT '' COMMENT 'iOS更新地址',
  `ios_update_content` varchar(1000) DEFAULT NULL COMMENT 'iOS更新内容',
  `ios_review` tinyint(1) DEFAULT '0' COMMENT 'iOS审核中',
  `android_ver` varchar(20) DEFAULT '',
  `android_force_update` tinyint(1) DEFAULT '0',
  `android_update_url` varchar(200) DEFAULT '',
  `android_update_content` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `app_config` WRITE;
/*!40000 ALTER TABLE `app_config` DISABLE KEYS */;

INSERT INTO `app_config` (`id`, `ios_ver`, `ios_force_update`, `ios_update_url`, `ios_update_content`, `ios_review`, `android_ver`, `android_force_update`, `android_update_url`, `android_update_content`)
VALUES
	(2,'1.0.1',1,'http://www.baidu.com','null',1,'1.0.0',0,'http://www.baidu.com','null');

/*!40000 ALTER TABLE `app_config` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table message_board
# ------------------------------------------------------------

DROP TABLE IF EXISTS `message_board`;

CREATE TABLE `message_board` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` varchar(32) DEFAULT NULL,
  `create_at` int(11) DEFAULT NULL COMMENT '创建时间',
  `close_at` int(11) DEFAULT NULL COMMENT '关闭时间',
  `user_id` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `message_board_to_user` (`user_id`),
  CONSTRAINT `message_board_to_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `message_board` WRITE;
/*!40000 ALTER TABLE `message_board` DISABLE KEYS */;

INSERT INTO `message_board` (`id`, `record_id`, `create_at`, `close_at`, `user_id`)
VALUES
	(1,'209bdc71402cf5a820093e715dec7508',1521088869,NULL,1);

/*!40000 ALTER TABLE `message_board` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table message_board_msg
# ------------------------------------------------------------

DROP TABLE IF EXISTS `message_board_msg`;

CREATE TABLE `message_board_msg` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `board_id` int(11) unsigned DEFAULT NULL,
  `message_id` varchar(32) DEFAULT NULL,
  `user_id` int(11) unsigned DEFAULT NULL,
  `message` varchar(1000) DEFAULT NULL,
  `create_at` int(11) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `message_id` (`board_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `message_id` FOREIGN KEY (`board_id`) REFERENCES `message_board` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `message_board_msg` WRITE;
/*!40000 ALTER TABLE `message_board_msg` DISABLE KEYS */;

INSERT INTO `message_board_msg` (`id`, `board_id`, `message_id`, `user_id`, `message`, `create_at`, `is_admin`)
VALUES
	(1,1,'6029dfbdb9c6a190cb7ab10a8cf99c51',1,'hello',1521088869,0),
	(2,1,'d87f16cfaa49204084f8860adfb98377',NULL,'hi',1521089038,1);

/*!40000 ALTER TABLE `message_board_msg` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table notice
# ------------------------------------------------------------

DROP TABLE IF EXISTS `notice`;

CREATE TABLE `notice` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `record_id` varchar(32) DEFAULT NULL COMMENT '记录id',
  `create_at` int(11) DEFAULT '0' COMMENT '创建时间',
  `update_at` int(11) DEFAULT '0' COMMENT '编辑时间',
  `type` tinyint(1) DEFAULT '-1' COMMENT '0闪屏 1公告 2banner',
  `title` varchar(20) DEFAULT '' COMMENT '标题',
  `content` text COMMENT '内容',
  `picture_url` text COMMENT '图片',
  `begin_time` int(11) DEFAULT '0' COMMENT '开始时间',
  `end_time` int(11) DEFAULT '0' COMMENT '结束时间',
  `enable` tinyint(1) DEFAULT '1' COMMENT '1上线0下线',
  `url` text COMMENT '跳转url',
  `remark` text COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `record_id` (`record_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `notice` WRITE;
/*!40000 ALTER TABLE `notice` DISABLE KEYS */;

INSERT INTO `notice` (`id`, `record_id`, `create_at`, `update_at`, `type`, `title`, `content`, `picture_url`, `begin_time`, `end_time`, `enable`, `url`, `remark`)
VALUES
	(1,'ab22ef71dd4d18a7c0db644e5182407e',1521088160,1521088160,0,'','','http://test-1252137158.file.myqcloud.com/myFloder/1521088139960_alert_picture_bg%402x.png',1521088149,1571113750,1,'',''),
	(2,'d300b40610fe44600a5555f2071a6e92',1521088228,1521088228,1,'新年活动','。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。','',1521088214,1521174623,1,'','');

/*!40000 ALTER TABLE `notice` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table user
# ------------------------------------------------------------

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) DEFAULT '' COMMENT '加密用户id',
  `username` varchar(20) DEFAULT '',
  `password` varchar(32) DEFAULT '',
  `phone` varchar(11) DEFAULT '',
  `email` varchar(100) DEFAULT '',
  `token` varchar(32) DEFAULT '',
  `expire_at` int(11) DEFAULT NULL COMMENT '过期时间',
  `last_login_ip` varchar(15) DEFAULT '' COMMENT '上次登录ip',
  `last_login_time` int(11) DEFAULT NULL COMMENT '上次登录时间',
  `real_name` varchar(4) DEFAULT '' COMMENT '身份证姓名',
  `id_card` varchar(18) DEFAULT '' COMMENT '身份证号码',
  `address` varchar(200) DEFAULT '' COMMENT '地址',
  `create_at` int(11) DEFAULT NULL COMMENT '注册时间',
  `create_ip` varchar(15) DEFAULT '' COMMENT '注册ip',
  `nick_name` varchar(10) DEFAULT '' COMMENT '昵称',
  `is_identity` tinyint(1) DEFAULT NULL COMMENT '是否身份认证',
  `avatar` varchar(200) DEFAULT '' COMMENT '头像',
  `sex` tinyint(1) DEFAULT NULL COMMENT '1男0女',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;

INSERT INTO `user` (`id`, `user_id`, `username`, `password`, `phone`, `email`, `token`, `expire_at`, `last_login_ip`, `last_login_time`, `real_name`, `id_card`, `address`, `create_at`, `create_ip`, `nick_name`, `is_identity`, `avatar`, `sex`)
VALUES
	(1,'7f456fb0c1dd174c9894c46612b45189','aaa','32a62443c5ff5bc9247022e766046760',NULL,NULL,'6a94996d9a9fe2cb31c90aca7e1116d3',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);

/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
