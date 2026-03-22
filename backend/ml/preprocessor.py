import re
import string
from typing import List

class TextPreprocessor:
    """
    NLP cleaning pipeline to normalize text.
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Removes special characters, extra whitespace, and converts to lowercase.
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove phone numbers (simplified)
        text = re.sub(r'\+?\d[\d -]{8,}\d', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove specific symbols and keep alphanumeric
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    @staticmethod
    def extract_skills(text: str, predefined_skills: List[str]) -> List[str]:
        """
        Simple keyword-based extraction (can be improved with NER).
        """
        text = text.lower()
        found_skills = []
        for skill in predefined_skills:
            # Word boundary check for accuracy (e.g., avoid 'C' in 'CAT')
            pattern = rf'\b{re.escape(skill.lower())}\b'
            if re.search(pattern, text):
                found_skills.append(skill)
        return list(set(found_skills))
