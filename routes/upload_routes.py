import os
import pandas as pd
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from utils import sanitize_table_name, token_required
from models import db_session, UserTable, GAResult, GAGeneration, engine
from services.ga_service import run_ga_on_df
from services.traditional_service import run_traditional_on_df
from models import TraditionalResult

upload_bp = Blueprint("upload", __name__, url_prefix="/api/upload")
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    safe_filename = sanitize_table_name(f"{request.user.username}_{secure_filename(file.filename)}")
    file_path = os.path.join(UPLOAD_FOLDER, safe_filename + ext)
    file.save(file_path)

    try:
        if ext in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    table_name = sanitize_table_name(f"{request.user.username}_{filename_only}")
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)

    old_entry = db_session.query(UserTable).filter_by(user_id=request.user.id, table_name=table_name).first()
    if old_entry:
        db_session.delete(old_entry)
        db_session.commit()

    new_user_table = UserTable(user_id=request.user.id, table_name=table_name, source_file=file_path)
    db_session.add(new_user_table)
    db_session.commit()

    ga_result_data = run_ga_on_df(df)
    new_ga_entry = GAResult(
        user_table_id=new_user_table.id,
        best_chromosome=ga_result_data["best_chromosome"],
        selected_features=ga_result_data["selected_features"],
        fitness=ga_result_data["fitness"],
    )
    db_session.add(new_ga_entry)
    db_session.commit()

    for gen in ga_result_data["generations_stats"]:
        new_gen_entry = GAGeneration(
            ga_result_id=new_ga_entry.id,
            generation=gen["generation"],
            best_genes=gen["best_genes"],
            avg_fitness=gen["avg_fitness"],
            best_fitness=gen["best_fitness"]
        )
        db_session.add(new_gen_entry)

    traditional_result_data = run_traditional_on_df(df)
    
    new_traditional_entry = TraditionalResult(
        user_table_id=new_user_table.id,
        best_chromosome=traditional_result_data["best_chromosome"],
        selected_features=traditional_result_data["selected_features"],
        feature_weights=traditional_result_data["feature_weights"],
        stages=traditional_result_data["stages"]
    )
    db_session.add(new_traditional_entry)
    db_session.commit()

    return jsonify({
        "message": f"File uploaded and both algorithms executed successfully.",
        "ga_result_id": new_ga_entry.id,
        "lasso_result_id": new_traditional_entry.id
    })