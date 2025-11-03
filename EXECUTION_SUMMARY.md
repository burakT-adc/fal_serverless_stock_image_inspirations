# Stock Inspirations - Execution Unit Summary

## 🎯 Overview

Modular execution system that supports both **BATCH** and **PARALLEL** execution modes. Each inspiration can specify its own execution strategy and model.

## 🔧 Execution Modes

### BATCH Mode
**How it works:** Single request with `num_images=3`  
**When to use:** When you need consistent, similar results  
**Processing:** ~9-11 seconds

**Inspirations using BATCH:**
- `free_editing` - Consistent editing
- `creative_color_pop` - Consistent color enhancement
- `marketplace_remove_overlays` - Consistent overlay removal
- `marketplace_pure` - Consistent white background
- `marketplace_lifestyle` - Consistent lifestyle style
- `background_change` - Consistent background replacement
- `fuse_images` - Consistent image fusion

### PARALLEL Mode
**How it works:** 3 separate requests executed simultaneously  
**When to use:** When you need diversity and variation  
**Processing:** ~11-12 seconds (slightly slower but more diverse)

**Inspirations using PARALLEL:**
- `creative_color_material` - Different colors/materials
- `creative_different_angles` - Different camera angles
- `marketplace_close_ups` - Different closeup details
- `fashion_change_pose` - Different poses

## 📊 Performance Comparison

| Mode | Time | Quality | Use Case |
|------|------|---------|----------|
| **BATCH** | ~9s | Consistent | Same style variations |
| **PARALLEL** | ~11s | Diverse | Different angles/poses |

## 🎨 All Inspirations (11 total)

### Creative (4)
- `free_editing` [BATCH] - Free editing
- `creative_color_material` [PARALLEL] - Color/material variations
- `creative_different_angles` [PARALLEL] - Different angles
- `creative_color_pop` [BATCH] - Color enhancement
- `background_change` [BATCH] - Background replacement

### Marketplace (5)
- `marketplace_remove_overlays` [BATCH] - Remove overlays
- `marketplace_pure` [BATCH] - White background
- `marketplace_lifestyle` [BATCH] - Lifestyle setting
- `marketplace_close_ups` [PARALLEL] - Close-up details
- `fuse_images` [BATCH] - Image fusion

### Fashion (1)
- `fashion_change_pose` [PARALLEL] - Pose variations

## 💻 Configuration Structure

Each inspiration includes:

```python
"inspiration_name": {
    "name": "Display Name",
    "category": "Creative|Marketplace|Fashion",
    "description": "What it does",
    "prompt_template": "The actual prompt sent to model",
    "num_images": 3,  # Always 3
    "input_type": "single|multiple",
    "min_images": 1,
    "max_images": 1,
    "execution_mode": "batch|parallel",  # ⭐ Execution strategy
    "model": "fal-ai/nano-banana/edit"    # ⭐ Model endpoint
}
```

## 🚀 Execution Unit API

```python
async def execute_generation(
    model: str,                    # Model endpoint
    prompt: str,                   # Generation prompt
    image_urls: List[str],         # Input images
    aspect_ratio: Optional[str],   # Optional aspect ratio
    execution_mode: str,           # "parallel" or "batch"
    request_id: str               # For logging
) -> List[Dict[str, Any]]:        # Always returns 3 images
```

## 📝 Adding New Models

To add support for a new model (e.g., DALL-E, Midjourney):

1. Add inspiration with model field:
```python
"my_inspiration": {
    ...
    "execution_mode": "batch",
    "model": "fal-ai/dalle-3"  # ⭐ Different model
}
```

2. Execution unit automatically handles it!

No code changes needed - just specify the model endpoint.

## 🔍 Testing

### Test BATCH mode:
```python
result = await fal_client.submit_async(
    "Adc/stock-inspirations",
    arguments={
        "inspiration_name": "marketplace_pure",
        "image_urls": [image_url]
    }
)
# Result will show: execution_mode: "batch"
```

### Test PARALLEL mode:
```python
result = await fal_client.submit_async(
    "Adc/stock-inspirations",
    arguments={
        "inspiration_name": "creative_different_angles",
        "image_urls": [image_url]
    }
)
# Result will show: execution_mode: "parallel"
```

## 📈 Output Format

```python
{
    "success": True,
    "images": [
        {"url": "...", "index": 0},
        {"url": "...", "index": 1},
        {"url": "...", "index": 2}
    ],
    "inspiration_name": "marketplace_pure",
    "prompt_used": "transform into clean...",
    "execution_mode": "batch",  # ⭐ Shows which mode was used
    "model": "fal-ai/nano-banana/edit",  # ⭐ Shows which model
    "aspect_ratio": "1:1",
    "processing_time": 9.45,
    "request_id": "a1b2c3d4"
}
```

## 🎯 Best Practices

1. **Use BATCH for:**
   - Consistent product photography
   - Same-style variations
   - Background replacements
   - Color corrections

2. **Use PARALLEL for:**
   - Different angles/perspectives
   - Pose variations
   - Diverse creative output
   - Close-up details from different areas

3. **Aspect Ratio:**
   - Always optional
   - Works with both modes
   - Common: `1:1`, `16:9`, `4:3`

## 🔗 Live Endpoint

**Production:** https://fal.ai/models/Adc/stock-inspirations/

**Testing Options:**

1. **fal run** (temporary):
   ```bash
   fal run stock_inspirations_app.py
   # Creates temporary URL, stops on Ctrl+C
   ```

2. **fal deploy** (permanent):
   ```bash
   fal deploy stock_inspirations_app.py
   # Creates permanent production URL
   ```

## 🎉 Summary

- ✅ **11 inspirations** across 3 categories
- ✅ **2 execution modes** (batch/parallel)
- ✅ **Modular design** - easy to add new models
- ✅ **Automatic strategy** - each inspiration knows its best mode
- ✅ **~9-12 seconds** per request
- ✅ **Always 3 images** guaranteed
- ✅ **Aspect ratio support** for all inspirations

