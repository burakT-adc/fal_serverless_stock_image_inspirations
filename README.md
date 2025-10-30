# Stock Image Inspirations

A blackbox FAL serverless service that applies professional photo editing inspirations to images using Google's Nano Banana model.

## Features

- 🎨 **8 Professional Inspirations** - Variations, marketplace, cinematic, and more
- 🖼️ **Always 3 Images** - Consistent output for every request
- 📐 **Aspect Ratio Support** - 1:1, 16:9, 4:3, and more
- ⚡ **Fast & Scalable** - CPU-optimized, scales to zero
- 🔒 **Blackbox Design** - Simple API, complex prompts handled internally

## Live Endpoint

**Playground:** https://fal.ai/models/Adc/stock-inspirations/

**API:**
- Async (Recommended): `https://queue.fal.run/Adc/stock-inspirations/`
- Sync: `https://fal.run/Adc/stock-inspirations/`

## Quick Start

### 1. Install Dependencies

```bash
pip install fal-client python-dotenv
```

### 2. Setup Environment

Create `.env` file:
```bash
FAL_KEY=your-fal-api-key-here
```

### 3. Use the API

```python
import fal_client

# Upload your image
image_url = fal_client.upload_file("your_image.jpg")

# Apply inspiration
handler = await fal_client.submit_async(
    "Adc/stock-inspirations",
    arguments={
        "inspiration_name": "marketplace_pure",
        "image_urls": [image_url],
        "aspect_ratio": "1:1",  # Optional
        "extra_prompt": "vibrant colors"  # Optional
    }
)

result = await handler.get()

# Get your 3 generated images
for img in result['images']:
    print(img['url'])
```

## Available Inspirations

| Inspiration | Description | Images Required |
|------------|-------------|----------------|
| `variations` | Professional variations with different styles | 1 |
| `marketplace_pure` | Clean product photography (white background) | 1 |
| `marketplace_lifestyle` | Lifestyle marketplace photography with context | 1 |
| `change_pose` | Change subject pose while maintaining identity | 1 |
| `style_cinematic` | Apply cinematic film photography style | 1 |
| `background_white` | Replace background with white studio background | 1 |
| `enhance` | Enhance image quality and sharpness | 1 |
| `fuse_images` | Combine multiple images into compositions | 2-5 |

## Aspect Ratios

Supported aspect ratios (optional):
- `21:9` - Ultra-wide
- `16:9` - Widescreen
- `4:3` - Standard
- `3:2` - Classic photo
- `1:1` - Square
- `9:16` - Vertical
- And more...

## Input Parameters

```python
{
    "inspiration_name": str,      # Required: Name of inspiration
    "image_urls": List[str],      # Required: List of image URLs
    "aspect_ratio": str,          # Optional: Output aspect ratio
    "extra_prompt": str           # Optional: Additional instructions
}
```

## Output Format

```python
{
    "success": bool,
    "images": [
        {"url": str, "index": int},  # 3 images
        {"url": str, "index": int},
        {"url": str, "index": int}
    ],
    "inspiration_name": str,
    "prompt_used": str,
    "aspect_ratio": str,
    "processing_time": float,
    "request_id": str,
    "error": str                    # Only if success=False
}
```

## Examples

Run examples:
```bash
python example_usage.py
```

Test deployed endpoint:
```bash
python test_deployed_endpoint.py
```

## Development

### Deploy to FAL

```bash
# Authenticate
fal auth login

# Deploy
bash deploy.sh
# or
fal deploy stock_inspirations_app.py
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run examples
python example_usage.py
```

## Architecture

- **Machine Type:** M (CPU) - Fast deployment, low cost
- **Concurrency:** 0-2 workers, scales to zero
- **Timeout:** 120s per request
- **Engine:** Google Nano Banana Edit model via FAL

## Cost

Typical processing time: 9-11 seconds per request  
Cost: Based on FAL's nano-banana/edit pricing

## License

MIT
