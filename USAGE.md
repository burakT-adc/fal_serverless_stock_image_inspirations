# Usage Guide - Stock Image Inspirations

## Overview

The Stock Image Inspirations service generates creative, optimized prompts for AI image generation based on user concepts. It's designed to help create commercially viable stock images with detailed prompts, keywords, and style tags.

## Basic Usage

### 1. Initialize Client

```python
from stock_inspirations_fal_client import StockImageInspirationsFalServerless

client = StockImageInspirationsFalServerless(
    endpoint="fal-ai/your-username/stock-image-inspirations"
)
```

### 2. Generate Inspirations

```python
import asyncio

async def generate():
    result = await client.generate_inspirations(
        user_prompt="professional business meeting in modern office",
        style_preferences=["corporate", "professional", "bright"],
        num_inspirations=3,
        include_keywords=True,
        include_negative_prompts=True,
        target_use_case="marketing"
    )
    
    for inspiration in result["inspirations"]:
        print(f"Title: {inspiration['title']}")
        print(f"Prompt: {inspiration['prompt']}")
        print(f"Keywords: {', '.join(inspiration['keywords'])}")
        print(f"Negative: {inspiration['negative_prompt']}")
        print()

asyncio.run(generate())
```

## Parameters

### Required
- `user_prompt` (str): Base concept or idea for the stock image

### Optional
- `style_preferences` (List[str]): Style preferences like "modern", "minimalist", "vintage"
- `num_inspirations` (int): Number of variations to generate (1-10, default: 3)
- `include_keywords` (bool): Include searchable keywords (default: True)
- `include_negative_prompts` (bool): Include negative prompts (default: True)
- `target_use_case` (str): Target use case like "marketing", "editorial", "social media"

## Response Structure

```python
{
    "inspirations": [
        {
            "title": "Modern Glass-Walled Conference Room Discussion",
            "prompt": "A diverse group of professionals engaged in a collaborative meeting...",
            "negative_prompt": "blurry, low quality, distorted faces, bad lighting...",
            "keywords": ["business", "meeting", "office", "teamwork", "professional"],
            "style_tags": ["corporate", "modern", "professional"]
        },
        # ... more inspirations
    ],
    "original_prompt": "professional business meeting in modern office",
    "processing_time": 2.34,
    "request_id": "uuid-here",
    "success": true,
    "warnings": null
}
```

## Use Cases

### Marketing Content
```python
result = await client.generate_inspirations(
    user_prompt="happy customer using product",
    style_preferences=["lifestyle", "bright", "relatable"],
    target_use_case="marketing",
    num_inspirations=5
)
```

### Editorial Photography
```python
result = await client.generate_inspirations(
    user_prompt="urban street photography at sunset",
    style_preferences=["cinematic", "moody", "storytelling"],
    target_use_case="editorial",
    num_inspirations=3
)
```

### Social Media Content
```python
result = await client.generate_inspirations(
    user_prompt="aesthetic workspace with coffee",
    style_preferences=["minimalist", "cozy", "instagram-worthy"],
    target_use_case="social media",
    num_inspirations=4
)
```

### E-commerce Product Photography
```python
result = await client.generate_inspirations(
    user_prompt="product on white background",
    style_preferences=["clean", "professional", "high-key"],
    target_use_case="e-commerce",
    num_inspirations=3
)
```

## Error Handling

```python
try:
    result = await client.generate_inspirations(
        user_prompt="your concept here",
        num_inspirations=3
    )
    
    if result["success"]:
        print(f"Generated {len(result['inspirations'])} inspirations")
    else:
        print(f"Failed: {result['warnings']}")
        
except Exception as e:
    print(f"Error: {e}")
```

## Retry Logic

The client includes built-in retry logic:

```python
result = await client.generate_inspirations_with_retry(
    user_prompt="your concept here",
    max_retries=3,
    timeout=30
)
```

## Direct FAL Client Usage

You can also call the endpoint directly using fal_client:

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/your-username/stock-image-inspirations",
    arguments={
        "user_prompt": "lifestyle photography concept",
        "style_preferences": ["natural", "authentic"],
        "num_inspirations": 3,
        "include_keywords": True,
        "include_negative_prompts": True
    },
    with_logs=True
)
```

## Environment Variables

Create a `.env` file:

```bash
OPENAI_API_KEY=sk-your-key-here
FAL_API_KEY=your-fal-key
FAL_SERVERLESS_INSPIRATIONS_ENDPOINT=fal-ai/your-username/stock-image-inspirations
```

Load in your code:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Best Practices

1. **Be Specific**: More detailed prompts generate better inspirations
   ```python
   # Good
   user_prompt="professional female entrepreneur working on laptop in bright modern office"
   
   # Less effective
   user_prompt="person working"
   ```

2. **Use Style Preferences**: Guide the aesthetic direction
   ```python
   style_preferences=["cinematic", "warm lighting", "shallow depth of field"]
   ```

3. **Specify Use Case**: Helps tailor the output
   ```python
   target_use_case="social media"  # vs "editorial" or "marketing"
   ```

4. **Generate Multiple Options**: Get variety
   ```python
   num_inspirations=5  # More options to choose from
   ```

5. **Use Keywords**: Enable better searchability in stock libraries
   ```python
   include_keywords=True
   ```

## Performance Tips

- Typical response time: 2-5 seconds
- Concurrent requests supported
- No GPU needed (CPU-based)
- Scales automatically with demand

## Troubleshooting

### "OPENAI_API_KEY not set"
```bash
export OPENAI_API_KEY='sk-your-key'
```

### "Endpoint not found"
Check your endpoint URL:
```bash
fal apps list
```

### Slow responses
- Increase machine size in `stock_inspirations_app.py`
- Increase keep_alive duration

## Support

- GitHub Issues: [Your repo]
- FAL Discord: https://discord.gg/fal
- Documentation: https://docs.fal.ai

