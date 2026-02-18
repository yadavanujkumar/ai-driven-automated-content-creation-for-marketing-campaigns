from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from typing import List, Optional, Dict
import uuid
import random
from pydantic import BaseModel, Field
import re
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.content_analytics import ContentAnalytics
from services.cache_service import content_cache
from utils.exceptions import (
    ContentNotFoundError,
    CampaignNotFoundError,
    ContentGenerationError,
    InsufficientDataError
)

# Router for content routes
content_router = APIRouter()

# Initialize analytics service
analytics_service = ContentAnalytics()

# Mock database (in-memory for demonstration purposes)
campaigns_db = {}
content_db = {}

# Enhanced Pydantic models
class ContentGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="Content generation prompt")
    tone: Optional[str] = Field("neutral", description="Tone of the content")
    length: Optional[int] = Field(250, ge=1, le=5000, description="Desired content length")
    keywords: Optional[List[str]] = Field(default_factory=list, description="Keywords to include")
    platform: Optional[str] = Field(None, description="Target platform (e.g., Twitter, LinkedIn)")

class ContentResponse(BaseModel):
    id: str
    content: str
    created_at: datetime
    quality_score: float
    seo_score: Optional[float] = None
    sentiment: Optional[str] = None

class CampaignCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, description="Campaign name")
    description: Optional[str] = Field("", description="Campaign description")
    content_ids: Optional[List[str]] = Field(default_factory=list, description="Associated content IDs")
    target_audience: Optional[str] = Field(None, description="Target audience")

class CampaignResponse(BaseModel):
    id: str
    name: str
    description: str
    content_ids: List[str]
    created_at: datetime
    target_audience: Optional[str] = None

class SentimentAnalysisResult(BaseModel):
    sentiment: str
    confidence: float

# Enhanced helper functions
def calculate_quality_score(content: str, keywords: List[str] = None) -> float:
    """Calculate content quality score based on various factors"""
    score = 50.0  # Base score
    
    # Length factor
    word_count = len(content.split())
    if 50 <= word_count <= 300:
        score += 20
    elif word_count > 300:
        score += 10
    
    # Readability factor (simple heuristic)
    avg_word_length = sum(len(word) for word in content.split()) / max(word_count, 1)
    if 4 <= avg_word_length <= 6:
        score += 15
    
    # Keyword presence
    if keywords:
        keywords_found = sum(1 for kw in keywords if kw.lower() in content.lower())
        score += min(keywords_found * 5, 15)
    
    return min(score, 100.0)

def calculate_seo_score(content: str, keywords: List[str] = None) -> float:
    """Calculate SEO score based on keyword density and other factors"""
    if not keywords:
        return 50.0
    
    content_lower = content.lower()
    total_words = len(content.split())
    keyword_count = sum(content_lower.count(kw.lower()) for kw in keywords)
    
    # Ideal keyword density is 1-3%
    keyword_density = (keyword_count / max(total_words, 1)) * 100
    
    if 1 <= keyword_density <= 3:
        return 90.0
    elif keyword_density < 1:
        return 60.0
    else:
        return 70.0

def analyze_sentiment(content: str) -> SentimentAnalysisResult:
    """Simple sentiment analysis based on keywords"""
    positive_words = ['great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'best', 'perfect']
    negative_words = ['bad', 'terrible', 'awful', 'worst', 'hate', 'poor', 'disappointing']
    
    content_lower = content.lower()
    positive_count = sum(1 for word in positive_words if word in content_lower)
    negative_count = sum(1 for word in negative_words if word in content_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
        confidence = min(positive_count * 0.3, 0.95)
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = min(negative_count * 0.3, 0.95)
    else:
        sentiment = "neutral"
        confidence = 0.5
    
    return SentimentAnalysisResult(sentiment=sentiment, confidence=confidence)

def generate_ai_content(prompt: str, tone: str, length: int, keywords: List[str] = None, platform: str = None) -> str:
    """Enhanced AI content generation with platform-specific formatting"""
    # Base content templates
    sample_responses = [
        f"{prompt} - A captivating and engaging message tailored for your audience.",
        f"{prompt} - A professional and concise message to drive conversions.",
        f"{prompt} - A creative and innovative approach to marketing your product.",
        f"{prompt} - Discover the power of exceptional marketing that resonates.",
        f"{prompt} - Transform your brand story with compelling, audience-focused content."
    ]
    
    base_content = random.choice(sample_responses)
    
    # Add keywords naturally if provided
    if keywords:
        keyword_phrase = " Focus on: " + ", ".join(keywords[:3])
        base_content += keyword_phrase
    
    # Platform-specific formatting
    if platform:
        platform_lower = platform.lower()
        if platform_lower == "twitter":
            base_content = base_content[:280]  # Twitter character limit
            base_content += " #marketing #content"
        elif platform_lower == "linkedin":
            base_content += "\n\nLet's connect and discuss how this can benefit your business."
        elif platform_lower == "instagram":
            base_content += "\n\n📸✨ #marketing #creative #engagement"
    
    return base_content[:length]

# Route: Generate AI-driven marketing content
@content_router.post("/generate", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def generate_content(request: ContentGenerateRequest):
    """
    Generate AI-driven marketing content with quality scoring and sentiment analysis.
    Results are cached to improve performance for repeated requests.
    """
    try:
        # Check cache first
        cached_result = content_cache.get_content(
            request.prompt,
            request.tone,
            request.length,
            request.keywords,
            request.platform
        )
        
        if cached_result:
            # Return cached content with cache indicator
            cached_result['from_cache'] = True
            return ContentResponse(**cached_result)
        
        # Generate new content
        generated_content = generate_ai_content(
            request.prompt, 
            request.tone, 
            request.length,
            request.keywords,
            request.platform
        )
        content_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        # Calculate scores
        quality_score = calculate_quality_score(generated_content, request.keywords)
        seo_score = calculate_seo_score(generated_content, request.keywords)
        sentiment_result = analyze_sentiment(generated_content)
        
        # Save to mock content database
        content_db[content_id] = {
            'id': content_id,
            'prompt': request.prompt,
            'tone': request.tone,
            'length': request.length,
            'content': generated_content,
            'created_at': timestamp,
            'quality_score': quality_score,
            'seo_score': seo_score,
            'sentiment': sentiment_result.sentiment,
            'keywords': request.keywords,
            'platform': request.platform
        }

        response_data = {
            'id': content_id,
            'content': generated_content,
            'created_at': timestamp,
            'quality_score': quality_score,
            'seo_score': seo_score,
            'sentiment': sentiment_result.sentiment
        }
        
        # Cache the result
        content_cache.cache_content(
            request.prompt,
            request.tone,
            request.length,
            response_data,
            request.keywords,
            request.platform
        )

        return ContentResponse(**response_data)
    except Exception as e:
        raise ContentGenerationError(detail=f"Content generation failed: {str(e)}")

# Route: Retrieve content by ID
@content_router.get("/content/{content_id}", response_model=Dict)
async def get_content(content_id: str):
    """
    Retrieve generated content by ID
    """
    content = content_db.get(content_id)
    if not content:
        raise ContentNotFoundError(content_id)
    return content

# Route: Get sentiment analysis for existing content
@content_router.get("/content/{content_id}/sentiment", response_model=SentimentAnalysisResult)
async def get_content_sentiment(content_id: str):
    """
    Get sentiment analysis for existing content
    """
    content = content_db.get(content_id)
    if not content:
        raise ContentNotFoundError(content_id)
    
    return analyze_sentiment(content['content'])

# Route: Create a new campaign
@content_router.post("/campaigns", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(request: CampaignCreateRequest):
    """
    Create a new marketing campaign
    """
    campaign_id = str(uuid.uuid4())
    timestamp = datetime.utcnow()
    
    # Save to mock campaigns database
    campaigns_db[campaign_id] = {
        'id': campaign_id,
        'name': request.name,
        'description': request.description,
        'content_ids': request.content_ids,
        'created_at': timestamp,
        'target_audience': request.target_audience
    }

    return CampaignResponse(
        id=campaign_id,
        name=request.name,
        description=request.description,
        content_ids=request.content_ids,
        created_at=timestamp,
        target_audience=request.target_audience
    )

# Route: Retrieve all campaigns
@content_router.get("/campaigns", response_model=List[CampaignResponse])
async def get_campaigns():
    """
    Retrieve all marketing campaigns
    """
    return [
        CampaignResponse(**campaign) 
        for campaign in campaigns_db.values()
    ]

# Route: Retrieve a specific campaign by ID
@content_router.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(campaign_id: str):
    """
    Retrieve a specific campaign by ID
    """
    campaign = campaigns_db.get(campaign_id)
    if not campaign:
        raise CampaignNotFoundError(campaign_id)
    return CampaignResponse(**campaign)

# Route: Delete a campaign by ID
@content_router.delete("/campaigns/{campaign_id}", status_code=status.HTTP_200_OK)
async def delete_campaign(campaign_id: str):
    """
    Delete a campaign by ID
    """
    if campaign_id not in campaigns_db:
        raise CampaignNotFoundError(campaign_id)
    
    del campaigns_db[campaign_id]
    return {"message": "Campaign deleted successfully"}

# Route: Get campaign analytics
@content_router.get("/campaigns/{campaign_id}/analytics")
async def get_campaign_analytics(campaign_id: str):
    """
    Get analytics for a specific campaign
    """
    campaign = campaigns_db.get(campaign_id)
    if not campaign:
        raise CampaignNotFoundError(campaign_id)
    
    # Get analytics for all content in the campaign
    content_analytics = []
    for content_id in campaign.get('content_ids', []):
        if content_id in content_db:
            content = content_db[content_id]
            content_analytics.append({
                'content_id': content_id,
                'quality_score': content.get('quality_score', 0),
                'seo_score': content.get('seo_score', 0),
                'sentiment': content.get('sentiment', 'unknown')
            })
    
    avg_quality = sum(c['quality_score'] for c in content_analytics) / max(len(content_analytics), 1)
    avg_seo = sum(c['seo_score'] for c in content_analytics) / max(len(content_analytics), 1)
    
    return {
        'campaign_id': campaign_id,
        'campaign_name': campaign['name'],
        'total_content_pieces': len(campaign.get('content_ids', [])),
        'average_quality_score': round(avg_quality, 2),
        'average_seo_score': round(avg_seo, 2),
        'content_analytics': content_analytics
    }

# Route: Get detailed content analysis
@content_router.get("/content/{content_id}/analysis")
async def get_detailed_content_analysis(content_id: str):
    """
    Get detailed analysis report for specific content including readability,
    engagement metrics, and SEO recommendations
    """
    content = content_db.get(content_id)
    if not content:
        raise ContentNotFoundError(content_id)
    
    # Generate comprehensive analysis report
    keywords = content.get('keywords', [])
    analysis_report = analytics_service.generate_content_report(
        content['content'],
        keywords
    )
    
    # Add content metadata
    analysis_report['content_id'] = content_id
    analysis_report['content_preview'] = content['content'][:100] + "..." if len(content['content']) > 100 else content['content']
    analysis_report['created_at'] = content['created_at']
    
    return analysis_report

# Route: Compare multiple content pieces
@content_router.post("/content/compare")
async def compare_content(content_ids: List[str]):
    """
    Compare multiple content pieces and get comparative analytics
    """
    if len(content_ids) < 2:
        raise InsufficientDataError("At least 2 content IDs required for comparison")
    
    comparisons = []
    for content_id in content_ids:
        content = content_db.get(content_id)
        if content:
            analysis = analytics_service.generate_content_report(
                content['content'],
                content.get('keywords', [])
            )
            comparisons.append({
                'content_id': content_id,
                'overall_score': analysis['overall_score'],
                'readability_score': analysis['readability']['reading_ease_score'],
                'engagement_score': analysis['engagement']['engagement_score'],
                'keyword_density': analysis['keyword_analysis']['keyword_density']
            })
    
    if not comparisons:
        raise ContentNotFoundError("None of the provided content IDs")
    
    # Find best performing content
    best_overall = max(comparisons, key=lambda x: x['overall_score'])
    best_readability = max(comparisons, key=lambda x: x['readability_score'])
    best_engagement = max(comparisons, key=lambda x: x['engagement_score'])
    
    return {
        'comparison_count': len(comparisons),
        'content_comparisons': comparisons,
        'insights': {
            'best_overall_content_id': best_overall['content_id'],
            'best_readability_content_id': best_readability['content_id'],
            'best_engagement_content_id': best_engagement['content_id']
        }
    }

# Route: Get cache statistics
@content_router.get("/cache/stats")
async def get_cache_stats():
    """
    Get cache performance statistics
    """
    return content_cache.get_stats()

# Route: Clear cache
@content_router.post("/cache/clear")
async def clear_cache():
    """
    Clear content generation cache
    """
    content_cache.clear()
    return {"message": "Cache cleared successfully"}