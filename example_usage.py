"""
Example usage of Stock Image Inspirations FAL Serverless
"""

import asyncio
import os
from stock_inspirations_fal_client import StockImageInspirationsFalServerless


async def basic_example():
    """Basic usage example."""
    print("=" * 80)
    print("BASIC EXAMPLE")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    result = await client.generate_inspirations(
        user_prompt="professional business meeting in modern office",
        num_inspirations=3
    )
    
    if result["success"]:
        print(f"\n✅ Generated {len(result['inspirations'])} inspirations in {result['processing_time']:.2f}s\n")
        
        for i, inspiration in enumerate(result["inspirations"], 1):
            print(f"{'─' * 80}")
            print(f"Inspiration {i}: {inspiration['title']}")
            print(f"{'─' * 80}")
            print(f"\n{inspiration['prompt']}\n")
            
            if inspiration.get("keywords"):
                print(f"Keywords: {', '.join(inspiration['keywords'])}")
            
            if inspiration.get("style_tags"):
                print(f"Style: {', '.join(inspiration['style_tags'])}")
            
            if inspiration.get("negative_prompt"):
                print(f"Negative: {inspiration['negative_prompt']}")
            print()
    else:
        print(f"❌ Failed: {result.get('warnings')}")


async def advanced_example():
    """Advanced usage with all parameters."""
    print("\n" + "=" * 80)
    print("ADVANCED EXAMPLE")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    result = await client.generate_inspirations(
        user_prompt="lifestyle coffee shop scene",
        style_preferences=["cozy", "natural light", "minimalist", "warm tones"],
        num_inspirations=3,
        include_keywords=True,
        include_negative_prompts=True,
        target_use_case="social media"
    )
    
    if result["success"]:
        print(f"\n✅ Generated {len(result['inspirations'])} inspirations in {result['processing_time']:.2f}s\n")
        
        for i, inspiration in enumerate(result["inspirations"], 1):
            print(f"{'─' * 80}")
            print(f"Inspiration {i}: {inspiration['title']}")
            print(f"{'─' * 80}")
            print(f"\nPrompt:\n{inspiration['prompt']}\n")
            print(f"Keywords: {', '.join(inspiration['keywords'])}")
            print(f"Style Tags: {', '.join(inspiration['style_tags'])}")
            print(f"Negative Prompt: {inspiration['negative_prompt']}\n")
    else:
        print(f"❌ Failed: {result.get('warnings')}")


async def multiple_use_cases():
    """Examples of different use cases."""
    print("\n" + "=" * 80)
    print("MULTIPLE USE CASES EXAMPLES")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    use_cases = [
        {
            "name": "Marketing",
            "prompt": "happy customer testimonial",
            "styles": ["authentic", "bright", "engaging"],
            "use_case": "marketing"
        },
        {
            "name": "Editorial",
            "prompt": "urban architecture at golden hour",
            "styles": ["cinematic", "dramatic", "artistic"],
            "use_case": "editorial"
        },
        {
            "name": "E-commerce",
            "prompt": "product flatlay on marble surface",
            "styles": ["clean", "professional", "high-key"],
            "use_case": "e-commerce"
        }
    ]
    
    for case in use_cases:
        print(f"\n{'═' * 80}")
        print(f"USE CASE: {case['name']}")
        print(f"{'═' * 80}")
        
        result = await client.generate_inspirations(
            user_prompt=case["prompt"],
            style_preferences=case["styles"],
            num_inspirations=2,
            target_use_case=case["use_case"]
        )
        
        if result["success"]:
            for i, inspiration in enumerate(result["inspirations"], 1):
                print(f"\n{i}. {inspiration['title']}")
                print(f"   {inspiration['prompt'][:150]}...")
        
        # Small delay between requests
        await asyncio.sleep(1)


async def retry_example():
    """Example with retry logic."""
    print("\n" + "=" * 80)
    print("RETRY EXAMPLE")
    print("=" * 80)
    
    client = StockImageInspirationsFalServerless()
    
    try:
        result = await client.generate_inspirations_with_retry(
            user_prompt="futuristic workspace with AI technology",
            style_preferences=["sci-fi", "modern", "high-tech"],
            num_inspirations=2,
            max_retries=3,
            timeout=30
        )
        
        if result["success"]:
            print(f"\n✅ Success with retry logic!")
            print(f"Generated {len(result['inspirations'])} inspirations")
        else:
            print(f"❌ Failed even with retries: {result.get('warnings')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


async def main():
    """Run all examples."""
    print("\n🎨 Stock Image Inspirations - Usage Examples\n")
    
    # Check environment
    if not os.getenv("FAL_SERVERLESS_INSPIRATIONS_ENDPOINT"):
        print("⚠️  Warning: FAL_SERVERLESS_INSPIRATIONS_ENDPOINT not set")
        print("   Set it with: export FAL_SERVERLESS_INSPIRATIONS_ENDPOINT='fal-ai/your-username/stock-image-inspirations'")
        print()
    
    try:
        # Run examples
        await basic_example()
        await asyncio.sleep(2)
        
        await advanced_example()
        await asyncio.sleep(2)
        
        await multiple_use_cases()
        await asyncio.sleep(2)
        
        await retry_example()
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\nMake sure:")
        print("  1. FAL endpoint is deployed")
        print("  2. FAL_SERVERLESS_INSPIRATIONS_ENDPOINT is set")
        print("  3. OPENAI_API_KEY is set (in FAL secrets)")
        print("  4. FAL_API_KEY is set (if needed)")
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())

