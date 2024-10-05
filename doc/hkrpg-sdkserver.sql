/*
hkrpg-sdkserver by cokesever@qq.com
latest update time: 2024-10-05
*/
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `t_accounts`;
CREATE TABLE `t_accounts`  (
  `uid` int NOT NULL AUTO_INCREMENT COMMENT '玩家UID',
  `name` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '用户名',
  `mobile` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '手机号',
  `email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '电子邮件',
  `password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '哈希密码',
  `type` int NOT NULL COMMENT '1 注册 0 未注册',
  `epoch_created` int NOT NULL COMMENT '时间戳',
  PRIMARY KEY (`uid`) USING BTREE,
  UNIQUE INDEX `mobile`(`mobile` ASC) USING BTREE,
  UNIQUE INDEX `email`(`email` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '玩家账号信息表' ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `t_accounts_guests`;
CREATE TABLE `t_accounts_guests`  (
  `device` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '设备ID',
  `client` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '客户端类型',
  `version` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '客户端版本',
  `token` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '游客登录Token',
  `epoch_generated` int NOT NULL COMMENT 'Token时间戳',
  PRIMARY KEY (`device`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '游客登录信息表' ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `t_accounts_tokens`;
CREATE TABLE `t_accounts_tokens`  (
  `uid` int NOT NULL COMMENT '玩家UID',
  `token` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '登录Token',
  `device` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NULL DEFAULT NULL COMMENT '设备ID',
  `ip` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '登录IP',
  `epoch_generated` int NOT NULL COMMENT '时间戳',
  PRIMARY KEY (`uid`, `token`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '账号登录token' ROW_FORMAT = Dynamic;

DROP TABLE IF EXISTS `t_combo_tokens`;
CREATE TABLE `t_combo_tokens`  (
  `uid` int NOT NULL COMMENT '玩家UID',
  `token` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '登录Token',
  `device` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '设备ID',
  `ip` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL COMMENT '登录IP',
  `epoch_generated` int NOT NULL COMMENT '时间戳',
  PRIMARY KEY (`uid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb3 COLLATE = utf8mb3_general_ci COMMENT = '设备信息token' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
