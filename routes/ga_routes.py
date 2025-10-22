from flask import Blueprint, jsonify, request
from utils import token_required
from models import db_session, GAResult

ga_bp = Blueprint("ga", __name__, url_prefix="/api")

@ga_bp.route("/ga-results/<int:ga_result_id>", methods=["GET"])
@token_required
def get_ga_result(ga_result_id):
    ga_result = db_session.query(GAResult).filter_by(id=ga_result_id).first()
    if not ga_result or ga_result.user_table.user_id != request.user.id:
        return jsonify({"error": "GA result not found"}), 404

    generations = []
    for g in ga_result.generations:
        generations.append({
            "generation": g.generation,
            "best_genes": g.best_genes,
            "best_fitness": round(g.best_fitness, 4),
            "avg_fitness": round(g.avg_fitness, 4),
        })

    generations.sort(key=lambda x: x["generation"])

    response = {
        "id": ga_result.id,
        "table_id": ga_result.user_table_id,
        "fitness": round(ga_result.fitness, 4),
        "selected_features": ga_result.selected_features,
        "best_chromosome": ga_result.best_chromosome,
        "summary": {
            "total_generations": len(generations),
            "best_fitness": round(max(g["best_fitness"] for g in generations), 4),
            "avg_of_avgs": round(sum(g["avg_fitness"] for g in generations) / len(generations), 4) if generations else 0,
        },
        "generations": generations
    }

    return jsonify(response)
