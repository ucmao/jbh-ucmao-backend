from flask import Blueprint, jsonify, send_file
import csv
import io
from configs.logging_config import logger
from configs.general_constants import DB_CONFIG
import pymysql

# 创建蓝图
bp = Blueprint('export', __name__)


# 获取数据库连接
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)


# 导出用户物品为 CSV
@bp.route('/export-items/<string:openid>', methods=['GET'])
def export_items(openid):
    if not openid:
        return jsonify({'error': 'openid is required'}), 400

    try:
        # 获取用户的所有物品
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # 根据 openid 查询 user_id
            sql = "SELECT id FROM users WHERE openid = %s"
            cursor.execute(sql, (openid,))
            user = cursor.fetchone()

            if not user:
                return jsonify({'error': 'User not found'}), 404

            user_id = user['id']

            # 获取用户的所有 items
            sql = """
                SELECT * FROM items
                WHERE user_id = %s AND deleted_at IS NULL
            """
            cursor.execute(sql, (user_id,))
            items = cursor.fetchall()

        # 将数据写入 CSV 文件
        output = io.StringIO()
        writer = csv.writer(output)

        # 写入表头
        writer.writerow([
            '分类', '物品名称', '购买日期', '购买价格',
            '退役日期', '退役价格', '备注', '是否收藏', '使用次数', '日均价格',
            '创建时间', '更新时间'
        ])

        # 写入数据
        for item in items:
            writer.writerow([
                item['category'],
                item['item_name'],
                item['purchase_date'].isoformat() if item['purchase_date'] else '',
                item['purchase_price'],
                item['retirement_date'].isoformat() if item['retirement_date'] else '',
                item['retirement_price'],
                item['description'],
                item['is_favorite'],
                item['use_count_value'],
                item['daily_price'],
                item['created_at'].isoformat(),
                item['updated_at'].isoformat()
            ])

        output.seek(0)

        # 返回文件
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='items.csv'
        )
    except Exception as e:
        logger.error(f"Error in export_items: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection:
            connection.close()
