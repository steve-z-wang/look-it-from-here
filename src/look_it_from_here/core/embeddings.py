from typing import List, Optional
import os
from abc import ABC, abstractmethod

# Try to load .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, use environment variables only


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    def create_embedding(self, text: str) -> List[float]:
        """Create embedding vector from text."""
        pass

    @abstractmethod
    def get_dimension(self) -> int:
        """Get the dimension of embeddings from this provider."""
        pass


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embedding provider using text-embedding-3-large."""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.model = model or os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-large')
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')

        # Model dimensions
        self._dimensions = {
            "text-embedding-3-large": 3072,
            "text-embedding-3-small": 1536,
            "text-embedding-ada-002": 1536
        }

        # Try to import OpenAI
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key) if self.api_key else None
            self._openai_available = True
        except ImportError:
            self.client = None
            self._openai_available = False

    def create_embedding(self, text: str) -> List[float]:
        """Create embedding using OpenAI API."""
        if not self._openai_available:
            raise RuntimeError("OpenAI package not available. Install with: pip install openai")

        if not self.client:
            raise RuntimeError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable.")

        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")

    def get_dimension(self) -> int:
        """Get embedding dimension for the current model."""
        return self._dimensions.get(self.model, 3072)


class DummyEmbeddingProvider(EmbeddingProvider):
    """Dummy embedding provider for testing and fallback."""

    def __init__(self, dimension: int = 3072):
        self.dimension = dimension

    def create_embedding(self, text: str) -> List[float]:
        """Create dummy embedding vector."""
        # Simple hash-based pseudo-embedding for consistent results
        hash_val = hash(text) % 1000000
        base_val = hash_val / 1000000.0
        return [base_val + (i * 0.001) for i in range(self.dimension)]

    def get_dimension(self) -> int:
        """Get embedding dimension."""
        return self.dimension


class Embedder:
    """Main class for creating embeddings with different providers."""

    def __init__(self, provider: Optional[EmbeddingProvider] = None):
        """
        Initialize embedder.

        Args:
            provider: Embedding provider to use. If None, will auto-select based on availability.
        """
        if provider:
            self.provider = provider
        else:
            # Auto-select provider
            try:
                self.provider = OpenAIEmbeddingProvider()
                # Test if OpenAI is actually available
                if not self.provider._openai_available or not self.provider.client:
                    raise RuntimeError("OpenAI not available")
                print("✅ Using OpenAI embedding provider")
            except (ImportError, RuntimeError):
                print("⚠️ OpenAI not available, using dummy embeddings")
                self.provider = DummyEmbeddingProvider()

    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding vector from text.

        Args:
            text: Input text to embed

        Returns:
            Embedding vector
        """
        return self.provider.create_embedding(text)

    def get_dimension(self) -> int:
        """Get the dimension of embeddings from current provider."""
        return self.provider.get_dimension()

    def get_provider_name(self) -> str:
        """Get the name of the current provider."""
        return self.provider.__class__.__name__