import unittest
from unittest.mock import patch, MagicMock
from services.content_generation_service import ContentGenerationService

class TestContentGenerationService(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by initializing the ContentGenerationService instance.
        """
        self.service = ContentGenerationService()
        self.mock_input_data = {
            "campaign_name": "Summer Sale",
            "target_audience": "young adults",
            "keywords": ["discount", "summer", "fashion"],
            "tone": "casual",
            "platforms": ["Instagram", "Facebook"]
        }
        self.mock_generated_content = {
            "Instagram": "🔥 Summer Sale Alert! Get the hottest fashion trends at unbeatable discounts. 🌞 #SummerStyle #Discounts",
            "Facebook": "Summer is here, and so are the deals! 🌴 Shop now for exclusive discounts on fashion essentials. 🛍️ #SummerSale"
        }

    @patch("services.content_generation_service.ExternalAPIClient")
    def test_generate_content_success(self, MockExternalAPIClient):
        """
        Test successful content generation with mocked external API calls.
        """
        # Mock the external API client behavior
        mock_api_client = MockExternalAPIClient.return_value
        mock_api_client.generate_content.return_value = self.mock_generated_content

        # Call the service method
        result = self.service.generate_content(self.mock_input_data)

        # Assertions
        self.assertEqual(result, self.mock_generated_content)
        mock_api_client.generate_content.assert_called_once_with(self.mock_input_data)

    @patch("services.content_generation_service.ExternalAPIClient")
    def test_generate_content_api_failure(self, MockExternalAPIClient):
        """
        Test content generation when the external API fails.
        """
        # Mock the external API client behavior
        mock_api_client = MockExternalAPIClient.return_value
        mock_api_client.generate_content.side_effect = Exception("API Error")

        # Call the service method and assert exception is raised
        with self.assertRaises(Exception) as context:
            self.service.generate_content(self.mock_input_data)

        self.assertEqual(str(context.exception), "API Error")
        mock_api_client.generate_content.assert_called_once_with(self.mock_input_data)

    @patch("services.content_generation_service.ExternalAPIClient")
    def test_generate_content_empty_response(self, MockExternalAPIClient):
        """
        Test content generation when the external API returns an empty response.
        """
        # Mock the external API client behavior
        mock_api_client = MockExternalAPIClient.return_value
        mock_api_client.generate_content.return_value = {}

        # Call the service method
        result = self.service.generate_content(self.mock_input_data)

        # Assertions
        self.assertEqual(result, {})
        mock_api_client.generate_content.assert_called_once_with(self.mock_input_data)

    def test_validate_input_data_success(self):
        """
        Test input data validation with valid data.
        """
        # Call the validation method
        result = self.service.validate_input_data(self.mock_input_data)

        # Assertions
        self.assertTrue(result)

    def test_validate_input_data_missing_fields(self):
        """
        Test input data validation when required fields are missing.
        """
        invalid_data = {
            "campaign_name": "Summer Sale",
            "keywords": ["discount", "summer", "fashion"]
        }

        # Call the validation method and assert exception is raised
        with self.assertRaises(ValueError) as context:
            self.service.validate_input_data(invalid_data)

        self.assertEqual(str(context.exception), "Missing required fields in input data.")

    def test_validate_input_data_invalid_types(self):
        """
        Test input data validation when fields have invalid types.
        """
        invalid_data = {
            "campaign_name": "Summer Sale",
            "target_audience": 12345,  # Invalid type
            "keywords": "discount, summer, fashion",  # Invalid type
            "tone": "casual",
            "platforms": ["Instagram", "Facebook"]
        }

        # Call the validation method and assert exception is raised
        with self.assertRaises(ValueError) as context:
            self.service.validate_input_data(invalid_data)

        self.assertEqual(str(context.exception), "Invalid data types in input fields.")

if __name__ == "__main__":
    unittest.main()