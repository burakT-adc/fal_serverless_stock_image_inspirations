"""
Local test script for Stock Image Inspirations.
Tests fixed inspirations with FAL endpoints.
"""

import asyncio
import os
from dotenv import load_dotenv
from stock_inspirations_fal_client import StockImageInspirationsFalServerless
from inspirations_config import list_inspiration_types, get_inspiration_config

# Load environment variables
load_dotenv()

# Example test images (replace with your own)
TEST_IMAGE_SINGLE = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
TEST_IMAGE_MULTI = [
    "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png",
    "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
]


async def test_single_inspiration(client, inspiration_type: str):
    """Test a single inspiration type."""
    print(f"\n{'='*80}")
    print(f"TEST: {inspiration_type}")
    print(f"{'='*80}")
    
    config = get_inspiration_config(inspiration_type)
    print(f"Name: {config['name']}")
    print(f"Description: {config['description']}")
    print(f"Category: {config['category']}")
    print(f"Endpoint: {config['fal_endpoint']}")
    print(f"Input: {config['min_input_images']}-{config['max_input_images']} images")
    
    # Determine which images to use
    if config['min_input_images'] > 1:
        image_urls = TEST_IMAGE_MULTI[:config['max_input_images']]
    else:
        image_urls = [TEST_IMAGE_SINGLE]
    
    print(f"Testing with {len(image_urls)} image(s)...")
    
    try:
        result = await client.apply_inspiration(
            inspiration_type=inspiration_type,
            image_urls=image_urls
        )
        
        if result.get("success"):
            print(f"\n✅ Success!")
            print(f"⏱️  Processing time: {result['processing_time']:.2f}s")
            print(f"🆔 Request ID: {result['request_id']}")
            print(f"📸 Generated {result['output_image_count']} images")
            print(f"💬 Prompt used: {result['prompt_used'][:100]}...")
            
            if result.get("images"):
                print(f"\n Generated image URLs:")
                for img in result["images"][:3]:  # Show first 3
                    print(f"   {img['index']}: {img['url'][:80]}...")
        else:
            print(f"\n❌ Failed: {result.get('warnings', ['Unknown error'])}")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


async def test_all_inspirations():
    """Test all available inspirations."""
    print("=" * 80)
    print("TESTING ALL INSPIRATIONS")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    # List all inspirations
    inspirations = list_inspiration_types()
    print(f"\nFound {len(inspirations)} inspirations to test\n")
    
    # Test each one
    for i, insp_type in enumerate(inspirations, 1):
        print(f"\n[{i}/{len(inspirations)}]", end=" ")
        await test_single_inspiration(client, insp_type)
        
        # Add delay between tests
        if i < len(inspirations):
            print("\nWaiting 2 seconds before next test...")
            await asyncio.sleep(2)


async def test_specific_inspirations():
    """Test specific important inspirations."""
    print("=" * 80)
    print("TESTING SPECIFIC INSPIRATIONS")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    test_cases = [
        {
            "inspiration_type": "variations",
            "image_urls": [TEST_IMAGE_SINGLE],
            "custom_params": {"num_variations": 3}
        },
        {
            "inspiration_type": "marketplace_pure",
            "image_urls": [TEST_IMAGE_SINGLE],
            "custom_params": None
        },
        {
            "inspiration_type": "marketplace_lifestyle",
            "image_urls": [TEST_IMAGE_SINGLE],
            "custom_params": {"lifestyle_context": "modern home interior setting"}
        },
        {
            "inspiration_type": "change_pose",
            "image_urls": [TEST_IMAGE_SINGLE],
            "custom_params": {"pose_option": "professional portrait pose"}
        },
        {
            "inspiration_type": "fuse_images",
            "image_urls": TEST_IMAGE_MULTI,
            "custom_params": {"fusion_style": "natural blend maintaining all subjects"}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test_case['inspiration_type']}")
        print(f"{'='*80}")
        
        try:
            result = await client.apply_inspiration(**test_case)
            
            if result.get("success"):
                print(f"\n✅ Success!")
                print(f"⏱️  Processing time: {result['processing_time']:.2f}s")
                print(f"📸 Input: {result['input_image_count']} → Output: {result['output_image_count']} images")
                print(f"💬 Prompt: {result['prompt_used'][:150]}...")
            else:
                print(f"\n❌ Failed: {result.get('warnings')}")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        
        # Add delay between tests
        if i < len(test_cases):
            print("\nWaiting 2 seconds before next test...")
            await asyncio.sleep(2)


async def test_with_retry():
    """Test with retry logic."""
    print("\n" + "=" * 80)
    print("TESTING WITH RETRY LOGIC")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    try:
        result = await client.apply_inspiration_with_retry(
            inspiration_type="variations",
            image_urls=[TEST_IMAGE_SINGLE],
            max_retries=3,
            timeout=60
        )
        
        if result.get("success"):
            print(f"\n✅ Success with retry logic!")
            print(f"Generated {result['output_image_count']} images")
        else:
            print(f"\n❌ Failed even with retries: {result.get('warnings')}")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")


async def main():
    """Run tests."""
    print("\n🎨 Stock Image Inspirations - Test Suite\n")
    print("="*80)
    
    # Check environment
    if not os.getenv("FAL_SERVERLESS_INSPIRATIONS_ENDPOINT"):
        print("⚠️  Warning: FAL_SERVERLESS_INSPIRATIONS_ENDPOINT not set")
        print("   Using default endpoint (may not work until deployed)")
        print("   Set it with: export FAL_SERVERLESS_INSPIRATIONS_ENDPOINT='fal-ai/your-username/stock-image-inspirations'")
    else:
        endpoint = os.getenv("FAL_SERVERLESS_INSPIRATIONS_ENDPOINT")
        print(f"✅ Endpoint configured: {endpoint}")
    
    print("\nSelect test mode:")
    print("  1. Test all inspirations (comprehensive)")
    print("  2. Test specific inspirations (quick)")
    print("  3. Test with retry logic")
    print()
    
    # For automated testing, default to specific
    test_mode = os.getenv("TEST_MODE", "2")
    
    try:
        if test_mode == "1":
            await test_all_inspirations()
        elif test_mode == "3":
            await test_with_retry()
        else:
            await test_specific_inspirations()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test suite error: {e}")
        print("\nMake sure:")
        print("  1. FAL endpoint is deployed: ./deploy.sh")
        print("  2. FAL_SERVERLESS_INSPIRATIONS_ENDPOINT is set")
        print("  3. FAL_API_KEY is set (if needed)")
    
    print(f"\n{'='*80}")
    print("Tests completed!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    print("Stock Image Inspirations - Test Script")
    print("=" * 80)
    asyncio.run(main())
