from flask import Flask, request, Response
import os
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

VERSION = os.environ.get("APP_VERSION", "v1")
FAIL_MODE = os.environ.get("FAIL_MODE", "false")

VERSION_COLORS = {"v1": "#2ecc71", "v2": "#3498db"}

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "status", "path"],
)


@app.after_request
def track(resp):
    # Exclude /metrics itself to avoid skewing success-rate calculations
    if request.path != "/metrics":
        REQUEST_COUNT.labels(
            method=request.method,
            status=resp.status_code,
            path=request.path,
        ).inc()
    return resp


@app.route("/")
def index():
    color = VERSION_COLORS.get(VERSION, "#95a5a6")
    return (
        f"<html><body style='margin:0;background:{color};height:100vh;"
        f"display:flex;align-items:center;justify-content:center'>"
        f"<h1 style='color:white;font-family:sans-serif;font-size:3rem'>"
        f"Version: {VERSION}</h1></body></html>"
    )


@app.route("/version")
def version():
    return {"version": VERSION}


@app.route("/health")
def health():
    if FAIL_MODE == "true":
        return "unhealthy", 500
    return "ok", 200


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
