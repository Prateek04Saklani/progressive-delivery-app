FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8080

# Bake FAIL_MODE into the image at build time (used for the bad-release demo image)
ARG FAIL_MODE=false
ENV FAIL_MODE=${FAIL_MODE}

CMD ["python", "app.py"]
