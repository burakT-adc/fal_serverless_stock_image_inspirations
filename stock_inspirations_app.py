"""
FAL.ai Serverless Deployment for Stock Image Inspirations Generator
"""

import os
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
import fal


# Input Model
class StockImageInspirationsInput(BaseModel):
    user_prompt: str = Field(
        default="professional business meeting in modern office",
        description="User's base prompt or concept for the stock image",
        min_length=1,
        max_length=500
    )
    style_preferences: Optional[List[str]] = Field(
        default=None,
        description="List of style preferences (e.g., 'modern', 'minimalist', 'vintage')",
        max_length=10
    )
    num_inspirations: int = Field(
        default=3,
        description="Number of inspiration variations to generate",
        ge=1,
        le=10
    )
    include_keywords: bool = Field(
        default=True,
        description="Whether to include searchable keywords for each inspiration"
    )
    include_negative_prompts: bool = Field(
        default=True,
        description="Whether to include negative prompts for better image generation"
    )
    target_use_case: Optional[str] = Field(
        default=None,
        description="Target use case (e.g., 'marketing', 'editorial', 'social media')"
    )


# Output Models
class InspirationItem(BaseModel):
    title: str = Field(description="Creative title for the inspiration")
    prompt: str = Field(description="Detailed, optimized prompt for image generation")
    negative_prompt: Optional[str] = Field(default=None, description="Negative prompt to avoid unwanted elements")
    keywords: List[str] = Field(description="Relevant keywords for searchability")
    style_tags: List[str] = Field(description="Style categorization tags")


class StockImageInspirationsOutput(BaseModel):
    inspirations: List[InspirationItem] = Field(description="List of generated inspirations")
    original_prompt: str = Field(description="The original user prompt")
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
    request_timeout = 30
    startup_timeout = 30
    concurrency_buffer = 0
    concurrency_buffer_perc = 0
    
    host_kwargs = {
        "keep_alive": 0,
        "request_timeout": 30,
        "startup_timeout": 30,
    }
    
    requirements = [
        "openai>=1.0.0",
        "python-dotenv",
        "pydantic>=2.0.0",
        "orjson>=3.9.0",
    ]
    
    def setup(self):
        """Initialize any required resources."""
        print("INFO: Stock Image Inspirations application setup completed")
    
    @fal.endpoint("/")
    async def generate_inspirations(
        self, 
        input: StockImageInspirationsInput
    ) -> StockImageInspirationsOutput:
        """Generates creative inspirations for stock image generation."""
        import time
        from openai import OpenAI
        import json
        
        request_id = str(uuid.uuid4())
        start_time = time.time()
        warnings = []
        
        try:
            print(f"[{request_id}] Starting inspiration generation request")
            print(f"[{request_id}] User prompt: {input.user_prompt}")
            
            # Check OpenAI API key
            openai_key = os.getenv("OPENAI_API_KEY")
            if not openai_key:
                raise ValueError("OPENAI_API_KEY not set in environment")
            
            # Build the system prompt
            system_prompt = build_system_prompt(
                num_inspirations=input.num_inspirations,
                include_keywords=input.include_keywords,
                include_negative_prompts=input.include_negative_prompts,
                target_use_case=input.target_use_case
            )
            
            # Build the user message
            user_message = build_user_message(
                user_prompt=input.user_prompt,
                style_preferences=input.style_preferences,
                target_use_case=input.target_use_case
            )
            
            print(f"[{request_id}] Calling OpenAI API")
            
            # Call OpenAI
            client = OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=2000,
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            response_text = response.choices[0].message.content
            
            # Parse JSON response
            print(f"[{request_id}] Parsing response")
            response_json = json.loads(response_text)
            
            # Validate and structure the response
            inspirations = []
            for item in response_json.get("inspirations", []):
                inspiration = InspirationItem(
                    title=item.get("title", "Untitled"),
                    prompt=item.get("prompt", ""),
                    negative_prompt=item.get("negative_prompt") if input.include_negative_prompts else None,
                    keywords=item.get("keywords", []) if input.include_keywords else [],
                    style_tags=item.get("style_tags", [])
                )
                inspirations.append(inspiration)
            
            processing_time = time.time() - start_time
            print(f"[{request_id}] Completed in {processing_time:.2f}s")
            print(f"[{request_id}] Generated {len(inspirations)} inspirations")
            
            return StockImageInspirationsOutput(
                inspirations=inspirations,
                original_prompt=input.user_prompt,
                processing_time=processing_time,
                request_id=request_id,
                success=True,
                warnings=warnings if warnings else None
            )
        
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"[{request_id}] Error: {str(e)}")
            
            return StockImageInspirationsOutput(
                inspirations=[],
                original_prompt=input.user_prompt,
                processing_time=processing_time,
                request_id=request_id,
                success=False,
                warnings=[f"Request failed: {str(e)}"]
            )


# Helper functions
def build_system_prompt(
    num_inspirations: int,
    include_keywords: bool,
    include_negative_prompts: bool,
    target_use_case: Optional[str]
) -> str:
    """Build the system prompt for OpenAI."""
    
    base_prompt = f"""You are an expert stock photography curator and prompt engineer specializing in AI image generation.

Your task is to generate {num_inspirations} creative, diverse inspirations based on the user's concept. Each inspiration should:
1. Have a catchy, descriptive title
2. Include a detailed, optimized prompt for AI image generation (FLUX, Stable Diffusion, etc.)
3. Be commercially viable as a stock image
4. Include specific details about lighting, composition, mood, and technical aspects
"""
    
    if target_use_case:
        base_prompt += f"\n5. Be optimized for {target_use_case} use cases"
    
    if include_keywords:
        base_prompt += "\n6. Include 5-10 searchable keywords that would help people find this image in a stock library"
    
    if include_negative_prompts:
        base_prompt += "\n7. Include a negative prompt listing elements to avoid (e.g., 'blurry, low quality, distorted')"
    
    json_structure = {
        "inspirations": [
            {
                "title": "Creative title for the image concept",
                "prompt": "Detailed prompt for image generation...",
                "style_tags": ["tag1", "tag2", "tag3"]
            }
        ]
    }
    
    if include_keywords:
        json_structure["inspirations"][0]["keywords"] = ["keyword1", "keyword2", "keyword3"]
    
    if include_negative_prompts:
        json_structure["inspirations"][0]["negative_prompt"] = "Elements to avoid..."
    
    base_prompt += f"\n\nReturn your response as a JSON object with this structure:\n{json.dumps(json_structure, indent=2)}"
    base_prompt += "\n\nMake each inspiration unique and distinct from the others. Focus on commercial viability and visual appeal."
    
    return base_prompt


def build_user_message(
    user_prompt: str,
    style_preferences: Optional[List[str]],
    target_use_case: Optional[str]
) -> str:
    """Build the user message for OpenAI."""
    
    message = f"Base concept: {user_prompt}"
    
    if style_preferences:
        message += f"\n\nStyle preferences: {', '.join(style_preferences)}"
    
    if target_use_case:
        message += f"\n\nTarget use case: {target_use_case}"
    
    message += "\n\nGenerate creative, diverse inspirations that would work well as professional stock images."
    
    return message


# For local testing
if __name__ == "__main__":
    print("Stock Image Inspirations FAL Serverless App")
    print("This file should be deployed using: fal deploy stock_inspirations_app.py")

