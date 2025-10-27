"""
Example usage of Stock Image Inspirations FAL Serverless
"""

import asyncio
import os
from stock_inspirations_fal_client import StockImageInspirationsFalServerless
from inspirations_config import list_inspiration_types, get_inspiration_config


# Example image URLs (replace with your own)
EXAMPLE_IMAGE_SINGLE = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
EXAMPLE_IMAGE_MULTI = [
    "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png",
    "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
]


async def basic_example():
    """Basic usage example - variations."""
    print("=" * 80)
    print("BASIC EXAMPLE - Variations")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    result = await client.apply_inspiration(
        inspiration_type="variations",
        image_urls=[EXAMPLE_IMAGE_SINGLE],
        custom_params={"num_variations": 4}
    )
    
    if result["success"]:
        print(f"\n✅ Success! Generated {result['output_image_count']} images in {result['processing_time']:.2f}s")
        print(f"Inspiration: {result['inspiration_name']}")
        print(f"Prompt used: {result['prompt_used']}")
        print(f"\nGenerated images:")
        for img in result["images"]:
            print(f"  {img['index']}: {img['url']}")
    else:
        print(f"\n❌ Failed: {result.get('warnings')}")


async def marketplace_pure_example():
    """Marketplace pure product photography."""
    print("\n" + "=" * 80)
    print("MARKETPLACE PURE EXAMPLE")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    result = await client.apply_inspiration(
        inspiration_type="marketplace_pure",
        image_urls=[EXAMPLE_IMAGE_SINGLE]
    )
    
    if result["success"]:
        print(f"\n✅ Transformed to marketplace pure style")
        print(f"Generated {result['output_image_count']} variations")
        print(f"Prompt: {result['prompt_used']}")
    else:
        print(f"\n❌ Failed: {result.get('warnings')}")


async def marketplace_lifestyle_example():
    """Marketplace lifestyle photography."""
    print("\n" + "=" * 80)
    print("MARKETPLACE LIFESTYLE EXAMPLE")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    result = await client.apply_inspiration(
        inspiration_type="marketplace_lifestyle",
        image_urls=[EXAMPLE_IMAGE_SINGLE],
        custom_params={"lifestyle_context": "modern home interior setting"}
    )
    
    if result["success"]:
        print(f"\n✅ Transformed to marketplace lifestyle")
        print(f"Context: modern home interior")
        print(f"Generated {result['output_image_count']} images")
    else:
        print(f"\n❌ Failed: {result.get('warnings')}")


async def change_pose_example():
    """Change pose example."""
    print("\n" + "=" * 80)
    print("CHANGE POSE EXAMPLE")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    result = await client.apply_inspiration(
        inspiration_type="change_pose",
        image_urls=[EXAMPLE_IMAGE_SINGLE],
        custom_params={"pose_option": "confident standing pose"}
    )
    
    if result["success"]:
        print(f"\n✅ Pose changed successfully")
        print(f"New pose: confident standing pose")
        print(f"Generated {result['output_image_count']} variations")
    else:
        print(f"\n❌ Failed: {result.get('warnings')}")


async def fuse_images_example():
    """Fuse multiple images example."""
    print("\n" + "=" * 80)
    print("FUSE IMAGES EXAMPLE")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    result = await client.apply_inspiration(
        inspiration_type="fuse_images",
        image_urls=EXAMPLE_IMAGE_MULTI,
        custom_params={"fusion_style": "seamless integration with unified lighting"}
    )
    
    if result["success"]:
        print(f"\n✅ Images fused successfully")
        print(f"Fusion style: seamless integration")
        print(f"Input: {result['input_image_count']} images")
        print(f"Output: {result['output_image_count']} images")
    else:
        print(f"\n❌ Failed: {result.get('warnings')}")


async def style_transfer_example():
    """Style transfer example."""
    print("\n" + "=" * 80)
    print("STYLE TRANSFER EXAMPLE")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    result = await client.apply_inspiration(
        inspiration_type="style_transfer",
        image_urls=[EXAMPLE_IMAGE_SINGLE],
        custom_params={"style_type": "cinematic film photography"}
    )
    
    if result["success"]:
        print(f"\n✅ Style applied successfully")
        print(f"Style: cinematic film photography")
        print(f"Generated {result['output_image_count']} variations")
    else:
        print(f"\n❌ Failed: {result.get('warnings')}")


async def list_all_inspirations():
    """List all available inspirations."""
    print("\n" + "=" * 80)
    print("ALL AVAILABLE INSPIRATIONS")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    inspirations = client.list_inspirations()
    
    print(f"\nTotal: {len(inspirations)} inspirations available\n")
    
    for insp_type in inspirations:
        config = client.get_inspiration_info(insp_type)
        print(f"📸 {config['name']} ({insp_type})")
        print(f"   {config['description']}")
        print(f"   Category: {config['category']}")
        print(f"   Input: {config['min_input_images']}-{config['max_input_images']} images")
        print(f"   Output: ~{config['typical_output_count']} images")
        print(f"   Endpoint: {config['fal_endpoint']}")
        print()


async def batch_inspirations_example():
    """Apply multiple inspirations to the same image."""
    print("\n" + "=" * 80)
    print("BATCH INSPIRATIONS EXAMPLE")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    inspirations_to_apply = [
        "variations",
        "marketplace_pure",
        "style_transfer"
    ]
    
    for insp_type in inspirations_to_apply:
        print(f"\n→ Applying {insp_type}...")
        
        try:
            result = await client.apply_inspiration(
                inspiration_type=insp_type,
                image_urls=[EXAMPLE_IMAGE_SINGLE]
            )
            
            if result["success"]:
                print(f"  ✅ {result['inspiration_name']}: {result['output_image_count']} images")
            else:
                print(f"  ❌ Failed: {result.get('warnings')}")
        
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        # Small delay between requests
        await asyncio.sleep(1)


async def main():
    """Run all examples."""
    print("\n🎨 Stock Image Inspirations - Usage Examples\n")
    
    # Check environment
    if not os.getenv("FAL_SERVERLESS_INSPIRATIONS_ENDPOINT"):
        print("⚠️  Warning: FAL_SERVERLESS_INSPIRATIONS_ENDPOINT not set")
        print("   Set it with: export FAL_SERVERLESS_INSPIRATIONS_ENDPOINT='fal-ai/your-username/stock-image-inspirations'")
        print()
    
    try:
        # List all inspirations first
        await list_all_inspirations()
        await asyncio.sleep(2)
        
        # Run examples
        await basic_example()
        await asyncio.sleep(2)
        
        await marketplace_pure_example()
        await asyncio.sleep(2)
        
        await marketplace_lifestyle_example()
        await asyncio.sleep(2)
        
        await change_pose_example()
        await asyncio.sleep(2)
        
        await fuse_images_example()
        await asyncio.sleep(2)
        
        await style_transfer_example()
        await asyncio.sleep(2)
        
        await batch_inspirations_example()
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure:")
        print("  1. FAL endpoint is deployed")
        print("  2. FAL_SERVERLESS_INSPIRATIONS_ENDPOINT is set")
        print("  3. FAL_API_KEY is set (if needed)")
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
