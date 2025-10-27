from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db_session, User
from utils import create_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def get_request_data():
    if request.is_json:
        return request.get_json()
    return request.form.to_dict()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = get_request_data()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if db_session.query(User).filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username, password=generate_password_hash(password))
    db_session.add(user)
    db_session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = get_request_data()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = db_session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_token(user.id, user.username)
    return jsonify({"token": token, "message": "Login successful"}), 200

