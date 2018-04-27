SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for agent
-- ----------------------------
DROP TABLE IF EXISTS `agent`;
CREATE TABLE `agent` (
  `id` int(255) unsigned NOT NULL AUTO_INCREMENT,
  `type` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `port` int(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_getailist` (`type`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of agent
-- ----------------------------

-- ----------------------------
-- Table structure for config
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `key` varchar(255) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`key`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of config
-- ----------------------------
INSERT INTO `config` VALUES ('maximum_agent', '1');

-- ----------------------------
-- Table structure for quota
-- ----------------------------
DROP TABLE IF EXISTS `quota`;
CREATE TABLE `quota` (
  `type` varchar(255) NOT NULL,
  `maximum_quota` int(11) DEFAULT NULL,
  PRIMARY KEY (`type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of quota
-- ----------------------------
INSERT INTO `quota` VALUES ('entangled_endive', '512');
SET FOREIGN_KEY_CHECKS=1;
