"""
Local test script for Stock Image Inspirations.
This tests the logic without deploying to FAL.
"""

import asyncio
import os
from dotenv import load_dotenv
from stock_inspirations_fal_client import StockImageInspirationsFalServerless

# Load environment variables
load_dotenv()


async def test_local():
    """Test the inspirations generation locally."""
    
    # Note: This will still call the deployed FAL endpoint
    # For truly local testing, you would need to extract the logic
    
    client = StockImageInspirationsFalServerless()
    
    # Test parameters
    test_cases = [
        {
            "user_prompt": "professional business meeting in modern office",
            "style_preferences": ["corporate", "professional", "bright"],
            "num_inspirations": 3,
            "target_use_case": "marketing"
        },
        {
            "user_prompt": "lifestyle photography of coffee and laptop",
            "style_preferences": ["minimalist", "cozy", "natural light"],
            "num_inspirations": 2,
            "target_use_case": "social media"
        },
        {
            "user_prompt": "urban street photography at golden hour",
            "style_preferences": ["cinematic", "moody", "dynamic"],
            "num_inspirations": 3,
            "target_use_case": "editorial"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test_case['user_prompt']}")
        print(f"{'='*80}")
        
        try:
            result = await client.generate_inspirations(**test_case)
            
            if result.get("success"):
                print(f"\n✅ Success! Generated {len(result['inspirations'])} inspirations")
                print(f"⏱️  Processing time: {result['processing_time']:.2f}s")
                print(f"🆔 Request ID: {result['request_id']}")
                
                for j, inspiration in enumerate(result["inspirations"], 1):
                    print(f"\n--- Inspiration {j}: {inspiration['title']} ---")
                    print(f"Prompt: {inspiration['prompt'][:100]}...")
                    
                    if inspiration.get("keywords"):
                        print(f"Keywords: {', '.join(inspiration['keywords'][:5])}")
                    
                    if inspiration.get("style_tags"):
                        print(f"Style Tags: {', '.join(inspiration['style_tags'])}")
                    
                    if inspiration.get("negative_prompt"):
                        print(f"Negative Prompt: {inspiration['negative_prompt'][:80]}...")
            else:
                print(f"\n❌ Failed: {result.get('warnings', ['Unknown error'])}")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        
        # Add delay between tests
        if i < len(test_cases):
            print("\nWaiting 2 seconds before next test...")
            await asyncio.sleep(2)
    
    print(f"\n{'='*80}")
    print("All tests completed!")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    print("Stock Image Inspirations - Local Test")
    print("="*80)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment")
        print("   Set it with: export OPENAI_API_KEY='your-key'")
        print("   Or add it to a .env file")
    
    # Check if FAL endpoint is set
    if not os.getenv("FAL_SERVERLESS_INSPIRATIONS_ENDPOINT"):
        print("⚠️  Warning: FAL_SERVERLESS_INSPIRATIONS_ENDPOINT not set")
        print("   Using default endpoint (may not work)")
        print("   Set it with: export FAL_SERVERLESS_INSPIRATIONS_ENDPOINT='fal-ai/your-username/stock-image-inspirations'")
    
    print("\nStarting tests...")
    asyncio.run(test_local())

