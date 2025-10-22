from flask import Blueprint, jsonify, request
from models import db_session, UserTable
from utils import token_required

user_tables_bp = Blueprint("tables", __name__, url_prefix="/api")


@user_tables_bp.route("/user-tables", methods=["GET"])
@token_required
def get_my_tables():
    user = request.user
    try:
        tables = db_session.query(UserTable).filter_by(user_id=user.id).all()

        result = []
        for t in tables:
            ga = t.ga_results[-1] if t.ga_results else None
            result.append({
                "id": t.id,
                "table_name": t.table_name,
                "source_file": t.source_file,
                "ga_result": {
                    "id": ga.id if ga else None,
                    "fitness": ga.fitness if ga else None,
                    "selected_features": ga.selected_features if ga else []
                }
            })

        return jsonify({"tables": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500