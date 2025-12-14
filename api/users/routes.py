from flask import Blueprint, request, jsonify
import pymysql
from configs.logging_config import logger
from configs.general_constants import DB_CONFIG, BASE_URL

bp = Blueprint('users', __name__)


def get_db_connection():
    return pymysql.connect(**DB_CONFIG)


@bp.route('/update', methods=['POST'])
def user_update():
    data = request.get_json()
    openid = data.get('openid')
    username = data.get('username')
    avatar = data.get('avatar')

    if not openid:
        return jsonify({'error': 'openid is required'}), 400

    # 处理 avatar：从完整 URL 提取 static 后的路径
    if avatar and isinstance(avatar, str):
        base = BASE_URL.rstrip('/')
        full_static_prefix = base + '/static/'
        if avatar.startswith(full_static_prefix):
            # 提取 "default/xxx.png" 部分
            avatar = avatar[len(full_static_prefix):]
        else:
            # 如果不符合格式，可选择拒绝或保留原值（建议拒绝）
            logger.warning(f"Invalid avatar URL format from user {openid}: {avatar}")
            return jsonify({'error': 'Avatar URL must be under your static domain'}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                UPDATE users
                SET username = %s, avatar = %s
                WHERE openid = %s
            """
            cursor.execute(sql, (username, avatar, openid))
            affected_rows = cursor.rowcount
        connection.commit()

        if affected_rows > 0:
            logger.info(f"User {openid} updated successfully")
            return jsonify({'message': 'User updated successfully'}), 200
        else:
            logger.warning(f"Update failed: user with openid {openid} not found")
            return jsonify({'error': 'User not found'}), 404

    except pymysql.IntegrityError as e:
        logger.error(f"Integrity error in user_update: {e}")
        return jsonify({'error': 'Database integrity error'}), 400
    except pymysql.Error as e:
        logger.error(f"MySQL error in user_update: {e}")
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        logger.error(f"Unexpected error in user_update: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if connection:
            connection.close()
