# 记宝盒 后端服务（jbh-ucmao-backend）

## 项目简介

**jbh-ucmao-backend** 是 记宝盒 微信小程序的后端服务，提供物品管理、用户认证、数据统计和导出等核心功能。

> 本仓库提供记宝盒小程序的后端服务。如果你需要前端代码，请参考[前端仓库链接](https://github.com/ucmao/jbh-ucmao-mp)

## 📱 立即体验与总览 ✨

欢迎扫码体验本项目的实际功能和效果。

| 扫码体验正式版 | 后端服务仓库 |
|:---:|:---:|
| ![记宝盒太阳码](qr_code.jpg)<br>🚀 [记宝盒前端服务](https://github.com/ucmao/jbh-ucmao-mp) | 当前仓库 |

## 技术栈

- **框架**：Flask 3.0.3
- **数据库**：MySQL
- **ORM**：PyMySQL
- **认证**：微信小程序登录
- **日志**：Python logging
- **部署**：支持 Gunicorn、Uvicorn 等 WSGI/ASGI 服务器

## 项目结构

```
jbh-ucmao-backend/
├── api/                    # API 路由模块
│   ├── export/             # 数据导出模块
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── items/              # 物品管理模块
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── login/              # 用户登录模块
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── report/             # 数据统计模块
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── users/              # 用户管理模块
│   │   ├── __init__.py
│   │   └── routes.py
│   └── __init__.py
├── configs/                # 配置文件
│   ├── general_constants.py  # 通用常量
│   └── logging_config.py     # 日志配置
├── static/                 # 静态资源
│   ├── default/            # 默认资源
│   └── icons/              # 分类图标
├── .env.example            # 环境变量示例
├── .gitignore              # Git 忽略文件
├── app.py                  # 应用入口
├── requirements.txt        # 依赖列表
└── schema.sql              # 数据库结构文件
```

## 环境要求

- Python 3.8+
- MySQL 5.7+
- pip 20.0+

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/ucmao/jbh-ucmao-backend.git
cd jbh-ucmao-backend
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
# 编辑 .env 文件，设置数据库、微信小程序等配置
```

### 4. 初始化数据库

#### 创建数据库

首先，创建一个MySQL数据库：

```bash
mysql -u root -p
CREATE DATABASE ucmao_jbh CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
EXIT;
```

#### 导入数据库结构

使用 `schema.sql` 文件初始化数据库表结构：

```bash
mysql -u root -p ucmao_jbh < schema.sql
```

### 5. 启动服务

#### 开发模式

```bash
python app.py
```

服务将在 `http://0.0.0.0:5007` 启动。

#### 生产模式

使用 Gunicorn：

```bash
gunicorn -w 4 -b 0.0.0.0:5007 app:app
```

或使用 Uvicorn：

```bash
uvicorn app:app --host 0.0.0.0 --port 5007
```

## 配置说明

### 环境变量

| 配置项 | 描述 | 默认值 |
|--------|------|--------|
| BASE_URL | 服务基础 URL | - |
| WECHAT_APP_ID | 微信小程序 AppID | - |
| WECHAT_APP_SECRET | 微信小程序 AppSecret | - |
| DB_HOST | 数据库主机 | - |
| DB_PORT | 数据库端口 | - |
| DB_USER | 数据库用户名 | - |
| DB_PASSWORD | 数据库密码 | - |
| DB_NAME | 数据库名称 | - |
| DB_CHARSET | 数据库字符集 | utf8mb4 |

## API 文档

### 登录模块

#### 微信登录
```
POST /api/login
```

参数：
- `code`: 微信小程序登录 code

返回：
- `openid`: 用户唯一标识

### 物品管理模块

#### 获取分类列表
```
GET /api/items/categories
```

返回：分类列表及图标 URL

#### 添加物品
```
POST /api/items/add_item
```

参数：
- `openid`: 用户唯一标识
- `category`: 分类
- `item_name`: 物品名称
- `purchase_date`: 购买日期
- `purchase_price`: 购买价格
- `use_count_value`: 使用次数
- `daily_price`: 日均价格
- `retirement_date`: 退役日期
- `retirement_price`: 退役价格
- `description`: 描述
- `is_favorite`: 是否收藏

#### 获取用户物品列表
```
GET /api/items/user/<openid>
```

返回：用户所有物品列表

#### 更新物品
```
PUT /api/items/item/<item_id>
```

参数：
- 同添加物品（可选）

#### 删除物品
```
DELETE /api/items/item/<item_id>
```

### 用户管理模块

#### 更新用户信息
```
POST /api/users/update
```

参数：
- `openid`: 用户唯一标识
- `username`: 用户名
- `avatar`: 头像 URL

### 数据导出模块

#### 导出用户物品为 CSV
```
GET /api/export/export-items/<openid>
```

返回：CSV 文件下载

### 数据统计模块

#### 生成用户物品统计报告
```
GET /api/report/report-items/<openid>
```

返回：用户物品统计报告

## 开发指南

### 日志

日志文件位于 `logs/jbh_ucmao.log`，包含应用运行状态、错误信息等。

### 静态资源

图标等静态资源位于 `static/icons/` 目录，按分类组织。

## 贡献

欢迎提交 Issue 和 Pull Request！

### 提交规范

- 提交代码前请确保通过语法检查
- 提交信息请使用清晰的描述，如：`fix: 修复数据库连接错误`

## 许可证

本项目采用 MIT 许可证，详情请见 [LICENSE](LICENSE) 文件。

## 联系方式

- GitHub: [ucmao](https://github.com/ucmao)
- Email: leoucmao@gmail.com