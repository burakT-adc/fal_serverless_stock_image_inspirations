"""
Direct test of Vertex AI Gemini 2.5 Flash Image
Tests inspirations without FAL endpoint
"""
import asyncio
import os
from PIL import Image
from io import BytesIO
import requests
from vertex_ai_integration import VertexAIImageEditor
from inspirations_config import get_inspiration_config

# Test image URL
TEST_IMAGE_URL = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"

async def test_vertex_variations():
    """Test variations inspiration with Vertex AI"""
    print("=" * 80)
    print("VERTEX AI GEMINI 2.5 FLASH IMAGE - TEST")
    print("=" * 80)
    print()
    
    # Download test image
    print(f"📥 Downloading test image...")
    print(f"   URL: {TEST_IMAGE_URL[:60]}...")
    response = requests.get(TEST_IMAGE_URL)
    test_image = Image.open(BytesIO(response.content))
    print(f"   ✅ Image loaded: {test_image.size} ({test_image.mode})")
    print()
    
    # Resize if too large
    max_size = 1024
    if max(test_image.size) > max_size:
        ratio = max_size / max(test_image.size)
        new_size = tuple(int(dim * ratio) for dim in test_image.size)
        test_image = test_image.resize(new_size, Image.Resampling.LANCZOS)
        print(f"   📐 Resized to: {test_image.size}")
    
    # Convert RGBA to RGB if needed
    if test_image.mode == 'RGBA':
        rgb_image = Image.new('RGB', test_image.size, (255, 255, 255))
        rgb_image.paste(test_image, mask=test_image.split()[3])
        test_image = rgb_image
        print(f"   🔄 Converted to RGB")
    print()
    
    # Get inspiration config
    inspiration_type = "variations"
    config = get_inspiration_config(inspiration_type)
    
    print(f"🎨 Testing Inspiration: {config['name']}")
    print(f"   Description: {config['description']}")
    print(f"   Expected output: {config['typical_output_count']} images")
    print()
    
    # Build prompt from template
    prompt_template = config['prompt_template']
    prompt = prompt_template.format(num_variations=3)
    
    print(f"💬 Prompt:")
    print(f"   {prompt}")
    print()
    
    # Initialize Vertex AI editor
    print("🚀 Initializing Vertex AI Gemini 2.5 Flash Image...")
    try:
        editor = VertexAIImageEditor()
        print(f"   ✅ Model: {editor.model_id}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("\n⚠️  Make sure google-genai is installed and credentials are configured!")
        return
    print()
    
    # Generate variations
    print(f"⏳ Generating {config['typical_output_count']} variations...")
    print("   This may take 15-30 seconds...")
    print()
    
    try:
        import time
        start_time = time.time()
        
        # Generate multiple images
        results = await editor.edit_image(
            pil_images=[test_image],
            prompt=prompt,
            num_images=config['typical_output_count']
        )
        
        elapsed = time.time() - start_time
        
        print(f"✅ SUCCESS!")
        print(f"⏱️  Total processing time: {elapsed:.2f}s")
        print(f"📸 Generated {len(results)} images")
        print(f"💰 Average time per image: {elapsed/len(results):.2f}s")
        print()
        
        # Save results
        output_dir = "test_output"
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"💾 Saving results to {output_dir}/")
        for i, img_bytes in enumerate(results):
            output_path = f"{output_dir}/variation_{i+1}.png"
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            
            # Get file size
            size_kb = len(img_bytes) / 1024
            print(f"   {i+1}. {output_path} ({size_kb:.1f} KB)")
        
        print()
        print("=" * 80)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print(f"Check the output in: {output_dir}/")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print()
        import traceback
        traceback.print_exc()


async def test_marketplace_pure():
    """Test marketplace_pure inspiration"""
    print("\n" + "=" * 80)
    print("TEST 2: MARKETPLACE PURE")
    print("=" * 80)
    print()
    
    # Download test image
    print(f"📥 Downloading test image...")
    response = requests.get(TEST_IMAGE_URL)
    test_image = Image.open(BytesIO(response.content))
    
    # Resize and convert
    max_size = 1024
    if max(test_image.size) > max_size:
        ratio = max_size / max(test_image.size)
        new_size = tuple(int(dim * ratio) for dim in test_image.size)
        test_image = test_image.resize(new_size, Image.Resampling.LANCZOS)
    
    if test_image.mode == 'RGBA':
        rgb_image = Image.new('RGB', test_image.size, (255, 255, 255))
        rgb_image.paste(test_image, mask=test_image.split()[3])
        test_image = rgb_image
    
    print(f"   ✅ Image ready: {test_image.size}")
    print()
    
    # Get config
    config = get_inspiration_config("marketplace_pure")
    prompt = config['prompt_template']
    
    print(f"🎨 Inspiration: {config['name']}")
    print(f"💬 Prompt: {prompt[:100]}...")
    print()
    
    # Generate
    editor = VertexAIImageEditor()
    
    print(f"⏳ Generating {config['typical_output_count']} marketplace images...")
    
    try:
        import time
        start_time = time.time()
        
        results = await editor.edit_image(
            pil_images=[test_image],
            prompt=prompt,
            num_images=config['typical_output_count']
        )
        
        elapsed = time.time() - start_time
        
        print(f"✅ SUCCESS!")
        print(f"⏱️  Processing time: {elapsed:.2f}s")
        print(f"📸 Generated {len(results)} images")
        print()
        
        # Save
        output_dir = "test_output"
        os.makedirs(output_dir, exist_ok=True)
        
        for i, img_bytes in enumerate(results):
            output_path = f"{output_dir}/marketplace_pure_{i+1}.png"
            with open(output_path, "wb") as f:
                f.write(img_bytes)
            print(f"   {i+1}. {output_path} ({len(img_bytes)/1024:.1f} KB)")
        
        print()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  VERTEX AI GEMINI 2.5 FLASH IMAGE - DIRECT TEST".center(78) + "║")
    print("║" + "  Testing Stock Image Inspirations".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # Test 1: Variations
    await test_vertex_variations()
    
    # Prompt for second test
    print("\n" + "-" * 80)
    print("Ready to test marketplace_pure? (will generate 3 more images)")
    print("-" * 80)
    await asyncio.sleep(2)
    
    # Test 2: Marketplace Pure
    await test_marketplace_pure()
    
    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETED!")
    print("=" * 80)
    print()
    print("📁 Check test_output/ folder for generated images")
    print()


if __name__ == "__main__":
    asyncio.run(main())

