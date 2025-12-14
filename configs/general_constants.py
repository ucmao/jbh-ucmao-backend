import os
from pymysql.cursors import DictCursor
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 图标文件路径
ICONS_DIR = os.path.join(BASE_DIR, 'static', 'icons')

# 微信配置
WECHAT_APP_ID = os.getenv('WECHAT_APP_ID')
WECHAT_APP_SECRET = os.getenv('WECHAT_APP_SECRET')

# 基础URL
BASE_URL = os.getenv('BASE_URL')

# MySQL 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': os.getenv('DB_CHARSET', 'utf8mb4'),  # 提供默认值
    'cursorclass': DictCursor
}

# 如果 host 是 localhost，移除 port 配置
if DB_CONFIG["host"] == "localhost":
    DB_CONFIG.pop("port", None)
