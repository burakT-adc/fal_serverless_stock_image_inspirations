#!/bin/bash
# FAL.ai Serverless Deployment Script for Stock Image Inspirations

echo "🚀 Deploying Stock Image Inspirations to FAL.ai Serverless..."

# Check if fal CLI is installed
if ! command -v fal &> /dev/null; then
    echo "❌ fal CLI not found. Installing..."
    pip install fal-client[cli]
fi

# Authenticate (if needed)
echo "🔐 Checking authentication..."
fal auth status || fal auth login

# Set secrets (if not already set)
echo "🔑 Setting up secrets..."
if [ ! -z "$OPENAI_API_KEY" ]; then
    fal secrets set OPENAI_API_KEY="$OPENAI_API_KEY"
else
    echo "⚠️  Warning: OPENAI_API_KEY not found in environment"
    echo "    You can set it later with: fal secrets set OPENAI_API_KEY='your-key'"
fi

# Deploy the app
echo "📦 Deploying application..."
fal deploy stock_inspirations_app.py

# Get the endpoint URL
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Your endpoint is available at:"
echo "   fal-ai/<your-username>/stock-image-inspirations"
echo ""
echo "🔧 Usage example:"
echo '   import fal_client'
echo '   result = fal_client.subscribe("fal-ai/<your-username>/stock-image-inspirations", arguments={...})'
echo ""
echo "📊 Monitor your deployment:"
echo "   fal apps list"
echo "   fal logs <app-id>"

