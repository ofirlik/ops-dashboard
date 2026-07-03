#!/bin/bash
set -e
cd /opt/spoolman
docker compose pull
docker compose up -d
echo "Spoolman updated and running."
