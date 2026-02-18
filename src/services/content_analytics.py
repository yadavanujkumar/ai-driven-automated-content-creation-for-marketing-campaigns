"""
Content Analytics Service
Provides advanced analytics and insights for generated marketing content
"""

from typing import Dict, List, Optional
from datetime import datetime
import re
from collections import Counter


class ContentAnalytics:
    """Service for analyzing marketing content quality and performance"""
    
    def __init__(self):
        self.positive_keywords = [
            'amazing', 'excellent', 'fantastic', 'great', 'outstanding',
            'wonderful', 'perfect', 'best', 'love', 'incredible'
        ]
        self.negative_keywords = [
            'bad', 'terrible', 'awful', 'worst', 'hate',
            'disappointing', 'poor', 'failure', 'useless'
        ]
        self.action_words = [
            'buy', 'get', 'discover', 'learn', 'start', 'join',
            'subscribe', 'download', 'register', 'click', 'shop'
        ]
    
    def analyze_readability(self, content: str) -> Dict[str, float]:
        """
        Analyze content readability using various metrics
        
        Returns:
            Dictionary with readability scores
        """
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        word_count = len(words)
        sentence_count = max(len(sentences), 1)
        
        # Calculate average words per sentence
        avg_words_per_sentence = word_count / sentence_count
        
        # Calculate average syllables per word (simplified estimation)
        total_syllables = sum(self._count_syllables(word) for word in words)
        avg_syllables_per_word = total_syllables / max(word_count, 1)
        
        # Flesch Reading Ease (simplified)
        reading_ease = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        reading_ease = max(0, min(100, reading_ease))  # Clamp between 0-100
        
        return {
            'reading_ease_score': round(reading_ease, 2),
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'total_words': word_count,
            'total_sentences': sentence_count
        }
    
    def analyze_engagement_potential(self, content: str) -> Dict[str, any]:
        """
        Analyze potential engagement factors in content
        
        Returns:
            Dictionary with engagement metrics
        """
        content_lower = content.lower()
        
        # Count action words
        action_word_count = sum(1 for word in self.action_words if word in content_lower)
        
        # Count emotional words
        positive_count = sum(1 for word in self.positive_keywords if word in content_lower)
        negative_count = sum(1 for word in self.negative_keywords if word in content_lower)
        
        # Check for questions (engagement trigger)
        has_questions = bool(re.search(r'\?', content))
        question_count = content.count('?')
        
        # Check for numbers (tend to increase engagement)
        has_numbers = bool(re.search(r'\d', content))
        
        # Calculate engagement score
        engagement_score = 50.0  # Base score
        engagement_score += min(action_word_count * 10, 30)
        engagement_score += min(positive_count * 5, 15)
        engagement_score += question_count * 5
        if has_numbers:
            engagement_score += 5
        
        engagement_score = min(engagement_score, 100.0)
        
        return {
            'engagement_score': round(engagement_score, 2),
            'action_words_count': action_word_count,
            'positive_words_count': positive_count,
            'negative_words_count': negative_count,
            'has_questions': has_questions,
            'question_count': question_count,
            'has_numbers': has_numbers
        }
    
    def analyze_keyword_density(self, content: str, keywords: List[str]) -> Dict[str, any]:
        """
        Analyze keyword usage and density
        
        Args:
            content: The content to analyze
            keywords: List of target keywords
            
        Returns:
            Dictionary with keyword metrics
        """
        if not keywords:
            return {
                'keyword_density': 0.0,
                'keywords_found': [],
                'keyword_frequency': {}
            }
        
        content_lower = content.lower()
        words = content_lower.split()
        total_words = len(words)
        
        keyword_frequency = {}
        keywords_found = []
        total_keyword_count = 0
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = content_lower.count(keyword_lower)
            if count > 0:
                keyword_frequency[keyword] = count
                keywords_found.append(keyword)
                total_keyword_count += count
        
        keyword_density = (total_keyword_count / max(total_words, 1)) * 100
        
        return {
            'keyword_density': round(keyword_density, 2),
            'keywords_found': keywords_found,
            'keyword_frequency': keyword_frequency,
            'total_keyword_occurrences': total_keyword_count
        }
    
    def generate_seo_recommendations(self, content: str, keywords: List[str] = None) -> List[str]:
        """
        Generate SEO improvement recommendations
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        word_count = len(content.split())
        
        # Word count recommendations
        if word_count < 300:
            recommendations.append("Content is short. Consider adding more detail (aim for 300-1000 words).")
        elif word_count > 2000:
            recommendations.append("Content is very long. Consider breaking it into multiple pieces.")
        
        # Keyword recommendations
        if keywords:
            keyword_analysis = self.analyze_keyword_density(content, keywords)
            density = keyword_analysis['keyword_density']
            
            if density < 1:
                recommendations.append("Keyword density is low. Try to naturally incorporate more target keywords.")
            elif density > 3:
                recommendations.append("Keyword density is high. Reduce keyword usage to avoid keyword stuffing.")
            
            missing_keywords = set(keywords) - set(keyword_analysis['keywords_found'])
            if missing_keywords:
                recommendations.append(f"Missing keywords: {', '.join(list(missing_keywords)[:3])}")
        
        # Structure recommendations
        if '?' not in content:
            recommendations.append("Consider adding questions to increase engagement.")
        
        if not re.search(r'\d', content):
            recommendations.append("Adding numbers or statistics can improve credibility and engagement.")
        
        # Readability recommendations
        readability = self.analyze_readability(content)
        if readability['avg_words_per_sentence'] > 20:
            recommendations.append("Sentences are long. Shorten them for better readability.")
        
        if not recommendations:
            recommendations.append("Content looks good! No major SEO issues detected.")
        
        return recommendations
    
    def generate_content_report(self, content: str, keywords: List[str] = None) -> Dict:
        """
        Generate a comprehensive content analysis report
        
        Returns:
            Complete analysis report dictionary
        """
        readability = self.analyze_readability(content)
        engagement = self.analyze_engagement_potential(content)
        keyword_analysis = self.analyze_keyword_density(content, keywords or [])
        recommendations = self.generate_seo_recommendations(content, keywords)
        
        # Calculate overall score
        overall_score = (
            readability['reading_ease_score'] * 0.3 +
            engagement['engagement_score'] * 0.4 +
            (100 if keyword_analysis['keyword_density'] >= 1 and keyword_analysis['keyword_density'] <= 3 else 50) * 0.3
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'readability': readability,
            'engagement': engagement,
            'keyword_analysis': keyword_analysis,
            'seo_recommendations': recommendations,
            'analyzed_at': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def _count_syllables(word: str) -> int:
        """
        Estimate syllable count in a word (simplified algorithm)
        """
        word = word.lower()
        syllable_count = 0
        vowels = 'aeiouy'
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent 'e'
        if word.endswith('e'):
            syllable_count -= 1
        
        # Ensure at least one syllable
        if syllable_count == 0:
            syllable_count = 1
        
        return syllable_count


# Example usage
if __name__ == "__main__":
    analytics = ContentAnalytics()
    
    sample_content = """
    Discover the amazing power of AI-driven marketing! 
    Are you ready to transform your campaigns? 
    Get started today with our innovative solutions. 
    Over 10,000 businesses trust our platform.
    """
    
    report = analytics.generate_content_report(
        sample_content, 
        keywords=['AI', 'marketing', 'campaigns']
    )
    
    print("Content Analysis Report:")
    print(f"Overall Score: {report['overall_score']}")
    print(f"Reading Ease: {report['readability']['reading_ease_score']}")
    print(f"Engagement Score: {report['engagement']['engagement_score']}")
    print(f"Recommendations: {report['seo_recommendations']}")
