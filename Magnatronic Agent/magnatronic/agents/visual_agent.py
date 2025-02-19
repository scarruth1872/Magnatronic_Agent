from magnatronic.core.agent import Agent
from magnatronic.core.tasks import Task
from typing import Dict, Any, Optional
import requests
import io
from PIL import Image

class VisualAgent(Agent):
    def __init__(self):
        super().__init__("visual_agent")
        self.supported_models = ["dall-e", "stable-diffusion"]
        self.image_size = (1024, 1024)
        self.default_model = "dall-e"

    async def generate_image(self, prompt: str, model: Optional[str] = None) -> bytes:
        """Generate an image based on the given prompt using the specified model."""
        model = model or self.default_model
        if model not in self.supported_models:
            raise ValueError(f"Unsupported model: {model}")
        
        if model == "dall-e":
            try:
                # Make API call to DALL-E
                # Note: In production, use environment variables for API key
                response = requests.post(
                    "https://api.openai.com/v1/images/generations",
                    headers={
                        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "prompt": prompt,
                        "n": 1,
                        "size": f"{self.image_size[0]}x{self.image_size[1]}"
                    }
                )
                response.raise_for_status()
                image_url = response.json()["data"][0]["url"]
                
                # Download the generated image
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                return image_response.content
            except Exception as e:
                raise RuntimeError(f"Failed to generate image: {str(e)}")
        elif model == "stable-diffusion":
            # TODO: Implement Stable Diffusion API integration
            raise NotImplementedError("Stable Diffusion integration not implemented yet")
        
        return b""  # Return image bytes

    async def create_design(self, design_type: str, specifications: Dict[str, Any]) -> bytes:
        """Create a design based on the given specifications."""
        # TODO: Implement design creation logic
        return b""

    async def style_transfer(self, content_image: bytes, style_image: bytes) -> bytes:
        """Apply style transfer from style_image to content_image."""
        try:
            # Convert bytes to PIL Images
            content = Image.open(io.BytesIO(content_image))
            style = Image.open(io.BytesIO(style_image))
            
            # Resize style image to match content image size
            style = style.resize(content.size)
            
            # Convert images to RGBA if they aren't already
            content = content.convert('RGBA')
            style = style.convert('RGBA')
            
            # Simple alpha blending for demonstration
            # In production, use a proper neural style transfer model
            blended = Image.blend(content, style, 0.5)
            
            # Convert back to bytes
            output = io.BytesIO()
            blended.save(output, format='PNG')
            return output.getvalue()
        except Exception as e:
            raise RuntimeError(f"Failed to apply style transfer: {str(e)}")

    async def process_task(self, task: Task) -> Any:
        """Process incoming tasks based on their type."""
        task_type = task.task_type
        task_data = task.data

        if task_type == "generate_image":
            return await self.generate_image(
                prompt=task_data["prompt"],
                model=task_data.get("model")
            )
        elif task_type == "create_design":
            return await self.create_design(
                design_type=task_data["design_type"],
                specifications=task_data["specifications"]
            )
        elif task_type == "style_transfer":
            return await self.style_transfer(
                content_image=task_data["content_image"],
                style_image=task_data["style_image"]
            )
        else:
            raise ValueError(f"Unsupported task type: {task_type}")