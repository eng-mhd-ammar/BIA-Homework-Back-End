from flask import Blueprint, jsonify, request
from utils import token_required
from models import db_session, UserTable
from sqlalchemy import text
import pandas as pd


# Get Data from Database ====================================================================
table_view_bp = Blueprint("table_view", __name__, url_prefix="/api")

# @table_view_bp.route("/view-table/<int:table_id>", methods=["GET"])
# @token_required
# def view_table(table_id):
#     user_table = db_session.query(UserTable).filter_by(id=table_id).first()
#     if not user_table or user_table.user_id != request.user.id:
#         return jsonify({"error": "Table not found"}), 404

#     try:
#         table_name = user_table.table_name

#         result = db_session.execute(text(f"SELECT * FROM `{table_name}`"))
#         rows = [dict(row) for row in result.mappings().all()]

#         columns = list(rows[0].keys()) if rows else []

#         return jsonify({
#             "table_name": table_name,
#             "columns": columns,
#             "data": rows
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# Get Data from file (faster than database)
@table_view_bp.route("/view-table/<int:table_id>", methods=["GET"])
@token_required
def view_table(table_id):
    user_table = db_session.query(UserTable).filter_by(id=table_id).first()
    if not user_table or user_table.user_id != request.user.id:
        return jsonify({"error": "Table not found"}), 404

    try:
        file_path = user_table.source_file
        if file_path.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        data = df.to_dict(orient="records")
        columns = list(df.columns)
        return jsonify({"table_name": user_table.table_name, "columns": columns, "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500