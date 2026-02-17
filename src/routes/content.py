from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from datetime import datetime
import uuid
import random

# Blueprint for content routes
content_bp = Blueprint('content', __name__)

# Mock database (in-memory for demonstration purposes)
campaigns_db = {}
content_db = {}

# Helper function to generate AI-driven content
def generate_ai_content(prompt, tone, length):
    # Simulate AI content generation with realistic data
    sample_responses = [
        f"{prompt} - A captivating and engaging message tailored for your audience.",
        f"{prompt} - A professional and concise message to drive conversions.",
        f"{prompt} - A creative and innovative approach to marketing your product."
    ]
    return random.choice(sample_responses)[:length]

# Route: Generate AI-driven marketing content
@content_bp.route('/generate', methods=['POST'])
@cross_origin()
def generate_content():
    try:
        data = request.json
        prompt = data.get('prompt')
        tone = data.get('tone', 'neutral')
        length = data.get('length', 250)

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        generated_content = generate_ai_content(prompt, tone, length)
        content_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()

        # Save to mock content database
        content_db[content_id] = {
            'id': content_id,
            'prompt': prompt,
            'tone': tone,
            'length': length,
            'content': generated_content,
            'created_at': timestamp
        }

        return jsonify({
            'id': content_id,
            'content': generated_content,
            'created_at': timestamp
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route: Retrieve content by ID
@content_bp.route('/content/<content_id>', methods=['GET'])
@cross_origin()
def get_content(content_id):
    try:
        content = content_db.get(content_id)
        if not content:
            return jsonify({'error': 'Content not found'}), 404

        return jsonify(content), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route: Create a new campaign
@content_bp.route('/campaigns', methods=['POST'])
@cross_origin()
def create_campaign():
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        content_ids = data.get('content_ids', [])

        if not name:
            return jsonify({'error': 'Campaign name is required'}), 400

        campaign_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()

        # Save to mock campaigns database
        campaigns_db[campaign_id] = {
            'id': campaign_id,
            'name': name,
            'description': description,
            'content_ids': content_ids,
            'created_at': timestamp
        }

        return jsonify({
            'id': campaign_id,
            'name': name,
            'description': description,
            'content_ids': content_ids,
            'created_at': timestamp
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route: Retrieve all campaigns
@content_bp.route('/campaigns', methods=['GET'])
@cross_origin()
def get_campaigns():
    try:
        campaigns = list(campaigns_db.values())
        return jsonify(campaigns), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route: Retrieve a specific campaign by ID
@content_bp.route('/campaigns/<campaign_id>', methods=['GET'])
@cross_origin()
def get_campaign(campaign_id):
    try:
        campaign = campaigns_db.get(campaign_id)
        if not campaign:
            return jsonify({'error': 'Campaign not found'}), 404

        return jsonify(campaign), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route: Delete a campaign by ID
@content_bp.route('/campaigns/<campaign_id>', methods=['DELETE'])
@cross_origin()
def delete_campaign(campaign_id):
    try:
        if campaign_id not in campaigns_db:
            return jsonify({'error': 'Campaign not found'}), 404

        del campaigns_db[campaign_id]
        return jsonify({'message': 'Campaign deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500