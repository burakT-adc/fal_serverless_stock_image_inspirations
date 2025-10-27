# Usage Guide - Stock Image Inspirations

## Overview

The Stock Image Inspirations service applies fixed, pre-configured inspirations to your stock images using FAL AI models. Each inspiration is optimized for specific use cases like marketplace photography, pose changes, style transfer, and more.

## Installation

```bash
pip install fal-client python-dotenv aiohttp pydantic
```

## Basic Usage

### 1. Initialize Client

```python
from stock_inspirations_fal_client import StockImageInspirationsFalServerless

client = StockImageInspirationsFalServerless(
    endpoint="fal-ai/your-username/stock-image-inspirations"
)
```

### 2. List Available Inspirations

```python
# Get all available inspirations
inspirations = client.list_inspirations()
print(inspirations)
# ['variations', 'change_pose', 'fuse_images', 'marketplace_pure', ...]

# Get info about a specific inspiration
info = client.get_inspiration_info("variations")
print(info)
# {
#   'name': 'Variations',
#   'description': 'Generate multiple variations...',
#   'category': 'variations',
#   'min_input_images': 1,
#   'max_input_images': 5,
#   ...
# }
```

### 3. Apply Inspiration

```python
result = await client.apply_inspiration(
    inspiration_type="variations",
    image_urls=["https://example.com/image.jpg"]
)

if result["success"]:
    for img in result["images"]:
        print(f"Generated: {img['url']}")
```

## Available Inspirations

### 1. Variations
Generate multiple variations with different styles and compositions.

```python
result = await client.apply_inspiration(
    inspiration_type="variations",
    image_urls=["https://example.com/photo.jpg"],
    custom_params={"num_variations": 4}
)
```

**Input**: 1-5 images  
**Output**: ~4 images  
**Custom params**: `num_variations` (number of variations to generate)

---

### 2. Change Pose
Change the pose of subjects while maintaining their identity.

```python
result = await client.apply_inspiration(
    inspiration_type="change_pose",
    image_urls=["https://example.com/person.jpg"],
    custom_params={"pose_option": "professional portrait pose"}
)
```

**Input**: 1 image  
**Output**: ~3 images  
**Custom params**:
- `pose_option`: One of:
  - "confident standing pose"
  - "seated working position"
  - "dynamic action pose"
  - "relaxed casual stance"
  - "professional portrait pose"

---

### 3. Fuse Images
Combine multiple images into a cohesive composition.

```python
result = await client.apply_inspiration(
    inspiration_type="fuse_images",
    image_urls=[
        "https://example.com/image1.jpg",
        "https://example.com/image2.jpg"
    ],
    custom_params={"fusion_style": "seamless integration with unified lighting"}
)
```

**Input**: 2-5 images  
**Output**: ~2 images  
**Custom params**:
- `fusion_style`: One of:
  - "natural blend maintaining all subjects"
  - "artistic collage style"
  - "professional montage"
  - "seamless integration with unified lighting"
  - "creative overlay composition"

---

### 4. Marketplace Pure
Transform into clean marketplace product photography (white background).

```python
result = await client.apply_inspiration(
    inspiration_type="marketplace_pure",
    image_urls=["https://example.com/product.jpg"]
)
```

**Input**: 1 image  
**Output**: ~3 images  
**No custom params** (uses fixed template)

---

### 5. Marketplace Lifestyle
Transform into lifestyle marketplace photography with context.

```python
result = await client.apply_inspiration(
    inspiration_type="marketplace_lifestyle",
    image_urls=["https://example.com/product.jpg"],
    custom_params={"lifestyle_context": "modern home interior setting"}
)
```

**Input**: 1 image  
**Output**: ~3 images  
**Custom params**:
- `lifestyle_context`: One of:
  - "modern home interior setting"
  - "outdoor natural environment"
  - "contemporary office space"
  - "stylish cafe or restaurant"
  - "minimalist lifestyle scene"

---

### 6. Style Transfer
Apply different artistic or photographic styles.

```python
result = await client.apply_inspiration(
    inspiration_type="style_transfer",
    image_urls=["https://example.com/photo.jpg"],
    custom_params={"style_type": "cinematic film photography"}
)
```

**Input**: 1 image  
**Output**: ~4 images  
**Custom params**:
- `style_type`: One of:
  - "cinematic film photography"
  - "high-key bright and airy"
  - "moody and dramatic"
  - "vintage analog film"
  - "modern minimalist"
  - "warm golden hour"
  - "cool professional corporate"

---

### 7. Background Change
Replace or modify background while keeping subject.

```python
result = await client.apply_inspiration(
    inspiration_type="background_change",
    image_urls=["https://example.com/photo.jpg"],
    custom_params={"background_type": "modern office interior"}
)
```

**Input**: 1 image  
**Output**: ~3 images  
**Custom params**:
- `background_type`: One of:
  - "clean white studio background"
  - "modern office interior"
  - "natural outdoor setting"
  - "urban city environment"
  - "abstract gradient backdrop"
  - "luxurious interior space"

---

### 8. Upscale & Enhance
Upscale resolution and enhance image quality.

```python
result = await client.apply_inspiration(
    inspiration_type="upscale_enhance",
    image_urls=["https://example.com/photo.jpg"]
)
```

**Input**: 1 image  
**Output**: 1 image  
**No custom params**

---

### 9. Seasonal Variants
Create seasonal variations.

```python
result = await client.apply_inspiration(
    inspiration_type="seasonal_variants",
    image_urls=["https://example.com/photo.jpg"],
    custom_params={"season": "winter"}
)
```

**Input**: 1 image  
**Output**: ~4 images  
**Custom params**:
- `season`: One of: "spring", "summer", "autumn", "winter"

---

### 10. Time of Day
Generate variations with different times of day lighting.

```python
result = await client.apply_inspiration(
    inspiration_type="time_of_day",
    image_urls=["https://example.com/photo.jpg"],
    custom_params={"time_of_day": "golden_hour"}
)
```

**Input**: 1 image  
**Output**: ~4 images  
**Custom params**:
- `time_of_day`: One of:
  - "golden_hour" - warm golden sunlight
  - "blue_hour" - cool blue twilight
  - "midday" - bright clear daylight
  - "overcast" - soft diffused lighting

---

## Response Structure

```python
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

## Error Handling

```python
try:
    result = await client.apply_inspiration(
        inspiration_type="variations",
        image_urls=["https://example.com/image.jpg"]
    )
    
    if result["success"]:
        print(f"Generated {result['output_image_count']} images")
        for img in result["images"]:
            print(img["url"])
    else:
        print(f"Failed: {result['warnings']}")
        
except ValueError as e:
    print(f"Invalid parameters: {e}")
except RuntimeError as e:
    print(f"FAL error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Retry Logic

The client includes built-in retry logic:

```python
result = await client.apply_inspiration_with_retry(
    inspiration_type="variations",
    image_urls=["https://example.com/image.jpg"],
    max_retries=3,
    timeout=60
)
```

## Direct FAL Client Usage

You can also call the endpoint directly:

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/your-username/stock-image-inspirations",
    arguments={
        "inspiration_type": "variations",
        "image_urls": ["https://example.com/image.jpg"],
        "output_format": "png"
    },
    with_logs=True
)
```

## Batch Processing

Process multiple inspirations on the same image:

```python
inspirations = ["variations", "marketplace_pure", "style_transfer"]

for insp_type in inspirations:
    result = await client.apply_inspiration(
        inspiration_type=insp_type,
        image_urls=["https://example.com/image.jpg"]
    )
    
    if result["success"]:
        print(f"{insp_type}: {result['output_image_count']} images generated")
    
    await asyncio.sleep(1)  # Rate limiting
```

## Environment Variables

Create a `.env` file:

```bash
FAL_SERVERLESS_INSPIRATIONS_ENDPOINT=fal-ai/your-username/stock-image-inspirations
FAL_API_KEY=your-fal-key
```

Load in your code:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Best Practices

1. **Validate before calling**: Use `client.get_inspiration_info()` to check requirements
2. **Handle errors**: Always check `result["success"]`
3. **Use retry logic**: For production, use `apply_inspiration_with_retry()`
4. **Rate limiting**: Add delays between batch requests
5. **Monitor costs**: Each output image costs ~$0.039
6. **Upload images**: For large images, upload to FAL storage first
7. **Cache results**: Store generated images if reused

## Performance Tips

- Typical response time: 3-5 seconds
- Concurrent requests supported (up to 5)
- No GPU needed for the serverless function (CPU-based)
- FAL model (Nano Banana) uses GPU
- Scales automatically with demand

## Troubleshooting

### "Unknown inspiration type"
Check available types: `client.list_inspirations()`

### "Requires X-Y input images"
Check inspiration requirements: `client.get_inspiration_info(type)`

### "Endpoint not found"
Check your endpoint URL:
```bash
fal apps list
```

### Slow responses
- Increase machine size in `stock_inspirations_app.py`
- Use FAL storage for images
- Enable keep_alive

## Support

- GitHub Issues: [Your repo]
- FAL Discord: https://discord.gg/fal
- Documentation: https://docs.fal.ai
- Nano Banana: https://fal.ai/models/fal-ai/nano-banana/edit
