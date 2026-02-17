"""
Initialization module for the `src` package of the AI-Driven Automated Content Creation for Marketing Campaigns project.

This module sets up the package-level imports and initializes any necessary configurations for the project.
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Configure logging for the package
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("src")

# Package-level constants
PROJECT_NAME = "AI-Driven Automated Content Creation for Marketing Campaigns"
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
SUPPORTED_LANGUAGES = ["en", "es", "fr", "de", "it", "pt", "zh", "ja", "ko"]

# Import key modules for easier access at the package level
from .content_generator import ContentGenerator
from .campaign_manager import CampaignManager
from .analytics import Analytics

# Initialize global configurations or services if needed
def initialize():
    """
    Perform any necessary initialization for the package.
    This could include setting up external services, preloading models, etc.
    """
    logger.info(f"Initializing {PROJECT_NAME} package...")
    # Example: Preload AI models or connect to external services
    ContentGenerator.preload_models()
    CampaignManager.setup()
    logger.info(f"{PROJECT_NAME} package initialized successfully.")


# Automatically initialize the package when imported
initialize()