#!/usr/bin/env python3
"""
Example usage of Stock Image Inspirations endpoint.
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import fal_client

# Load environment
load_dotenv()

# Your deployed endpoint
ENDPOINT = "Adc/stock-inspirations"


async def setup_fal():
    """Setup FAL client."""
    fal_key = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
    if not fal_key:
        raise ValueError("FAL_KEY not found in .env file")
    os.environ["FAL_KEY"] = fal_key


async def example_variations():
    """Example: Generate variations of an image."""
    print("\n" + "="*60)
    print("Example 1: Variations")
    print("="*60)
    
    # Upload test image
    test_image = Path(__file__).parent / "test" / "image_kontext_inpaint.jpeg"
    image_url = fal_client.upload_file(test_image)
    
    handler = await fal_client.submit_async(
        ENDPOINT,
        arguments={
            "inspiration_name": "variations",
            "image_urls": [image_url]
        }
    )
    
    result = await handler.get()
    
    print(f"Success: {result['success']}")
    print(f"Processing time: {result['processing_time']:.2f}s")
    print(f"Generated {len(result['images'])} images:")
    for img in result['images']:
        print(f"  [{img['index']}] {img['url']}")


async def example_marketplace_with_aspect_ratio():
    """Example: Marketplace with custom aspect ratio."""
    print("\n" + "="*60)
    print("Example 2: Marketplace Pure (1:1 aspect ratio)")
    print("="*60)
    
    test_image = Path(__file__).parent / "test" / "image_kontext_inpaint.jpeg"
    image_url = fal_client.upload_file(test_image)
    
    handler = await fal_client.submit_async(
        ENDPOINT,
        arguments={
            "inspiration_name": "marketplace_pure",
            "image_urls": [image_url],
            "aspect_ratio": "1:1"  # Square format
        }
    )
    
    result = await handler.get()
    
    print(f"Success: {result['success']}")
    print(f"Aspect ratio: {result.get('aspect_ratio', 'default')}")
    print(f"Prompt used: {result['prompt_used']}")
    print(f"Generated {len(result['images'])} images:")
    for img in result['images']:
        print(f"  [{img['index']}] {img['url']}")


async def example_with_extra_prompt():
    """Example: Use extra prompt for customization."""
    print("\n" + "="*60)
    print("Example 3: Cinematic Style with Extra Prompt")
    print("="*60)
    
    test_image = Path(__file__).parent / "test" / "image_kontext_inpaint.jpeg"
    image_url = fal_client.upload_file(test_image)
    
    handler = await fal_client.submit_async(
        ENDPOINT,
        arguments={
            "inspiration_name": "style_cinematic",
            "image_urls": [image_url],
            "aspect_ratio": "16:9",
            "extra_prompt": "add dramatic golden hour lighting and deep shadows"
        }
    )
    
    result = await handler.get()
    
    print(f"Success: {result['success']}")
    print(f"Aspect ratio: {result.get('aspect_ratio', 'default')}")
    print(f"Prompt used: {result['prompt_used']}")
    print(f"Generated {len(result['images'])} images:")
    for img in result['images']:
        print(f"  [{img['index']}] {img['url']}")


async def list_available_inspirations():
    """List all available inspirations."""
    print("\n" + "="*60)
    print("Available Inspirations")
    print("="*60)
    
    inspirations = {
        "variations": "Generate 3 variations with different styles",
        "marketplace_pure": "Clean marketplace product photography (white background)",
        "marketplace_lifestyle": "Lifestyle marketplace photography with context",
        "change_pose": "Change subject pose while maintaining identity",
        "style_cinematic": "Apply cinematic film photography style",
        "background_white": "Replace background with clean white studio background",
        "enhance": "Enhance image quality and sharpness",
        "fuse_images": "Combine multiple images into cohesive compositions (2-5 images)"
    }
    
    for name, desc in inspirations.items():
        print(f"  • {name}")
        print(f"    {desc}")
        print()


async def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("Stock Image Inspirations - Usage Examples")
    print("="*60)
    print(f"\nEndpoint: {ENDPOINT}")
    print("="*60)
    
    try:
        await setup_fal()
        
        await list_available_inspirations()
        await example_variations()
        await example_marketplace_with_aspect_ratio()
        await example_with_extra_prompt()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. You have FAL_KEY in .env file")
        print("  2. You're authenticated: fal auth login")
        print("  3. Test image exists in test/ directory")


if __name__ == "__main__":
    asyncio.run(main())
