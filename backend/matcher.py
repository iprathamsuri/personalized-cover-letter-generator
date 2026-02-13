"""
Matcher Module
Advanced matching algorithms for cover letter generation and job matching
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Any
from similarity import SimilarityCalculator, ContentMatcher
from vectorizer import TextVectorizer, SkillExtractor
import re


class AdvancedMatcher:
    """Advanced matching algorithms for cover letters and jobs."""
    
    def __init__(self):
        """Initialize the AdvancedMatcher."""
        self.similarity_calculator = SimilarityCalculator()
        self.content_matcher = ContentMatcher()
        self.vectorizer = TextVectorizer("tfidf", max_features=1000)
        self.skill_extractor = SkillExtractor()
        
        # Pre-defined templates for different experience levels
        self.experience_keywords = {
            'fresher': ['entry level', 'junior', 'recent graduate', 'new', 'beginner', 'trainee', 'intern'],
            'mid-level': ['intermediate', 'mid-level', 'experienced', 'professional', 'skilled'],
            'senior': ['senior', 'lead', 'principal', 'expert', 'advanced', 'specialist'],
            'expert': ['expert', 'architect', 'head', 'chief', 'director', 'vp', 'executive']
        }
    
    def match_cover_letter_to_job(self, cover_letter: str, job_description: str, 
                                 resume_text: str = "") -> Dict[str, Any]:
        """
        Advanced matching of cover letter to job description.
        
        Args:
            cover_letter (str): Generated cover letter
            job_description (str): Job description
            resume_text (str): Original resume text (optional)
            
        Returns:
            Dict[str, Any]: Comprehensive matching results
        """
        if not cover_letter or not job_description:
            return self._empty_match_result()
        
        # Calculate various similarity metrics
        results = {
            'overall_score': 0.0,
            'content_similarity': 0.0,
            'skill_alignment': 0.0,
            'tone_appropriateness': 0.0,
            'length_appropriateness': 0.0,
            'keyword_coverage': 0.0,
            'experience_level_match': 0.0,
            'detailed_analysis': {}
        }
        
        # Content similarity
        results['content_similarity'] = self.similarity_calculator.combined_similarity(
            cover_letter, job_description
        )
        
        # Skill alignment
        results['skill_alignment'] = self._calculate_skill_alignment(
            cover_letter, job_description, resume_text
        )
        
        # Tone appropriateness
        results['tone_appropriateness'] = self._analyze_tone_appropriateness(
            cover_letter, job_description
        )
        
        # Length appropriateness
        results['length_appropriateness'] = self._analyze_length_appropriateness(
            cover_letter
        )
        
        # Keyword coverage
        results['keyword_coverage'] = self._calculate_keyword_coverage(
            cover_letter, job_description
        )
        
        # Experience level match
        results['experience_level_match'] = self._match_experience_level(
            cover_letter, job_description, resume_text
        )
        
        # Calculate overall score
        weights = {
            'content_similarity': 0.3,
            'skill_alignment': 0.25,
            'tone_appropriateness': 0.15,
            'length_appropriateness': 0.1,
            'keyword_coverage': 0.15,
            'experience_level_match': 0.05
        }
        
        results['overall_score'] = sum(
            results[metric] * weights[metric] for metric in weights
        )
        
        # Detailed analysis
        results['detailed_analysis'] = self._generate_detailed_analysis(
            cover_letter, job_description, resume_text, results
        )
        
        return results
    
    def _empty_match_result(self) -> Dict[str, Any]:
        """Return empty match result."""
        return {
            'overall_score': 0.0,
            'content_similarity': 0.0,
            'skill_alignment': 0.0,
            'tone_appropriateness': 0.0,
            'length_appropriateness': 0.0,
            'keyword_coverage': 0.0,
            'experience_level_match': 0.0,
            'detailed_analysis': {'error': 'Empty input provided'}
        }
    
    def _calculate_skill_alignment(self, cover_letter: str, job_description: str, 
                                resume_text: str) -> float:
        """Calculate skill alignment between cover letter and job requirements."""
        # Extract skills from all sources
        cl_skills = self.skill_extractor.extract_skills(cover_letter)
        jd_skills = self.skill_extractor.extract_skills(job_description)
        
        all_cl_skills = []
        for category_skills in cl_skills.values():
            all_cl_skills.extend(category_skills)
        
        all_jd_skills = []
        for category_skills in jd_skills.values():
            all_jd_skills.extend(category_skills)
        
        if not all_jd_skills:
            return 0.0
        
        # Calculate alignment
        matched_skills = set(all_cl_skills).intersection(set(all_jd_skills))
        alignment = len(matched_skills) / len(all_jd_skills)
        
        return min(alignment, 1.0)
    
    def _analyze_tone_appropriateness(self, cover_letter: str, job_description: str) -> float:
        """Analyze if the tone of the cover letter is appropriate for the job."""
        # Define tone indicators
        formal_indicators = ['sincerely', 'respectfully', 'dear', 'regards', 'faithfully']
        casual_indicators = ['hey', 'hi', 'guys', 'awesome', 'cool', 'great']
        enthusiastic_indicators = ['excited', 'thrilled', 'passionate', 'eager', 'enthusiastic']
        
        cl_lower = cover_letter.lower()
        jd_lower = job_description.lower()
        
        # Detect tone from job description
        jd_formal = any(indicator in jd_lower for indicator in formal_indicators)
        jd_casual = any(indicator in jd_lower for indicator in casual_indicators)
        jd_enthusiastic = any(indicator in jd_lower for indicator in enthusiastic_indicators)
        
        # Detect tone from cover letter
        cl_formal = any(indicator in cl_lower for indicator in formal_indicators)
        cl_casual = any(indicator in cl_lower for indicator in casual_indicators)
        cl_enthusiastic = any(indicator in cl_lower for indicator in enthusiastic_indicators)
        
        # Calculate appropriateness score
        score = 0.0
        
        if jd_formal and cl_formal:
            score += 0.4
        elif not jd_formal and not cl_formal:
            score += 0.3
        elif jd_formal and not cl_formal:
            score += 0.1
        
        if jd_enthusiastic and cl_enthusiastic:
            score += 0.3
        elif not jd_enthusiastic and not cl_enthusiastic:
            score += 0.2
        elif jd_enthusiastic and not cl_enthusiastic:
            score += 0.1
        
        if not jd_casual and not cl_casual:
            score += 0.3
        elif jd_casual and cl_casual:
            score += 0.2
        elif jd_casual and not cl_casual:
            score += 0.1
        
        return min(score, 1.0)
    
    def _analyze_length_appropriateness(self, cover_letter: str) -> float:
        """Analyze if the length of the cover letter is appropriate."""
        word_count = len(cover_letter.split())
        
        # Ideal range: 200-500 words
        if 200 <= word_count <= 500:
            return 1.0
        elif 150 <= word_count < 200 or 500 < word_count <= 600:
            return 0.8
        elif 100 <= word_count < 150 or 600 < word_count <= 700:
            return 0.6
        elif 50 <= word_count < 100 or 700 < word_count <= 800:
            return 0.4
        else:
            return 0.2
    
    def _calculate_keyword_coverage(self, cover_letter: str, job_description: str) -> float:
        """Calculate how well the cover letter covers keywords from the job description."""
        # Extract important keywords from job description
        jd_words = re.findall(r'\b\w+\b', job_description.lower())
        
        # Filter out common words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
                     'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
                     'how', 'man', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
                     'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use'}
        
        important_jd_words = [word for word in jd_words if word not in stop_words and len(word) > 3]
        
        if not important_jd_words:
            return 0.0
        
        # Check coverage in cover letter
        cl_words = re.findall(r'\b\w+\b', cover_letter.lower())
        covered_words = set(important_jd_words).intersection(set(cl_words))
        
        coverage = len(covered_words) / len(important_jd_words)
        
        return min(coverage, 1.0)
    
    def _match_experience_level(self, cover_letter: str, job_description: str, 
                             resume_text: str) -> float:
        """Match experience level between cover letter and job requirements."""
        # Detect experience level from job description
        jd_level = self._detect_experience_level(job_description)
        
        # Detect experience level from cover letter and resume
        combined_text = cover_letter + " " + resume_text
        cl_level = self._detect_experience_level(combined_text)
        
        # Calculate match
        if jd_level == cl_level:
            return 1.0
        elif self._is_adjacent_level(jd_level, cl_level):
            return 0.7
        else:
            return 0.3
    
    def _detect_experience_level(self, text: str) -> str:
        """Detect experience level from text."""
        text_lower = text.lower()
        
        level_scores = {}
        for level, keywords in self.experience_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            level_scores[level] = score
        
        if not level_scores:
            return 'mid-level'  # Default
        
        return max(level_scores, key=level_scores.get)
    
    def _is_adjacent_level(self, level1: str, level2: str) -> bool:
        """Check if two experience levels are adjacent."""
        level_order = ['fresher', 'mid-level', 'senior', 'expert']
        
        try:
            idx1 = level_order.index(level1)
            idx2 = level_order.index(level2)
            return abs(idx1 - idx2) == 1
        except ValueError:
            return False
    
    def _generate_detailed_analysis(self, cover_letter: str, job_description: str, 
                                resume_text: str, results: Dict) -> Dict[str, Any]:
        """Generate detailed analysis of the matching results."""
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'recommendations': [],
            'metrics_breakdown': {}
        }
        
        # Strengths
        if results['content_similarity'] > 0.7:
            analysis['strengths'].append("Strong content alignment with job requirements")
        
        if results['skill_alignment'] > 0.8:
            analysis['strengths'].append("Excellent skill coverage")
        
        if results['tone_appropriateness'] > 0.8:
            analysis['strengths'].append("Appropriate professional tone")
        
        if results['length_appropriateness'] > 0.8:
            analysis['strengths'].append("Appropriate cover letter length")
        
        # Weaknesses
        if results['content_similarity'] < 0.4:
            analysis['weaknesses'].append("Low content alignment with job requirements")
        
        if results['skill_alignment'] < 0.5:
            analysis['weaknesses'].append("Insufficient skill coverage")
        
        if results['tone_appropriateness'] < 0.5:
            analysis['weaknesses'].append("Inappropriate tone for this position")
        
        if results['length_appropriateness'] < 0.5:
            analysis['weaknesses'].append("Inappropriate cover letter length")
        
        # Recommendations
        if results['skill_alignment'] < 0.6:
            analysis['recommendations'].append("Include more relevant skills from the job description")
        
        if results['keyword_coverage'] < 0.5:
            analysis['recommendations'].append("Incorporate more keywords from the job posting")
        
        if results['length_appropriateness'] < 0.6:
            word_count = len(cover_letter.split())
            if word_count < 200:
                analysis['recommendations'].append("Expand your cover letter with more details")
            else:
                analysis['recommendations'].append("Make your cover letter more concise")
        
        # Metrics breakdown
        analysis['metrics_breakdown'] = {
            'Content Similarity': f"{results['content_similarity']:.2%}",
            'Skill Alignment': f"{results['skill_alignment']:.2%}",
            'Tone Appropriateness': f"{results['tone_appropriateness']:.2%}",
            'Length Appropriateness': f"{results['length_appropriateness']:.2%}",
            'Keyword Coverage': f"{results['keyword_coverage']:.2%}",
            'Experience Level Match': f"{results['experience_level_match']:.2%}"
        }
        
        return analysis
    
    def find_best_template_match(self, job_description: str, resume_text: str, 
                                templates: Dict[str, List[str]]) -> str:
        """
        Find the best template match for given job and resume.
        
        Args:
            job_description (str): Job description
            resume_text (str): Resume text
            templates (Dict[str, List[str]]): Templates by experience level
            
        Returns:
            str: Best matching template
        """
        if not job_description or not resume_text or not templates:
            return 'mid-level'  # Default
        
        # Detect experience level
        combined_text = job_description + " " + resume_text
        detected_level = self._detect_experience_level(combined_text)
        
        # Return template for detected level, fallback to mid-level
        return templates.get(detected_level, templates.get('mid-level', []))[0] if templates.get(detected_level) else 'mid-level'
    
    def batch_analyze_cover_letters(self, cover_letters: List[str], 
                                    job_description: str) -> List[Dict[str, Any]]:
        """
        Analyze multiple cover letters against a job description.
        
        Args:
            cover_letters (List[str]): List of cover letters
            job_description (str): Job description
            
        Returns:
            List[Dict[str, Any]]: Analysis results for each cover letter
        """
        results = []
        
        for i, cover_letter in enumerate(cover_letters):
            result = self.match_cover_letter_to_job(cover_letter, job_description)
            result['index'] = i
            result['word_count'] = len(cover_letter.split())
            results.append(result)
        
        # Sort by overall score
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return results


def main():
    """Test the advanced matching functionality."""
    # Sample data
    cover_letter = """
    Dear Hiring Manager,
    
    I am writing to express my strong interest in the Senior Software Engineer position at TechCorp. 
    With over 6 years of experience in software development, I have developed expertise in Python, 
    JavaScript, and React. I am particularly skilled in building scalable web applications and 
    leading development teams.
    
    My experience includes working with AWS, Docker, and machine learning projects. I am passionate 
    about creating innovative solutions and mentoring junior developers.
    
    Thank you for your consideration.
    
    Sincerely,
    John Doe
    """
    
    job_description = """
    Senior Software Engineer position requiring 5+ years of experience.
    Must have expertise in Python, JavaScript, React, and cloud technologies.
    Experience with Docker, AWS, and team leadership is required.
    Looking for candidates passionate about innovation and mentoring.
    """
    
    resume_text = """
    John Doe - Senior Software Engineer
    6 years of experience in full-stack development
    Skills: Python, JavaScript, React, Node.js, AWS, Docker, Kubernetes
    Led teams of 5-8 developers on multiple projects
    Implemented machine learning solutions for data analysis
    """
    
    print("🧪 ADVANCED MATCHING TEST")
    print("=" * 50)
    
    # Test advanced matcher
    matcher = AdvancedMatcher()
    
    print("\n🎯 Comprehensive Matching Analysis:")
    results = matcher.match_cover_letter_to_job(cover_letter, job_description, resume_text)
    
    print(f"   Overall Score: {results['overall_score']:.3f}")
    print(f"   Content Similarity: {results['content_similarity']:.3f}")
    print(f"   Skill Alignment: {results['skill_alignment']:.3f}")
    print(f"   Tone Appropriateness: {results['tone_appropriateness']:.3f}")
    print(f"   Length Appropriateness: {results['length_appropriateness']:.3f}")
    print(f"   Keyword Coverage: {results['keyword_coverage']:.3f}")
    print(f"   Experience Level Match: {results['experience_level_match']:.3f}")
    
    print("\n📊 Detailed Analysis:")
    analysis = results['detailed_analysis']
    
    print("   Strengths:")
    for strength in analysis['strengths']:
        print(f"     • {strength}")
    
    print("   Weaknesses:")
    for weakness in analysis['weaknesses']:
        print(f"     • {weakness}")
    
    print("   Recommendations:")
    for rec in analysis['recommendations']:
        print(f"     • {rec}")
    
    print("\n📈 Metrics Breakdown:")
    for metric, value in analysis['metrics_breakdown'].items():
        print(f"   {metric}: {value}")


if __name__ == "__main__":
    main()
