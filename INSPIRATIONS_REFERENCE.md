# Inspirations Quick Reference

## Overview

This document provides a quick reference for all available inspirations, their parameters, and use cases.

## Inspiration Categories

- **Variations**: Generate different versions of the same image
- **Pose**: Change poses and positions
- **Fusion**: Combine multiple images
- **Marketplace**: E-commerce and product photography
- **Style**: Apply artistic and photographic styles

---

## Complete Inspiration List

### 🎨 Variations

#### 1. variations
Generate multiple variations with different styles and compositions.

- **Input**: 1-5 images
- **Output**: 4 images
- **FAL Endpoint**: `fal-ai/nano-banana/edit`
- **Custom Params**:
  - `num_variations`: Number of variations (default: 4)
  
```python
await client.apply_inspiration(
    inspiration_type="variations",
    image_urls=["https://..."],
    custom_params={"num_variations": 4}
)
```

---

#### 2. background_change
Replace or modify the background while keeping the main subject.

- **Input**: 1 image
- **Output**: 3 images
- **FAL Endpoint**: `fal-ai/nano-banana/edit`
- **Custom Params**:
  - `background_type`: Type of background
    - "clean white studio background"
    - "modern office interior"
    - "natural outdoor setting"
    - "urban city environment"
    - "abstract gradient backdrop"
    - "luxurious interior space"

```python
await client.apply_inspiration(
    inspiration_type="background_change",
    image_urls=["https://..."],
    custom_params={"background_type": "modern office interior"}
)
```

---

#### 3. upscale_enhance
Upscale resolution and enhance image quality.

- **Input**: 1 image
- **Output**: 1 image
- **FAL Endpoint**: `fal-ai/nano-banana/edit`
- **No custom params**

```python
await client.apply_inspiration(
    inspiration_type="upscale_enhance",
    image_urls=["https://..."]
)
```

---

#### 4. seasonal_variants
Create seasonal variations of the image.

- **Input**: 1 image
- **Output**: 4 images
- **FAL Endpoint**: `fal-ai/nano-banana/edit`
- **Custom Params**:
  - `season`: "spring" | "summer" | "autumn" | "winter"

```python
await client.apply_inspiration(
    inspiration_type="seasonal_variants",
    image_urls=["https://..."],
    custom_params={"season": "winter"}
)
```

---

#### 5. time_of_day
Generate variations with different times of day lighting.

- **Input**: 1 image
- **Output**: 4 images
- **FAL Endpoint**: `fal-ai/nano-banana/edit`
- **Custom Params**:
  - `time_of_day`:
    - "golden_hour" - warm golden sunlight
    - "blue_hour" - cool blue twilight
    - "midday" - bright clear daylight
    - "overcast" - soft diffused lighting

```python
await client.apply_inspiration(
    inspiration_type="time_of_day",
    image_urls=["https://..."],
    custom_params={"time_of_day": "golden_hour"}
)
```

---

### 🧍 Pose

#### 6. change_pose
Change the pose or position of subjects while maintaining identity.

- **Input**: 1 image
- **Output**: 3 images
- **FAL Endpoint**: `fal-ai/nano-banana/edit`
- **Custom Params**:
  - `pose_option`:
    - "confident standing pose"
    - "seated working position"
    - "dynamic action pose"
    - "relaxed casual stance"
    - "professional portrait pose"

```python
await client.apply_inspiration(
    inspiration_type="change_pose",
    image_urls=["https://..."],
    custom_params={"pose_option": "professional portrait pose"}
)
```

---

### 🔗 Fusion

#### 7. fuse_images
Combine multiple images into a cohesive composition.

- **Input**: 2-5 images
- **Output**: 2 images
- **FAL Endpoint**: `fal-ai/nano-banana/edit`
- **Custom Params**:
  - `fusion_style`:
    - "natural blend maintaining all subjects"
    - "artistic collage style"
    - "professional montage"
    - "seamless integration with unified lighting"
    - "creative overlay composition"

```python
await client.apply_inspiration(
    inspiration_type="fuse_images",
    image_urls=["https://img1...", "https://img2..."],
    custom_params={"fusion_style": "seamless integration with unified lighting"}
)
```

---

### 🛒 Marketplace

#### 8. marketplace_pure
Transform into clean marketplace product photography (white background).

- **Input**: 1 image
- **Output**: 3 images
- **FAL Endpoint**: `fal-ai/nano-banana/edit`
- **No custom params**

```python
await client.apply_inspiration(
    inspiration_type="marketplace_pure",
    image_urls=["https://..."]
)
```

**Use case**: Product listings, e-commerce, Amazon/eBay

---

#### 9. marketplace_lifestyle
Transform into lifestyle marketplace photography with context.

- **Input**: 1 image
- **Output**: 3 images
- **FAL Endpoint**: `fal-ai/nano-banana/edit`
- **Custom Params**:
  - `lifestyle_context`:
    - "modern home interior setting"
    - "outdoor natural environment"
    - "contemporary office space"
    - "stylish cafe or restaurant"
    - "minimalist lifestyle scene"

```python
await client.apply_inspiration(
    inspiration_type="marketplace_lifestyle",
    image_urls=["https://..."],
    custom_params={"lifestyle_context": "modern home interior setting"}
)
```

**Use case**: Lifestyle product shots, contextual marketing

---

### 🎭 Style

#### 10. style_transfer
Apply different artistic or photographic styles to the image.

- **Input**: 1 image
- **Output**: 4 images
- **FAL Endpoint**: `fal-ai/nano-banana/edit`
- **Custom Params**:
  - `style_type`:
    - "cinematic film photography"
    - "high-key bright and airy"
    - "moody and dramatic"
    - "vintage analog film"
    - "modern minimalist"
    - "warm golden hour"
    - "cool professional corporate"

```python
await client.apply_inspiration(
    inspiration_type="style_transfer",
    image_urls=["https://..."],
    custom_params={"style_type": "cinematic film photography"}
)
```

---

## Use Case Matrix

| Use Case | Recommended Inspirations |
|----------|-------------------------|
| **E-commerce Products** | marketplace_pure, marketplace_lifestyle, background_change |
| **Stock Photography** | variations, seasonal_variants, time_of_day, style_transfer |
| **Marketing Materials** | variations, style_transfer, marketplace_lifestyle |
| **Portrait Photography** | change_pose, style_transfer, upscale_enhance |
| **Social Media** | variations, seasonal_variants, style_transfer |
| **Product Composites** | fuse_images, marketplace_lifestyle |
| **Seasonal Campaigns** | seasonal_variants, time_of_day |
| **Quality Enhancement** | upscale_enhance |

## Cost Estimation

Based on [Nano Banana pricing](https://fal.ai/models/fal-ai/nano-banana/edit): **$0.039 per output image**

| Inspiration | Output Images | Cost per Request |
|-------------|--------------|------------------|
| variations | 4 | $0.156 |
| change_pose | 3 | $0.117 |
| fuse_images | 2 | $0.078 |
| marketplace_pure | 3 | $0.117 |
| marketplace_lifestyle | 3 | $0.117 |
| style_transfer | 4 | $0.156 |
| background_change | 3 | $0.117 |
| upscale_enhance | 1 | $0.039 |
| seasonal_variants | 4 | $0.156 |
| time_of_day | 4 | $0.156 |

## Tips & Best Practices

### Choosing the Right Inspiration

1. **Product Photography?** → Start with `marketplace_pure` or `marketplace_lifestyle`
2. **Need Variety?** → Use `variations` or `seasonal_variants`
3. **Change Composition?** → Try `background_change` or `change_pose`
4. **Artistic Look?** → Apply `style_transfer` with desired style
5. **Combine Images?** → Use `fuse_images` with 2+ images
6. **Low Quality Image?** → Start with `upscale_enhance`

### Workflow Examples

**E-commerce Product Workflow:**
```python
# 1. Clean up background
result1 = await client.apply_inspiration(
    inspiration_type="marketplace_pure",
    image_urls=["product.jpg"]
)

# 2. Add lifestyle context
result2 = await client.apply_inspiration(
    inspiration_type="marketplace_lifestyle",
    image_urls=[result1["images"][0]["url"]],
    custom_params={"lifestyle_context": "modern home interior setting"}
)

# 3. Create variations
result3 = await client.apply_inspiration(
    inspiration_type="variations",
    image_urls=[result2["images"][0]["url"]]
)
```

**Stock Photography Workflow:**
```python
# 1. Enhance quality
result1 = await client.apply_inspiration(
    inspiration_type="upscale_enhance",
    image_urls=["photo.jpg"]
)

# 2. Create seasonal variants
result2 = await client.apply_inspiration(
    inspiration_type="seasonal_variants",
    image_urls=[result1["images"][0]["url"]]
)

# 3. Apply different styles
result3 = await client.apply_inspiration(
    inspiration_type="style_transfer",
    image_urls=[result1["images"][0]["url"]],
    custom_params={"style_type": "cinematic film photography"}
)
```

## Configuration

All inspirations are configured in `inspirations_config.py`. To modify:

1. Edit the configuration
2. Test locally: `python test_local.py`
3. Deploy: `fal deploy stock_inspirations_app.py`

## Adding Custom Inspirations

See `inspirations_config.py` for the structure:

```python
"your_inspiration": {
    "name": "Your Inspiration Name",
    "description": "What it does...",
    "category": InspirationCategory.VARIATIONS,
    "fal_endpoint": "fal-ai/nano-banana/edit",
    "input_type": InputType.SINGLE_IMAGE,
    "default_params": {"num_images": 3},
    "prompt_template": "your prompt here...",
    "min_input_images": 1,
    "max_input_images": 1,
    "typical_output_count": 3
}
```

---

For detailed API documentation, see [USAGE.md](USAGE.md).

