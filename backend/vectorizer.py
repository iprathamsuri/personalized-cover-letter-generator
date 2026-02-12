"""
Vectorizer Module
Handles text vectorization and feature extraction for the cover letter generator
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re


class TextVectorizer:
    """Handles text vectorization and feature extraction."""
    
    def __init__(self, vectorizer_type: str = "tfidf", max_features: int = 1000):
        """
        Initialize the TextVectorizer.
        
        Args:
            vectorizer_type (str): Type of vectorizer ('tfidf', 'count', 'binary')
            max_features (int): Maximum number of features
        """
        self.vectorizer_type = vectorizer_type
        self.max_features = max_features
        self.vectorizer = None
        self.feature_names = []
        self.vocabulary = {}
        
        # Initialize vectorizer based on type
        if vectorizer_type == "tfidf":
            self.vectorizer = TfidfVectorizer(
                max_features=max_features,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
        elif vectorizer_type == "count":
            self.vectorizer = CountVectorizer(
                max_features=max_features,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
        elif vectorizer_type == "binary":
            self.vectorizer = CountVectorizer(
                max_features=max_features,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8,
                binary=True
            )
        else:
            raise ValueError(f"Unsupported vectorizer type: {vectorizer_type}")
    
    def fit(self, texts: List[str]) -> 'TextVectorizer':
        """
        Fit the vectorizer on the given texts.
        
        Args:
            texts (List[str]): List of texts to fit on
            
        Returns:
            TextVectorizer: Self for method chaining
        """
        if not texts:
            raise ValueError("No texts provided for fitting")
        
        # Fit vectorizer
        self.vectorizer.fit(texts)
        
        # Store feature names and vocabulary
        self.feature_names = self.vectorizer.get_feature_names_out()
        self.vocabulary = self.vectorizer.vocabulary_
        
        return self
    
    def transform(self, texts: List[str]) -> np.ndarray:
        """
        Transform texts to vectors.
        
        Args:
            texts (List[str]): List of texts to transform
            
        Returns:
            np.ndarray: Transformed vectors
        """
        if not texts:
            return np.array([])
        
        if self.vectorizer is None:
            raise ValueError("Vectorizer not fitted. Call fit() first.")
        
        return self.vectorizer.transform(texts).toarray()
    
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """
        Fit the vectorizer and transform texts.
        
        Args:
            texts (List[str]): List of texts to process
            
        Returns:
            np.ndarray: Transformed vectors
        """
        return self.vectorizer.fit_transform(texts).toarray()
    
    def get_feature_importance(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Get feature importance for a single text.
        
        Args:
            text (str): Input text
            top_n (int): Number of top features to return
            
        Returns:
            List[Tuple[str, float]]: List of (feature, score) tuples
        """
        if self.vectorizer is None:
            raise ValueError("Vectorizer not fitted. Call fit() first.")
        
        # Transform text
        vector = self.transform([text])[0]
        
        # Get feature scores
        feature_scores = [(self.feature_names[i], vector[i]) 
                         for i in range(len(self.feature_names)) 
                         if vector[i] > 0]
        
        # Sort by score and return top N
        feature_scores.sort(key=lambda x: x[1], reverse=True)
        
        return feature_scores[:top_n]
    
    def get_vocabulary_size(self) -> int:
        """Get the size of the vocabulary."""
        return len(self.vocabulary)
    
    def get_feature_names(self) -> List[str]:
        """Get the feature names."""
        return self.feature_names.copy()


class TopicModeler:
    """Handles topic modeling using LDA."""
    
    def __init__(self, n_topics: int = 5, max_features: int = 1000):
        """
        Initialize the TopicModeler.
        
        Args:
            n_topics (int): Number of topics
            max_features (int): Maximum number of features
        """
        self.n_topics = n_topics
        self.max_features = max_features
        self.vectorizer = CountVectorizer(
            max_features=max_features,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        self.lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42,
            max_iter=100
        )
        self.topic_words = {}
        self.feature_names = []
    
    def fit(self, texts: List[str]) -> 'TopicModeler':
        """
        Fit the topic model on the given texts.
        
        Args:
            texts (List[str]): List of texts to fit on
            
        Returns:
            TopicModeler: Self for method chaining
        """
        if not texts:
            raise ValueError("No texts provided for fitting")
        
        # Vectorize texts
        doc_term_matrix = self.vectorizer.fit_transform(texts)
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        # Fit LDA
        self.lda.fit(doc_term_matrix)
        
        # Extract topic words
        self._extract_topic_words()
        
        return self
    
    def transform(self, texts: List[str]) -> np.ndarray:
        """
        Transform texts to topic distributions.
        
        Args:
            texts (List[str]): List of texts to transform
            
        Returns:
            np.ndarray: Topic distributions
        """
        if not texts:
            return np.array([])
        
        if not hasattr(self.lda, 'components_'):
            raise ValueError("Model not fitted. Call fit() first.")
        
        # Vectorize texts
        doc_term_matrix = self.vectorizer.transform(texts)
        
        # Transform to topic distributions
        return self.lda.transform(doc_term_matrix)
    
    def fit_transform(self, texts: List[str]) -> np.ndarray:
        """
        Fit the topic model and transform texts.
        
        Args:
            texts (List[str]): List of texts to process
            
        Returns:
            np.ndarray: Topic distributions
        """
        # Vectorize texts
        doc_term_matrix = self.vectorizer.fit_transform(texts)
        self.feature_names = self.vectorizer.get_feature_names_out()
        
        # Fit LDA and transform
        topic_distributions = self.lda.fit_transform(doc_term_matrix)
        
        # Extract topic words
        self._extract_topic_words()
        
        return topic_distributions
    
    def _extract_topic_words(self, top_words: int = 10):
        """Extract top words for each topic."""
        self.topic_words = {}
        
        for topic_idx, topic in enumerate(self.lda.components_):
            # Get top words for this topic
            top_word_indices = topic.argsort()[-top_words:][::-1]
            top_words_list = [self.feature_names[i] for i in top_word_indices]
            self.topic_words[topic_idx] = top_words_list
    
    def get_topic_words(self, topic_idx: int, top_words: int = 10) -> List[str]:
        """
        Get top words for a specific topic.
        
        Args:
            topic_idx (int): Topic index
            top_words (int): Number of top words to return
            
        Returns:
            List[str]: Top words for the topic
        """
        if topic_idx not in self.topic_words:
            return []
        
        return self.topic_words[topic_idx][:top_words]
    
    def get_all_topics(self) -> Dict[int, List[str]]:
        """Get all topics with their top words."""
        return self.topic_words.copy()
    
    def get_dominant_topic(self, text: str) -> Tuple[int, float]:
        """
        Get the dominant topic for a text.
        
        Args:
            text (str): Input text
            
        Returns:
            Tuple[int, float]: (topic_index, probability)
        """
        topic_dist = self.transform([text])[0]
        dominant_idx = np.argmax(topic_dist)
        dominant_prob = topic_dist[dominant_idx]
        
        return dominant_idx, dominant_prob


class SkillExtractor:
    """Extracts and analyzes skills from text."""
    
    def __init__(self):
        """Initialize the SkillExtractor."""
        # Common tech skills
        self.tech_skills = {
            'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin'],
            'web': ['html', 'css', 'react', 'vue', 'angular', 'nodejs', 'express', 'django', 'flask', 'spring', 'laravel'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra', 'elasticsearch'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'gitlab', 'github'],
            'ai_ml': ['machine learning', 'tensorflow', 'pytorch', 'nlp', 'computer vision', 'deep learning', 'scikit-learn', 'pandas', 'numpy'],
            'tools': ['git', 'linux', 'ubuntu', 'windows', 'macos', 'vscode', 'intellij', 'eclipse', 'postman', 'jira']
        }
        
        # Soft skills
        self.soft_skills = [
            'communication', 'leadership', 'teamwork', 'problem solving', 'critical thinking', 'creativity',
            'adaptability', 'time management', 'collaboration', 'analytical skills', 'attention to detail',
            'project management', 'decision making', 'interpersonal skills', 'presentation skills', 'negotiation'
        ]
        
        # Business skills
        self.business_skills = [
            'marketing', 'sales', 'finance', 'accounting', 'strategy', 'planning', 'analysis', 'research',
            'reporting', 'budgeting', 'forecasting', 'consulting', 'management', 'operations', 'logistics'
        ]
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills from text.
        
        Args:
            text (str): Input text
            
        Returns:
            Dict[str, List[str]]: Dictionary of skill categories and found skills
        """
        if not text:
            return {}
        
        text_lower = text.lower()
        found_skills = {
            'tech_skills': [],
            'soft_skills': [],
            'business_skills': []
        }
        
        # Extract tech skills
        for category, skills in self.tech_skills.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills['tech_skills'].append(skill)
        
        # Extract soft skills
        for skill in self.soft_skills:
            if skill in text_lower:
                found_skills['soft_skills'].append(skill)
        
        # Extract business skills
        for skill in self.business_skills:
            if skill in text_lower:
                found_skills['business_skills'].append(skill)
        
        # Remove duplicates
        for category in found_skills:
            found_skills[category] = list(set(found_skills[category]))
        
        return found_skills
    
    def calculate_skill_coverage(self, text: str, required_skills: List[str]) -> Dict:
        """
        Calculate skill coverage against required skills.
        
        Args:
            text (str): Input text
            required_skills (List[str]): List of required skills
            
        Returns:
            Dict: Coverage statistics
        """
        found_skills = self.extract_skills(text)
        all_found_skills = []
        
        for category_skills in found_skills.values():
            all_found_skills.extend(category_skills)
        
        # Calculate coverage
        matched_skills = []
        for skill in required_skills:
            if any(skill.lower() in found.lower() for found in all_found_skills):
                matched_skills.append(skill)
        
        coverage_percentage = (len(matched_skills) / len(required_skills)) * 100 if required_skills else 0
        
        return {
            'required_skills': required_skills,
            'matched_skills': matched_skills,
            'missing_skills': [skill for skill in required_skills if skill not in matched_skills],
            'coverage_percentage': coverage_percentage,
            'total_found_skills': len(all_found_skills)
        }


def main():
    """Test the vectorization functionality."""
    # Sample texts
    texts = [
        "I am a software developer with experience in Python, JavaScript, and React.",
        "Looking for a data analyst position with strong SQL and Excel skills.",
        "Marketing manager with expertise in digital marketing and team leadership.",
        "DevOps engineer experienced in Docker, Kubernetes, and cloud infrastructure.",
        "Business analyst with strong analytical and communication skills."
    ]
    
    print("🧪 VECTORIZATION TEST")
    print("=" * 40)
    
    # Test TF-IDF Vectorizer
    print("\n📊 TF-IDF Vectorization:")
    tfidf_vectorizer = TextVectorizer("tfidf", max_features=100)
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)
    print(f"   Matrix shape: {tfidf_matrix.shape}")
    print(f"   Vocabulary size: {tfidf_vectorizer.get_vocabulary_size()}")
    
    # Test feature importance
    print("\n🔍 Feature Importance for first text:")
    features = tfidf_vectorizer.get_feature_importance(texts[0], top_n=5)
    for feature, score in features:
        print(f"   {feature}: {score:.3f}")
    
    # Test Topic Modeling
    print("\n🎯 Topic Modeling:")
    topic_modeler = TopicModeler(n_topics=3, max_features=50)
    topic_distributions = topic_modeler.fit_transform(texts)
    print(f"   Topic distributions shape: {topic_distributions.shape}")
    
    print("\n📝 Top words per topic:")
    all_topics = topic_modeler.get_all_topics()
    for topic_idx, words in all_topics.items():
        print(f"   Topic {topic_idx}: {', '.join(words[:5])}")
    
    # Test Skill Extraction
    print("\n🛠️ Skill Extraction:")
    skill_extractor = SkillExtractor()
    for i, text in enumerate(texts):
        skills = skill_extractor.extract_skills(text)
        print(f"   Text {i+1}: {len(sum(skills.values(), []))} skills found")
        for category, skill_list in skills.items():
            if skill_list:
                print(f"     {category}: {', '.join(skill_list[:3])}")


if __name__ == "__main__":
    main()
