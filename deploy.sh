#!/bin/bash

# Deploy Stock Image Inspirations to FAL Serverless

echo "========================================"
echo "Deploying Stock Image Inspirations"
echo "========================================"
echo ""

# Check if authenticated
if ! fal auth whoami &> /dev/null; then
    echo "❌ Not authenticated with FAL"
    echo "Please run: fal auth login"
    exit 1
fi

echo "✅ Authenticated with FAL"
echo ""

# Deploy
echo "Deploying stock_inspirations_app.py..."
fal deploy stock_inspirations_app.py

echo ""
echo "========================================"
echo "✅ Deployment complete!"
echo "========================================"
echo ""
echo "Your endpoint: https://fal.ai/models/Adc/stock-inspirations/"
