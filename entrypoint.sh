#!/bin/sh

# Use the provided UUID environment variable or generate a random one
USER_UUID=${UUID:-$(cat /proc/sys/kernel/random/uuid)}

echo "Starting V2Ray with UUID: $USER_UUID"

# Replace the placeholder in config.json
sed -i "s/UUID_PLACEHOLDER/$USER_UUID/g" /app/config.json

# Execute V2Ray
./v2ray run
