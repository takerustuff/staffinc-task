#!/usr/bin/env bash
# Deploy React frontend to S3 static hosting
# Usage: S3_BUCKET=my-bucket VITE_API_URL=http://<ec2-ip>:8000 ./deploy-frontend.sh
set -e

BUCKET=${S3_BUCKET:?Set S3_BUCKET env var}
API_URL=${VITE_API_URL:?Set VITE_API_URL env var}

cd "$(dirname "$0")/../frontend"

echo "→ Installing dependencies..."
npm ci

echo "→ Building with API URL: $API_URL"
VITE_API_URL="$API_URL" npm run build

echo "→ Syncing to s3://$BUCKET"
aws s3 sync dist/ "s3://$BUCKET" --delete

echo "→ Setting bucket for static website hosting..."
aws s3 website "s3://$BUCKET" --index-document index.html --error-document index.html

echo "✓ Frontend deployed. Visit: http://$BUCKET.s3-website-$(aws configure get region).amazonaws.com"
