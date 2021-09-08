/*
 Navicat Premium Data Transfer

 Source Server         : cl
 Source Server Type    : MySQL
 Source Server Version : 50732
 Source Schema         : lc_oversea_product

 Target Server Type    : MySQL
 Target Server Version : 50732
 File Encoding         : 65001

 Date: 08/09/2021 10:02:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for oversea_products
-- ----------------------------
DROP TABLE IF EXISTS `oversea_products`;
CREATE TABLE `oversea_products`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `catalog1` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `provider` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '供应商',
  `productCodeProvider` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '供应商商物料码',
  `productCodeManufacturer` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '生产商物料码',
  `productCodeManufacturerHighlight` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `productGradePlateName` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `productGradePlateNameHighlight` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `stockNumber` int(11) NULL DEFAULT NULL COMMENT '库存',
  `minBuyNumber` int(11) NULL DEFAULT NULL,
  `productMinEncapsulationNumber` int(11) NULL DEFAULT NULL,
  `breviaryImageUrl` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `bigImageUrl` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `brandId` int(11) NULL DEFAULT NULL,
  `brandName` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `packaging` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `detailUrl` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `updateTime` datetime(0) NULL DEFAULT NULL,
  `eccn` varchar(60) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `dataSheetUrl` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9123 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
