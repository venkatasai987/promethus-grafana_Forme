from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUESTS = Counter(
    "app_requests_total",
    "Total requests received",
    ["application"]
)

PROCESSED = Counter(
    "app_processed_items_total",
    "Total processed items",
    ["application"]
)

APP_NAME = "app1"

@app.route("/")
def home():
    return "App1 is running"

@app.route("/process")
def process():
    REQUESTS.labels(application=APP_NAME).inc()
    PROCESSED.labels(application=APP_NAME).inc()

    return {
        "application": APP_NAME,
        "status": "success",
        "processed": PROCESSED.labels(application=APP_NAME)._value.get()
    }

@app.route("/health")
def health():
    return "OK", 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
