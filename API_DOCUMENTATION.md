# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Table of Contents
- [Health Check](#health-check)
- [Content Generation](#content-generation)
- [Content Retrieval](#content-retrieval)
- [Content Analytics](#content-analytics)
- [Campaign Management](#campaign-management)
- [Cache Management](#cache-management)

---

## Health Check

### Get Service Health Status
Check if the service is running and see enabled features.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "features": {
    "content_generation": "enabled",
    "sentiment_analysis": "enabled",
    "seo_analytics": "enabled",
    "rate_limiting": "enabled",
    "campaign_management": "enabled"
  }
}
```

---

## Content Generation

### Generate Content
Generate AI-driven marketing content with automatic quality and SEO scoring.

**Endpoint:** `POST /content/generate`

**Request Body:**
```json
{
  "prompt": "Create an engaging social media post about our new AI product",
  "tone": "exciting",
  "length": 280,
  "keywords": ["AI", "innovation", "technology"],
  "platform": "twitter"
}
```

**Parameters:**
- `prompt` (required): Content generation prompt
- `tone` (optional): Tone of content (default: "neutral")
- `length` (optional): Desired length in characters (default: 250, max: 5000)
- `keywords` (optional): List of keywords to include
- `platform` (optional): Target platform (twitter, linkedin, instagram)

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "content": "🚀 Revolutionize your workflow with AI! Our new product brings innovation to your fingertips. #AI #innovation #technology",
  "created_at": "2026-02-17T10:30:00",
  "quality_score": 85.5,
  "seo_score": 78.0,
  "sentiment": "positive"
}
```

---

## Content Retrieval

### Get Content by ID
Retrieve previously generated content by its ID.

**Endpoint:** `GET /content/{content_id}`

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "prompt": "Create an engaging social media post",
  "tone": "exciting",
  "length": 280,
  "content": "🚀 Revolutionize your workflow...",
  "created_at": "2026-02-17T10:30:00",
  "quality_score": 85.5,
  "seo_score": 78.0,
  "sentiment": "positive",
  "keywords": ["AI", "innovation"],
  "platform": "twitter"
}
```

### Get Content Sentiment
Get sentiment analysis for specific content.

**Endpoint:** `GET /content/{content_id}/sentiment`

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.85
}
```

---

## Content Analytics

### Get Detailed Content Analysis
Get comprehensive analysis including readability, engagement, and SEO metrics.

**Endpoint:** `GET /content/{content_id}/analysis`

**Response:**
```json
{
  "content_id": "550e8400-e29b-41d4-a716-446655440000",
  "overall_score": 82.5,
  "readability": {
    "reading_ease_score": 75.2,
    "avg_words_per_sentence": 12.5,
    "total_words": 50,
    "total_sentences": 4
  },
  "engagement": {
    "engagement_score": 85.0,
    "action_words_count": 3,
    "positive_words_count": 5,
    "negative_words_count": 0,
    "has_questions": true,
    "question_count": 1,
    "has_numbers": true
  },
  "keyword_analysis": {
    "keyword_density": 2.5,
    "keywords_found": ["AI", "innovation"],
    "keyword_frequency": {
      "AI": 2,
      "innovation": 1
    },
    "total_keyword_occurrences": 3
  },
  "seo_recommendations": [
    "Content looks good! No major SEO issues detected."
  ],
  "analyzed_at": "2026-02-17T10:35:00"
}
```

### Compare Multiple Content Pieces
Compare multiple content pieces to identify the best performer.

**Endpoint:** `POST /content/compare`

**Request Body:**
```json
["content_id_1", "content_id_2", "content_id_3"]
```

**Response:**
```json
{
  "comparison_count": 3,
  "content_comparisons": [
    {
      "content_id": "content_id_1",
      "overall_score": 85.5,
      "readability_score": 75.2,
      "engagement_score": 88.0,
      "keyword_density": 2.5
    },
    {
      "content_id": "content_id_2",
      "overall_score": 78.0,
      "readability_score": 70.0,
      "engagement_score": 82.0,
      "keyword_density": 1.8
    }
  ],
  "insights": {
    "best_overall_content_id": "content_id_1",
    "best_readability_content_id": "content_id_1",
    "best_engagement_content_id": "content_id_1"
  }
}
```

---

## Campaign Management

### Create Campaign
Create a new marketing campaign.

**Endpoint:** `POST /campaigns`

**Request Body:**
```json
{
  "name": "Summer Product Launch",
  "description": "Marketing campaign for new summer product line",
  "content_ids": ["content_id_1", "content_id_2"],
  "target_audience": "Young professionals aged 25-35"
}
```

**Response:**
```json
{
  "id": "campaign_id_123",
  "name": "Summer Product Launch",
  "description": "Marketing campaign for new summer product line",
  "content_ids": ["content_id_1", "content_id_2"],
  "created_at": "2026-02-17T10:30:00",
  "target_audience": "Young professionals aged 25-35"
}
```

### Get All Campaigns
Retrieve all campaigns.

**Endpoint:** `GET /campaigns`

**Response:**
```json
[
  {
    "id": "campaign_id_123",
    "name": "Summer Product Launch",
    "description": "...",
    "content_ids": ["content_id_1"],
    "created_at": "2026-02-17T10:30:00",
    "target_audience": "Young professionals"
  }
]
```

### Get Campaign by ID
Retrieve a specific campaign.

**Endpoint:** `GET /campaigns/{campaign_id}`

### Delete Campaign
Delete a campaign.

**Endpoint:** `DELETE /campaigns/{campaign_id}`

**Response:**
```json
{
  "message": "Campaign deleted successfully"
}
```

### Get Campaign Analytics
Get analytics for a specific campaign including aggregated metrics.

**Endpoint:** `GET /campaigns/{campaign_id}/analytics`

**Response:**
```json
{
  "campaign_id": "campaign_id_123",
  "campaign_name": "Summer Product Launch",
  "total_content_pieces": 5,
  "average_quality_score": 82.5,
  "average_seo_score": 75.8,
  "content_analytics": [
    {
      "content_id": "content_id_1",
      "quality_score": 85.5,
      "seo_score": 78.0,
      "sentiment": "positive"
    }
  ]
}
```

---

## Cache Management

### Get Cache Statistics
View cache performance statistics.

**Endpoint:** `GET /cache/stats`

**Response:**
```json
{
  "size": 150,
  "max_size": 500,
  "hit_count": 450,
  "miss_count": 100,
  "hit_rate_percent": 81.82,
  "total_requests": 550
}
```

### Clear Cache
Clear the content generation cache.

**Endpoint:** `POST /cache/clear`

**Response:**
```json
{
  "message": "Cache cleared successfully"
}
```

---

## Rate Limiting

All API endpoints (except `/health`) are rate-limited:
- **Per Minute Limit**: 60 requests
- **Per Hour Limit**: 1000 requests

Rate limit information is included in response headers:
```
X-RateLimit-Limit-Minute: 60
X-RateLimit-Remaining-Minute: 45
X-RateLimit-Limit-Hour: 1000
X-RateLimit-Remaining-Hour: 850
```

If rate limit is exceeded, you'll receive a 429 response:
```json
{
  "error": "Rate limit exceeded",
  "message": "Rate limit exceeded: 60 requests per minute",
  "retry_after_seconds": 60
}
```

---

## Error Responses

### 400 Bad Request
Invalid request parameters.
```json
{
  "detail": "Invalid content parameters"
}
```

### 404 Not Found
Resource not found.
```json
{
  "detail": "Content with ID 'xyz' not found"
}
```

### 429 Too Many Requests
Rate limit exceeded.
```json
{
  "error": "Rate limit exceeded",
  "message": "Rate limit exceeded: 60 requests per minute",
  "retry_after_seconds": 60
}
```

### 500 Internal Server Error
Server error occurred.
```json
{
  "detail": "Content generation failed: [error details]"
}
```

---

## Example Usage

### Python Example
```python
import requests

# Generate content
response = requests.post(
    "http://localhost:8000/api/v1/content/generate",
    json={
        "prompt": "Write a tweet about AI innovation",
        "tone": "exciting",
        "keywords": ["AI", "innovation"],
        "platform": "twitter"
    }
)
content = response.json()
print(f"Generated: {content['content']}")
print(f"Quality Score: {content['quality_score']}")

# Get detailed analysis
analysis = requests.get(
    f"http://localhost:8000/api/v1/content/{content['id']}/analysis"
).json()
print(f"Engagement Score: {analysis['engagement']['engagement_score']}")
```

### cURL Example
```bash
# Generate content
curl -X POST http://localhost:8000/api/v1/content/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create an Instagram post about summer fashion",
    "tone": "casual",
    "keywords": ["fashion", "summer", "style"],
    "platform": "instagram"
  }'

# Get cache stats
curl http://localhost:8000/api/v1/cache/stats
```
