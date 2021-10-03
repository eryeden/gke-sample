#!/bin/bash

#Set CLUSTER_NAM and NODE_POOL
CLUSTER_NAME="gke-test-cluster"
ZONE="us-central1-c"

# Create cluster and nodes
gcloud container clusters create $CLUSTER_NAME --machine-type=e2-small --num-nodes 1 --disk-size 10 --zone $ZONE
# Fetch the credential
gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE