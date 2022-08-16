FROM python:3.10-alpine as builder

# Create app directory
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.10-alpine
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN mkdir -p /app/results
WORKDIR /app

COPY . .

# Exports
ENV SM_COMMAND "docker run punksecurity/dnsreaper --" 
ENTRYPOINT [ "python3", "/app/main.py" ]