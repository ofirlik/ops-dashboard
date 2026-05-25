#!/bin/sh
git config --global --add safe.directory /opt/combind-chat
cd /opt/combind-chat
git pull origin main
docker compose build --no-cache
docker compose up -d
