"""
Client wrapper for FAL Serverless Stock Image Inspirations endpoint.
Applies fixed inspirations to images using FAL models.
"""

import asyncio
from typing import List, Optional, Dict, Any
from logging import Logger
import os
from inspirations_config import (
    get_inspiration_config,
    list_inspiration_types,
    validate_input_images
)


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
    
    def list_inspirations(self) -> List[str]:
        """List all available inspiration types."""
        return list_inspiration_types()
    
    def get_inspiration_info(self, inspiration_type: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific inspiration type."""
        return get_inspiration_config(inspiration_type)
    
    async def apply_inspiration(
        self,
        inspiration_type: str,
        image_urls: List[str],
        custom_params: Optional[Dict[str, Any]] = None,
        output_format: str = "png"
    ) -> Dict[str, Any]:
        """
        Apply a fixed inspiration to input images.
        
        Args:
            inspiration_type: Type of inspiration (variations, change_pose, fuse_images, etc.)
            image_urls: List of input image URLs (1-5 images depending on inspiration)
            custom_params: Optional custom parameters to override defaults
            output_format: Output image format (png, jpeg, webp)
            
        Returns:
            Dict containing generated images and metadata
        """
        if not self.fal_available:
            raise RuntimeError("fal_client not available. Install with: pip install fal-client")
        
        # Validate inspiration type
        if inspiration_type not in list_inspiration_types():
            available = list_inspiration_types()
            raise ValueError(
                f"Unknown inspiration type: {inspiration_type}. "
                f"Available: {', '.join(available)}"
            )
        
        # Validate input image count
        if not validate_input_images(inspiration_type, len(image_urls)):
            config = get_inspiration_config(inspiration_type)
            min_imgs = config.get("min_input_images", 1)
            max_imgs = config.get("max_input_images", 1)
            raise ValueError(
                f"Inspiration '{inspiration_type}' requires {min_imgs}-{max_imgs} "
                f"input images, but {len(image_urls)} were provided"
            )
        
        import fal_client
        
        try:
            # Prepare arguments
            arguments = {
                "inspiration_type": inspiration_type,
                "image_urls": image_urls,
                "output_format": output_format,
            }
            
            if custom_params:
                arguments["custom_params"] = custom_params
            
            # Call FAL Serverless endpoint
            self._log("info", f"Calling FAL Serverless endpoint: {self.endpoint}")
            self._log("info", f"Inspiration type: {inspiration_type}")
            self._log("info", f"Input images: {len(image_urls)}")
            
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
            self._log("info", f"Generated {result.get('output_image_count', 0)} images")
            
            return result
            
        except Exception as e:
            error_msg = f"FAL Serverless inspiration application failed: {e}"
            self._log("error", error_msg)
            raise RuntimeError(error_msg)
    
    async def apply_inspiration_with_retry(
        self,
        inspiration_type: str,
        image_urls: List[str],
        max_retries: int = 3,
        timeout: int = 60,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Apply inspiration with retry logic.
        
        Args:
            inspiration_type: Type of inspiration to apply
            image_urls: List of input image URLs
            max_retries: Maximum retry attempts
            timeout: Timeout in seconds per attempt
            **kwargs: Additional arguments for apply_inspiration()
            
        Returns:
            Dict containing generated images and metadata
        """
        attempt = 0
        last_error = None
        
        while attempt < max_retries:
            attempt += 1
            try:
                self._log("info", f"Attempt {attempt}/{max_retries}")
                result = await asyncio.wait_for(
                    self.apply_inspiration(
                        inspiration_type=inspiration_type,
                        image_urls=image_urls,
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
async def apply_stock_image_inspiration(
    inspiration_type: str,
    image_urls: List[str],
    endpoint: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Convenience function to apply inspiration without creating a client instance.
    
    Args:
        inspiration_type: Type of inspiration to apply
        image_urls: List of input image URLs
        endpoint: FAL endpoint URL (optional)
        **kwargs: Additional arguments for apply_inspiration()
        
    Returns:
        Dict containing generated images and metadata
    """
    client = StockImageInspirationsFalServerless(endpoint=endpoint)
    return await client.apply_inspiration(
        inspiration_type=inspiration_type,
        image_urls=image_urls,
        **kwargs
    )
