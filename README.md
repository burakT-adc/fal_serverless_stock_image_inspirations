# FAL.ai Serverless - Stock Image Inspirations

Transform your stock images with AI-powered fixed inspirations using FAL.ai Serverless platform.

## 🎯 What is This?

This serverless function applies **fixed inspirations** to stock images using FAL AI models (like [Nano Banana](https://fal.ai/models/fal-ai/nano-banana/edit)). Instead of manually crafting prompts, you select from pre-configured inspirations that automatically transform your images.

### Available Inspirations

| Inspiration | Description | Input | Output |
|------------|-------------|-------|--------|
| **variations** | Generate multiple variations with different styles | 1 image | 4 images |
| **change_pose** | Change subject pose while maintaining identity | 1 image | 3 images |
| **fuse_images** | Combine multiple images into cohesive composition | 2-5 images | 2 images |
| **marketplace_pure** | Clean marketplace product photography (white bg) | 1 image | 3 images |
| **marketplace_lifestyle** | Lifestyle marketplace photography with context | 1 image | 3 images |
| **style_transfer** | Apply different artistic/photographic styles | 1 image | 4 images |
| **background_change** | Replace background while keeping subject | 1 image | 3 images |
| **upscale_enhance** | Upscale resolution and enhance quality | 1 image | 1 image |
| **seasonal_variants** | Create seasonal variations (spring/summer/fall/winter) | 1 image | 4 images |
| **time_of_day** | Different time of day lighting variations | 1 image | 4 images |

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install fal-client[cli]
```

### 2. Deploy to FAL.ai

```bash
# Login to FAL
fal auth login

# Deploy
fal deploy stock_inspirations_app.py

# You'll get an endpoint like:
# fal-ai/your-username/stock-image-inspirations
```

### 3. Use the Service

```python
from stock_inspirations_fal_client import StockImageInspirationsFalServerless

client = StockImageInspirationsFalServerless()

# Apply "variations" inspiration
result = await client.apply_inspiration(
    inspiration_type="variations",
    image_urls=["https://example.com/your-image.jpg"]
)

# Get generated images
for img in result["images"]:
    print(f"Generated: {img['url']}")
```

## 📖 Usage Examples

### Marketplace Pure (Product Photography)

```python
result = await client.apply_inspiration(
    inspiration_type="marketplace_pure",
    image_urls=["https://example.com/product.jpg"]
)
# Transforms to clean white background product shot
```

### Marketplace Lifestyle

```python
result = await client.apply_inspiration(
    inspiration_type="marketplace_lifestyle",
    image_urls=["https://example.com/product.jpg"],
    custom_params={"lifestyle_context": "modern home interior setting"}
)
# Adds lifestyle context to product
```

### Change Pose

```python
result = await client.apply_inspiration(
    inspiration_type="change_pose",
    image_urls=["https://example.com/person.jpg"],
    custom_params={"pose_option": "professional portrait pose"}
)
# Changes person's pose
```

### Fuse Multiple Images

```python
result = await client.apply_inspiration(
    inspiration_type="fuse_images",
    image_urls=[
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ],
    custom_params={"fusion_style": "seamless integration with unified lighting"}
)
# Combines images into one composition
```

### Style Transfer

```python
result = await client.apply_inspiration(
    inspiration_type="style_transfer",
    image_urls=["https://example.com/photo.jpg"],
    custom_params={"style_type": "cinematic film photography"}
)
# Applies cinematic style
```

## 🎨 Customization

Each inspiration supports custom parameters:

```python
# Variations with custom count
result = await client.apply_inspiration(
    inspiration_type="variations",
    image_urls=["https://example.com/image.jpg"],
    custom_params={"num_variations": 6}
)

# Seasonal with specific season
result = await client.apply_inspiration(
    inspiration_type="seasonal_variants",
    image_urls=["https://example.com/image.jpg"],
    custom_params={"season": "winter"}
)

# Time of day with specific time
result = await client.apply_inspiration(
    inspiration_type="time_of_day",
    image_urls=["https://example.com/image.jpg"],
    custom_params={"time_of_day": "golden_hour"}
)
```

## 🏗️ Architecture

```
Your App → FAL Serverless Endpoint → Fixed Inspiration Logic → FAL Model (Nano Banana) → Generated Images
```

### How It Works

1. **You call** the serverless endpoint with inspiration type + images
2. **Endpoint loads** the fixed inspiration configuration
3. **Configuration defines**:
   - Which FAL model to use (e.g., nano-banana/edit)
   - Prompt template
   - Default parameters
   - Input/output requirements
4. **Endpoint calls** the FAL model with optimized parameters
5. **You receive** generated images

## 📦 Installation & Setup

### Option 1: Quick Setup (Recommended)

```bash
cd /Users/burak/Desktop/repos/fal_serverless_stock_image_inspirations
./setup_and_deploy.sh
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Login to FAL
fal auth login

# 4. Deploy
./deploy.sh
```

## 🔧 Configuration

All inspirations are configured in `inspirations_config.py`:

```python
INSPIRATIONS_CONFIG = {
    "variations": {
        "name": "Variations",
        "description": "Generate multiple variations...",
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.OPTIONAL_MULTI,
        "default_params": {
            "num_images": 4,
            "output_format": "png"
        },
        "prompt_template": "create {num_variations} professional variations...",
        "min_input_images": 1,
        "max_input_images": 5
    },
    # ... more inspirations
}
```

### Adding New Inspirations

1. Add config to `inspirations_config.py`
2. Define prompt template
3. Set FAL endpoint
4. Configure parameters
5. Deploy: `fal deploy stock_inspirations_app.py`

## 💰 Pricing

- **FAL Serverless**: ~$0.0001/sec (CPU instance, M size)
- **Nano Banana**: ~$0.039 per output image ([source](https://fal.ai/models/fal-ai/nano-banana/edit))

**Example Cost:**
- 1 request with 4 output images: ~$0.156
- Processing time: ~3 seconds
- Total: ~$0.156 per request

## 📊 Response Format

```json
{
  "images": [
    {"url": "https://...", "index": 0},
    {"url": "https://...", "index": 1}
  ],
  "inspiration_type": "variations",
  "inspiration_name": "Variations",
  "prompt_used": "create 4 professional variations...",
  "fal_endpoint": "fal-ai/nano-banana/edit",
  "input_image_count": 1,
  "output_image_count": 4,
  "processing_time": 3.45,
  "request_id": "uuid-here",
  "success": true,
  "warnings": null
}
```

## 🧪 Testing

```bash
# Test specific inspirations
python test_local.py

# Run examples
python example_usage.py

# Test all inspirations
TEST_MODE=1 python test_local.py
```

## 📚 Documentation

- **README.md** - This file (overview & quick start)
- **USAGE.md** - Detailed API documentation
- **PROJECT_SUMMARY.md** - Complete project structure
- **GITHUB_SETUP.md** - GitHub connection guide
- **NEXT_STEPS.md** - What to do next

## 🔗 FAL Models Used

Currently using:
- [Nano Banana](https://fal.ai/models/fal-ai/nano-banana/edit) - Google's image editing model

Can be extended to support:
- Flux models
- Stable Diffusion variants
- Custom trained models

## 🛠️ Development

```bash
# Activate environment
source venv/bin/activate

# Make changes to inspirations_config.py or stock_inspirations_app.py

# Test locally
python test_local.py

# Deploy changes
fal deploy stock_inspirations_app.py

# Check logs
fal apps list
fal logs <app-id>
```

## 🎯 Use Cases

- **E-commerce**: Product photography variations
- **Marketing**: Multiple ad creative variations
- **Stock Photography**: Expand portfolio with variations
- **Content Creation**: Quick style exploration
- **Product Design**: Visualize in different contexts

## ⚠️ Requirements

- Python 3.8+
- FAL.ai account ([sign up](https://fal.ai))
- Input images must be accessible URLs

## 🤝 Contributing

Contributions welcome! To add new inspirations:

1. Fork the repository
2. Add inspiration config to `inspirations_config.py`
3. Test with `test_local.py`
4. Submit pull request

## 📄 License

MIT License - See LICENSE file

## 🔗 Links

- [FAL.ai Platform](https://fal.ai)
- [FAL Serverless Docs](https://docs.fal.ai/serverless)
- [Nano Banana Model](https://fal.ai/models/fal-ai/nano-banana/edit)

## 💡 Tips

1. **Upload images first**: Use FAL storage for better performance
2. **Batch processing**: Process multiple images in sequence
3. **Monitor costs**: Check FAL dashboard regularly
4. **Cache results**: Store generated images if used frequently
5. **Retry logic**: Use `apply_inspiration_with_retry()` for production

## 🚀 Next Steps

1. **Deploy**: `./deploy.sh`
2. **Test**: `python test_local.py`
3. **Integrate**: Import client in your app
4. **Monitor**: Check FAL dashboard for usage

---

**Ready to transform your stock images?** Start with `./setup_and_deploy.sh` 🎨
