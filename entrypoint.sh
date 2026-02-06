#!/bin/sh
set -e

echo "--- V2Ray Entrypoint Starting ---"

# Set the port
V_PORT=${PORT:-8080}
echo "Detected Port: $V_PORT"

# Handle UUID
if [ -z "$UUID" ]; then
    # Generate random UUID if not provided
    V_UUID=$(cat /proc/sys/kernel/random/uuid 2>/dev/null || cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 32 | head -n 1 | sed 's/\(.\{8\}\)\(.\{4\}\)\(.\{4\}\)\(.\{4\}\)\(.\{12\}\)/\1-\2-\3-\4-\5/')
    echo "Using generated random UUID"
else
    V_UUID=$UUID
    echo "Using provided UUID"
fi

# Replace placeholders
sed -i "s/PORT_PLACEHOLDER/$V_PORT/g" /app/config.json
sed -i "s/UUID_PLACEHOLDER/$V_UUID/g" /app/config.json

echo "--- Config Verification ---"
# Check if config is valid JSON (using grep as a simple check)
grep -q "\"port\": $V_PORT" /app/config.json && echo "Port replacement successful"
grep -q "$V_UUID" /app/config.json && echo "UUID replacement successful"

echo "--- Starting V2Ray ---"
# Use exec to let V2Ray be PID 1
exec ./v2ray run -config /app/config.json
