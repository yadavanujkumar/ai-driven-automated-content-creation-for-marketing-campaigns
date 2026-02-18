"""
Initialization module for the `src` package of the AI-Driven Automated Content Creation for Marketing Campaigns project.

This module sets up the package-level imports and initializes any necessary configurations for the project.
"""

import os
import logging

# Configure logging for the package
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("src")

# Package-level constants
PROJECT_NAME = "AI-Driven Automated Content Creation for Marketing Campaigns"
VERSION = "2.0.0"