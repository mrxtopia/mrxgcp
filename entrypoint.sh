#!/bin/sh
set -e

echo "--- V2Ray Multi-User Entrypoint ---"

V_PORT=${PORT:-8080}
echo "Listening on Port: $V_PORT"
sed -i "s/PORT_PLACEHOLDER/$V_PORT/g" /app/config.json

# If a single UUID is provided, use it for the first slot
if [ -n "$UUID" ] && [ -z "$UUIDS" ]; then
    UUIDS=$UUID
fi

# Fill up to 10 slots
IFS=','
i=1
for val in $UUIDS; do
    if [ $i -le 10 ]; then
        echo "Slot $i: Using provided UUID ($val)"
        sed -i "s/UUID_$i/$val/g" /app/config.json
        i=$((i+1))
    fi
done

# Fill remaining slots with random UUIDs
while [ $i -le 10 ]; do
    R_UUID=$(cat /proc/sys/kernel/random/uuid 2>/dev/null || cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 32 | head -n 1 | sed 's/\(.\{8\}\)\(.\{4\}\)\(.\{4\}\)\(.\{4\}\)\(.\{12\}\)/\1-\2-\3-\4-\5/')
    echo "Slot $i: Generated random UUID ($R_UUID)"
    sed -i "s/UUID_$i/$R_UUID/g" /app/config.json
    i=$((i+1))
done

echo "--- Starting V2Ray ---"
exec ./v2ray run -config /app/config.json
