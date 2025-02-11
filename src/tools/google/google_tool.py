"""
Google API integration tool for MCP server.
Provides access to various Google services like Search, Maps, etc.
"""
import os
from typing import Dict, Any, Optional
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleTool:
    MODELS = {
        'default': 'gemini-2.0-pro-exp-02-05',
        'flash': 'gemini-2.0-flash-thinking-exp-01-21'
    }

    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")

        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.MODELS['default'])
        self.flash_model = genai.GenerativeModel(self.MODELS['flash'])

    async def generate_content(self, prompt: str, use_flash: bool = False, **kwargs) -> Dict[str, Any]:
        """
        Generate content using Gemini models.

        Args:
            prompt: The input prompt
            use_flash: Whether to use the flash thinking model
            **kwargs: Additional parameters for the model

        Returns:
            Dictionary containing the generated content
        """
        try:
            model = self.flash_model if use_flash else self.model
            response = model.generate_content(prompt, **kwargs)

            return {
                'status': 'success',
                'content': response.text,
                'model': self.MODELS['flash'] if use_flash else self.MODELS['default']
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Gemini API error: {str(e)}'
            }

    async def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Perform a Google search using the Custom Search API.

        Args:
            query: The search query string
            num_results: Number of results to return (max 10)

        Returns:
            Dictionary containing search results
        """
        try:
            service = build('customsearch', 'v1', developerKey=self.api_key)
            result = service.cse().list(
                q=query,
                cx=os.getenv('GOOGLE_SEARCH_ENGINE_ID'),
                num=min(num_results, 10)
            ).execute()

            return {
                'status': 'success',
                'results': result.get('items', [])
            }
        except HttpError as e:
            return {
                'status': 'error',
                'message': f'Google API error: {str(e)}'
            }

    async def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """
        Get details about a specific place using the Places API.

        Args:
            place_id: The Google Places ID

        Returns:
            Dictionary containing place details
        """
        try:
            service = build('places', 'v1', developerKey=self.api_key)
            result = service.places().details(
                placeId=place_id,
                fields=['name', 'formatted_address', 'rating', 'reviews']
            ).execute()

            return {
                'status': 'success',
                'details': result
            }
        except HttpError as e:
            return {
                'status': 'error',
                'message': f'Google Places API error: {str(e)}'
            }

    async def get_directions(
        self,
        origin: str,
        destination: str,
        mode: str = 'driving'
    ) -> Dict[str, Any]:
        """
        Get directions using the Google Maps Directions API.

        Args:
            origin: Starting point address or coordinates
            destination: Ending point address or coordinates
            mode: Transportation mode (driving, walking, bicycling, transit)

        Returns:
            Dictionary containing directions data
        """
        try:
            service = build('directions', 'v1', developerKey=self.api_key)
            result = service.directions().route(
                origin=origin,
                destination=destination,
                mode=mode
            ).execute()

            return {
                'status': 'success',
                'directions': result
            }
        except HttpError as e:
            return {
                'status': 'error',
                'message': f'Google Directions API error: {str(e)}'
            }