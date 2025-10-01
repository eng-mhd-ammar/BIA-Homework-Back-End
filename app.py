from flask import Flask, jsonify
from auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)

@app.route("/api/ping")
def ping():
    return {"message": "pong"}

# @app.route("/api/hello")
# def hello():
#     return jsonify({"message": "Hello"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)