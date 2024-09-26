

IMAGE_NAME="api-service"
GCP_URL="europe-central2-docker.pkg.dev/aluminium-prediction/aluminium-prediction"
echo "pushing $GCP_URL/$IMAGE_NAME:v0"
docker tag "$IMAGE_NAME:latest" "$GCP_URL/$IMAGE_NAME:v0"
docker push "$GCP_URL/$IMAGE_NAME:v0"
