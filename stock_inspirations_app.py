"""
Stock Image Inspirations - FAL Serverless App
A blackbox service that applies fixed inspirations to images.
Always generates 3 images per request.
Self-contained version with embedded configuration.
"""

import uuid
import time
import asyncio
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
import fal

# ============================================================================
# INSPIRATIONS CONFIGURATION (Embedded)
# ============================================================================

INSPIRATIONS = {

    "free_editing": {
        "name": "Free Editing",
        "category": "Free",
        "description": "Free editing of the input image",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # batch = single request with num_images=3
        "model": "fal-ai/nano-banana/edit"
    },

    "creative_color_material": {
        "name": "Variations Color Material",
        "category": "Creative",
        "description": "Generate variations of the input image with selected colors/materials",
        "prompt_template": "create professional variations of this image, maintaining the core subject/product but varying colors/materials for stock photography use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "parallel",  # parallel = 3 separate requests for diversity
        "model": "fal-ai/nano-banana/edit"
    },

    "creative_different_angles": {
        "name": "Different Angles",
        "category": "Creative",
        "description": "Generate variations of the input image with different angles",
        "prompt_template": "create professional variations of this image, maintaining the core subject/product but varying angles for stock photography use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "parallel",  # Need different angles, so parallel
        "model": "fal-ai/nano-banana/edit"
    },

    "creative_color_pop": {
        "name": "Color Pop",
        "category": "Creative",
        "description": "Pop the color to make it more vibrant and dramatic with selected colors",
        "prompt_template": "create professional variations of this image, maintaining the core subject/product but pop the color to make it more vibrant and dramatic",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Similar color enhancements, batch is fine
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_remove_overlays": {
        "name": "Marketplace Remove Overlays",
        "category": "Marketplace",
        "description": "Rebuild a compliant image for Shopping feeds—clear product, no promotional text or watermarks.",
        "prompt_template": "remove all marketplace overlays like logos, text, and other branding from the image, maintaining the core subject/product",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent removal, batch is fine
        "model": "fal-ai/nano-banana/edit"
    },
    
    "marketplace_pure": {
        "name": "Marketplace Pure",
        "category": "Marketplace",
        "description": "Auto‑clean, crop, and center a product on a pure white background for marketplace compliance and fast approvals.",
        "prompt_template": "transform into clean marketplace product photography: white background, professional studio lighting, high resolution, sharp focus, commercial quality, no distractions",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent style, batch is fine
        "model": "fal-ai/nano-banana/edit"
    },
    
    "marketplace_lifestyle": {
        "name": "Marketplace Lifestyle",
        "category": "Marketplace",
        "description": "Turn a basic packshot into a minimal lifestyle image that shows real‑world use without distracting overlays.",
        "prompt_template": "transform into lifestyle marketplace photography: modern home interior setting, natural lighting, authentic setting, professional e-commerce quality, contextual background",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent lifestyle style
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_close_ups": {
        "name": "Marketplace Close Ups",
        "category": "Marketplace",
        "description": "Capture macro cut‑ins that reveal craftsmanship and texture.",
        "prompt_template": "closeup shot of this product to show its details, like its details, patterns, fabric, capture small important creative details if there is like stiches, collars, logo, very closeup from different angle, closeup macro, no background, no grid just one detail, professional photography quality",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "parallel",  # Different closeup angles, need parallel
        "model": "fal-ai/nano-banana/edit"
    },
    
    "fashion_change_pose": {
        "name": "Change Pose",
        "category": "Fashion",
        "description": "Change subject/model pose while maintaining identity and background",
        "prompt_template": "change the pose of the subject to different professional pose, maintaining the same background and lighting style, professional fashion photography quality",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "parallel",  # Different poses, need parallel
        "model": "fal-ai/nano-banana/edit"
    },
    
    "background_change": {
        "name": "Change Background",
        "category": "Creative",
        "description": "Replace background with described background",
        "prompt_template": "replace the background with the described background, maintaining the subject perfectly, professional compositing, natural lighting consistency",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent background change
        "model": "fal-ai/nano-banana/edit"
    },
    
    "fuse_images": {
        "name": "Fuse Images",
        "category": "Marketplace",
        "description": "Combine multiple products into cohesive compositions for marketplace compliance",
        "prompt_template": "seamlessly combine these images into a single cohesive composition, natural blend maintaining all subjects, professional stock photography quality",
        "num_images": 3,
        "input_type": "multiple",
        "min_images": 2,
        "max_images": 5,
        "execution_mode": "batch",  # Fusion is consistent operation
        "model": "fal-ai/nano-banana/edit"
    }
}


def get_inspiration(name: str) -> Optional[Dict[str, Any]]:
    """Get inspiration configuration by name."""
    return INSPIRATIONS.get(name)


def list_inspirations() -> List[str]:
    """List all available inspiration names."""
    return list(INSPIRATIONS.keys())


def validate_input_count(inspiration_name: str, num_images: int) -> bool:
    """Check if the number of input images is valid for this inspiration."""
    inspiration = get_inspiration(inspiration_name)
    if not inspiration:
        return False
    return inspiration["min_images"] <= num_images <= inspiration["max_images"]


def build_prompt(inspiration_name: str, extra_prompt: Optional[str] = None) -> str:
    """Build the final prompt for the inspiration."""
    inspiration = get_inspiration(inspiration_name)
    if not inspiration:
        return ""
    
    base_prompt = inspiration["prompt_template"]
    
    if extra_prompt:
        return f"{base_prompt}. {extra_prompt}"
    
    return base_prompt


# ============================================================================
# EXECUTION UNIT - Handles both parallel and batch execution
# ============================================================================

async def execute_generation(
    model: str,
    prompt: str,
    image_urls: List[str],
    aspect_ratio: Optional[str],
    execution_mode: str,
    request_id: str
) -> List[Dict[str, Any]]:
    """
    Execute image generation with specified strategy.
    
    Args:
        model: Model endpoint (e.g., "fal-ai/nano-banana/edit")
        prompt: Generation prompt
        image_urls: Input image URLs
        aspect_ratio: Optional aspect ratio
        execution_mode: "parallel" or "batch"
        request_id: Request ID for logging
    
    Returns:
        List of generated images (always 3)
    """
    import fal_client
    
    # Build base arguments
    base_arguments = {
        "prompt": prompt,
        "image_urls": image_urls,
        "output_format": "png",
        "limit_generations": True
    }
    
    # Add aspect_ratio only if provided
    if aspect_ratio:
        base_arguments["aspect_ratio"] = aspect_ratio
    
    if execution_mode == "parallel":
        # PARALLEL MODE: 3 separate requests for maximum diversity
        print(f"[{request_id}] Execution mode: PARALLEL (3 separate requests)")
        
        handlers = []
        for i in range(3):
            arguments = {**base_arguments, "num_images": 1}
            handler = await fal_client.submit_async(model, arguments=arguments)
            handlers.append(handler)
            print(f"[{request_id}] Request {i+1}/3 submitted")
        
        # Wait for all 3 requests to complete in parallel
        results = await asyncio.gather(*[h.get() for h in handlers])
        
        # Parse results from all 3 requests
        generated_images = []
        for idx, result in enumerate(results):
            if "images" in result and len(result["images"]) > 0:
                generated_images.append({
                    "url": result["images"][0].get("url", ""),
                    "index": idx
                })
        
        print(f"[{request_id}] Collected {len(generated_images)} images from parallel requests")
        return generated_images
        
    else:
        # BATCH MODE: Single request with num_images=3
        print(f"[{request_id}] Execution mode: BATCH (single request, 3 images)")
        
        arguments = {**base_arguments, "num_images": 3}
        handler = await fal_client.submit_async(model, arguments=arguments)
        
        # Wait for completion
        async for event in handler.iter_events(with_logs=True):
            if hasattr(event, 'message'):
                print(f"[{request_id}] {event.message}")
        
        result = await handler.get()
        
        # Parse results
        generated_images = []
        if "images" in result:
            for idx, img in enumerate(result["images"]):
                generated_images.append({
                    "url": img.get("url", ""),
                    "index": idx
                })
        
        print(f"[{request_id}] Generated {len(generated_images)} images in batch mode")
        return generated_images


# ============================================================================
# INPUT & OUTPUT MODELS
# ============================================================================

class InspirationInput(BaseModel):
    """Input for the inspiration endpoint."""
    inspiration_name: str = Field(
        description="Name of the inspiration to apply (e.g., 'marketplace_pure', 'creative_color_material')",
        examples=["marketplace_pure"]
    )
    image_urls: List[str] = Field(
        description="List of input image URLs (1-5 images depending on inspiration)",
        examples=[["https://v3b.fal.media/files/b/zebra/shBQJppM86yD1p3nKJxS2.jpg"]]
    )
    aspect_ratio: Optional[Literal["21:9", "1:1", "4:3", "3:2", "2:3", "5:4", "4:5", "3:4", "16:9", "9:16"]] = Field(
        default=None,
        description="Aspect ratio of the generated image. Possible values: 21:9, 1:1, 4:3, 3:2, 2:3, 5:4, 4:5, 3:4, 16:9, 9:16"
    )
    extra_prompt: Optional[str] = Field(
        default=None,
        description="Optional extra instructions to append to the base prompt",
        examples=["make the image more vibrant and dramatic, with different camera angles"]
    )


class GeneratedImage(BaseModel):
    """A single generated image."""
    url: str = Field(description="URL of the generated image")
    index: int = Field(description="Index of the image (0-2)")


class InspirationOutput(BaseModel):
    """Output from the inspiration endpoint."""
    success: bool = Field(description="Whether the generation was successful")
    images: List[GeneratedImage] = Field(description="List of generated images (always 3)")
    inspiration_name: str = Field(description="The inspiration that was applied")
    prompt_used: str = Field(description="The actual prompt sent to the model")
    input_image_count: int = Field(description="Number of input images provided")
    aspect_ratio: Optional[str] = Field(
        default=None,
        description="Aspect ratio used for generation"
    )
    execution_mode: str = Field(description="Execution mode used (parallel or batch)")
    model: str = Field(description="Model used for generation")
    processing_time: float = Field(description="Time taken in seconds")
    request_id: str = Field(description="Unique request ID")
    error: Optional[str] = Field(default=None, description="Error message if failed")


# ============================================================================
# FAL SERVERLESS APP
# ============================================================================

class StockInspirations(fal.App):
    """Stock Image Inspirations serverless endpoint."""
    
    # CPU-optimized configuration (nano-banana runs on FAL's GPU infrastructure)
    machine_type = "M"  # M = CPU machine (cheap & fast deployment)
    min_concurrency = 0  # Scale to zero when idle
    max_concurrency = 2  # Limit concurrent requests
    max_multiplexing = 2  # Handle multiple requests per worker
    request_timeout = 120  # 2 minutes max per request
    startup_timeout = 60  # 1 minute for startup
    keep_alive = 0  # No keep-alive (scale to zero)
    
    # Minimal requirements for CPU deployment
    requirements = [
        "fal-client>=0.4.0",
        "pydantic>=2.0.0",
    ]
    
    def setup(self):
        """Initialize the app."""
        print("Stock Inspirations app initialized")
        print(f"Available inspirations: {', '.join(list_inspirations())}")
    
    @fal.endpoint("/")
    async def generate(self, input: InspirationInput) -> InspirationOutput:
        """
        Apply an inspiration to input images and generate 3 output images.
        
        This is a blackbox service - you provide:
        - inspiration_name: Which inspiration to apply
        - image_urls: Input images
        - aspect_ratio: (optional) Aspect ratio for output
        - extra_prompt: (optional) Extra instructions
        
        You get back 3 generated images.
        
        Execution modes:
        - PARALLEL: 3 separate requests for maximum diversity (variations, angles, close-ups)
        - BATCH: Single request with 3 images for consistent results (backgrounds, styles)
        """
        request_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        try:
            print(f"[{request_id}] Starting request")
            print(f"[{request_id}] Inspiration: {input.inspiration_name}")
            print(f"[{request_id}] Input images: {len(input.image_urls)}")
            if input.aspect_ratio:
                print(f"[{request_id}] Aspect ratio: {input.aspect_ratio}")
            
            # Get inspiration config
            inspiration = get_inspiration(input.inspiration_name)
            if not inspiration:
                available = list_inspirations()
                raise ValueError(
                    f"Unknown inspiration: {input.inspiration_name}. "
                    f"Available: {', '.join(available)}"
                )
            
            # Validate input image count
            if not validate_input_count(input.inspiration_name, len(input.image_urls)):
                raise ValueError(
                    f"Inspiration '{input.inspiration_name}' requires "
                    f"{inspiration['min_images']}-{inspiration['max_images']} images, "
                    f"but {len(input.image_urls)} were provided"
                )
            
            # Build prompt (blackbox magic)
            prompt = build_prompt(input.inspiration_name, input.extra_prompt)
            print(f"[{request_id}] Prompt: {prompt}")
            
            # Get execution strategy from inspiration config
            execution_mode = inspiration.get("execution_mode", "batch")
            model = inspiration.get("model", "fal-ai/nano-banana/edit")
            
            print(f"[{request_id}] Model: {model}")
            print(f"[{request_id}] Strategy: {execution_mode.upper()}")
            
            # Execute generation using the configured strategy
            generated_images = await execute_generation(
                model=model,
                prompt=prompt,
                image_urls=input.image_urls,
                aspect_ratio=input.aspect_ratio,
                execution_mode=execution_mode,
                request_id=request_id
            )
            
            processing_time = time.time() - start_time
            print(f"[{request_id}] Success! Generated {len(generated_images)} images in {processing_time:.2f}s")
            
            return InspirationOutput(
                success=True,
                images=[GeneratedImage(**img) for img in generated_images],
                inspiration_name=input.inspiration_name,
                prompt_used=prompt,
                input_image_count=len(input.image_urls),
                aspect_ratio=input.aspect_ratio,
                execution_mode=execution_mode,
                model=model,
                processing_time=processing_time,
                request_id=request_id,
                error=None
            )
        
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            print(f"[{request_id}] Error: {error_msg}")
            
            return InspirationOutput(
                success=False,
                images=[],
                inspiration_name=input.inspiration_name,
                prompt_used="",
                input_image_count=len(input.image_urls),
                aspect_ratio=input.aspect_ratio,
                execution_mode="unknown",
                model="unknown",
                processing_time=processing_time,
                request_id=request_id,
                error=error_msg
            )


# ============================================================================
# LOCAL TESTING
# ============================================================================

if __name__ == "__main__":
    print("Stock Image Inspirations - FAL Serverless App")
    print("=" * 60)
    print()
    print("Available Inspirations:")
    for name in list_inspirations():
        inspiration = get_inspiration(name)
        mode = inspiration.get('execution_mode', 'batch').upper()
        model = inspiration.get('model', 'unknown')
        print(f"  • {name}")
        print(f"    Category: {inspiration.get('category', 'N/A')}")
        print(f"    Mode: {mode} | Model: {model}")
        print(f"    {inspiration['description']}")
        print()
    print("Deploy with: fal deploy stock_inspirations_app.py")
