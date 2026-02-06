FROM alpine:latest
EXPOSE 8080
WORKDIR /app

# Install dependencies and fix line endings
RUN apk add --no-cache ca-certificates libc6-compat sed

# Download and install V2Ray
RUN wget https://github.com/v2fly/v2ray-core/releases/latest/download/v2ray-linux-64.zip \
    && unzip v2ray-linux-64.zip \
    && rm v2ray-linux-64.zip \
    && rm config.json

COPY config.json /app
COPY entrypoint.sh /app

# Ensure line endings are LF (to prevent "not found" errors on Windows-to-Linux transfers)
RUN sed -i 's/\r$//' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
