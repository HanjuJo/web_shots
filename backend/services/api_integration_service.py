import openai
from huggingface_hub import InferenceClient
from typing import Dict, Any
import requests
import os
import json

class APIIntegrationService:
    def __init__(self):
        """Initialize API clients"""
        # OpenAI setup
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Hugging Face setup
        self.hf_client = InferenceClient(token=os.getenv('HUGGINGFACE_API_KEY'))
        
        # Stability AI setup
        self.stability_api_key = os.getenv('STABILITY_API_KEY')
        
    def generate_text(self, prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
        """Generate text using OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant for content creators."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return {
                "success": True,
                "text": response.choices[0].message.content,
                "usage": response.usage
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def generate_image(self, prompt: str, size: str = "1024x1024") -> Dict[str, Any]:
        """Generate image using Stability AI API"""
        try:
            response = requests.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.stability_api_key}"
                },
                json={
                    "text_prompts": [{"text": prompt}],
                    "cfg_scale": 7,
                    "height": int(size.split('x')[1]),
                    "width": int(size.split('x')[0]),
                    "samples": 1,
                    "steps": 30,
                }
            )
            if response.status_code == 200:
                return {
                    "success": True,
                    "images": response.json()["artifacts"]
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment using Hugging Face API"""
        try:
            response = self.hf_client.text_classification(
                text,
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            return {
                "success": True,
                "sentiment": response[0],
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
            
    def generate_video_script(self, topic: str, duration: str = "short") -> Dict[str, Any]:
        """Generate video script using OpenAI API"""
        try:
            prompt = f"""Create a video script for a {duration} video about {topic}.
            Include:
            1. Opening hook
            2. Main points
            3. Call to action
            4. Estimated timing for each section"""
            
            response = self.generate_text(prompt)
            if response["success"]:
                return {
                    "success": True,
                    "script": response["text"],
                    "usage": response["usage"]
                }
            else:
                return response
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
