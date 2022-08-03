#!/bin/bash

cd project-404-team-name-not-found
git fetch && git reset origin/main --hard
docker compose -f docker-compose.prod.yml
docker compose -f docker-compose.prod.yml up -d --build