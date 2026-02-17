from pydantic import BaseModel, Field, HttpUrl, validator
from typing import List, Optional
from datetime import datetime


class CampaignMetadata(BaseModel):
    """
    Schema for campaign metadata.
    """
    campaign_id: str = Field(..., description="Unique identifier for the marketing campaign.")
    campaign_name: str = Field(..., description="Name of the marketing campaign.")
    created_at: datetime = Field(..., description="Timestamp when the campaign was created.")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the campaign was last updated.")
    owner: str = Field(..., description="Owner or creator of the campaign.")
    tags: List[str] = Field(default_factory=list, description="List of tags associated with the campaign.")

    @validator("campaign_name")
    def validate_campaign_name(cls, value):
        if len(value) < 3:
            raise ValueError("Campaign name must be at least 3 characters long.")
        return value


class ContentGenerationRequest(BaseModel):
    """
    Schema for content generation request.
    """
    campaign_id: str = Field(..., description="Unique identifier for the campaign.")
    prompt: str = Field(..., description="Prompt or input text for content generation.")
    tone: Optional[str] = Field("neutral", description="Tone of the generated content (e.g., friendly, professional).")
    length: Optional[int] = Field(500, description="Desired length of the generated content in characters.")
    keywords: List[str] = Field(default_factory=list, description="List of keywords to include in the content.")

    @validator("length")
    def validate_length(cls, value):
        if value <= 0:
            raise ValueError("Length must be a positive integer.")
        return value


class ContentGenerationResponse(BaseModel):
    """
    Schema for content generation response.
    """
    campaign_id: str = Field(..., description="Unique identifier for the campaign.")
    generated_content: str = Field(..., description="The generated content.")
    word_count: int = Field(..., description="Word count of the generated content.")
    created_at: datetime = Field(..., description="Timestamp when the content was generated.")

    @validator("word_count")
    def validate_word_count(cls, value):
        if value <= 0:
            raise ValueError("Word count must be a positive integer.")
        return value


class APIResponse(BaseModel):
    """
    Generic schema for API responses.
    """
    status: str = Field(..., description="Status of the API response (e.g., success, error).")
    message: Optional[str] = Field(None, description="Additional message or information about the response.")
    data: Optional[dict] = Field(None, description="Response data, if applicable.")

    @validator("status")
    def validate_status(cls, value):
        if value not in ["success", "error"]:
            raise ValueError("Status must be either 'success' or 'error'.")
        return value


class CampaignListResponse(BaseModel):
    """
    Schema for a list of campaigns in response.
    """
    campaigns: List[CampaignMetadata] = Field(..., description="List of campaigns.")


class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    """
    error_code: int = Field(..., description="Error code representing the type of error.")
    error_message: str = Field(..., description="Detailed error message.")
    details: Optional[dict] = Field(None, description="Additional details about the error, if available.")