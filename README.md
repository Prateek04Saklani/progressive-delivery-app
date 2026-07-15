# Progressive Delivery App

A minimal Flask application designed to demonstrate progressive delivery techniques such as canary releases and blue/green deployments. It exposes version-aware UI, a health endpoint, and Prometheus metrics to support traffic splitting and automated rollback scenarios.

## Features

- **Version-aware UI** — renders a colored page based on the active version (`v1` = green, `v2` = blue)
- **Prometheus metrics** — tracks HTTP request counts by method, status code, and path
- **Configurable failure mode** — simulate an unhealthy release by setting `FAIL_MODE=true`
- **Health endpoint** — useful for liveness/readiness probes in Kubernetes

## Endpoints

| Endpoint   | Description                                      |
|------------|--------------------------------------------------|
| `GET /`    | Returns a color-coded HTML page showing the version |
| `GET /version` | Returns the current version as JSON          |
| `GET /health`  | Returns `200 ok` or `500 unhealthy` depending on `FAIL_MODE` |
| `GET /metrics` | Exposes Prometheus metrics                   |

## Environment Variables

| Variable      | Default | Description                                         |
|---------------|---------|-----------------------------------------------------|
| `APP_VERSION` | `v1`    | Version label shown in the UI and `/version` endpoint |
| `FAIL_MODE`   | `false` | Set to `true` to make `/health` return `500`        |

## Running Locally

**Requirements:** Python 3.12+

```bash
pip install -r requirements.txt
python src/app.py
```

The app listens on `http://localhost:8080`.

## Docker

**Build a normal release:**

```bash
docker build -t progressive-delivery-app:v1 .
```

**Build a bad release (for rollback demos):**

```bash
docker build --build-arg FAIL_MODE=true -t progressive-delivery-app:v1-bad .
```

**Run:**

```bash
docker run -p 8080:8080 -e APP_VERSION=v1 progressive-delivery-app:v1
```

## Project Structure

```
.
├── Dockerfile
├── requirements.txt
└── src/
    └── app.py
```
