from flask import Flask, jsonify, send_from_directory
from auth import auth_bp
from upload import upload_bp

app = Flask(__name__)
app = Flask(__name__, static_url_path="/uploaded_files", static_folder="uploaded_files")
app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)


@app.route("/api/ping")
def ping():
    return {"message": "pong"}

# @app.route("/api/hello")
# def hello():
#     return jsonify({"message": "Hello"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)