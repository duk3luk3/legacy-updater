docker-compose build legacy-updater
docker-compose stop legacy-updater
echo "y" | docker-compose rm legacy-updater
docker-compose up -d legacy-updater
