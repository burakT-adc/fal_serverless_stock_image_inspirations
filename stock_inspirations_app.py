"""
Stock Image Inspirations - FAL Serverless App
A blackbox service that applies fixed inspirations to images.
Always generates 3 images per request.
Self-contained version with embedded configuration.
"""

import uuid
import time
import asyncio
from typing import List, Optional, Dict, Any, Literal, get_args
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException
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
        "name": "Color Material",
        "category": "Creative",
        "description": "Generate variations of the input image with selected colors/materials",
        "prompt_template": "create professional variation of this image, maintaining the core subject/product but varying colors/materials for stock photography use",
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
        "prompt_template": "create professional variation of this image, maintaining the core subject/product but varying angles for stock photography use, same subject/product, remaining the same background and lighting style, just change the angle",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "parallel",  # parallel = 3 separate requests for diversity
        "model": "fal-ai/nano-banana/edit"
    },

    "creative_worms_eye_full": {
        "name": "Worm's Eye Full",
        "category": "Creative",
        "description": "Full worm's eye view - looking up from ground level",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"vertical_angle": 1}
    },

    "creative_worms_eye_half": {
        "name": "Worm's Eye Half",
        "category": "Creative",
        "description": "Partial worm's eye view - looking up at slight angle",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"vertical_angle": 0.7}
    },

    "creative_birds_eye_full": {
        "name": "Bird's Eye Full",
        "category": "Creative",
        "description": "Full bird's eye view - looking down from above",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"vertical_angle": -0.9}
    },

    "creative_birds_eye_half": {
        "name": "Bird's Eye Half",
        "category": "Creative",
        "description": "Partial bird's eye view - looking down at moderate angle",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"vertical_angle": -0.6}
    },

    "creative_wide_angle": {
        "name": "Wide Angle",
        "category": "Creative",
        "description": "Wide angle lens effect with slightly forward camera movement",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"wide_angle_lens": True, "move_forward": 0.5}
    },

    "creative_closeup_half": {
        "name": "Close-up Half",
        "category": "Creative",
        "description": "Moderate close-up with wide angle lens",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"wide_angle_lens": True, "move_forward": 5.5}
    },

    "creative_closeup_full": {
        "name": "Close-up Full",
        "category": "Creative",
        "description": "Maximum close-up with wide angle lens",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"wide_angle_lens": True, "move_forward": 9.0}
    },

    "creative_rotate_left_90": {
        "name": "Rotate Left 90°",
        "category": "Creative",
        "description": "Rotate camera 90 degrees to the left",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"rotate_right_left": 90}
    },

    "creative_rotate_left_45": {
        "name": "Rotate Left 45°",
        "category": "Creative",
        "description": "Rotate camera 45 degrees to the left",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"rotate_right_left": 45}
    },

    "creative_rotate_right_90": {
        "name": "Rotate Right 90°",
        "category": "Creative",
        "description": "Rotate camera 90 degrees to the right",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"rotate_right_left": -90}
    },

    "creative_rotate_right_45": {
        "name": "Rotate Right 45°",
        "category": "Creative",
        "description": "Rotate camera 45 degrees to the right",
        "prompt_template": "",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",
        "model": "fal-ai/qwen-image-edit-plus-lora-gallery/multiple-angles",
        "camera_params": {"rotate_right_left": -45}
    },

    "creative_color_pop": {
        "name": "Color Pop",
        "category": "Creative",
        "description": "Pop the color to make it more vibrant and dramatic with selected colors",
        "prompt_template": "create professional variation of this image, maintaining the core subject/product but pop the color to make it more vibrant and dramatic, same subject/product, remaining the same background, just pop the color for better stock photography use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Similar color enhancements, batch is fine
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_remove_overlays": {
        "name": "Remove Overlays",
        "category": "Marketplace",
        "description": "Rebuild a compliant image for Shopping feeds—clear product, no promotional text or watermarks.",
        "prompt_template": "remove all marketplace overlays like logos, text, and other branding from the image, maintaining the core subject/product, same subject/product, remaining the same background, just remove the overlays for better stock photography use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "parallel",  # Consistent removal, batch is fine
        "model": "fal-ai/nano-banana/edit"
    },
    
    "marketplace_pure": {
        "name": "Pure",
        "category": "Marketplace",
        "description": "Auto‑clean, crop, and center a product on a pure white background for marketplace compliance and fast approvals.",
        "prompt_template": "transform into clean marketplace product photography: white background, professional studio lighting, high resolution, sharp focus, commercial quality, no distractions, same subject/product but with clean solid background,",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent style, batch is fine
        "model": "fal-ai/nano-banana/edit"
    },
    
    "marketplace_lifestyle": {
        "name": "Lifestyle",
        "category": "Marketplace",
        "description": "Turn a basic packshot into a minimal lifestyle image that shows real‑world use without distracting overlays.",
        "prompt_template": "transform into lifestyle marketplace photography: lifestyle creative setting with meaningful context for the product, natural/dramatic/creative lighting, authentic setting, professional e-commerce quality, contextual background, create the background with meaningful context for the product",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "parallel",  # Consistent lifestyle style
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_close_ups": {
        "name": "Close Ups",
        "category": "Marketplace",
        "description": "Capture macro cut‑ins that reveal craftsmanship and texture.",
        "prompt_template": "closeup shot of this product to show its details, like its details, patterns, fabric, capture small important creative details (if there is like stiches, collars, the detail is important) very closeup from different angle, closeup macro, no background, no grid just one detail, professional photography quality",
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
        "prompt_template": "change the pose of the subject to different professional pose, maintaining the same background and lighting style, professional fashion photography quality, same subject/product, remaining the same background, just change the pose for better fashion photography use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "parallel",  # Different poses, need parallel
        "model": "fal-ai/nano-banana/edit"
    },

    "fashion_backshot": {
        "name": "Backshot",
        "category": "Fashion",
        "description": "Create a backshot of the uploaded model with the back of the garment",
        "prompt_template": "make the fashion model wear this clothing while posing to show the back of the clothing, same background, fashion photoshoot",
        "num_images": 3,
        "input_type": "multiple",
        "min_images": 2,
        "max_images": 5,
        "execution_mode": "batch",  # Consistent backshot style
        "model": "fal-ai/nano-banana/edit"
    },
    
    "creative_background_change": {
        "name": "Background Change",
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
    
    "creative_fuse_images": {
        "name": "Fuse Images",
        "category": "Creative",
        "description": "Combine multiple elements into cohesive compositions for marketplace compliance",
        "prompt_template": "seamlessly combine these images into a single cohesive composition, natural blend maintaining all subjects, professional stock photography quality, create the scene with meaningful context for the products",
        "num_images": 3,
        "input_type": "multiple",
        "min_images": 2,
        "max_images": 5,
        "execution_mode": "batch",  # Fusion is consistent operation
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_holiday_season": {
        "name": "Holiday Season",
        "category": "Marketplace",
        "description": "Create a holiday season image for holiday season promotion",
        "prompt_template": "create a holiday season image for marketplace compliance, same subject/product, holiday season for better marketplace compliance use, create the background with meaningful context for the product",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent holiday season style
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_social_promo": {
        "name": "Social Promo",
        "category": "Marketplace",
        "description": "Create a social media promotion image for social media promotion",
        "prompt_template": "create a social media promotion card for social media promotion, same subject/product, create the background with meaningful context for the product, create social media promo card with product details and call to action, creative and engaging social media promo card for better marketplace compliance use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent social media promotion style
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_ugc_model": {
        "name": "UGC Model",
        "category": "Marketplace",
        "description": "Create a UGC model image for social media UGC style",
        "prompt_template": "create a UGC model image holding/presenting the product, same subject/product, realistic and authentic UGC style social media model for better marketplace compliance use, no text, no social media banners, amateur photography quality, mid sentence",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent UGC model style
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_bundle_kit": {
        "name": "Bundle Kit",
        "category": "Marketplace",
        "description": "Fuse multiple products into a bundle kit with consistent background and lighting style",
        "prompt_template": "fuse the uploaded images into a bundle kit with consistent background and lighting style, create the background with meaningful context for the products, Compose a bundle with the products. Align scale, height, and shadows; evenly spaced, centered, white or light background, no overlapping labels, ",
        "num_images": 3,
        "input_type": "multiple",
        "min_images": 2,
        "max_images": 5,
        "execution_mode": "batch",  # Consistent bundle kit style
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_product_grid": {
        "name": "Product Grid",
        "category": "Marketplace",
        "description": "Create a product grid image for product grid promotion",
        "prompt_template": "create a product grid image for product grid promotion, same subject/product, product grid for better marketplace compliance use, create the background with meaningful context for the product, create product grid with product details and call to action, creative and engaging product grid for better marketplace compliance use",
        "num_images": 3,
        "input_type": "multiple",
        "min_images": 2,
        "max_images": 5,
        "execution_mode": "batch",  # Consistent product grid style
        "model": "fal-ai/nano-banana/edit"
    },

    "creative_relight": {
        "name": "Relight",
        "category": "Creative",
        "description": "Relight the image with consistent background style",
        "prompt_template": "relight the image with same background, same subject/product, remaining the same background, just change the lighting of the image for better stock photography use, creative/dramatic lighting style",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent relight style
        "model": "fal-ai/nano-banana/edit"
    },

    "creative_shadow_reflection": {
        "name": "Shadow Reflection",
        "category": "Creative",
        "description": "Shadow/Reflection Enhancer Add realistic shadow/reflection for premium depth on otherwise flat assets",
        "prompt_template": "add realistic shadow/reflection for premium depth on otherwise flat assets, same subject/product, match light direction and intensity; no halos, just add the shadow/reflection for better stock photography use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent shadow reflection style
    },

    "creative_depth_enhancer": {
        "name": "Depth Enhancer",
        "category": "Creative",
        "description": "Depth Enhancer Add realistic depth and perspective to photos",
        "prompt_template": "add realistic depth and perspective to input image, same subject/product, match light direction and intensity; no halos, just add the depth/perspective for better stock photography use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent depth enhancer style
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_food_menu": {
        "name": "Food Menu",
        "category": "Marketplace",
        "description": "Produce a menu‑compliant hero for delivery apps: single item, centered, bright, and clean.",
        "prompt_template": "Render food photography centered, appetizing directional light, clean surface, no text, no logos/watermarks, no people except hands if requested; neutral background",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent food menu style
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_price_sticker": {
        "name": "Price Sticker",
        "category": "Marketplace",
        "description": "Create platform‑safe sale treatments (for owned channels), with smart contrast and margins.",
        "prompt_template": "Overlay a small badge top‑right with descripted text and price. Round shape, high contrast, accessible font; keep product unobstructed, same subject/product, just add the price sticker for better marketplace compliance use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent price sticker style
        "model": "fal-ai/nano-banana/edit"
    },

    "marketplace_testimonial_card": {
        "name": "Testimonial Card",
        "category": "Marketplace",
        "description": "Turn user testimonial quote into a polished card for email/social",
        "prompt_template": "Combine the input image with quote  and name given (create realistic name and location and quote if no extra prompt given). Clean typographic hierarchy, discreet brand lockup, generous padding, create a testimonial card for testimonial card promotion, same subject/product, testimonial card for better marketplace compliance use, testomonial cards with creative detailed design",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent testimonial card style
        "model": "fal-ai/nano-banana/edit"
    },

    "creative_logo_mockup": {
        "name": "Logo Mockup",
        "category": "Creative",
        "description": "Create a logo mockup for brand promotion",
        "prompt_template": "create a logo mockup on with the given logo related object (phone case, mug, travel bag, etc., be creative and realistic), logo mockup for better marketplace compliance use, brand promotion material and realistic logo mockup for better brand promotion use",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent logo mockup style
        "model": "fal-ai/nano-banana/edit"
    },

    "creative_youtube_thumbnail": {
        "name": "YouTube Thumbnail",
        "category": "Creative",
        "description": "Create high‑contrast, readable thumbnails that boost CTR",
        "prompt_template": "Design a YouTube thumbnail for  featuring the input image. Cut out main subject, add big headline (3–6 words) (if not given, create a creative headline), strong contrast, background gradient, brand lockup bottom‑right, generous safe margins. high contrast, readable, boost CTR",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent YouTube thumbnail style
        "model": "fal-ai/nano-banana/edit"
    },

    "creative_tiktok_cover": {
        "name": "Reels/TikTok Cover Frame",
        "category": "Creative",
        "description": "Craft a scroll‑stopping cover that remains readable behind UI chrome",
        "prompt_template": "Create a vertical cover for Reel/TikTok. Center the input image; reserve top/bottom safe areas; add bold title (if not given, create a creative title);, make the subject intriguing and engaging with subtle gradient background; brand lockup small; crisp edges; scroll‑stopping cover that remains readable behind UI chrome",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent TikTok cover style
        "model": "fal-ai/nano-banana/edit"
    },

    "creative_text_driven": {
        "name": "Text Driven",
        "category": "Creative",
        "description": "Create type‑led graphics for quotes, launches, or quick promos with safe margins for social",
        "prompt_template": "For the input image, Design a type‑first visual with headline (if not created, create a creative headline), optional subhead (if not given, create a creative subhead), CTA (if not given, create a creative CTA). Background. Use high contrast, accessible typography, generous padding/safe zones, ",
        "num_images": 3,
        "input_type": "single",
        "min_images": 1,
        "max_images": 1,
        "execution_mode": "batch",  # Consistent text driven style
        "model": "fal-ai/nano-banana/edit"
    }

}

# ============================================================================
# DYNAMIC TYPE GENERATION
# ============================================================================

# Dynamically create a Literal type from all inspiration keys
# This ensures the API always shows all available inspirations
def _create_inspiration_literal():
    """Create a Literal type from all inspiration keys."""
    keys = tuple(INSPIRATIONS.keys())
    if not keys:
        return str
    return Literal[keys]  # type: ignore

# Create the dynamic Literal type
InspirationName = Literal[tuple(INSPIRATIONS.keys())]  # type: ignore


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
    request_id: str,
    camera_params: Optional[Dict[str, Any]] = None
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
    
    # Aspect ratio to dimensions mapping for Qwen model
    QWEN_ASPECT_RATIO_DIMENSIONS = {
        "1:1": {"width": 1080, "height": 1080},
        "2:3": {"width": 1000, "height": 1500},
        "4:5": {"width": 1080, "height": 1350},
        "16:9": {"width": 1920, "height": 1080},
        "9:16": {"width": 1080, "height": 1920}
    }
    
    # Check if this is a Qwen model
    is_qwen_model = "qwen-image-edit-plus-lora-gallery" in model
    
    # Build base arguments
    base_arguments = {
        "image_urls": image_urls,
        "output_format": "png"
    }
    
    # Add prompt only for non-Qwen models (Qwen doesn't use text prompts)
    if not is_qwen_model:
        base_arguments["prompt"] = prompt
        base_arguments["limit_generations"] = True
    else:
        # Qwen model - add fixed parameters
        base_arguments["guidance_scale"] = 5
        base_arguments["num_inference_steps"] = 30
        base_arguments["acceleration"] = "none"
        base_arguments["negative_prompt"] = "bad quality, blurred, artifact"
        
        # Add camera parameters if provided
        if camera_params:
            base_arguments.update(camera_params)
            print(f"[{request_id}] Qwen model - camera params: {camera_params}")
    
    # Handle aspect ratio based on model type
    if aspect_ratio:
        if is_qwen_model:
            # Qwen model uses width/height instead of aspect_ratio string
            if aspect_ratio in QWEN_ASPECT_RATIO_DIMENSIONS:
                base_arguments["image_size"] = QWEN_ASPECT_RATIO_DIMENSIONS[aspect_ratio]
                print(f"[{request_id}] Qwen model - using dimensions: {QWEN_ASPECT_RATIO_DIMENSIONS[aspect_ratio]}")
            else:
                raise ValueError(f"Unsupported aspect ratio for Qwen model: {aspect_ratio}")
        else:
            # Nano Banana uses aspect_ratio string
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
    inspiration_name: InspirationName = Field(  # type: ignore
        description="Name of the inspiration to apply (e.g., 'marketplace_pure', 'creative_color_material')",
        examples=["marketplace_pure"]
    )
    image_urls: List[str] = Field(
        description="List of input image URLs (1-5 images depending on inspiration)",
        examples=[["https://v3b.fal.media/files/b/zebra/shBQJppM86yD1p3nKJxS2.jpg"]]
    )
    aspect_ratio: Optional[Literal["1:1", "2:3", "4:5", "16:9", "9:16"]] = Field(
        default=None,
        description="Aspect ratio of the generated image. Supported values: 1:1, 2:3, 4:5, 16:9, 9:16"
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
        
        print(f"[{request_id}] Starting request")
        print(f"[{request_id}] Inspiration: {input.inspiration_name}")
        print(f"[{request_id}] Input images: {len(input.image_urls)}")
        if input.aspect_ratio:
            print(f"[{request_id}] Aspect ratio: {input.aspect_ratio}")
        
        # Get inspiration config
        inspiration = get_inspiration(input.inspiration_name)
        if not inspiration:
            available = list_inspirations()
            error_msg = f"Unknown inspiration: {input.inspiration_name}. Available: {', '.join(available)}"
            print(f"[{request_id}] Error: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Validate input image count
        if not validate_input_count(input.inspiration_name, len(input.image_urls)):
            error_msg = (
                f"Inspiration '{input.inspiration_name}' requires "
                f"{inspiration['min_images']}-{inspiration['max_images']} images, "
                f"but {len(input.image_urls)} were provided"
            )
            print(f"[{request_id}] Error: {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        # Build prompt (blackbox magic)
        prompt = build_prompt(input.inspiration_name, input.extra_prompt)
        print(f"[{request_id}] Prompt: {prompt}")
        
        # Get execution strategy from inspiration config
        execution_mode = inspiration.get("execution_mode", "batch")
        model = inspiration.get("model", "fal-ai/nano-banana/edit")
        camera_params = inspiration.get("camera_params", None)
        
        print(f"[{request_id}] Model: {model}")
        print(f"[{request_id}] Strategy: {execution_mode.upper()}")
        
        try:
            # Execute generation using the configured strategy
            generated_images = await execute_generation(
                model=model,
                prompt=prompt,
                image_urls=input.image_urls,
                aspect_ratio=input.aspect_ratio,
                execution_mode=execution_mode,
                request_id=request_id,
                camera_params=camera_params
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
        
        except ValueError as e:
            # Client errors (invalid input, unsupported aspect ratio, etc.)
            processing_time = time.time() - start_time
            error_msg = str(e)
            print(f"[{request_id}] Client Error ({processing_time:.2f}s): {error_msg}")
            raise HTTPException(status_code=400, detail=error_msg)
        
        except Exception as e:
            # Server errors (model failures, network issues, etc.)
            processing_time = time.time() - start_time
            error_msg = str(e)
            print(f"[{request_id}] Server Error ({processing_time:.2f}s): {error_msg}")
            raise HTTPException(status_code=500, detail=f"Image generation failed: {error_msg}")


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
