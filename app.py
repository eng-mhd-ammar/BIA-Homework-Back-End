from flask import Flask, jsonify
from routes.auth_routes import auth_bp
from routes.upload_routes import upload_bp
from routes.user_tables_routes import user_tables_bp
from routes.ga_routes import ga_bp
from routes.table_view_routes import table_view_bp
from routes.traditional_routes import traditional_bp
from flask_cors import CORS

app = Flask(__name__, static_url_path="/uploaded_files", static_folder="uploaded_files")
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(user_tables_bp)
app.register_blueprint(ga_bp)
app.register_blueprint(table_view_bp)
app.register_blueprint(traditional_bp)

@app.route("/api/ping")
def ping():
    return jsonify({"message": "pong"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
