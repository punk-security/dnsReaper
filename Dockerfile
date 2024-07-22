FROM python:3.11-alpine AS builder
RUN apk add gcc libffi musl-dev libffi-dev

# Create app directory
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-alpine
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN mkdir -p /app/results
WORKDIR /app

COPY . .

# Exports
ENV SM_COMMAND "docker run punksecurity/dnsreaper --" 
ENTRYPOINT [ "python3", "/app/main.py" ]
