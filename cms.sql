/*
Navicat MariaDB Data Transfer

Source Server         : localhost_3306
Source Server Version : 100414
Source Host           : localhost:3306
Source Database       : tmp

Target Server Type    : MariaDB
Target Server Version : 100414
File Encoding         : 65001

Date: 2021-03-08 18:27:03
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for lin_group
-- ----------------------------
DROP TABLE IF EXISTS `lin_group`;
CREATE TABLE `lin_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(60) DEFAULT NULL COMMENT '权限组名称',
  `info` varchar(255) DEFAULT NULL COMMENT '权限组描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of lin_group
-- ----------------------------
INSERT INTO `lin_group` VALUES ('1', '超级管理员', '');

-- ----------------------------
-- Table structure for lin_user
-- ----------------------------
DROP TABLE IF EXISTS `lin_user`;
CREATE TABLE `lin_user` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `delete_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(24) NOT NULL COMMENT '用户名',
  `nickname` varchar(24) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像url',
  `admin` smallint(6) NOT NULL COMMENT '是否为超级管理员 ;  1 -> 普通用户 |  2 -> 超级管理员',
  `active` smallint(6) NOT NULL COMMENT '当前用户是否为激活状态，非激活状态默认失去用户权限 ; 1 -> 激活 | 2 -> 非激活',
  `email` varchar(100) DEFAULT NULL COMMENT '电子邮箱',
  `group_id` int(11) DEFAULT NULL COMMENT '用户所属的权限组id',
  `password` varchar(100) DEFAULT NULL COMMENT '密码',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `nickname` (`nickname`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of lin_user
-- ----------------------------
INSERT INTO `lin_user` VALUES ('2020-11-20 18:12:18', '2020-12-10 21:16:03', null, '1', 'super', null, null, '2', '1', '1234995678@qq.com', '1', 'pbkdf2:sha256:50000$5smVp1DK$ef1e91c8f4a85969dac466fa3152a99f4ac3fdd42212c60bd25ba3f70905c0e5');
