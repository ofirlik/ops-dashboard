#!/bin/bash
set -e
cd /opt/spoolman
docker compose restart
echo "Spoolman restarted."
