import os
import pandas as pd
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine
from config import DATABASE_URL
from utils import sanitize_table_name, token_required
from models import db_session, UserTables

upload_bp = Blueprint("upload", __name__, url_prefix="/api/upload")
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

@upload_bp.route("/", methods=["POST"])
@token_required
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filename_only, ext = os.path.splitext(file.filename)
    ext = ext.lower()

    if ext not in [".xlsx", ".xls", ".csv"]:
        return jsonify({"error": "Only .xlsx, .xls, .csv files are supported"}), 400

    try:
        if ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")
        elif ext == ".xls":
            df = pd.read_excel(file, engine="xlrd")
        elif ext == ".csv":
            df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    # Create table name as username_filename
    username = request.user.username
    table_name = sanitize_table_name(f"{username}_{filename_only}")

    df.to_sql(table_name, con=engine, if_exists="replace", index=False)

    old_entry = db_session.query(UserTables).filter_by(user_id=request.user.id, table_name=table_name).first()
    if old_entry:
        db_session.delete(old_entry)
        db_session.commit()

    new_entry = UserTables(user_id=request.user.id, table_name=table_name)
    db_session.add(new_entry)
    db_session.commit()

    return jsonify({"message": f"File uploaded successfully to table {table_name}"})
