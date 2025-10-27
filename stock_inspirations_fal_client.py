"""
Client wrapper for FAL Serverless Stock Image Inspirations endpoint.
"""

import asyncio
from typing import List, Optional, Dict, Any
from logging import Logger
import os


class StockImageInspirationsFalServerless:
    """
    Client for FAL Serverless Stock Image Inspirations endpoint.
    """
    
    def __init__(
        self, 
        logger: Optional[Logger] = None,
        endpoint: Optional[str] = None
    ):
        """
        Initialize the FAL Serverless client.
        
        Args:
            logger: Logger instance (optional)
            endpoint: FAL endpoint URL (e.g., "fal-ai/your-username/stock-image-inspirations")
                     If None, will try to read from FAL_SERVERLESS_INSPIRATIONS_ENDPOINT env var
        """
        # Simple print logging if no logger provided
        self._logger = logger
        
        # Get endpoint from parameter or environment
        self.endpoint = endpoint or os.getenv(
            "FAL_SERVERLESS_INSPIRATIONS_ENDPOINT", 
            "fal-ai/your-username/stock-image-inspirations"  # Default fallback
        )
        
        # Check if fal_client is available
        try:
            import fal_client
            self.fal_available = True
            self._log("info", f"FAL Serverless client initialized for endpoint: {self.endpoint}")
        except ImportError:
            self.fal_available = False
            self._log("error", "fal_client not available. Install with: pip install fal-client")
    
    def _log(self, level: str, message: str):
        """Simple logging helper."""
        if self._logger:
            getattr(self._logger, level)(message)
        else:
            print(f"[{level.upper()}] {message}")
    
    async def generate_inspirations(
        self,
        user_prompt: str,
        style_preferences: Optional[List[str]] = None,
        num_inspirations: int = 3,
        include_keywords: bool = True,
        include_negative_prompts: bool = True,
        target_use_case: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate creative inspirations for stock image generation.
        
        Args:
            user_prompt: User's base prompt or concept for the stock image
            style_preferences: List of style preferences (e.g., 'modern', 'minimalist')
            num_inspirations: Number of inspiration variations to generate (1-10)
            include_keywords: Whether to include searchable keywords
            include_negative_prompts: Whether to include negative prompts
            target_use_case: Target use case (e.g., 'marketing', 'editorial')
            
        Returns:
            Dict containing inspirations and metadata
        """
        if not self.fal_available:
            raise RuntimeError("fal_client not available. Install with: pip install fal-client")
        
        import fal_client
        
        try:
            # Prepare arguments
            arguments = {
                "user_prompt": user_prompt,
                "num_inspirations": num_inspirations,
                "include_keywords": include_keywords,
                "include_negative_prompts": include_negative_prompts,
            }
            
            if style_preferences:
                arguments["style_preferences"] = style_preferences
            
            if target_use_case:
                arguments["target_use_case"] = target_use_case
            
            # Call FAL Serverless endpoint
            self._log("info", f"Calling FAL Serverless endpoint: {self.endpoint}")
            self._log("info", f"User prompt: {user_prompt}")
            
            handler = await fal_client.submit_async(
                self.endpoint,
                arguments=arguments,
            )
            
            # Wait for completion
            async for event in handler.iter_events(with_logs=True):
                if hasattr(event, 'message'):
                    self._log("debug", f"FAL Event: {event.message}")
            
            result = await handler.get()
            
            # Log results
            self._log("info", f"FAL Serverless processing time: {result.get('processing_time', 'N/A')}s")
            self._log("info", f"Generated {len(result.get('inspirations', []))} inspirations")
            
            return result
            
        except Exception as e:
            error_msg = f"FAL Serverless inspiration generation failed: {e}"
            self._log("error", error_msg)
            raise RuntimeError(error_msg)
    
    async def generate_inspirations_with_retry(
        self,
        user_prompt: str,
        max_retries: int = 3,
        timeout: int = 30,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate inspirations with retry logic.
        
        Args:
            user_prompt: User's base prompt or concept
            max_retries: Maximum retry attempts
            timeout: Timeout in seconds per attempt
            **kwargs: Additional arguments for generate_inspirations()
            
        Returns:
            Dict containing inspirations and metadata
        """
        attempt = 0
        last_error = None
        
        while attempt < max_retries:
            attempt += 1
            try:
                self._log("info", f"Attempt {attempt}/{max_retries}")
                result = await asyncio.wait_for(
                    self.generate_inspirations(
                        user_prompt=user_prompt,
                        **kwargs
                    ),
                    timeout=timeout
                )
                return result
                
            except asyncio.TimeoutError:
                self._log("error", f"Request timed out after {timeout}s on attempt {attempt}/{max_retries}")
                last_error = RuntimeError(f"Request timed out after {timeout}s")
                continue
                
            except Exception as e:
                self._log("error", f"Request failed on attempt {attempt}/{max_retries}: {e}")
                last_error = e
                continue
        
        self._log("error", f"All {max_retries} attempts failed")
        if last_error:
            raise last_error
        else:
            raise RuntimeError("Request failed after all retries")


# Convenience function
async def generate_stock_image_inspirations(
    user_prompt: str,
    endpoint: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience function to generate inspirations without creating a client instance.
    
    Args:
        user_prompt: User's base prompt or concept
        endpoint: FAL endpoint URL (optional)
        **kwargs: Additional arguments for generate_inspirations()
        
    Returns:
        Dict containing inspirations and metadata
    """
    client = StockImageInspirationsFalServerless(endpoint=endpoint)
    return await client.generate_inspirations(user_prompt=user_prompt, **kwargs)

