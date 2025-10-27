# utils.py
import re
from flask import request, jsonify
from itsdangerous import URLSafeTimedSerializer as Serializer, BadSignature, SignatureExpired
from config import SECRET_KEY
from models import db_session, User

# Create Table Name
def sanitize_table_name(s: str) -> str:
    s = re.sub(r"[^\w]", "_", s)
    return s.lower()

def get_serializer():
    return Serializer(SECRET_KEY)

# Create Bearer Token
def create_token(user_id, username):
    s = get_serializer()
    return s.dumps({"id": user_id, "username": username})

# Token Validation
def verify_token(token, expires_sec=604800):
    s = get_serializer()
    try:
        data = s.loads(token, max_age=expires_sec)
    except SignatureExpired:
        return None
    except BadSignature:
        return None
    return db_session.query(User).filter_by(id=data["id"]).first()

# To Make Token Required
def token_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth or not auth.lower().startswith("bearer "):
            return jsonify({"error": "Missing token"}), 401
        token = auth.split()[1]
        user = verify_token(token)
        if not user:
            return jsonify({"error": "Invalid or expired token"}), 401
        request.user = user
        return f(*args, **kwargs)
    return decorated
