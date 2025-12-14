from flask import Blueprint, request, jsonify, url_for
import requests
import pymysql
from configs.logging_config import logger
from configs.general_constants import DB_CONFIG, WECHAT_APP_ID, WECHAT_APP_SECRET, BASE_URL

bp = Blueprint('login', __name__)


def get_db_connection():
    return pymysql.connect(**DB_CONFIG)


def create_user(openid, username=None, avatar=None):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO users (openid, username, avatar)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (openid, username, avatar))
            connection.commit()
            return True, "User created successfully"
    except pymysql.Error as e:
        logger.error(f"Error in create_user: {e}")
        if connection:
            connection.rollback()
        return False, str(e)
    finally:
        if connection:
            connection.close()


def check_user_exists(openid):
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM users WHERE openid = %s", (openid,))
            return cursor.fetchone() is not None
    except pymysql.Error as e:
        logger.error(f"Error in check_user_exists: {e}")
        return False
    finally:
        if connection:
            connection.close()


@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    code = data.get('code')
    if not code:
        return jsonify({'error': 'Missing code'}), 400

    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': WECHAT_APP_ID,
        'secret': WECHAT_APP_SECRET,
        'js_code': code,
        'grant_type': 'authorization_code'
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            result = response.json()
            openid = result.get('openid')
            if not openid:
                logger.error('Failed to get openid from WeChat API')
                return jsonify({'error': 'Failed to get openid'}), 500

            if check_user_exists(openid):
                logger.info(f"User with openid {openid} already exists")
                return jsonify({'openid': openid})
            else:
                # 只存相对 static 的路径：如 "default/default_avatar.png"
                default_avatar_path = 'default/default_avatar.png'
                success, message = create_user(
                    openid=openid,
                    username="用户",
                    avatar=default_avatar_path  # 不带 /static/
                )
                if not success:
                    logger.error(f"Failed to create user: {message}")
                    return jsonify({'error': message}), 500
                logger.info(f"Success to create user: {message}")
                return jsonify({'openid': openid})
        else:
            logger.error(f"WeChat API returned status {response.status_code}: {response.text}")
            return jsonify({'error': 'Failed to connect to WeChat server'}), 500
    except Exception as e:
        logger.error(f"Error in login: {e}")
        return jsonify({'error': f"Error in login: {str(e)}"}), 500
