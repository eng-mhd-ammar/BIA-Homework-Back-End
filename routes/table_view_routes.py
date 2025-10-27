from flask import Blueprint, jsonify, request
from utils import token_required
from models import db_session, UserTable
from sqlalchemy import text
import pandas as pd


# Get Data from Database ====================================================================
table_view_bp = Blueprint("table_view", __name__, url_prefix="/api")

@table_view_bp.route("/view-table/<int:table_id>", methods=["GET"])
@token_required
def view_table(table_id):
    user_table = db_session.query(UserTable).filter_by(id=table_id).first()
    if not user_table or user_table.user_id != request.user.id:
        return jsonify({"error": "Table not found"}), 404

    try:
        table_name = user_table.table_name

        per_page = 30

        page = request.args.get("page", 1, type=int)
        offset = (page - 1) * per_page

        query = text(f"SELECT * FROM `{table_name}` LIMIT :limit OFFSET :offset")
        result = db_session.execute(query, {"limit": per_page, "offset": offset})
        rows = [dict(row) for row in result.mappings().all()]

        total_query = db_session.execute(text(f"SELECT COUNT(*) as total FROM `{table_name}`"))
        total_records = total_query.scalar()
        total_pages = (total_records + per_page - 1) // per_page

        columns = list(rows[0].keys()) if rows else []

        return jsonify({
            "table_name": table_name,
            "columns": columns,
            "data": rows,
            "pagination": {
                "current_page": page,
                "per_page": per_page,
                "total_records": total_records,
                "total_pages": total_pages
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Get Data from file (faster than database)
# @table_view_bp.route("/view-table/<int:table_id>", methods=["GET"])
# @token_required
# def view_table(table_id):
#     user_table = db_session.query(UserTable).filter_by(id=table_id).first()
#     if not user_table or user_table.user_id != request.user.id:
#         return jsonify({"error": "Table not found"}), 404

#     try:
#         file_path = user_table.source_file
#         if file_path.endswith((".xls", ".xlsx")):
#             df = pd.read_excel(file_path)
#         else:
#             df = pd.read_csv(file_path)

#         data = df.to_dict(orient="records")
#         columns = list(df.columns)
#         return jsonify({"table_name": user_table.table_name, "columns": columns, "data": data})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500