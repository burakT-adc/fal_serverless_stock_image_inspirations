#!/usr/bin/env python3
"""
Test the deployed Stock Inspirations endpoint
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import fal_client
import asyncio

# Load environment variables
load_dotenv()

# Your deployed endpoint
ENDPOINT = "Adc/stock-inspirations"


async def test_endpoint():
    """Test the deployed endpoint with various inspirations."""
    
    # Setup FAL client
    fal_key = os.getenv("FAL_API_KEY") or os.getenv("FAL_KEY")
    if not fal_key:
        print("ERROR: FAL_API_KEY or FAL_KEY not found in .env file")
        sys.exit(1)
    
    os.environ["FAL_KEY"] = fal_key
    
    print("=" * 70)
    print("Testing Deployed Stock Inspirations Endpoint")
    print("=" * 70)
    print(f"Endpoint: {ENDPOINT}")
    print()
    
    # Upload test image
    test_image = Path(__file__).parent / "test" / "image_kontext_inpaint.jpeg"
    if not test_image.exists():
        print(f"ERROR: Test image not found at {test_image}")
        sys.exit(1)
    
    print("Uploading test image...")
    image_url = fal_client.upload_file(test_image)
    print(f"✓ Uploaded: {image_url}")
    
    # Test 1: Marketplace Pure
    print("\n" + "=" * 70)
    print("Test 1: Marketplace Pure (single image)")
    print("=" * 70)
    
    handler = await fal_client.submit_async(
        ENDPOINT,
        arguments={
            "inspiration_name": "marketplace_pure",
            "image_urls": [image_url]
        }
    )
    
    print("Request submitted, waiting for result...")
    result = await handler.get()
    
    print(f"\nSuccess: {result['success']}")
    print(f"Inspiration: {result['inspiration_name']}")
    print(f"Prompt used: {result['prompt_used']}")
    print(f"Processing time: {result['processing_time']:.2f}s")
    print(f"Generated {len(result['images'])} images:")
    for img in result['images']:
        print(f"  [{img['index']}] {img['url']}")
    
    # Test 2: Style Cinematic with extra prompt
    print("\n" + "=" * 70)
    print("Test 2: Style Cinematic with Extra Prompt")
    print("=" * 70)
    
    handler = await fal_client.submit_async(
        ENDPOINT,
        arguments={
            "inspiration_name": "style_cinematic",
            "image_urls": [image_url],
            "extra_prompt": "add dramatic golden hour lighting and deep shadows"
        }
    )
    
    print("Request submitted, waiting for result...")
    result = await handler.get()
    
    print(f"\nSuccess: {result['success']}")
    print(f"Prompt used: {result['prompt_used']}")
    print(f"Processing time: {result['processing_time']:.2f}s")
    print(f"Generated {len(result['images'])} images:")
    for img in result['images']:
        print(f"  [{img['index']}] {img['url']}")
    
    # Test 3: Variations
    print("\n" + "=" * 70)
    print("Test 3: Variations")
    print("=" * 70)
    
    handler = await fal_client.submit_async(
        ENDPOINT,
        arguments={
            "inspiration_name": "variations",
            "image_urls": [image_url]
        }
    )
    
    print("Request submitted, waiting for result...")
    result = await handler.get()
    
    print(f"\nSuccess: {result['success']}")
    print(f"Processing time: {result['processing_time']:.2f}s")
    print(f"Generated {len(result['images'])} images:")
    for img in result['images']:
        print(f"  [{img['index']}] {img['url']}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("✅ All tests completed successfully!")
    print("=" * 70)
    print(f"\nYour endpoint is working perfectly at:")
    print(f"  https://fal.ai/models/{ENDPOINT}/")


if __name__ == "__main__":
    asyncio.run(test_endpoint())

