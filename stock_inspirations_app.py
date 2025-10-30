"""
Stock Image Inspirations - FAL Serverless App
A blackbox service that applies fixed inspirations to images.
Always generates 3 images per request.
Self-contained version with embedded configuration.
"""

import uuid
import time
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
import fal


# ============================================================================
# INSPIRATIONS CONFIGURATION (Embedded)
# ============================================================================

INSPIRATIONS = {
    "variations": {
        "name": "Variations",
        "description": "Generate 3 variations of the input image with different styles",
        "prompt_template": "create professional variations of this image, maintaining the core subject but varying composition, lighting, and perspective for stock photography use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1
    },
    
    "marketplace_pure": {
        "name": "Marketplace Pure",
        "description": "Transform into clean marketplace product photography (white background)",
        "prompt_template": "transform into clean marketplace product photography: white background, professional studio lighting, high resolution, sharp focus, commercial quality, no distractions",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1
    },
    
    "marketplace_lifestyle": {
        "name": "Marketplace Lifestyle",
        "description": "Transform into lifestyle marketplace photography with context",
        "prompt_template": "transform into lifestyle marketplace photography: modern home interior setting, natural lighting, authentic setting, professional e-commerce quality, contextual background",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1
    },
    
    "change_pose": {
        "name": "Change Pose",
        "description": "Change subject pose while maintaining identity",
        "prompt_template": "change the pose of the subject to a confident professional pose, maintaining the same background and lighting style, professional stock photography quality",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1
    },
    
    "style_cinematic": {
        "name": "Cinematic Style",
        "description": "Apply cinematic film photography style",
        "prompt_template": "apply cinematic film photography style to this image while maintaining the core subject and composition, professional photography quality",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1
    },
    
    "background_white": {
        "name": "White Background",
        "description": "Replace background with clean white studio background",
        "prompt_template": "replace the background with clean white studio background, maintaining the subject perfectly, professional compositing, natural lighting consistency",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1
    },
    
    "enhance": {
        "name": "Enhance Quality",
        "description": "Enhance image quality and sharpness",
        "prompt_template": "enhance image quality to professional stock photography standard: increase sharpness, improve lighting, enhance colors, maximize detail and clarity",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1
    },
    
    "fuse_images": {
        "name": "Fuse Images",
        "description": "Combine multiple images into cohesive compositions",
        "prompt_template": "seamlessly combine these images into a single cohesive composition, natural blend maintaining all subjects, professional stock photography quality",
        "num_images": 3,
        "input_type": "multiple",
        "min_images": 2,
        "max_images": 5
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
# INPUT & OUTPUT MODELS
# ============================================================================

class InspirationInput(BaseModel):
    """Input for the inspiration endpoint."""
    inspiration_name: str = Field(
        description="Name of the inspiration to apply (e.g., 'variations', 'marketplace_pure')",
        examples=["variations"]
    )
    image_urls: List[str] = Field(
        description="List of input image URLs (1-5 images depending on inspiration)",
        examples=[["https://example.com/image.jpg"]]
    )
    aspect_ratio: Optional[Literal["21:9", "1:1", "4:3", "3:2", "2:3", "5:4", "4:5", "3:4", "16:9", "9:16"]] = Field(
        default=None,
        description="Aspect ratio of the generated image. Possible values: 21:9, 1:1, 4:3, 3:2, 2:3, 5:4, 4:5, 3:4, 16:9, 9:16"
    )
    extra_prompt: Optional[str] = Field(
        default=None,
        description="Optional extra instructions to append to the base prompt",
        examples=["with vibrant colors and dramatic lighting"]
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
            
            # Call FAL Nano Banana model
            import fal_client
            
            print(f"[{request_id}] Calling fal-ai/nano-banana/edit...")
            
            # Build arguments
            arguments = {
                "prompt": prompt,
                "image_urls": input.image_urls,
                "num_images": 3,  # Always 3 images
                "output_format": "png",
                "limit_generations": True
            }
            
            # Add aspect_ratio only if provided
            if input.aspect_ratio:
                arguments["aspect_ratio"] = input.aspect_ratio
            
            handler = await fal_client.submit_async(
                "fal-ai/nano-banana/edit",
                arguments=arguments
            )
            
            # Wait for completion
            async for event in handler.iter_events(with_logs=True):
                if hasattr(event, 'message'):
                    print(f"[{request_id}] {event.message}")
            
            result = await handler.get()
            
            # Parse results
            generated_images = []
            if "images" in result:
                for idx, img in enumerate(result["images"]):
                    generated_images.append(GeneratedImage(
                        url=img.get("url", ""),
                        index=idx
                    ))
            
            processing_time = time.time() - start_time
            print(f"[{request_id}] Success! Generated {len(generated_images)} images in {processing_time:.2f}s")
            
            return InspirationOutput(
                success=True,
                images=generated_images,
                inspiration_name=input.inspiration_name,
                prompt_used=prompt,
                input_image_count=len(input.image_urls),
                aspect_ratio=input.aspect_ratio,
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
        print(f"  • {name}: {inspiration['description']}")
    print()
    print("Deploy with: fal deploy stock_inspirations_app.py")
