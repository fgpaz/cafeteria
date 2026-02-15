#!/usr/bin/env python3
"""
Claude Code LLM Classifier - Sandinas v1.6.0
Supports multiple LLM providers: Groq (primary), ZhipuAI (fallback).
Uses Groq (llama-3.3-70b-versatile) for enhanced prompt context classification.
Falls back to ZhipuAI or regex if APIs are unavailable.
"""
import json
import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union, cast

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env file from plugin directory if it exists
def _load_env_file():
    """Load .env file from plugin directory."""
    script_dir = Path(__file__).parent.parent
    env_file = script_dir / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())

_load_env_file()


class LLMClassifier:
    """LLM-based prompt classifier supporting multiple providers."""

    def __init__(self, api_key: Optional[str] = None):
        # Try Groq first (primary provider), then ZhipuAI (fallback)
        self.provider = None
        self.client = None
        self.model = None
        self.temperature = 0.1
        self.max_tokens = 800
        self.timeout = 10
        self.enabled = False

        # Try Groq first
        if self._init_groq(api_key):
            self.provider = "groq"
        elif self._init_zhipuai(api_key):
            self.provider = "zhipuai"
        else:
            logger.info("No LLM provider available (GROQ_API_KEY or ZHIPUAI_API_KEY not set)")

    def _get_env(self, prefix: str) -> Dict[str, Any]:
        """Get environment variables for a provider prefix."""
        return {
            "api_key": os.environ.get(f"{prefix}_API_KEY"),
            "model": os.environ.get(f"{prefix}_MODEL", self._get_default_model(prefix)),
            "temperature": self._parse_float(os.environ.get(f"{prefix}_TEMPERATURE", "0.1")),
            "max_tokens": int(os.environ.get(f"{prefix}_MAX_TOKENS", "800")),
            "timeout": int(os.environ.get(f"{prefix}_TIMEOUT", "10")),
            "enabled": os.environ.get(f"{prefix}_ENABLED", "true").lower() == "true",
        }

    def _get_default_model(self, prefix: str) -> str:
        """Get default model for provider."""
        if prefix == "GROQ":
            return "llama-3.3-70b-versatile"
        elif prefix == "ZHIPUAI":
            return "glm-4.7"
        return "llama-3.3-70b-versatile"

    def _parse_float(self, value: str) -> float:
        """Parse float from string with error handling."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.1

    def _init_groq(self, api_key: Optional[str] = None) -> bool:
        """Initialize Groq provider."""
        config = self._get_env("GROQ")
        api_key = api_key or config["api_key"]

        if not api_key or not config["enabled"]:
            return False

        try:
            from groq import Groq
            self.client = Groq(api_key=api_key)
            self.model = config["model"]
            self.temperature = config["temperature"]
            self.max_tokens = config["max_tokens"]
            self.timeout = config["timeout"]
            self.enabled = True
            logger.info(f"Groq LLM classifier initialized: model={self.model}, temp={self.temperature}")
            return True
        except ImportError:
            logger.warning("groq package not installed")
            return False
        except Exception as e:
            logger.warning(f"Failed to initialize Groq: {e}")
            return False

    def _init_zhipuai(self, api_key: Optional[str] = None) -> bool:
        """Initialize ZhipuAI provider (fallback)."""
        config = self._get_env("ZHIPUAI")
        api_key = api_key or config["api_key"]

        if not api_key or not config["enabled"]:
            return False

        try:
            from zhipuai import ZhipuAI
            self.client = ZhipuAI(api_key=api_key)
            self.model = config["model"]
            self.temperature = config["temperature"]
            self.max_tokens = config["max_tokens"]
            self.timeout = config["timeout"]
            self.enabled = True
            logger.info(f"ZhipuAI LLM classifier initialized: model={self.model}, temp={self.temperature}")
            return True
        except ImportError:
            logger.warning("zhipuai package not installed")
            return False
        except Exception as e:
            logger.warning(f"Failed to initialize ZhipuAI: {e}")
            return False

    def classify(self, prompt_text: str) -> Dict[str, Any]:
        """
        Classify prompt using LLM.

        Returns:
            {
                "clear_context": bool or None,
                "reasoning": str,
                "missing_context": ["list", "of", "missing", "elements"],
                "suggested_questions": ["question1", "question2"],
                "source": "llm",
                "provider": "groq" or "zhipuai"
            }
        """
        if not self.enabled:
            return self._unavailable_result()

        # Type assertion: when enabled=True, client and model are guaranteed to be set
        assert self.client is not None, "client must be set when enabled=True"
        assert self.model is not None, "model must be set when enabled=True"

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._build_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this prompt:\n\n{prompt_text}"
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=self.timeout
            )

            # Type ignore: Groq library has complex types, but we know this is non-streaming response
            content = response.choices[0].message.content  # type: ignore[attr-defined]
            if content is None:
                content = ""
            result = self._parse_response(content)
            result["provider"] = self.provider
            return result

        except Exception as e:
            logger.error(f"LLM classification failed: {e}")
            return self._unavailable_result()

    def _build_system_prompt(self) -> str:
        return """You are a prompt context analyzer for software development. Analyze the user's prompt and determine if it has sufficient context to proceed.

Check for the Sandinas 4-point context:
1. Project - Which project/codebase?
2. Business Rule - What feature/requirement?
3. Architecture/Flow - What part of the system?
4. Data Model - What entities/fields are involved?

Also check for Functional Requirements:
- Actor: Who is performing the action?
- Inputs: What data is being provided?
- Expected Output: What should happen?
- Acceptance Criteria: How do we know it works?

Respond ONLY with valid JSON:
{
    "clear_context": true/false,
    "reasoning": "Brief explanation",
    "missing_context": ["element1", "element2"],
    "suggested_questions": ["question1?", "question2?"]
}

Rules:
- clear_context=true only if ALL critical information is present
- missing_context: list what Sandinas context elements are missing
- suggested_questions: clarifying questions to ask the user"""

    def _parse_response(self, content: str) -> Dict[str, Any]:
        """Extract JSON from LLM response."""
        # Try direct parse
        try:
            result = json.loads(content)
            result["source"] = "llm"
            return result
        except json.JSONDecodeError:
            pass

        # Try to extract JSON from markdown or mixed content
        start = content.find('{')
        end = content.rfind('}') + 1
        if start >= 0 and end > start:
            try:
                result = json.loads(content[start:end])
                result["source"] = "llm"
                return result
            except json.JSONDecodeError:
                pass

        # Fallback
        return {
            "clear_context": False,
            "reasoning": f"Could not parse LLM response",
            "missing_context": ["technical_details"],
            "suggested_questions": [],
            "source": "llm_error"
        }

    def _unavailable_result(self) -> Dict[str, Any]:
        """Return result when LLM is unavailable."""
        return {
            "clear_context": None,  # None means "use regex fallback"
            "reasoning": "LLM unavailable, using regex-based classification",
            "missing_context": [],
            "suggested_questions": [],
            "source": "unavailable"
        }


# Singleton instance
_classifier: Optional[LLMClassifier] = None


def get_classifier() -> LLMClassifier:
    """Get or create the singleton classifier instance."""
    global _classifier
    if _classifier is None:
        _classifier = LLMClassifier()
    return _classifier


def classify_with_llm(prompt_text: str) -> Dict[str, Any]:
    """Convenience function to classify a prompt."""
    return get_classifier().classify(prompt_text)


# For standalone testing
if __name__ == "__main__":
    # Test prompts
    test_prompts = [
        "modificar auth.py para agregar refresh token",
        "arregla el bug del login",
        "mejorar el sistema de autenticacion",
        "implementar refresh token",
    ]

    classifier = get_classifier()

    for prompt in test_prompts:
        print(f"\nPrompt: {prompt}")
        print("-" * 50)
        result = classifier.classify(prompt)
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Provider: {result.get('provider', 'none')}")
        print(f"Clear: {result.get('clear_context')}")
        print(f"Reasoning: {result.get('reasoning', 'N/A')}")
        if result.get('missing_context'):
            print(f"Missing: {result['missing_context']}")
        if result.get('suggested_questions'):
            print(f"Questions: {result['suggested_questions']}")
