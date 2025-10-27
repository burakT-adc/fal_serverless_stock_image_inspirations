#!/bin/bash
# Complete setup and deployment script for Stock Image Inspirations

echo "🎨 Stock Image Inspirations - Setup & Deploy Script"
echo "="*60

# Step 1: Check Python
echo ""
echo "1️⃣  Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Step 2: Create virtual environment
echo ""
echo "2️⃣  Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Step 3: Activate virtual environment
echo ""
echo "3️⃣  Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Step 4: Install requirements
echo ""
echo "4️⃣  Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Requirements installed"

# Step 5: Check environment variables
echo ""
echo "5️⃣  Checking environment variables..."
if [ -f ".env" ]; then
    source .env
    echo "✅ Loading .env file"
else
    echo "⚠️  No .env file found. Copy env.example to .env and fill in your keys:"
    echo "   cp env.example .env"
    echo "   Then edit .env with your API keys"
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: OPENAI_API_KEY not set"
else
    echo "✅ OPENAI_API_KEY is set"
fi

# Step 6: Make deploy script executable
echo ""
echo "6️⃣  Making deploy script executable..."
chmod +x deploy.sh
echo "✅ deploy.sh is now executable"

# Step 7: Deploy to FAL
echo ""
echo "7️⃣  Ready to deploy!"
echo ""
read -p "Do you want to deploy to FAL.ai now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./deploy.sh
else
    echo "Skipping deployment. You can deploy later with: ./deploy.sh"
fi

echo ""
echo "="*60
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. If you haven't already, set your API keys in .env file"
echo "  2. Deploy with: ./deploy.sh"
echo "  3. Test with: python test_local.py"
echo "="*60

