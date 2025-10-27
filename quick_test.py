"""Quick test of deployed endpoint"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Set FAL_KEY from FAL_API_KEY if not set
if not os.getenv("FAL_KEY") and os.getenv("FAL_API_KEY"):
    os.environ["FAL_KEY"] = os.getenv("FAL_API_KEY")

from stock_inspirations_fal_client import StockImageInspirationsFalServerless

async def quick_test():
    print("=" * 80)
    print("QUICK TEST - Deployed Endpoint")
    print("=" * 80)
    
    endpoint = os.getenv("FAL_SERVERLESS_INSPIRATIONS_ENDPOINT")
    fal_key = os.getenv("FAL_KEY")
    
    print(f"Endpoint: {endpoint}")
    print(f"FAL_KEY: {fal_key[:20] if fal_key else 'NOT SET'}...")
    print()
    
    client = StockImageInspirationsFalServerless()
    
    print("Testing 'variations' inspiration...")
    print("-" * 80)
    
    try:
        result = await client.apply_inspiration(
            inspiration_type="variations",
            image_urls=["https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"],
            custom_params={"num_variations": 3}
        )
        
        if result.get("success"):
            print(f"\n✅ SUCCESS!")
            print(f"⏱️  Processing time: {result['processing_time']:.2f}s")
            print(f"🆔 Request ID: {result['request_id']}")
            print(f"📸 Generated {result['output_image_count']} images")
            print(f"💬 Prompt: {result['prompt_used'][:100]}...")
            print(f"\nGenerated images:")
            for img in result["images"]:
                print(f"  {img['index']}: {img['url'][:80]}...")
        else:
            print(f"\n❌ FAILED: {result.get('warnings')}")
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    asyncio.run(quick_test())

