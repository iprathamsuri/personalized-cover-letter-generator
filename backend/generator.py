"""
Cover Letter Generator Module
Handles personalized cover letter generation using templates and NLP matching.
"""

from typing import Dict, List, Optional
import re


class CoverLetterGenerator:
    """Generates personalized cover letters using templates and matched content."""
    
    def __init__(self):
        """Initialize the Cover Letter Generator."""
        self.templates = {
            'fresher': self._get_fresher_template(),
            'experienced': self._get_experienced_template()
        }
    
    def _get_fresher_template(self) -> str:
        """Get template for fresher candidates."""
        return """Dear {hiring_manager},

I am writing to express my strong interest in the {position} position at {company}. As a recent graduate with a foundation in {key_skills}, I am excited to apply my academic knowledge and enthusiasm to contribute to your team.

{matched_content}

As a fresher, I bring a fresh perspective, strong willingness to learn, and dedication to mastering new technologies quickly. I am particularly drawn to {company} because of your commitment to {company_values} and would welcome the opportunity to grow with your organization.

I am available for an interview at your earliest convenience and look forward to discussing how my skills and enthusiasm can benefit your team.

Thank you for your time and consideration.

Sincerely,
{candidate_name}"""
    
    def _get_experienced_template(self) -> str:
        """Get template for experienced candidates."""
        return """Dear {hiring_manager},

I am writing to express my interest in the {position} position at {company}. With {years_experience} years of professional experience in {key_skills}, I am confident in my ability to contribute effectively to your team and help achieve your goals.

{matched_content}

Throughout my career, I have successfully {key_achievements}. My experience has taught me the importance of {professional_values}, which aligns perfectly with {company}'s commitment to {company_values}.

I am particularly excited about this opportunity because it allows me to leverage my expertise in {specialized_skills} while taking on new challenges in a dynamic environment.

I would welcome the opportunity to discuss how my background and skills can benefit your organization.

Thank you for your consideration.

Best regards,
{candidate_name}"""
    
    def extract_job_info(self, job_description: str) -> Dict[str, str]:
        """Extract key information from job description."""
        # Simple keyword extraction for common job elements
        info = {}
        
        # Extract position title
        position_patterns = [
            r'(?:position|role)[:\s]*[:\s]*(?:of|as)?[:\s]*([A-Za-z\s&]+?)(?:\s+developer|\s+engineer|\s+analyst|\s+manager|\s+specialist)',
            r'(?:software|data|full[-\s]?stack|mobile|web|dev[-\s]?ops)[\s]*([A-Za-z\s&]+?)(?:\s+developer|\s+engineer|\s+analyst|\s+manager|\s+specialist)'
        ]
        
        for pattern in position_patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                info['position'] = match.group(1).strip().title()
                break
        else:
            info['position'] = 'Professional'
        
        # Extract skills mentioned
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'nodejs', 'sql', 'aws',
            'docker', 'kubernetes', 'git', 'agile', 'scrum', 'machine learning',
            'data analysis', 'tensorflow', 'pytorch', 'django', 'flask',
            'mongodb', 'postgresql', 'restful api', 'microservices'
        ]
        
        found_skills = []
        for skill in skill_keywords:
            if skill.lower() in job_description.lower():
                found_skills.append(skill)
        
        info['skills'] = ', '.join(found_skills[:5])  # Limit to top 5
        
        # Extract experience level
        if any(word in job_description.lower() for word in ['fresher', 'entry', 'junior', 'trainee']):
            info['experience_level'] = 'fresher'
        elif any(word in job_description.lower() for word in ['senior', 'lead', 'principal', '5\+', '7\+', '10\+']):
            info['experience_level'] = 'experienced'
        else:
            info['experience_level'] = 'mid-level'
        
        # Extract company values/themes
        if any(word in job_description.lower() for word in ['innovative', 'cutting-edge', 'forward-thinking']):
            info['company_values'] = 'innovation'
        elif any(word in job_description.lower() for word in ['collaborative', 'team', 'diverse']):
            info['company_values'] = 'collaboration'
        elif any(word in job_description.lower() for word in ['growth', 'learning', 'development']):
            info['company_values'] = 'professional growth'
        else:
            info['company_values'] = 'excellence'
        
        return info
    
    def extract_user_info(self, user_input: str) -> Dict[str, str]:
        """Extract user information from input."""
        info = {}
        
        # Extract name (simple heuristic)
        lines = user_input.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['name:', 'my name is', 'i am']):
                # Extract name from line
                words = line.split()
                for i, word in enumerate(words):
                    if word[0].isupper() and len(word) > 2:
                        info['name'] = word
                        break
                break
        
        # Extract skills
        skill_patterns = [
            r'(?:skills?[:\s]*(?:include|are)[:\s]*)([A-Za-z\s,\(\)&]+)',
            r'(?:proficient|experienced|skilled)\s+in\s+([A-Za-z\s,\(\)&]+)'
        ]
        
        for pattern in skill_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                info['skills'] = match.group(1).strip()
                break
        
        # Extract experience
        if any(word in user_input.lower() for word in ['fresher', 'recent graduate', 'entry level', '0\s*year']):
            info['experience_level'] = 'fresher'
        elif any(word in user_input.lower() for word in ['year', 'years', 'experienced']):
            info['experience_level'] = 'experienced'
        else:
            info['experience_level'] = 'mid-level'
        
        # Set defaults if not found
        info.setdefault('name', 'Candidate')
        info.setdefault('skills', 'relevant technologies')
        info.setdefault('experience_level', 'mid-level')
        
        return info
    
    def generate_cover_letter(self, job_description: str, user_input: str, 
                          best_match_content: str = "") -> str:
        """
        Generate a personalized cover letter.
        
        Args:
            job_description: The job description text
            user_input: User's skills and experience information
            best_match_content: Best matching content from existing cover letters
            
        Returns:
            Generated personalized cover letter
        """
        # Extract information
        job_info = self.extract_job_info(job_description)
        user_info = self.extract_user_info(user_input)
        
        # Select appropriate template
        template = self.templates.get(user_info['experience_level'], self._get_fresher_template())
        
        # Prepare template variables
        template_vars = {
            'hiring_manager': 'Hiring Manager',
            'position': job_info['position'],
            'company': 'the Company',
            'key_skills': job_info['skills'],
            'matched_content': best_match_content,
            'years_experience': '2+' if user_info['experience_level'] == 'experienced' else '0',
            'candidate_name': user_info['name'],
            'company_values': job_info['company_values'],
            'key_achievements': 'delivered successful projects and met objectives',
            'professional_values': 'collaboration and excellence',
            'specialized_skills': user_info['skills']
        }
        
        # Generate cover letter
        try:
            cover_letter = template.format(**template_vars)
            
            # Post-processing
            cover_letter = self._clean_generated_text(cover_letter)
            
            return cover_letter
            
        except Exception as e:
            # Fallback to simple template
            return f"""Dear Hiring Manager,

I am writing to express my interest in the {job_info_position} position.
Based on my skills in {user_info_skills} and the job requirements, 
I believe I would be a valuable addition to your team.

{best_match_content[:200]}

Thank you for your consideration.

Sincerely,
{user_info_name}"""
    
    def _clean_generated_text(self, text: str) -> str:
        """Clean and format the generated text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common formatting issues
        text = text.replace(' ,', ', ')
        text = text.replace(' .', '. ')
        
        # Ensure proper spacing
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1\n\n\2', text)
        
        return text.strip()
    
    def get_generation_info(self) -> Dict[str, str]:
        """Get information about the generation capabilities."""
        return {
            'approach': 'Template-based with NLP content selection',
            'features': [
                'Dynamic template selection based on experience level',
                'Job description parsing for key information',
                'User input extraction for skills and experience',
                'Integration with existing NLP matching system',
                'Professional formatting and structure'
            ],
            'templates_available': list(self.templates.keys()),
            'supported_inputs': ['Job description text', 'User skills/experience text']
        }


if __name__ == "__main__":
    # Example usage
    generator = CoverLetterGenerator()
    
    # Sample job description
    sample_jd = """
    We are looking for a Software Developer with experience in Python and JavaScript. 
    The ideal candidate should have strong problem-solving skills and be familiar with modern web technologies.
    """
    
    # Sample user input
    sample_user = """
    My name is John Doe and I have 3 years of experience in Python, Django, and React.
    I am skilled in SQL, Git, and AWS deployment.
    """
    
    # Generate cover letter
    cover_letter = generator.generate_cover_letter(
        job_description=sample_jd,
        user_input=sample_user,
        best_match_content="Based on my experience in full-stack development, I have successfully delivered multiple web applications using Python and JavaScript frameworks."
    )
    
    print("Generated Cover Letter:")
    print("=" * 50)
    print(cover_letter)
