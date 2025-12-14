-- --------------------------------------------------------
-- 数据库: `ucmao_jbh`
-- Mysql服务器版本: 5.7 
-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL COMMENT '用户ID，主键，自增',
  `openid` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户唯一标识',
  `username` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户昵称',
  `avatar` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '用户头像URL',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '软删除时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='用户表';

--
-- 表的索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `openid` (`openid`);

--
-- 在导出的表使用 AUTO_INCREMENT
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;


-- --------------------------------------------------------

--
-- 表的结构 `items`
--

CREATE TABLE `items` (
  `id` int(11) NOT NULL COMMENT '物品ID，主键，自增',
  `user_id` int(11) NOT NULL COMMENT '所属用户ID，外键关联 users.id',
  `category` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '物品类别',
  `item_image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '物品图片URL',
  `item_name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL COMMENT '物品名称',
  `purchase_date` date DEFAULT NULL COMMENT '购买日期',
  `purchase_price` decimal(10,2) DEFAULT NULL COMMENT '购买价格',
  `use_count_value` int(11) DEFAULT NULL COMMENT '使用次数或值',
  `daily_price` decimal(10,2) DEFAULT NULL COMMENT '每日价格（可能用于计算价值）',
  `retirement_date` date DEFAULT NULL COMMENT '预计报废/丢弃日期',
  `retirement_price` decimal(10,2) DEFAULT NULL COMMENT '报废/丢弃时估价',
  `description` text COLLATE utf8mb4_general_ci COMMENT '物品描述',
  `is_favorite` tinyint(1) DEFAULT '0' COMMENT '是否收藏 (0否, 1是)',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` timestamp NULL DEFAULT NULL COMMENT '软删除时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='物品清单表';

--
-- 表的索引 `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_items_user_id` (`user_id`); -- 为 user_id 添加索引

--
-- 在导出的表使用 AUTO_INCREMENT
--
ALTER TABLE `items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 限制导出的表
--
ALTER TABLE `items`
  ADD CONSTRAINT `fk_items_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;