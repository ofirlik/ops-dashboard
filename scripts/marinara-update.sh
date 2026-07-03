#!/bin/sh
cd /opt/marinara-engine
docker compose pull
docker compose up -d
echo "--- Image Info ---"
docker inspect ghcr.io/pasta-devs/marinara-engine:latest --format 'Digest: {{index .RepoDigests 0}}'
docker inspect ghcr.io/pasta-devs/marinara-engine:latest --format 'Created: {{.Created}}'
echo "------------------"
