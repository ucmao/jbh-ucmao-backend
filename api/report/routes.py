from flask import Blueprint, jsonify
from datetime import datetime
from configs.general_constants import DB_CONFIG
from configs.logging_config import logger
import pymysql

# 创建蓝图
bp = Blueprint('report', __name__)


# 获取数据库连接
def get_db_connection():
    try:
        connection = pymysql.connect(**DB_CONFIG)

        return connection
    except Exception as e:
        logger.error(f"Failed to connect to the database: {str(e)}")
        raise


# 导出用户报告
@bp.route('/report-items/<string:openid>', methods=['GET'])
def generate_report_by_openid(openid):
    try:
        connection = get_db_connection()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 根据 openid 查询 user_id

            cursor.execute("SELECT id FROM users WHERE openid = %s", (openid,))
            user = cursor.fetchone()
            if not user:
                logger.warning(f"User with openid {openid} not found.")
                return jsonify({'error': 'User not found'}), 404

            user_id = user['id']

            # 获取用户的所有 items

            cursor.execute("""
                SELECT * FROM items
                WHERE user_id = %s AND deleted_at IS NULL
            """, (user_id,))
            items = cursor.fetchall()

        today = datetime.now().date()
        report = {
            'assets': {
                'all': {'count': 0, 'amount': 0, 'days': 0, 'daily_avg': 0},
                'active': {'count': 0, 'amount': 0, 'days': 0, 'daily_avg': 0},
                'retired': {'count': 0, 'amount': 0, 'days': 0, 'daily_avg': 0},
                'favorite': {'count': 0, 'amount': 0, 'days': 0, 'daily_avg': 0}
            },
            'categories': {}
        }

        for item in items:
            purchase_price = item['purchase_price'] or 0
            purchase_date = item['purchase_date']
            retirement_price = item['retirement_price'] or 0
            retirement_date = item['retirement_date']

            price = purchase_price - retirement_price

            # 在计算 days 之前，确保数据类型的正确性
            if item['use_count_value']:
                # 将 use_count_value 转换为整数
                days = int(item['use_count_value'])
            elif item['daily_price']:
                # 计算浮点数天数
                days = int(float(purchase_price) / float(item['daily_price']))
            else:
                days = ((retirement_date or today) - purchase_date).days + 1

            # 更新资产统计
            report['assets']['all']['count'] += 1
            report['assets']['all']['amount'] += price
            report['assets']['all']['days'] += days

            if retirement_date:
                report['assets']['retired']['count'] += 1
                report['assets']['retired']['amount'] += price
                report['assets']['retired']['days'] += days
            else:
                report['assets']['active']['count'] += 1
                report['assets']['active']['amount'] += price
                report['assets']['active']['days'] += days

            if item['is_favorite']:
                report['assets']['favorite']['count'] += 1
                report['assets']['favorite']['amount'] += price
                report['assets']['favorite']['days'] += days

            # 更新类别统计
            category = item['category'] or "undefined"
            if category not in report['categories']:
                report['categories'][category] = {'count': 0, 'amount': 0, 'days': 0, 'daily_avg': 0}
            report['categories'][category]['count'] += 1
            report['categories'][category]['amount'] += price
            report['categories'][category]['days'] += days

        # 计算日均平均值

        for key in report['assets']:
            if report['assets'][key]['days'] > 0:
                report['assets'][key]['daily_avg'] = round(report['assets'][key]['amount'] / report['assets'][key]['days'], 2)

        for category in report['categories']:
            if report['categories'][category]['days'] > 0:
                report['categories'][category]['daily_avg'] = round(
                    report['categories'][category]['amount'] / report['categories'][category]['days'], 2
                )

        return jsonify(report)

    except Exception as e:
        logger.error(f"An error occurred while generating the report: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500
