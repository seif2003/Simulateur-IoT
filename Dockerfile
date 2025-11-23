FROM python:3.11-slim

# Install mosquitto + supervisor
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    mosquitto \
    mosquitto-clients \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Create mosquitto config
RUN mkdir -p /mosquitto/config
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose ports
EXPOSE 5000 1883 9001

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
