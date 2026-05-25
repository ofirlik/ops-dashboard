#!/bin/sh
cd /opt/combind-chat
git pull origin main
docker compose build --no-cache
docker compose up -d
