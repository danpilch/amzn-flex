#!/bin/bash

PROJECT_NAME=${PWD##*/}
# Local repo, you will need to change this
DOCKER_REPO=danpilch
CURRENT_TAG=$(docker images $PROJECT_NAME --format '{{.Tag}}' | sort -h -r | head -n1)
NEW_TAG=$((CURRENT_TAG+1))

# Build
docker build -t $PROJECT_NAME:$NEW_TAG .
# Tag 
docker tag $PROJECT_NAME:$NEW_TAG $DOCKER_REPO/$PROJECT_NAME:$NEW_TAG
# Push 
docker push $DOCKER_REPO/$PROJECT_NAME:$NEW_TAG
