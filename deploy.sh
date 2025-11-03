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

# Set secrets (if not already set)
echo "🔑 Setting up secrets..."
if [ ! -z "$OPENAI_API_KEY" ]; then
    fal secrets set OPENAI_API_KEY="$OPENAI_API_KEY"
else
    echo "⚠️  Warning: OPENAI_API_KEY not found in environment"
fi

if [ ! -z "$FAL_KEY" ]; then
    fal secrets set FAL_KEY="$FAL_KEY"
else
    echo "⚠️  Warning: FAL_KEY not found in environment"
fi


# Deploy
echo "Deploying stock_inspirations_app.py..."
fal deploy stock_inspirations_app.py

echo ""
echo "========================================"
echo "✅ Deployment complete!"
echo "========================================"
echo ""
echo "Your endpoint: https://fal.ai/models/Adc/stock-inspirations/"
