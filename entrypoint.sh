#!/bin/sh
set -e

echo "--- V2Ray Starting ---"

V_PORT=${PORT:-8080}
echo "Listening on Port: $V_PORT"

# Replace the port placeholder in the config
sed -i "s/PORT_PLACEHOLDER/$V_PORT/g" /app/config.json

echo "--- V2Ray Binary Start ---"
exec ./v2ray run -config /app/config.json
