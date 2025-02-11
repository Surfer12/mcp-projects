"""
Anthropic API integration module for enhanced AI capabilities.
"""
import os
from typing import Any, Dict, List, Optional
from unittest.mock import patch

import anthropic
from dotenv import load_dotenv


class AnthropicTool:
    def test_error_handling(self):
        """Test error handling in the tool."""
        # Simulate API error
        with patch('anthropic.Client') as mock_anthropic_client:
            mock_anthropic_client.return_value.messages.create.side_effect = Exception(
                "API Error"
            )

            # Test error handling in analyze_code
            result = self.analyze_code("Test code")
            assert result["success"] is False
            assert "error" in result

    def __init__(self):
        """Initialize the Anthropic tool with API configuration."""
        load_dotenv()
        self.client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
        self.model = "claude-3-opus-20240229"
        self.max_tokens = 4096

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response using the Anthropic API.

        Args:
            prompt: The user's input prompt
            system_prompt: Optional system prompt to guide the model's behavior
            temperature: Controls randomness in the response (0.0 to 1.0)
            max_tokens: Maximum number of tokens in the response

        Returns:
            Generated response text
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature,
                system=system_prompt
                if system_prompt is not None
                else anthropic.HUMAN_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            # Access content safely using type checking
            if message.content and len(message.content) > 0:
                content = message.content[0]
                return str(getattr(content, "text", ""))
            return ""
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return ""

    def analyze_code(
        self,
        code: str,
        analysis_type: str = "general",
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze code using the Anthropic API.

        Args:
            code: The code to analyze
            analysis_type: Type of analysis (e.g., "general", "security", "performance")
            context: Additional context for the analysis

        Returns:
            Dictionary containing analysis results
        """
        system_prompt = (
            "You are a code analysis expert. "
            f"Analyze the provided code focusing on {analysis_type} aspects.\n"
            "If context is provided, consider it in your analysis.\n"
            "Provide structured feedback including:\n"
            "1. Key observations\n"
            "2. Potential issues\n"
            "3. Improvement suggestions"
        )

        prompt = (
            "Code to analyze:\n"
            "```\n"
            f"{code}\n"
            "```\n\n"
            f"{f'Additional context: {context}' if context else ''}\n\n"
            f"Please provide a detailed analysis focusing on {analysis_type} aspects."
        )

        try:
            response = self.generate_response(prompt, system_prompt, temperature=0.3)
            # Parse the response into a structured format
            analysis = {
                "analysis_type": analysis_type,
                "response": response,
                "success": True,
            }
            return analysis
        except Exception as e:
            return {"analysis_type": analysis_type, "error": str(e), "success": False}

    def enhance_documentation(
        self, code: str, doc_style: str = "google", include_examples: bool = True
    ) -> str:
        """
        Enhance code documentation using the Anthropic API.

        Args:
            code: The code to document
            doc_style: Documentation style (e.g., "google", "numpy", "sphinx")
            include_examples: Whether to include usage examples

        Returns:
            Documented code as a string
        """
        example_text = "Include practical usage examples." if include_examples else ""
        system_prompt = (
            "You are a documentation expert. "
            "Generate comprehensive documentation for the provided code "
            f"following the {doc_style} style guide. {example_text}\n"
            "Focus on clarity, completeness, and adherence to documentation standards."
        )

        example_prompt = (
            "Include clear examples demonstrating the code usage."
            if include_examples
            else ""
        )
        prompt = (
            "Code to document:\n"
            "```\n"
            f"{code}\n"
            "```\n\n"
            f"Please provide enhanced documentation following the {doc_style} "
            f"style guide.\n{example_prompt}"
        )

        try:
            return self.generate_response(prompt, system_prompt, temperature=0.2)
        except Exception as e:
            print(f"Error enhancing documentation: {str(e)}")
            return code

    def suggest_improvements(
        self, code: str, focus_areas: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Suggest code improvements using the Anthropic API.

        Args:
            code: The code to improve
            focus_areas: Specific areas to focus on
                (e.g., ["performance", "readability", "security"])

        Returns:
            List of suggested improvements with explanations
        """
        areas = focus_areas or ["general", "performance", "readability", "security"]
        system_prompt = """
        You are a code improvement expert. Analyze the code and suggest specific,
        actionable improvements. For each suggestion, provide:
        1. A clear description of the improvement
        2. The rationale behind it
        3. Example implementation if applicable
        """

        prompt = f"""
        Code to improve:
        ```
        {code}
        ```

        Please suggest improvements focusing on the following areas:
        {', '.join(areas)}

        Provide specific, actionable suggestions with examples where appropriate.
        """

        try:
            response = self.generate_response(prompt, system_prompt, temperature=0.4)
            # Return the response as a single suggestion if not empty
            return [{"description": response, "area": "general"}] if response else []
        except Exception as e:
            print(f"Error suggesting improvements: {str(e)}")
            return []
