#!/bin/bash
set -e

echo "[+] Starting Jitsi stress container"
exec python3 /app/meet.py "$@"
