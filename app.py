"""Flask entry point, locally and on Vercel."""

from flask import Flask, jsonify, render_template, request

from calculator import calculate

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify(status="ok", service="devops-calculator")


@app.post("/api/calculate")
def api_calculate():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Send a JSON object"), 400

    try:
        result = calculate(payload.get("a"), payload.get("b"), payload.get("operation"))
    except ValueError as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(result=result)


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
