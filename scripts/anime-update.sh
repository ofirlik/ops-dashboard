#!/bin/sh
cd /opt/anime-downloader
git pull origin main 2>/dev/null || true
docker compose build --no-cache
docker compose up -d
