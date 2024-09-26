# Project console GCP
https://console.cloud.google.com/welcome?project=aluminium-prediction

https://console.cloud.google.com/kubernetes/service/europe-central2/aluminium-cluster


# Kubernetes deployment


https://cloud.google.com/kubernetes-engine/docs/tutorials/http-balancer



# Security

To store i.e. user passwords/api-keys we can use 'external' redis database (outside gke cluster -- memorystorage on gcp)

https://medium.com/google-cloud/use-google-cloud-memorystore-redis-with-the-online-boutique-sample-on-gke-82f7879a900d

## managing redis instances
https://console.cloud.google.com/memorystore/redis/locations/-/instances/new?project=aluminium-prediction
https://console.cloud.google.com/apis/api/redis.googleapis.com/metrics?project=aluminium-prediction       (metryki)

gcloud redis instances create myinstance --size=2 --region=europe-central2 --redis-version=redis_6_x







# Obrazy docker

https://console.cloud.google.com/artifacts/docker/aluminium-prediction/europe-central2/aluminium-prediction?project=aluminium-prediction
