"""
Similarity Module
Handles similarity calculations and matching algorithms for the cover letter generator
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
import re


class SimilarityCalculator:
    """Calculates various similarity metrics between texts."""
    
    def __init__(self):
        """Initialize the SimilarityCalculator."""
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
    
    def cosine_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Cosine similarity score (0-1)
        """
        if not text1 or not text2:
            return 0.0
        
        # Vectorize texts
        vectors = self.vectorizer.fit_transform([text1, text2]).toarray()
        
        # Calculate cosine similarity
        similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
        
        return float(similarity)
    
    def jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate Jaccard similarity between two texts.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            
        Returns:
            float: Jaccard similarity score (0-1)
        """
        if not text1 or not text2:
            return 0.0
        
        # Tokenize texts
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def skill_overlap_similarity(self, text1: str, text2: str, skills_list: List[str]) -> float:
        """
        Calculate similarity based on skill overlap.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            skills_list (List[str]): List of skills to check
            
        Returns:
            float: Skill overlap similarity score (0-1)
        """
        if not text1 or not text2 or not skills_list:
            return 0.0
        
        text1_lower = text1.lower()
        text2_lower = text2.lower()
        
        # Find skills in each text
        skills1 = [skill for skill in skills_list if skill.lower() in text1_lower]
        skills2 = [skill for skill in skills_list if skill.lower() in text2_lower]
        
        # Calculate overlap
        set1 = set(skills1)
        set2 = set(skills2)
        
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def combined_similarity(self, text1: str, text2: str, weights: Dict[str, float] = None) -> float:
        """
        Calculate combined similarity using multiple metrics.
        
        Args:
            text1 (str): First text
            text2 (str): Second text
            weights (Dict[str, float]): Weights for different similarity metrics
            
        Returns:
            float: Combined similarity score (0-1)
        """
        if weights is None:
            weights = {
                'cosine': 0.5,
                'jaccard': 0.3,
                'skill_overlap': 0.2
            }
        
        # Calculate individual similarities
        cosine_sim = self.cosine_similarity(text1, text2)
        jaccard_sim = self.jaccard_similarity(text1, text2)
        
        # For skill overlap, we need a skills list
        # Use common tech skills as default
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'nodejs', 'sql', 'aws', 'docker',
            'machine learning', 'data analysis', 'project management', 'communication'
        ]
        skill_sim = self.skill_overlap_similarity(text1, text2, tech_skills)
        
        # Calculate weighted average
        combined = (
            weights['cosine'] * cosine_sim +
            weights['jaccard'] * jaccard_sim +
            weights['skill_overlap'] * skill_sim
        )
        
        return combined
    
    def calculate_text_similarity_matrix(self, texts: List[str]) -> np.ndarray:
        """
        Calculate similarity matrix for multiple texts.
        
        Args:
            texts (List[str]): List of texts
            
        Returns:
            np.ndarray: Similarity matrix
        """
        if not texts:
            return np.array([])
        
        n = len(texts)
        similarity_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    similarity_matrix[i][j] = 1.0
                else:
                    sim = self.cosine_similarity(texts[i], texts[j])
                    similarity_matrix[i][j] = sim
                    similarity_matrix[j][i] = sim
        
        return similarity_matrix


class ContentMatcher:
    """Matches content based on similarity and relevance."""
    
    def __init__(self):
        """Initialize the ContentMatcher."""
        self.similarity_calculator = SimilarityCalculator()
    
    def find_best_matches(self, query: str, candidates: List[str], 
                         top_k: int = 5, threshold: float = 0.1) -> List[Tuple[str, float]]:
        """
        Find best matching candidates for a query.
        
        Args:
            query (str): Query text
            candidates (List[str]): List of candidate texts
            top_k (int): Number of top matches to return
            threshold (float): Minimum similarity threshold
            
        Returns:
            List[Tuple[str, float]]: List of (candidate, similarity) tuples
        """
        if not query or not candidates:
            return []
        
        # Calculate similarities
        similarities = []
        for candidate in candidates:
            sim = self.similarity_calculator.combined_similarity(query, candidate)
            if sim >= threshold:
                similarities.append((candidate, sim))
        
        # Sort by similarity and return top K
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def match_resume_to_job(self, resume: str, job_description: str) -> Dict:
        """
        Match resume to job description.
        
        Args:
            resume (str): Resume text
            job_description (str): Job description text
            
        Returns:
            Dict: Matching results
        """
        if not resume or not job_description:
            return {
                'overall_similarity': 0.0,
                'skill_match': 0.0,
                'experience_match': 0.0,
                'missing_skills': []
            }
        
        # Calculate overall similarity
        overall_sim = self.similarity_calculator.combined_similarity(resume, job_description)
        
        # Extract skills (simplified approach)
        tech_skills = [
            'python', 'java', 'javascript', 'react', 'nodejs', 'sql', 'aws', 'docker',
            'machine learning', 'data analysis', 'project management', 'communication'
        ]
        
        resume_skills = [skill for skill in tech_skills if skill.lower() in resume.lower()]
        jd_skills = [skill for skill in tech_skills if skill.lower() in job_description.lower()]
        
        # Calculate skill match
        skill_match = 0.0
        if jd_skills:
            matched_skills = set(resume_skills).intersection(set(jd_skills))
            skill_match = len(matched_skills) / len(jd_skills)
        
        # Calculate experience match (simplified)
        experience_years = self._extract_experience_years(resume)
        required_experience = self._extract_experience_years(job_description)
        
        experience_match = 1.0
        if required_experience > 0:
            if experience_years >= required_experience:
                experience_match = 1.0
            else:
                experience_match = experience_years / required_experience
        
        # Find missing skills
        missing_skills = list(set(jd_skills) - set(resume_skills))
        
        return {
            'overall_similarity': overall_sim,
            'skill_match': skill_match,
            'experience_match': experience_match,
            'matched_skills': list(set(resume_skills).intersection(set(jd_skills))),
            'missing_skills': missing_skills,
            'resume_skills': resume_skills,
            'required_skills': jd_skills
        }
    
    def _extract_experience_years(self, text: str) -> int:
        """
        Extract years of experience from text.
        
        Args:
            text (str): Input text
            
        Returns:
            int: Years of experience
        """
        if not text:
            return 0
        
        # Look for patterns like "5 years experience", "3+ years", etc.
        patterns = [
            r'(\d+)\s*\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]*(\d+)\s*\+?\s*(?:years?|yrs?)',
            r'(\d+)\s*\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
        
        return 0
    
    def recommend_improvements(self, resume: str, job_description: str) -> List[str]:
        """
        Recommend improvements for resume based on job description.
        
        Args:
            resume (str): Resume text
            job_description (str): Job description text
            
        Returns:
            List[str]: List of improvement recommendations
        """
        match_results = self.match_resume_to_job(resume, job_description)
        recommendations = []
        
        # Skill-based recommendations
        if match_results['skill_match'] < 0.7:
            missing_skills = match_results['missing_skills'][:5]  # Top 5 missing skills
            if missing_skills:
                recommendations.append(f"Consider highlighting experience with: {', '.join(missing_skills)}")
        
        # Experience-based recommendations
        if match_results['experience_match'] < 0.8:
            recommendations.append("Consider emphasizing more relevant experience or achievements")
        
        # Overall similarity recommendations
        if match_results['overall_similarity'] < 0.5:
            recommendations.append("Try to align your resume more closely with the job requirements")
            recommendations.append("Include keywords from the job description in your resume")
        
        # Content length recommendations
        resume_words = len(resume.split())
        if resume_words < 200:
            recommendations.append("Consider expanding your resume with more detailed descriptions")
        elif resume_words > 800:
            recommendations.append("Consider making your resume more concise and focused")
        
        return recommendations


def main():
    """Test the similarity and matching functionality."""
    # Sample texts
    resume = """
    John Doe
    Software Engineer with 5 years of experience in Python, JavaScript, and React.
    Experienced in AWS, Docker, and machine learning projects.
    Strong communication and project management skills.
    """
    
    job_description = """
    Senior Software Engineer position requiring 5+ years of experience.
    Must have expertise in Python, JavaScript, React, and AWS.
    Experience with Docker and machine learning is a plus.
    Strong project management and communication skills required.
    """
    
    other_resumes = [
        "Data analyst with 3 years of experience in SQL and Excel.",
        "Marketing manager with expertise in digital marketing and team leadership.",
        "DevOps engineer experienced in Docker, Kubernetes, and cloud infrastructure.",
        "Business analyst with strong analytical and communication skills."
    ]
    
    print("🧪 SIMILARITY AND MATCHING TEST")
    print("=" * 50)
    
    # Test similarity calculator
    sim_calc = SimilarityCalculator()
    
    print("\n📊 Similarity Metrics:")
    cosine_sim = sim_calc.cosine_similarity(resume, job_description)
    jaccard_sim = sim_calc.jaccard_similarity(resume, job_description)
    combined_sim = sim_calc.combined_similarity(resume, job_description)
    
    print(f"   Cosine Similarity: {cosine_sim:.3f}")
    print(f"   Jaccard Similarity: {jaccard_sim:.3f}")
    print(f"   Combined Similarity: {combined_sim:.3f}")
    
    # Test content matcher
    matcher = ContentMatcher()
    
    print("\n🎯 Resume-Job Matching:")
    match_results = matcher.match_resume_to_job(resume, job_description)
    print(f"   Overall Similarity: {match_results['overall_similarity']:.3f}")
    print(f"   Skill Match: {match_results['skill_match']:.3f}")
    print(f"   Experience Match: {match_results['experience_match']:.3f}")
    print(f"   Matched Skills: {', '.join(match_results['matched_skills'])}")
    print(f"   Missing Skills: {', '.join(match_results['missing_skills'])}")
    
    # Test recommendations
    print("\n💡 Improvement Recommendations:")
    recommendations = matcher.recommend_improvements(resume, job_description)
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # Test finding best matches
    print("\n🔍 Best Matches for Resume:")
    best_matches = matcher.find_best_matches(resume, other_resumes, top_k=3)
    for i, (candidate, score) in enumerate(best_matches, 1):
        preview = candidate[:50] + "..." if len(candidate) > 50 else candidate
        print(f"   {i}. Score: {score:.3f} - {preview}")


if __name__ == "__main__":
    main()
