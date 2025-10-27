"""
Vertex AI integration for Stock Image Inspirations.
Uses Gemini 2.5 Flash Image for image editing as an alternative to Nano Banana.
"""

import os
from typing import List, Any, Optional
from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types


class VertexAIImageEditor:
    """
    Vertex AI Gemini 2.5 Flash Image editor.
    Alternative to FAL Nano Banana endpoint.
    """
    
    def __init__(self):
        """Initialize Vertex AI client."""
        self._client = None
        self.model_id = "gemini-2.5-flash-image"
    
    def get_client(self) -> genai.Client:
        """Get or create Vertex AI client."""
        if self._client is None:
            # Read project from credentials if available
            import os
            import json
            project_id = None
            location = "us-central1"  # Default location
            
            # Try to read from credentials file
            cred_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if cred_file and os.path.exists(cred_file):
                try:
                    with open(cred_file, 'r') as f:
                        creds = json.load(f)
                        project_id = creds.get("project_id")
                except:
                    pass
            
            # If not found, try environment variable
            if not project_id:
                project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "adcreative-official")
            
            self._client = genai.Client(
                vertexai=True,
                project=project_id,
                location=location
            )
        return self._client
    
    async def edit_image(
        self,
        pil_images: List[Image.Image],
        prompt: str,
        aspect_ratio: Optional[str] = None,
        num_images: int = 3
    ) -> List[bytes]:
        """
        Edit images using Gemini 2.5 Flash Image on Vertex AI.
        
        Args:
            pil_images: List of PIL.Image objects (1..N)
            prompt: Instruction string for the edit
            aspect_ratio: Optional aspect ratio (e.g., "1:1", "3:4", "16:9")
            num_images: Number of images to generate (Note: Gemini may return 1 image per call)
            
        Returns:
            List of image bytes (PNG format)
        """
        if not pil_images:
            raise ValueError("pil_images cannot be empty")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string")
        
        client = self.get_client()
        
        # Gemini 2.5 Flash Image typically returns 1 image per call
        # For multiple images, we need to call it multiple times
        results = []
        
        for i in range(num_images):
            # Build contents: images first, then prompt
            contents: List[Any] = []
            contents.extend(pil_images)
            contents.append(prompt)
            
            # Configure generation
            cfg = types.GenerateContentConfig(
                response_modalities=[types.Modality.IMAGE],
            )
            if aspect_ratio:
                cfg.image_config = types.ImageConfig(aspect_ratio=aspect_ratio)
            
            # Generate content
            resp = client.models.generate_content(
                model=self.model_id,
                contents=contents,
                config=cfg,
            )
            
            # Extract image data
            for cand in getattr(resp, "candidates", []) or []:
                for part in getattr(cand.content, "parts", []) or []:
                    inline = getattr(part, "inline_data", None)
                    data = getattr(inline, "data", None) if inline else None
                    if data:
                        results.append(data)
                        break
            
            if len(results) < i + 1:
                raise RuntimeError(f"Vertex AI returned no image for iteration {i+1}. Raw response: {resp}")
        
        return results
    
    async def edit_image_single(
        self,
        pil_images: List[Image.Image],
        prompt: str,
        aspect_ratio: Optional[str] = None
    ) -> bytes:
        """
        Edit images and return a single result.
        
        Args:
            pil_images: List of PIL.Image objects (1..N)
            prompt: Instruction string for the edit
            aspect_ratio: Optional aspect ratio (e.g., "1:1", "3:4", "16:9")
            
        Returns:
            Image bytes (PNG format)
        """
        if not pil_images:
            raise ValueError("pil_images cannot be empty")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be a non-empty string")
        
        client = self.get_client()
        
        # Build contents: images first, then prompt
        contents: List[Any] = []
        contents.extend(pil_images)
        contents.append(prompt)
        
        # Configure generation
        cfg = types.GenerateContentConfig(
            response_modalities=[types.Modality.IMAGE],
        )
        if aspect_ratio:
            cfg.image_config = types.ImageConfig(aspect_ratio=aspect_ratio)
        
        # Generate content
        resp = client.models.generate_content(
            model=self.model_id,
            contents=contents,
            config=cfg,
        )
        
        # Extract first image
        for cand in getattr(resp, "candidates", []) or []:
            for part in getattr(cand.content, "parts", []) or []:
                inline = getattr(part, "inline_data", None)
                data = getattr(inline, "data", None) if inline else None
                if data:
                    return data
        
        raise RuntimeError(f"Vertex AI returned no image. Raw response: {resp}")


# Convenience functions
async def edit_with_vertex(
    images: List[Image.Image],
    prompt: str,
    num_images: int = 3,
    aspect_ratio: Optional[str] = None
) -> List[bytes]:
    """
    Convenience function to edit images with Vertex AI.
    
    Args:
        images: List of PIL.Image objects
        prompt: Edit instruction
        num_images: Number of variations to generate
        aspect_ratio: Optional aspect ratio
        
    Returns:
        List of image bytes
    """
    editor = VertexAIImageEditor()
    return await editor.edit_image(images, prompt, aspect_ratio, num_images)


async def edit_with_vertex_single(
    images: List[Image.Image],
    prompt: str,
    aspect_ratio: Optional[str] = None
) -> bytes:
    """
    Convenience function to edit images with Vertex AI (single output).
    
    Args:
        images: List of PIL.Image objects
        prompt: Edit instruction
        aspect_ratio: Optional aspect ratio
        
    Returns:
        Image bytes
    """
    editor = VertexAIImageEditor()
    return await editor.edit_image_single(images, prompt, aspect_ratio)

