# AI-Driven Automated Content Creation for Marketing Campaigns

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Overview

The **AI-Driven Automated Content Creation for Marketing Campaigns** project is a cutting-edge solution designed to streamline and enhance the process of generating marketing content. By leveraging advanced AI models, this system automates the creation of high-quality, personalized content tailored to specific campaigns, audiences, and platforms. The project is built with scalability, flexibility, and ease of use in mind, making it an ideal tool for marketing teams and businesses of all sizes.

### ✨ Key Features

- **AI-Powered Content Generation**: Create engaging and platform-specific content using state-of-the-art natural language processing (NLP) models.
- **Advanced Content Analytics**: Comprehensive analysis including readability scores, engagement metrics, and SEO recommendations.
- **Sentiment Analysis**: Automatic sentiment detection for generated content to ensure appropriate tone.
- **Quality & SEO Scoring**: Real-time quality and SEO scoring to optimize content effectiveness.
- **Content Caching**: Intelligent caching system for improved performance and reduced API costs.
- **Rate Limiting**: Built-in rate limiting to protect API resources and ensure fair usage.
- **Multi-Platform Support**: Generate content optimized for various platforms, including Twitter, LinkedIn, Instagram, and more.
- **Campaign Analytics**: Track and compare performance metrics across multiple content pieces.
- **Customizable Campaigns**: Tailor content to specific audiences, industries, and marketing goals.
- **API Integration**: Seamlessly integrate with existing marketing tools and workflows.
- **Scalable Architecture**: Designed to handle large datasets and high traffic.

---

## 🎯 What's New in Version 2.0

### Enhanced Features

- **Content Analytics Service**: Advanced analysis including:
  - Flesch Reading Ease score for readability
  - Engagement potential scoring
  - Keyword density analysis
  - SEO recommendations
  
- **Sentiment Analysis**: Real-time sentiment detection (positive, negative, neutral) with confidence scores

- **Performance Optimization**:
  - In-memory caching with configurable TTL
  - Cache hit rate tracking
  - Automatic cache cleanup

- **API Security**:
  - Rate limiting (60 requests/minute, 1000 requests/hour)
  - Custom exception handling
  - Rate limit headers in responses

- **New API Endpoints**:
  - `GET /api/v1/content/{id}/analysis` - Detailed content analysis
  - `GET /api/v1/content/{id}/sentiment` - Sentiment analysis
  - `POST /api/v1/content/compare` - Compare multiple content pieces
  - `GET /api/v1/campaigns/{id}/analytics` - Campaign analytics
  - `GET /api/v1/cache/stats` - Cache performance statistics
  - `POST /api/v1/cache/clear` - Clear content cache

---

## 🏗️ Architecture

The system is built using a modular architecture to ensure scalability and maintainability. Below is an overview of the core components:

### 1. **Frontend**
- **Technology**: JavaScript (React.js)
- **Purpose**: Provides an intuitive user interface for creating and managing marketing campaigns.
- **Features**:
  - Campaign creation and customization
  - Real-time content preview
  - Analytics dashboard for performance tracking

### 2. **Backend**
- **Technology**: Python (FastAPI)
- **Purpose**: Handles API requests, business logic, and communication with the AI model.
- **Features**:
  - Content generation endpoints
  - Advanced analytics and scoring
  - Campaign management and storage
  - Rate limiting and caching

### 3. **AI Engine**
- **Technology**: Python (Hugging Face Transformers, OpenAI API)
- **Purpose**: Powers the content generation using pre-trained language models.
- **Features**:
  - Text generation and summarization
  - Sentiment analysis and tone adjustment
  - Keyword optimization

### 4. **Analytics Engine**
- **Technology**: Python (Custom Analytics Service)
- **Purpose**: Provides comprehensive content analysis and insights.
- **Features**:
  - Readability analysis
  - Engagement scoring
  - SEO optimization recommendations
  - Comparative analysis

### 5. **Containerization**
- **Technology**: Docker
- **Purpose**: Ensures consistent deployment across environments.
- **Features**:
  - Pre-configured Docker images for the frontend, backend, and AI engine
  - Docker Compose for multi-container orchestration

### 6. **Database**
- **Technology**: PostgreSQL
- **Purpose**: Stores user data, campaign details, and generated content.
- **Features**:
  - Relational database schema for structured data storage
  - Optimized queries for high performance

---

## 📦 Installation

Follow these steps to set up the project on your local machine:

### Prerequisites

- **Docker**: Ensure Docker is installed on your system. [Download Docker](https://www.docker.com/get-started)
- **Python 3.9+**: Required for running backend services locally (if needed)
- **Node.js 16+**: Required for running the frontend locally (if needed)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yadavanujkumar/ai-driven-automated-content-creation-for-marketing-campaigns.git
   cd ai-driven-automated-content-creation-for-marketing-campaigns
   ```

2. **Set Up Environment Variables**:
   - Copy the `.env.example` file to `.env` (or create a `.env` file)
   - Update the environment variables with your API keys and configuration:
     ```bash
     cp .env .env.local
     ```
   - Required environment variables:
     - `OPENAI_API_KEY`: Your OpenAI API key
     - `DATABASE_URL`: PostgreSQL connection string
     - `REDIS_URL`: Redis connection string (if using Redis for caching)

3. **Using Docker (Recommended)**:
   ```bash
   # Build and start all services
   docker-compose up --build

   # Run in detached mode
   docker-compose up -d
   ```

4. **Manual Installation** (Alternative):

   **Backend Setup**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Run the backend server
   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

   **Frontend Setup** (if applicable):
   ```bash
   cd frontend
   npm install
   npm start
   ```

5. **Access the Application**:
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/docs
   - **Frontend** (if running): http://localhost:3000

---

## 🎮 Usage

### Quick Start

1. **Access API Documentation**:
   Navigate to `http://localhost:8000/docs` to explore the interactive API documentation powered by Swagger UI.

2. **Generate Content**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/content/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "campaign_type": "social_media",
       "platform": "twitter",
       "topic": "AI in Marketing",
       "tone": "professional",
       "length": "short"
     }'
   ```

3. **Analyze Content**:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/content/{content_id}/analysis"
   ```

4. **Get Sentiment Analysis**:
   ```bash
   curl -X GET "http://localhost:8000/api/v1/content/{content_id}/sentiment"
   ```

### API Endpoints

For detailed API documentation, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

**Core Endpoints**:
- `POST /api/v1/content/generate` - Generate new content
- `GET /api/v1/content/{id}` - Get specific content
- `GET /api/v1/content/{id}/analysis` - Get content analysis
- `GET /api/v1/content/{id}/sentiment` - Get sentiment analysis
- `POST /api/v1/content/compare` - Compare multiple contents
- `GET /api/v1/campaigns` - List all campaigns
- `POST /api/v1/campaigns` - Create new campaign
- `GET /api/v1/campaigns/{id}/analytics` - Get campaign analytics

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_content_generation.py
```

---

## 📊 Performance Metrics

The system includes built-in monitoring and analytics:

- **Cache Performance**: Monitor cache hit rates via `/api/v1/cache/stats`
- **Rate Limiting**: Track API usage and limits
- **Content Analytics**: Comprehensive metrics for each generated content
- **Campaign Analytics**: Aggregate performance across campaigns

---

## 🛠️ Configuration

Key configuration options in `.env`:

```env
# AI Model Configuration
OPENAI_API_KEY=your_api_key_here
AI_MODEL=gpt-3.5-turbo
MAX_TOKENS=500

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/content_db

# Redis Cache (optional)
REDIS_URL=redis://localhost:6379/0
CACHE_TTL=3600

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Server
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false
```

---

## 🐛 Troubleshooting

### Common Issues

1. **Docker container fails to start**:
   - Check if ports 8000 and 5432 are already in use
   - Ensure Docker daemon is running
   - Check `.env` file is properly configured

2. **API returns 429 (Rate Limit)**:
   - Wait for the rate limit window to reset
   - Adjust rate limit settings in `.env`
   - Implement request queuing in your client

3. **Content generation fails**:
   - Verify OpenAI API key is valid
   - Check API quota and billing
   - Review error messages in logs

4. **Database connection errors**:
   - Ensure PostgreSQL is running
   - Verify DATABASE_URL is correct
   - Check database user permissions

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write unit tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Anuj Kumar Yadav** - [@yadavanujkumar](https://github.com/yadavanujkumar)

---

## 🙏 Acknowledgments

- OpenAI for GPT models
- Hugging Face for transformer models
- FastAPI framework
- The open-source community

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub Issues](https://github.com/yadavanujkumar/ai-driven-automated-content-creation-for-marketing-campaigns/issues)
- Check the [API Documentation](./API_DOCUMENTATION.md)
- Review existing issues before creating new ones

---

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Advanced A/B testing capabilities
- [ ] Integration with popular marketing platforms (HubSpot, Mailchimp)
- [ ] Real-time collaboration features
- [ ] Mobile application
- [ ] Enhanced analytics dashboard
- [ ] Custom AI model fine-tuning

---

