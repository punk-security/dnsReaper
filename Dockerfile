FROM python:3.11-alpine AS builder
RUN apk add gcc libffi musl-dev libffi-dev

# Create app directory
RUN python -m venv /opt/venv
ENV PATH "/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Prepares a zipped version of the application suitable for running on lambda
FROM amazon/aws-lambda-python:3.11 AS lambda

COPY requirements.txt /app/
COPY lambda-requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt -r lambda-requirements.txt --target .
COPY . /app

RUN yum install zip -y && zip -r9 /packaged_app.zip .

# Main application target
FROM python:3.11-alpine
COPY --from=builder /opt/venv /opt/venv
ENV PATH "/opt/venv/bin:$PATH"

RUN mkdir -p /app/results
WORKDIR /app

COPY . .

# Exports
ENV SM_COMMAND "docker run punksecurity/dnsreaper --" 
ENTRYPOINT [ "python3", "/app/main.py" ]

