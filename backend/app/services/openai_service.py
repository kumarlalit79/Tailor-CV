import json
from functools import lru_cache
from typing import Any, Literal

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AsyncOpenAI,
    OpenAIError,
    RateLimitError,
)

from app.config.settings import Settings, get_settings

CompletionResponseFormat = Literal["text", "json"]


class OpenAIServiceError(Exception):
    """Raised when the OpenAI service cannot complete a request safely."""


class OpenAIConfigurationError(OpenAIServiceError):
    """Raised when required OpenAI configuration is missing."""


class OpenAIService:
    def __init__(self, settings: Settings, timeout_seconds: float = 60.0) -> None:
        self.settings = settings
        self.timeout_seconds = timeout_seconds
        self._client: AsyncOpenAI | None = None

    @property
    def client(self) -> AsyncOpenAI:
        if not self.settings.openai_api_key:
            raise OpenAIConfigurationError("OPENAI_API_KEY is not configured")

        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self.settings.openai_api_key,
                base_url=self.settings.resolved_openai_base_url,
                timeout=self.timeout_seconds,
            )

        return self._client

    async def create_completion(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        response_format: CompletionResponseFormat = "text",
        model: str | None = None,
        max_tokens: int = 2_000,
        temperature: float = 0.2,
    ) -> str | dict[str, Any]:
        request_body: dict[str, Any] = {
            "model": model or self.settings.openai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if response_format == "json":
            request_body["response_format"] = {"type": "json_object"}

        try:
            completion = await self.client.chat.completions.create(**request_body)
        except APITimeoutError as exc:
            raise OpenAIServiceError("OpenAI request timed out") from exc
        except RateLimitError as exc:
            raise OpenAIServiceError("OpenAI rate limit exceeded") from exc
        except APIConnectionError as exc:
            raise OpenAIServiceError("Unable to connect to OpenAI") from exc
        except APIStatusError as exc:
            raise OpenAIServiceError(f"OpenAI request failed with status {exc.status_code}") from exc
        except OpenAIError as exc:
            raise OpenAIServiceError("OpenAI request failed") from exc
        except Exception as exc:
            raise OpenAIServiceError("Unexpected OpenAI client error") from exc

        if not completion.choices:
            raise OpenAIServiceError("OpenAI returned no choices")

        content = completion.choices[0].message.content
        if not content:
            raise OpenAIServiceError("OpenAI returned an empty response")

        if response_format == "json":
            try:
                parsed = json.loads(content)
            except json.JSONDecodeError as exc:
                raise OpenAIServiceError("OpenAI returned invalid JSON") from exc

            if not isinstance(parsed, dict):
                raise OpenAIServiceError("OpenAI JSON response must be an object")

            return parsed

        return content.strip()


@lru_cache
def get_openai_service() -> OpenAIService:
    return OpenAIService(settings=get_settings())
