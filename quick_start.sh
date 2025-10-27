#!/bin/bash
# Quick start script for Stock Image Inspirations

echo "🎨 Stock Image Inspirations - Quick Start"
echo ""

# Check if already deployed
if [ -z "$FAL_SERVERLESS_INSPIRATIONS_ENDPOINT" ]; then
    echo "📋 This script will help you get started with Stock Image Inspirations on FAL.ai"
    echo ""
    echo "Prerequisites:"
    echo "  ✓ OpenAI API key (for GPT-4 inspiration generation)"
    echo "  ✓ FAL.ai account (https://fal.ai)"
    echo ""
    echo "Quick setup steps:"
    echo "  1. Install FAL CLI: pip install fal-client[cli]"
    echo "  2. Login to FAL: fal auth login"
    echo "  3. Set OpenAI key: export OPENAI_API_KEY='your-key'"
    echo "  4. Deploy: ./deploy.sh"
    echo ""
    echo "Or run the complete setup: ./setup_and_deploy.sh"
else
    echo "✅ Endpoint configured: $FAL_SERVERLESS_INSPIRATIONS_ENDPOINT"
    echo ""
    echo "You're ready to use the service!"
    echo ""
    echo "Example usage:"
    echo ""
    echo "Python:"
    echo "  from stock_inspirations_fal_client import StockImageInspirationsFalServerless"
    echo "  client = StockImageInspirationsFalServerless()"
    echo "  result = await client.generate_inspirations("
    echo "      user_prompt='modern office workspace',"
    echo "      num_inspirations=3"
    echo "  )"
    echo ""
    echo "Or run the test: python test_local.py"
fi

