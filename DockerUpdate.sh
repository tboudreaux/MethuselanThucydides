#!/bin/bash
# This script will update the docker image and restart the container
docker stop MethuselanThucydides
docker rm MethuselanThucydides

docker build -t mt:latest .


docker run -p 5516:5000 -d --restart always -e "BEARER_TOKEN=$BEARER_TOKEN" \
	-e "OPENAI_API_KEY=$OPENAI_API_KEY" -e "DATASTORE=\'milvus\'" \
	-e "MT_NEW_USER_SECRET=$MT_NEW_USER_SECRET" -e \
	"MT_DB_NAME=$MT_DB_PROD_NAME" -e "MT_DB_USER=$MT_DB_USER" -e \
	"MT_DB_PASSWORD=$MT_DB_PASSWORD" -e "MT_DB_HOST=$MT_DB_HOST" \
	--name MethuselanThucydides mt:latest
