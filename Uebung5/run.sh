#!/usr/bin/env bash
set -e
echo "Loading Playwright Desktop Environment from GitHub Registry..."
docker compose pull
docker compose up