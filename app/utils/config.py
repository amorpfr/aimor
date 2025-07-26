import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    QLOO_API_KEY: str = os.getenv("QLOO_API_KEY", "")
    
    # API Configuration
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    QLOO_API_URL: str = os.getenv("QLOO_API_URL", "https://api.qloo.com/v1")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = int(os.getenv("MAX_REQUESTS_PER_MINUTE", 60))
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", 30))
    
    # Cache Settings
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", 3600))
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    
    # Application
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT == "production"
    
    def validate_required_keys(self) -> dict:
        """Validate that required API keys are present"""
        missing_keys = []
        
        if not self.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        if not self.QLOO_API_KEY:
            missing_keys.append("QLOO_API_KEY")
            
        return {
            "valid": len(missing_keys) == 0,
            "missing_keys": missing_keys
        }

# Create global settings instance
settings = Settings()