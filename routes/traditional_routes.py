from flask import Blueprint, jsonify, request
from utils import token_required
from models import db_session, TraditionalResult

traditional_bp = Blueprint("traditional", __name__, url_prefix="/api")

@traditional_bp.route("/traditional-results/<int:table_id>", methods=["GET"])
@token_required
def get_traditional_result(table_id):
    trad_result = db_session.query(TraditionalResult).filter_by(user_table_id=table_id).first()
    if not trad_result or trad_result.user_table.user_id != request.user.id:
        return jsonify({"error": "Traditional result not found"}), 404

    response = {
        "id": trad_result.id,
        "table_id": trad_result.user_table_id,
        "best_chromosome": trad_result.best_chromosome,
        "selected_features": trad_result.selected_features,
        "feature_weights": trad_result.feature_weights,
        "stages": trad_result.stages,
        "summary": {
            "num_selected_features": len(trad_result.selected_features),
            "max_weight": max(trad_result.feature_weights) if trad_result.feature_weights else 0,
            "min_weight": min(trad_result.feature_weights) if trad_result.feature_weights else 0,
        }
    }

    return jsonify(response)
