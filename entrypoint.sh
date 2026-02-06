#!/bin/sh

# Set the port to listen on (required by Cloud Run)
V_PORT=${PORT:-8080}
echo "V2Ray starting on port: $V_PORT"

# Replace the port placeholder
sed -i "s/PORT_PLACEHOLDER/$V_PORT/g" /app/config.json

# Support for up to 10 users
# If UUIDS is provided as a comma-separated list, use them.
# Otherwise, generate random ones.
IFS=','
i=1
for uuid in $UUIDS; do
    if [ $i -le 10 ]; then
        echo "User $i UUID: $uuid"
        sed -i "s/UUID_$i/$uuid/g" /app/config.json
        i=$((i+1))
    fi
done

# Fill remaining placeholders with random UUIDs
while [ $i -le 10 ]; do
    R_UUID=$(cat /proc/sys/kernel/random/uuid 2>/dev/null || (cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 8 | head -n 1 | tr -d '\n'; echo "-"; cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 4 | head -n 1 | tr -d '\n'; echo "-4"; cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 3 | head -n 1 | tr -d '\n'; echo "-"; cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 4 | head -n 1 | tr -d '\n'; echo "-"; cat /dev/urandom | tr -dc 'a-f0-9' | fold -w 12 | head -n 1))
    echo "User $i (Random) UUID: $R_UUID"
    sed -i "s/UUID_$i/$R_UUID/g" /app/config.json
    i=$((i+1))
done

# Start V2Ray
./v2ray run
