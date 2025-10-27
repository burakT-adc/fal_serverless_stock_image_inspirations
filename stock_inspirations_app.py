"""
FAL.ai Serverless Deployment for Stock Image Inspirations
Applies fixed inspirations to input images using FAL models
"""

import os
import uuid
import base64
from io import BytesIO
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
import fal
from inspirations_config import (
    get_inspiration_config, 
    list_inspiration_types,
    validate_input_images,
    get_endpoint_config
)


# Input Model
class StockImageInspirationsInput(BaseModel):
    inspiration_type: str = Field(
        default="variations",
        description="Type of inspiration to apply (variations, change_pose, fuse_images, marketplace_pure, marketplace_lifestyle, etc.)"
    )
    image_urls: List[str] = Field(
        default=[],
        description="List of input image URLs (1-5 images depending on inspiration type)",
        min_length=1,
        max_length=5
    )
    custom_params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional custom parameters to override defaults (e.g., num_images, style_option)"
    )
    output_format: str = Field(
        default="png",
        description="Output image format (png, jpeg, webp)",
        pattern="^(png|jpeg|webp)$"
    )


# Output Models
class GeneratedImage(BaseModel):
    url: str = Field(description="URL of the generated image")
    index: int = Field(description="Index of the generated image")


class StockImageInspirationsOutput(BaseModel):
    images: List[GeneratedImage] = Field(description="List of generated images")
    inspiration_type: str = Field(description="The inspiration type that was applied")
    inspiration_name: str = Field(description="Human-readable name of the inspiration")
    prompt_used: str = Field(description="The actual prompt sent to the FAL model")
    fal_endpoint: str = Field(description="The FAL endpoint that was called")
    input_image_count: int = Field(description="Number of input images provided")
    output_image_count: int = Field(description="Number of images generated")
    processing_time: float = Field(description="Time taken in seconds")
    request_id: str = Field(description="Unique request identifier")
    success: bool = Field(default=True, description="Whether the operation was successful")
    warnings: Optional[List[str]] = Field(default=None, description="Any warnings during processing")


# FAL App definition
class StockImageInspirations(fal.App):
    """Stock Image Inspirations serverless endpoint."""
    
    machine_type = "M"
    min_concurrency = 0
    max_concurrency = 5
    max_multiplexing = 3
    request_timeout = 60
    startup_timeout = 30
    concurrency_buffer = 0
    concurrency_buffer_perc = 0
    
    host_kwargs = {
        "keep_alive": 0,
        "request_timeout": 60,
        "startup_timeout": 30,
    }
    
    requirements = [
        "fal-client>=0.4.0",
        "Pillow>=10.0.0",
        "pydantic>=2.0.0",
        "aiohttp>=3.8.0",
    ]
    
    def setup(self):
        """Initialize any required resources."""
        print("INFO: Stock Image Inspirations application setup completed")
    
    @fal.endpoint("/")
    async def apply_inspiration(
        self, 
        input: StockImageInspirationsInput
    ) -> StockImageInspirationsOutput:
        """Apply a fixed inspiration to input images using FAL models."""
        import time
        import fal_client
        
        request_id = str(uuid.uuid4())
        start_time = time.time()
        warnings = []
        
        try:
            print(f"[{request_id}] Starting inspiration application")
            print(f"[{request_id}] Inspiration type: {input.inspiration_type}")
            print(f"[{request_id}] Input images: {len(input.image_urls)}")
            
            # Get inspiration configuration
            inspiration_config = get_inspiration_config(input.inspiration_type)
            if not inspiration_config:
                available = list_inspiration_types()
                raise ValueError(
                    f"Unknown inspiration type: {input.inspiration_type}. "
                    f"Available types: {', '.join(available)}"
                )
            
            # Validate input image count
            if not validate_input_images(input.inspiration_type, len(input.image_urls)):
                min_imgs = inspiration_config.get("min_input_images", 1)
                max_imgs = inspiration_config.get("max_input_images", 1)
                raise ValueError(
                    f"Inspiration '{input.inspiration_type}' requires {min_imgs}-{max_imgs} "
                    f"input images, but {len(input.image_urls)} were provided"
                )
            
            # Build prompt
            prompt = build_prompt(inspiration_config, input.custom_params)
            print(f"[{request_id}] Prompt: {prompt}")
            
            # Get FAL endpoint
            fal_endpoint = inspiration_config["fal_endpoint"]
            print(f"[{request_id}] FAL endpoint: {fal_endpoint}")
            
            # Prepare FAL arguments
            fal_arguments = prepare_fal_arguments(
                inspiration_config=inspiration_config,
                image_urls=input.image_urls,
                prompt=prompt,
                custom_params=input.custom_params,
                output_format=input.output_format
            )
            
            # Call FAL endpoint
            print(f"[{request_id}] Calling FAL endpoint...")
            handler = await fal_client.submit_async(
                fal_endpoint,
                arguments=fal_arguments,
            )
            
            # Wait for completion
            async for event in handler.iter_events(with_logs=True):
                if hasattr(event, 'message'):
                    print(f"[{request_id}] FAL: {event.message}")
            
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
            print(f"[{request_id}] Completed in {processing_time:.2f}s")
            print(f"[{request_id}] Generated {len(generated_images)} images")
            
            return StockImageInspirationsOutput(
                images=generated_images,
                inspiration_type=input.inspiration_type,
                inspiration_name=inspiration_config["name"],
                prompt_used=prompt,
                fal_endpoint=fal_endpoint,
                input_image_count=len(input.image_urls),
                output_image_count=len(generated_images),
                processing_time=processing_time,
                request_id=request_id,
                success=True,
                warnings=warnings if warnings else None
            )
        
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"[{request_id}] Error: {str(e)}")
            
            return StockImageInspirationsOutput(
                images=[],
                inspiration_type=input.inspiration_type,
                inspiration_name="Unknown",
                prompt_used="",
                fal_endpoint="",
                input_image_count=len(input.image_urls),
                output_image_count=0,
                processing_time=processing_time,
                request_id=request_id,
                success=False,
                warnings=[f"Request failed: {str(e)}"]
            )


# Helper functions
def build_prompt(
    inspiration_config: Dict[str, Any],
    custom_params: Optional[Dict[str, Any]]
) -> str:
    """Build the prompt from template and parameters."""
    prompt_template = inspiration_config.get("prompt_template", "")
    
    # Handle different template variables
    params = {}
    
    # For variations
    if "{num_variations}" in prompt_template:
        params["num_variations"] = custom_params.get("num_variations", 4) if custom_params else 4
    
    # For pose changes
    if "{pose_description}" in prompt_template:
        pose_options = inspiration_config.get("pose_options", [])
        if custom_params and "pose_option" in custom_params:
            params["pose_description"] = custom_params["pose_option"]
        elif pose_options:
            params["pose_description"] = pose_options[0]
        else:
            params["pose_description"] = "natural pose"
    
    # For fusion
    if "{fusion_style}" in prompt_template:
        fusion_styles = inspiration_config.get("fusion_styles", [])
        if custom_params and "fusion_style" in custom_params:
            params["fusion_style"] = custom_params["fusion_style"]
        elif fusion_styles:
            params["fusion_style"] = fusion_styles[0]
        else:
            params["fusion_style"] = "natural blend"
    
    # For lifestyle
    if "{lifestyle_context}" in prompt_template:
        lifestyle_contexts = inspiration_config.get("lifestyle_contexts", [])
        if custom_params and "lifestyle_context" in custom_params:
            params["lifestyle_context"] = custom_params["lifestyle_context"]
        elif lifestyle_contexts:
            params["lifestyle_context"] = lifestyle_contexts[0]
        else:
            params["lifestyle_context"] = "modern setting"
    
    # For style transfer
    if "{style_type}" in prompt_template:
        style_types = inspiration_config.get("style_types", [])
        if custom_params and "style_type" in custom_params:
            params["style_type"] = custom_params["style_type"]
        elif style_types:
            params["style_type"] = style_types[0]
        else:
            params["style_type"] = "professional"
    
    # For background change
    if "{background_type}" in prompt_template:
        background_types = inspiration_config.get("background_types", [])
        if custom_params and "background_type" in custom_params:
            params["background_type"] = custom_params["background_type"]
        elif background_types:
            params["background_type"] = background_types[0]
        else:
            params["background_type"] = "neutral background"
    
    # For seasonal
    if "{season}" in prompt_template:
        seasons = inspiration_config.get("seasons", ["spring", "summer", "autumn", "winter"])
        if custom_params and "season" in custom_params:
            params["season"] = custom_params["season"]
        else:
            params["season"] = seasons[0]
    
    # For time of day
    if "{time_of_day}" in prompt_template:
        times = inspiration_config.get("times_of_day", {})
        if custom_params and "time_of_day" in custom_params:
            time_key = custom_params["time_of_day"]
            if time_key in times:
                params["time_of_day"] = time_key
                params["lighting_description"] = times[time_key]
            else:
                params["time_of_day"] = list(times.keys())[0]
                params["lighting_description"] = list(times.values())[0]
        else:
            params["time_of_day"] = list(times.keys())[0] if times else "golden_hour"
            params["lighting_description"] = list(times.values())[0] if times else "warm light"
    
    # Format the template
    try:
        return prompt_template.format(**params)
    except KeyError:
        # If formatting fails, return template as-is
        return prompt_template


def prepare_fal_arguments(
    inspiration_config: Dict[str, Any],
    image_urls: List[str],
    prompt: str,
    custom_params: Optional[Dict[str, Any]],
    output_format: str
) -> Dict[str, Any]:
    """Prepare arguments for FAL endpoint call."""
    
    # Start with default params from config
    arguments = inspiration_config.get("default_params", {}).copy()
    
    # Add prompt
    arguments["prompt"] = prompt
    
    # Add images
    arguments["image_urls"] = image_urls
    
    # Override with custom params if provided
    if custom_params:
        for key, value in custom_params.items():
            if key not in ["pose_option", "fusion_style", "lifestyle_context", 
                          "style_type", "background_type", "season", "time_of_day",
                          "num_variations"]:  # These are used for prompt building
                arguments[key] = value
    
    # Set output format
    arguments["output_format"] = output_format
    
    return arguments


# For local testing
if __name__ == "__main__":
    print("Stock Image Inspirations FAL Serverless App")
    print("This file should be deployed using: fal deploy stock_inspirations_app.py")
    print()
    print("Available inspirations:")
    for insp_type in list_inspiration_types():
        config = get_inspiration_config(insp_type)
        print(f"  - {insp_type}: {config['description']}")
