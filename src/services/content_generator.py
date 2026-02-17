import openai
import logging
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentGenerator:
    """
    A service for AI-driven content generation for marketing campaigns.
    This class interacts with AI models (e.g., OpenAI API) to generate content.
    """

    def __init__(self, api_key: str, model: str = "gpt-4", max_tokens: int = 1000, temperature: float = 0.7):
        """
        Initialize the ContentGenerator with API credentials and model configuration.

        :param api_key: API key for the AI model (e.g., OpenAI API key).
        :param model: The AI model to use for content generation (default: gpt-4).
        :param max_tokens: Maximum number of tokens for the generated content.
        :param temperature: Sampling temperature for the AI model (higher values = more creative output).
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        openai.api_key = self.api_key

    def generate_content(self, prompt: str, num_variants: int = 1) -> List[Dict[str, str]]:
        """
        Generate marketing content based on the provided prompt.

        :param prompt: The input prompt for the AI model.
        :param num_variants: Number of content variants to generate.
        :return: A list of dictionaries containing the generated content.
        """
        try:
            logger.info("Generating content with prompt: %s", prompt)
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a marketing content generator."},
                          {"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                n=num_variants
            )
            generated_content = []
            for choice in response.get("choices", []):
                generated_content.append({
                    "content": choice["message"]["content"].strip(),
                    "finish_reason": choice.get("finish_reason", "unknown")
                })
            logger.info("Content generation successful. Generated %d variants.", len(generated_content))
            return generated_content
        except Exception as e:
            logger.error("Error during content generation: %s", str(e))
            raise RuntimeError("Failed to generate content") from e

    def generate_headlines(self, product_name: str, target_audience: str, tone: str = "exciting") -> List[str]:
        """
        Generate marketing headlines for a product.

        :param product_name: Name of the product or service.
        :param target_audience: The target audience for the marketing campaign.
        :param tone: The tone of the headlines (e.g., exciting, professional, casual).
        :return: A list of generated headlines.
        """
        prompt = (
            f"Generate 5 creative and engaging marketing headlines for a product named '{product_name}'. "
            f"The target audience is '{target_audience}', and the tone should be '{tone}'."
        )
        logger.info("Generating headlines for product: %s", product_name)
        content_variants = self.generate_content(prompt, num_variants=1)
        if content_variants:
            return content_variants[0]["content"].split("\n")
        return []

    def generate_social_media_post(self, product_name: str, campaign_goal: str, platform: str) -> str:
        """
        Generate a social media post for a marketing campaign.

        :param product_name: Name of the product or service.
        :param campaign_goal: The goal of the campaign (e.g., brand awareness, lead generation).
        :param platform: The social media platform (e.g., Twitter, Instagram, LinkedIn).
        :return: A generated social media post.
        """
        prompt = (
            f"Write a {platform} post for a marketing campaign. The product is '{product_name}', "
            f"and the goal is '{campaign_goal}'. Make it engaging and suitable for the platform."
        )
        logger.info("Generating social media post for platform: %s", platform)
        content_variants = self.generate_content(prompt, num_variants=1)
        if content_variants:
            return content_variants[0]["content"]
        return ""

    def generate_email_copy(self, product_name: str, target_audience: str, campaign_goal: str) -> str:
        """
        Generate an email copy for a marketing campaign.

        :param product_name: Name of the product or service.
        :param target_audience: The target audience for the email.
        :param campaign_goal: The goal of the campaign (e.g., product launch, customer retention).
        :return: A generated email copy.
        """
        prompt = (
            f"Write an email copy for a marketing campaign. The product is '{product_name}', "
            f"the target audience is '{target_audience}', and the goal is '{campaign_goal}'. "
            f"Make it professional and persuasive."
        )
        logger.info("Generating email copy for product: %s", product_name)
        content_variants = self.generate_content(prompt, num_variants=1)
        if content_variants:
            return content_variants[0]["content"]
        return ""

# Example usage:
if __name__ == "__main__":
    # Replace 'your_openai_api_key' with your actual OpenAI API key
    generator = ContentGenerator(api_key="your_openai_api_key")
    headlines = generator.generate_headlines("SuperWidget", "tech enthusiasts", "exciting")
    print("Generated Headlines:", headlines)

    social_post = generator.generate_social_media_post("SuperWidget", "increase brand awareness", "Twitter")
    print("Generated Social Media Post:", social_post)

    email_copy = generator.generate_email_copy("SuperWidget", "business professionals", "product launch")
    print("Generated Email Copy:", email_copy)