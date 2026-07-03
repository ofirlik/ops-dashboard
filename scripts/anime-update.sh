#!/bin/sh
export HOME=/root
git config --global --add safe.directory /opt/anime-downloader
cd /opt/anime-downloader
git pull origin master 2>/dev/null || true
echo "--- Branch Info ---"
echo "Branch : $(git rev-parse --abbrev-ref HEAD)"
echo "Commit : $(git rev-parse --short HEAD)"
echo "Message: $(git log -1 --format='%s')"
echo "Author : $(git log -1 --format='%an')"
echo "Date   : $(git log -1 --format='%ci')"
echo "-------------------"
docker compose build --no-cache
docker compose up -d
