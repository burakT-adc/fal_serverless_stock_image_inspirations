"""
Configuration for fixed inspirations and their FAL endpoints.
Each inspiration defines how to transform input images using specific FAL models.
"""

from typing import Dict, List, Optional, Any
from enum import Enum


class InspirationCategory(str, Enum):
    """Categories of inspirations."""
    VARIATIONS = "variations"
    POSE = "pose"
    FUSION = "fusion"
    MARKETPLACE = "marketplace"
    STYLE = "style"


class InputType(str, Enum):
    """Types of input requirements."""
    SINGLE_IMAGE = "single_image"
    MULTI_IMAGE = "multi_image"
    OPTIONAL_MULTI = "optional_multi"


# Fixed Inspirations Configuration
INSPIRATIONS_CONFIG = {
    "variations": {
        "name": "Variations",
        "description": "Generate multiple variations of the input image with different styles and compositions",
        "category": InspirationCategory.VARIATIONS,
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.OPTIONAL_MULTI,
        "default_params": {
            "num_images": 3,
            "output_format": "png",
            "enable_safety_checks": True
        },
        "prompt_template": "create {num_variations} professional variations of this image, maintaining the core subject but varying composition, lighting, and perspective for stock photography use",
        "min_input_images": 1,
        "max_input_images": 5,
        "typical_output_count": 3
    },
    
    "change_pose": {
        "name": "Change Pose",
        "description": "Change the pose or position of subjects in the image while maintaining their identity",
        "category": InspirationCategory.POSE,
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.SINGLE_IMAGE,
        "default_params": {
            "num_images": 3,
            "output_format": "png",
            "enable_safety_checks": True
        },
        "prompt_template": "change the pose of the subject to a {pose_description}, maintaining the same background and lighting style, professional stock photography quality",
        "pose_options": [
            "confident standing pose",
            "seated working position",
            "dynamic action pose",
            "relaxed casual stance",
            "professional portrait pose"
        ],
        "min_input_images": 1,
        "max_input_images": 1,
        "typical_output_count": 3
    },
    
    "fuse_images": {
        "name": "Fuse Images",
        "description": "Combine multiple images into a cohesive composition",
        "category": InspirationCategory.FUSION,
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.MULTI_IMAGE,
        "default_params": {
            "num_images": 2,
            "output_format": "png",
            "enable_safety_checks": True
        },
        "prompt_template": "seamlessly combine these images into a single cohesive composition, {fusion_style}, maintaining professional stock photography quality",
        "fusion_styles": [
            "natural blend maintaining all subjects",
            "artistic collage style",
            "professional montage",
            "seamless integration with unified lighting",
            "creative overlay composition"
        ],
        "min_input_images": 2,
        "max_input_images": 5,
        "typical_output_count": 2
    },
    
    "marketplace_pure": {
        "name": "Marketplace Pure",
        "description": "Transform image into clean marketplace product photography style",
        "category": InspirationCategory.MARKETPLACE,
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.SINGLE_IMAGE,
        "default_params": {
            "num_images": 3,
            "output_format": "png",
            "enable_safety_checks": True
        },
        "prompt_template": "transform into clean marketplace product photography: white background, professional studio lighting, high resolution, sharp focus, commercial quality, no distractions",
        "min_input_images": 1,
        "max_input_images": 1,
        "typical_output_count": 3
    },
    
    "marketplace_lifestyle": {
        "name": "Marketplace Lifestyle",
        "description": "Transform into lifestyle marketplace photography with context",
        "category": InspirationCategory.MARKETPLACE,
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.SINGLE_IMAGE,
        "default_params": {
            "num_images": 3,
            "output_format": "png",
            "enable_safety_checks": True
        },
        "prompt_template": "transform into lifestyle marketplace photography: {lifestyle_context}, natural lighting, authentic setting, professional e-commerce quality, contextual background",
        "lifestyle_contexts": [
            "modern home interior setting",
            "outdoor natural environment",
            "contemporary office space",
            "stylish cafe or restaurant",
            "minimalist lifestyle scene"
        ],
        "min_input_images": 1,
        "max_input_images": 1,
        "typical_output_count": 3
    },
    
    "style_transfer": {
        "name": "Style Transfer",
        "description": "Apply different artistic or photographic styles to the image",
        "category": InspirationCategory.STYLE,
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.SINGLE_IMAGE,
        "default_params": {
            "num_images": 3,
            "output_format": "png",
            "enable_safety_checks": True
        },
        "prompt_template": "apply {style_type} style to this image while maintaining the core subject and composition, professional photography quality",
        "style_types": [
            "cinematic film photography",
            "high-key bright and airy",
            "moody and dramatic",
            "vintage analog film",
            "modern minimalist",
            "warm golden hour",
            "cool professional corporate"
        ],
        "min_input_images": 1,
        "max_input_images": 1,
        "typical_output_count": 3
    },
    
    "background_change": {
        "name": "Background Change",
        "description": "Replace or modify the background while keeping the main subject",
        "category": InspirationCategory.VARIATIONS,
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.SINGLE_IMAGE,
        "default_params": {
            "num_images": 3,
            "output_format": "png",
            "enable_safety_checks": True
        },
        "prompt_template": "replace the background with {background_type}, maintaining the subject perfectly, professional compositing, natural lighting consistency",
        "background_types": [
            "clean white studio background",
            "modern office interior",
            "natural outdoor setting",
            "urban city environment",
            "abstract gradient backdrop",
            "luxurious interior space"
        ],
        "min_input_images": 1,
        "max_input_images": 1,
        "typical_output_count": 3
    },
    
    "upscale_enhance": {
        "name": "Upscale & Enhance",
        "description": "Upscale resolution and enhance image quality",
        "category": InspirationCategory.VARIATIONS,
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.SINGLE_IMAGE,
        "default_params": {
            "num_images": 1,
            "output_format": "png",
            "enable_safety_checks": True
        },
        "prompt_template": "enhance image quality to professional stock photography standard: increase sharpness, improve lighting, enhance colors, maximize detail and clarity",
        "min_input_images": 1,
        "max_input_images": 1,
        "typical_output_count": 1
    },
    
    "seasonal_variants": {
        "name": "Seasonal Variants",
        "description": "Create seasonal variations of the image",
        "category": InspirationCategory.VARIATIONS,
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.SINGLE_IMAGE,
        "default_params": {
            "num_images": 3,
            "output_format": "png",
            "enable_safety_checks": True
        },
        "prompt_template": "transform into {season} themed version: appropriate lighting, seasonal colors, contextual elements, maintaining professional stock photography quality",
        "seasons": ["spring", "summer", "autumn", "winter"],
        "min_input_images": 1,
        "max_input_images": 1,
        "typical_output_count": 3
    },
    
    "time_of_day": {
        "name": "Time of Day Variations",
        "description": "Generate variations with different times of day lighting",
        "category": InspirationCategory.VARIATIONS,
        "fal_endpoint": "fal-ai/nano-banana/edit",
        "input_type": InputType.SINGLE_IMAGE,
        "default_params": {
            "num_images": 3,
            "output_format": "png",
            "enable_safety_checks": True
        },
        "prompt_template": "transform lighting to {time_of_day}: {lighting_description}, maintaining composition and subject, professional photography quality",
        "times_of_day": {
            "golden_hour": "warm golden sunlight, soft shadows, magical hour glow",
            "blue_hour": "cool blue tones, twilight atmosphere, soft diffused light",
            "midday": "bright clear daylight, strong shadows, vibrant colors",
            "overcast": "soft diffused lighting, even tones, no harsh shadows"
        },
        "min_input_images": 1,
        "max_input_images": 1,
        "typical_output_count": 3
    }
}


def get_inspiration_config(inspiration_type: str) -> Optional[Dict[str, Any]]:
    """Get configuration for a specific inspiration type."""
    return INSPIRATIONS_CONFIG.get(inspiration_type)


def list_inspiration_types() -> List[str]:
    """List all available inspiration types."""
    return list(INSPIRATIONS_CONFIG.keys())


def get_inspirations_by_category(category: InspirationCategory) -> Dict[str, Dict[str, Any]]:
    """Get all inspirations in a specific category."""
    return {
        key: config for key, config in INSPIRATIONS_CONFIG.items()
        if config["category"] == category
    }


def validate_input_images(inspiration_type: str, num_images: int) -> bool:
    """Validate if the number of input images is valid for the inspiration type."""
    config = get_inspiration_config(inspiration_type)
    if not config:
        return False
    
    min_images = config.get("min_input_images", 1)
    max_images = config.get("max_input_images", 1)
    
    return min_images <= num_images <= max_images


# FAL Endpoint Configurations
FAL_ENDPOINTS_CONFIG = {
    "fal-ai/nano-banana/edit": {
        "description": "Google's Nano Banana image editing model",
        "supports_multi_image": True,
        "max_images_input": 5,
        "typical_latency_seconds": 3.0,
        "cost_per_image": 0.039,
        "documentation_url": "https://fal.ai/models/fal-ai/nano-banana/edit"
    },
    "vertex-ai/gemini-2.5-flash-image": {
        "description": "Gemini 2.5 Flash Image editing model on Vertex AI",
        "supports_multi_image": True,
        "max_images_input": 10,
        "typical_latency_seconds": 2.5,
        "cost_per_image": 0.025,  # Estimate - actual pricing varies
        "documentation_url": "https://ai.google.dev/gemini-api/docs/image-generation"
    }
}


def get_endpoint_config(endpoint: str) -> Optional[Dict[str, Any]]:
    """Get configuration for a specific FAL endpoint."""
    return FAL_ENDPOINTS_CONFIG.get(endpoint)

