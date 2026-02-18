"""
Custom Exception Classes
Provides specific exception types for better error handling
"""

from fastapi import HTTPException, status


class ContentGenerationError(HTTPException):
    """Exception raised when content generation fails"""
    def __init__(self, detail: str = "Content generation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class InvalidContentParametersError(HTTPException):
    """Exception raised when content parameters are invalid"""
    def __init__(self, detail: str = "Invalid content parameters"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class ContentNotFoundError(HTTPException):
    """Exception raised when content is not found"""
    def __init__(self, content_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content with ID '{content_id}' not found"
        )


class CampaignNotFoundError(HTTPException):
    """Exception raised when campaign is not found"""
    def __init__(self, campaign_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign with ID '{campaign_id}' not found"
        )


class RateLimitExceededError(HTTPException):
    """Exception raised when rate limit is exceeded"""
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            headers={"Retry-After": "60"}
        )


class AnalyticsError(HTTPException):
    """Exception raised when analytics generation fails"""
    def __init__(self, detail: str = "Analytics generation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class InsufficientDataError(HTTPException):
    """Exception raised when there's insufficient data for analysis"""
    def __init__(self, detail: str = "Insufficient data for analysis"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class CacheError(Exception):
    """Exception raised when cache operations fail"""
    pass


class APIKeyError(HTTPException):
    """Exception raised when API key is invalid or missing"""
    def __init__(self, detail: str = "Invalid or missing API key"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )
