/*
Navicat MySQL Data Transfer

Source Server         : 本地
Source Server Version : 80016
Source Host           : localhost:3306
Source Database       : k

Target Server Type    : MYSQL
Target Server Version : 80016
File Encoding         : 65001

Date: 2020-05-27 10:07:41
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `goods_kline_day1_info`
-- ----------------------------
DROP TABLE IF EXISTS `goods_kline_day1_info`;
CREATE TABLE `goods_kline_day1_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '代码',
  `period` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '期数 20180606',
  `volume` decimal(18,8) DEFAULT '0.00000000' COMMENT '成交量',
  `price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '当前价',
  `opening_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻开盘价',
  `closing_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻收盘价',
  `pre_closing_price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昨收盘价',
  `highest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最高价',
  `lowest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最低价',
  `date_ymd` date DEFAULT NULL COMMENT '日期',
  `date` datetime DEFAULT NULL COMMENT '日期时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) unsigned DEFAULT '0' COMMENT '1:删除，0:未删除',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='商品天分时信息';

-- ----------------------------
-- Table structure for `goods_kline_hour4_info`
-- ----------------------------
DROP TABLE IF EXISTS `goods_kline_hour4_info`;
CREATE TABLE `goods_kline_hour4_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '代码',
  `period` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '期数 20180606',
  `volume` decimal(18,8) DEFAULT '0.00000000' COMMENT '成交量',
  `price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '当前价',
  `opening_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻开盘价',
  `closing_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻收盘价',
  `pre_closing_price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昨收盘价',
  `highest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最高价',
  `lowest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最低价',
  `date_ymd` date DEFAULT NULL COMMENT '日期',
  `date` datetime DEFAULT NULL COMMENT '日期时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) unsigned DEFAULT '0' COMMENT '1:删除，0:未删除',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='商品分时信息';

-- ----------------------------
-- Table structure for `goods_kline_min1_info`
-- ----------------------------
DROP TABLE IF EXISTS `goods_kline_min1_info`;
CREATE TABLE `goods_kline_min1_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '代码',
  `period` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '期数 20180606',
  `volume` decimal(18,8) DEFAULT '0.00000000' COMMENT '成交量',
  `price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '当前价',
  `opening_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻开盘价',
  `closing_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻收盘价',
  `pre_closing_price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昨收盘价',
  `highest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最高价',
  `lowest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最低价',
  `date_ymd` date DEFAULT NULL COMMENT '日期',
  `date` datetime DEFAULT NULL COMMENT '日期时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) unsigned DEFAULT '0' COMMENT '1:删除，0:未删除',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=6303 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='商品分时信息';

-- ----------------------------
-- Table structure for `goods_kline_min15_info`
-- ----------------------------
DROP TABLE IF EXISTS `goods_kline_min15_info`;
CREATE TABLE `goods_kline_min15_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '代码',
  `period` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '期数 20180606',
  `volume` decimal(18,8) DEFAULT '0.00000000' COMMENT '成交量',
  `price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '当前价',
  `opening_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻开盘价',
  `closing_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻收盘价',
  `pre_closing_price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昨收盘价',
  `highest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最高价',
  `lowest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最低价',
  `date_ymd` date DEFAULT NULL COMMENT '日期',
  `date` datetime DEFAULT NULL COMMENT '日期时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) unsigned DEFAULT '0' COMMENT '1:删除，0:未删除',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=482 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='商品15分钟分时信息';

-- ----------------------------
-- Table structure for `goods_kline_min30_info`
-- ----------------------------
DROP TABLE IF EXISTS `goods_kline_min30_info`;
CREATE TABLE `goods_kline_min30_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '代码',
  `period` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '期数 20180606',
  `volume` decimal(18,8) DEFAULT '0.00000000' COMMENT '成交量',
  `price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '当前价',
  `opening_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻开盘价',
  `closing_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻收盘价',
  `pre_closing_price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昨收盘价',
  `highest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最高价',
  `lowest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最低价',
  `date_ymd` date DEFAULT NULL COMMENT '日期',
  `date` datetime DEFAULT NULL COMMENT '日期时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) unsigned DEFAULT '0' COMMENT '1:删除，0:未删除',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=242 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='商品30分钟分时信息';

-- ----------------------------
-- Table structure for `goods_kline_min5_info`
-- ----------------------------
DROP TABLE IF EXISTS `goods_kline_min5_info`;
CREATE TABLE `goods_kline_min5_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '代码',
  `period` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '期数 20180606',
  `volume` decimal(18,8) DEFAULT '0.00000000' COMMENT '成交量',
  `price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '当前价',
  `opening_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻开盘价',
  `closing_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻收盘价',
  `pre_closing_price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昨收盘价',
  `highest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最高价',
  `lowest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最低价',
  `date_ymd` date DEFAULT NULL COMMENT '日期',
  `date` datetime DEFAULT NULL COMMENT '日期时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) unsigned DEFAULT '0' COMMENT '1:删除，0:未删除',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1288 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='商品5分钟分时信息';

-- ----------------------------
-- Table structure for `goods_kline_min60_info`
-- ----------------------------
DROP TABLE IF EXISTS `goods_kline_min60_info`;
CREATE TABLE `goods_kline_min60_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '代码',
  `period` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '期数 20180606',
  `volume` decimal(18,8) DEFAULT '0.00000000' COMMENT '成交量',
  `price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '当前价',
  `opening_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻开盘价',
  `closing_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻收盘价',
  `pre_closing_price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昨收盘价',
  `highest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最高价',
  `lowest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最低价',
  `date_ymd` date DEFAULT NULL COMMENT '日期',
  `date` datetime DEFAULT NULL COMMENT '日期时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) unsigned DEFAULT '0' COMMENT '1:删除，0:未删除',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=223 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='商品60分钟分时信息';

-- ----------------------------
-- Table structure for `goods_kline_month_info`
-- ----------------------------
DROP TABLE IF EXISTS `goods_kline_month_info`;
CREATE TABLE `goods_kline_month_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '代码',
  `period` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '期数 20180606',
  `volume` decimal(32,16) DEFAULT '0.0000000000000000' COMMENT '成交量',
  `price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '当前价',
  `opening_price` decimal(32,16) DEFAULT '0.0000000000000000' COMMENT '前一刻开盘价',
  `closing_price` decimal(32,16) DEFAULT '0.0000000000000000' COMMENT '前一刻收盘价',
  `pre_closing_price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昨收盘价',
  `highest_price` decimal(32,16) DEFAULT '0.0000000000000000' COMMENT '最高价',
  `lowest_price` decimal(32,16) DEFAULT '0.0000000000000000' COMMENT '最低价',
  `date_ymd` date DEFAULT NULL COMMENT '日期',
  `date` datetime DEFAULT NULL COMMENT '日期时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) unsigned DEFAULT '0' COMMENT '1:删除，0:未删除',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='商品分时信息';

-- ----------------------------
-- Table structure for `goods_kline_week_info`
-- ----------------------------
DROP TABLE IF EXISTS `goods_kline_week_info`;
CREATE TABLE `goods_kline_week_info` (
  `id` bigint(32) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '代码',
  `period` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '期数 20180606',
  `volume` decimal(32,16) DEFAULT '0.0000000000000000' COMMENT '成交量',
  `price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '当前价',
  `opening_price` decimal(32,16) DEFAULT '0.0000000000000000' COMMENT '前一刻开盘价',
  `closing_price` decimal(32,16) DEFAULT '0.0000000000000000' COMMENT '前一刻收盘价',
  `pre_closing_price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昨收盘价',
  `highest_price` decimal(32,16) DEFAULT '0.0000000000000000' COMMENT '最高价',
  `lowest_price` decimal(32,16) DEFAULT '0.0000000000000000' COMMENT '最低价',
  `date_ymd` date DEFAULT NULL COMMENT '日期',
  `date` datetime DEFAULT NULL COMMENT '日期时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) unsigned DEFAULT '0' COMMENT '1:删除，0:未删除',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`date`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='WeeK信息表';

-- ----------------------------
-- Table structure for `goods_kline_year_info`
-- ----------------------------
DROP TABLE IF EXISTS `goods_kline_year_info`;
CREATE TABLE `goods_kline_year_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `code` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '代码',
  `period` char(8) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '期数 20180606',
  `volume` decimal(18,8) DEFAULT '0.00000000' COMMENT '成交量',
  `price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '当前价',
  `opening_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻开盘价',
  `closing_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '前一刻收盘价',
  `pre_closing_price` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL COMMENT '昨收盘价',
  `highest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最高价',
  `lowest_price` decimal(18,8) DEFAULT '0.00000000' COMMENT '最低价',
  `date_ymd` date DEFAULT NULL COMMENT '日期',
  `date` datetime DEFAULT NULL COMMENT '日期时间',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `is_deleted` tinyint(1) unsigned DEFAULT '0' COMMENT '1:删除，0:未删除',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `code` (`code`,`date`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT COMMENT='商品60分钟分时信息';
