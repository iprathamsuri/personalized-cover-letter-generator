"""
Advanced Cover Letter Generator Module
Basic implementation for web server functionality
"""

from typing import Dict, List, Optional, Tuple
import re
import random
from datetime import datetime


class CoverLetterGenerator:
    """Advanced cover letter generator with dynamic personalization."""
    
    def __init__(self):
        """Initialize the Advanced Cover Letter Generator."""
        # Don't set a fixed seed to allow for true randomness and variation
        # The system time will naturally provide variation between runs
        pass
        
        self.templates = {
            'fresher': self._get_fresher_templates(),
            'experienced': self._get_experienced_templates(),
            'mid-level': self._get_mid_level_templates()
        }
        
        # Enhanced skill database with more web technologies
        self.skill_database = {
            'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust'],
            'web': ['react', 'vue', 'angular', 'nodejs', 'express', 'django', 'flask', 'spring', 'html', 'css', 'html5', 'css3'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'database'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
            'ai_ml': ['machine learning', 'tensorflow', 'pytorch', 'nlp', 'computer vision'],
            'tools': ['git', 'agile', 'scrum', 'jenkins', 'ci/cd', 'linux', 'windows']
        }
        
        # Dynamic opening phrases
        self.opening_phrases = [
            "I am writing to express my strong interest in the",
            "I am excited to apply for the",
            "I am thrilled to submit my application for the",
            "I would like to express my enthusiasm for the",
            "I am delighted to apply for the position of"
        ]
        
        # Dynamic closing phrases
        self.closing_phrases = [
            "I look forward to discussing how my skills and experience can benefit your team.",
            "I am eager to explore how my background aligns with your needs.",
            "I would welcome the opportunity to discuss my qualifications further.",
            "I appreciate your time and consideration of my application.",
            "Thank you for reviewing my application. I am excited about the possibility of contributing to your team."
        ]
    
    def _get_fresher_templates(self) -> List[str]:
        """Get templates for freshers/entry-level positions."""
        return [
            """Dear {hiring_manager},

{opening_phrase} {position} position at {company}. As a recent graduate with a strong foundation in {key_skills}, I am eager to bring my fresh perspective and enthusiasm to your team.

During my academic career, I developed expertise in {specialized_skills} through coursework and projects. My experience with {matched_content} has prepared me to contribute effectively to your team's objectives. I've worked on several projects that required me to apply theoretical knowledge to real-world challenges, which has strengthened my problem-solving abilities.

I am particularly drawn to {company} because of your commitment to {company_values}. This aligns perfectly with my own values of {professional_values} and my desire to work for an organization that values innovation and growth. Your company's work in {dynamic_content} especially resonates with my career aspirations.

As a fresher, I bring a unique combination of theoretical knowledge and practical skills. I am a quick learner, adaptable, and passionate about {key_skills}. My academic projects have honed my problem-solving abilities and taught me the importance of collaboration and attention to detail. I believe my fresh perspective could bring new ideas to your team.

I would welcome the opportunity to discuss how my education, skills, and enthusiasm can benefit {company}. Thank you for considering my application.

{closing_phrase}

{candidate_name}""",
            
            """Dear {hiring_manager},

{opening_phrase} {position} role at {company}. As a motivated recent graduate with comprehensive training in {key_skills}, I am excited to begin my professional journey with a forward-thinking organization like yours.

My academic background has provided me with a solid foundation in {specialized_skills}, complemented by hands-on experience through various projects and internships. I have developed strong analytical and problem-solving skills that I am eager to apply in a professional setting. During my internships, I had the opportunity to work on real-world projects that taught me the importance of teamwork and meeting deadlines.

What particularly attracts me to {company} is your reputation for {company_values}. I am impressed by your innovative approach to {dynamic_content} and believe my fresh perspective and eagerness to learn would make me a valuable addition to your team. I've been following {company}'s projects and am particularly inspired by your recent work.

As a recent graduate, I offer a unique combination of up-to-date theoretical knowledge and practical application skills. I am proficient in {key_skills} and have demonstrated my ability to quickly adapt to new technologies and methodologies. I'm excited about the opportunity to contribute my energy and fresh ideas to your established team.

I am excited about the possibility of contributing my skills and enthusiasm to {company}. I would appreciate the opportunity to discuss how I can add value to your team.

{closing_phrase}

{candidate_name}"""
        ]
    
    def _get_experienced_templates(self) -> List[str]:
        """Get templates for experienced professionals."""
        return [
            """Dear {hiring_manager},

{opening_phrase} {position} position at {company}. With {years_experience} of professional experience in {key_skills}, I am confident that my expertise aligns perfectly with your requirements.

Throughout my career, I have consistently demonstrated excellence in {specialized_skills}. My experience with {matched_content} has enabled me to deliver measurable results and drive successful outcomes for my employers. I am particularly proud of my achievements in {key_achievements}, where I successfully led cross-functional teams to deliver projects ahead of schedule.

I have been following {company}'s work for some time and am deeply impressed by your commitment to {company_values}. Your innovative approach to {dynamic_content} resonates with my own professional philosophy and career aspirations. I particularly admire how {company} has positioned itself as a leader in the industry, and I'm excited about the possibility of contributing to your continued growth.

My professional journey has equipped me with comprehensive expertise in {key_skills}. I have successfully led projects, mentored team members, and contributed to strategic initiatives that have delivered significant business value. My ability to combine technical excellence with strategic thinking makes me an ideal candidate for this role. I believe my experience in navigating complex challenges would be valuable to your team.

I would welcome the opportunity to discuss how my experience and skills can contribute to {company}'s continued success. Thank you for considering my application.

{closing_phrase}

{candidate_name}""",
            
            """Dear {hiring_manager},

{opening_phrase} {position} opportunity at {company}. As a seasoned professional with {years_experience} of experience specializing in {key_skills}, I am excited about the possibility of bringing my expertise to your esteemed organization.

My professional background includes extensive work in {specialized_skills}, where I have consistently delivered exceptional results. My experience with {matched_content} has prepared me to tackle complex challenges and drive meaningful impact. I have a proven track record of {key_achievements}.

{company}'s reputation for excellence in {company_values} is well-known in our industry, and I am particularly drawn to your innovative approach to {dynamic_content}. I believe my experience and professional philosophy align perfectly with your organizational values and objectives.

Over the course of my career, I have developed deep expertise in {key_skills}, complemented by strong leadership abilities and strategic thinking. I have successfully managed complex projects, mentored junior professionals, and contributed to organizational growth and innovation.

I am eager to discuss how my background and expertise can benefit {company}. Thank you for your time and consideration.

{closing_phrase}

{candidate_name}"""
        ]
    
    def _get_mid_level_templates(self) -> List[str]:
        """Get templates for mid-level professionals."""
        return [
            """Dear {hiring_manager},

{opening_phrase} {position} position at {company}. With {years_experience} of experience in {key_skills}, I have developed the expertise and professional maturity needed to excel in this role and contribute meaningfully to your team.

My career has been focused on building comprehensive skills in {specialized_skills}. Through various roles and projects, I have gained hands-on experience with {matched_content}, which has prepared me to handle the responsibilities outlined in your job description. I am particularly proud of my contributions to {key_achievements}, where I successfully delivered projects that exceeded expectations and drove measurable business impact.

I have long admired {company}'s commitment to {company_values} and your innovative approach to {dynamic_content}. Your organization's culture of excellence and continuous learning aligns perfectly with my professional values and career aspirations. I've been particularly impressed by how {company} fosters innovation while maintaining high standards of quality.

As a mid-level professional, I bring a balanced combination of technical expertise and business acumen. I have experience in {key_skills} and have developed strong problem-solving abilities, project management skills, and the capacity to work effectively in cross-functional teams. I believe my experience in bridging technical solutions with business needs would be valuable to your organization.

{closing_phrase}

Thank you for your consideration.

Sincerely,
{candidate_name}""",
            
            """Dear {hiring_manager},

{opening_phrase} {position} role at {company}. As a professional with {years_experience} of experience in {key_skills}, I have developed the skills and expertise needed to make an immediate and meaningful contribution to your organization.

My professional journey has been characterized by continuous growth and learning in {specialized_skills}. I have gained valuable experience working with {matched_content}, which has equipped me to handle diverse challenges and deliver consistent results. My key achievements include {key_achievements}.

{company}'s reputation for excellence in {company_values} and your forward-thinking approach to {dynamic_content} make you an ideal employer for professionals seeking growth and impact. I am particularly impressed by your commitment to innovation and professional development.

With my background in {key_skills}, I offer a unique blend of technical proficiency and business understanding. I have experience leading projects, collaborating with diverse teams, and delivering solutions that drive business value and customer satisfaction.

I am enthusiastic about the opportunity to contribute my skills and experience to {company}. I would appreciate the chance to discuss how I can add value to your team.

{closing_phrase}

{candidate_name}"""
        ]
    
    def extract_job_info(self, job_description: str) -> Dict:
        """Extract key information from job description."""
        if not job_description:
            return {}
        
        # Extract position - improved patterns
        position_patterns = [
            r'(?:position|role|job title)[:\s]+([^\n]+)',
            r'(?:position|role|job title)[:\s]+([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:hiring|seeking|looking for)\s+(?:a|an)?\s*([^\n]+?(?:engineer|developer|manager|analyst|specialist)[^\n]*)',
            r'(?:software|data|marketing|sales)\s+(?:engineer|developer|manager|analyst|specialist)',
            r'(?:we are|we\'re)\s+(?:looking for|hiring|seeking)\s+(?:a|an)?\s*([^\n]+?(?:engineer|developer|manager|analyst|specialist)[^\n]*)',
            r'(?:Fresher|Junior|Senior|Lead|Principal)\s+([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*\((?:Fresher|Junior|Senior|Lead|Principal)\)',
            r'(?:engineer|developer|manager|analyst|specialist)'
        ]
        
        position = "Professional"
        for pattern in position_patterns:
            match = re.search(pattern, job_description, re.IGNORECASE)
            if match:
                if pattern == r'(?:engineer|developer|manager|analyst|specialist)':
                    # For this pattern, we need to get more context
                    position = match.group(0).strip()
                    print(f"🔍 Debug: Position extracted (general) - Pattern: {pattern}, Position: {position}")
                else:
                    position = match.group(1).strip()
                    print(f"🔍 Debug: Position extracted (specific) - Pattern: {pattern}, Raw: {match.group(1)}")
                    # Clean up the position - remove trailing phrases and extra words
                    position = match.group(1).strip()
                    
                    # First, limit to reasonable length and remove line breaks
                    position = position.split('\n')[0].strip()
                    position = re.sub(r'\s+', ' ', position)  # Normalize whitespace
                    
                    # Remove experience level indicators in parentheses first
                    position = re.sub(r'\s*\([^)]*\)', '', position).strip()
                    
                    # Remove trailing phrases ONLY after specific keywords, not after the main position
                    position = re.sub(r'\s+(?:with|for|who|that|and|the|a|an|to|join|our|innovative|team|experience|required|looking|team).*$', '', position, flags=re.IGNORECASE)
                    position = re.sub(r'[.!?]+$', '', position).strip()
                    
                    # Only remove trailing position/role/job if they're standalone words
                    position = re.sub(r'\s+(?:position|role|job)$', '', position, flags=re.IGNORECASE).strip()
                    
                    # Remove leading experience level indicators
                    position = re.sub(r'^(?:Fresher|Junior|Senior|Lead|Principal)\s+', '', position, flags=re.IGNORECASE).strip()
                    
                    print(f"🔍 Debug: Position after cleaning: {position}")
                break
        else:
            print(f"🔍 Debug: No position found in job_description: {job_description[:100]}...")
        
        # Extract skills
        skills = []
        for category, skill_list in self.skill_database.items():
            for skill in skill_list:
                if skill.lower() in job_description.lower():
                    skills.append(skill)
        
        # Extract company values
        values_keywords = ['innovation', 'excellence', 'collaboration', 'growth', 'integrity', 'diversity', 'customer focus']
        company_values = []
        for value in values_keywords:
            if value.lower() in job_description.lower():
                company_values.append(value)
        
        return {
            'position': position,
            'skills': ', '.join(skills[:5]) if skills else 'relevant technologies',
            'company_values': ', '.join(company_values[:3]) if company_values else 'innovation and excellence'
        }
    
    def extract_user_info(self, user_input: str) -> Dict:
        """Extract key information from user input."""
        if not user_input:
            return {}
        
        # Extract name (improved heuristic)
        name_patterns = [
            # Name after years enhancement (web server format)
            r'I have \d+ years of experience\.?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            # Name at very beginning (resume format) - first line only
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            # Explicit name statements
            r'(?:my name is|i am|i\'m)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:is|am|have|possess)',
            # Name label pattern (for resume format)
            r'Name[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            # Name at beginning of input
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[,.]?\s*(?:have|am|with|experienced)',
            # Name with experience patterns
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:with|having)\s+\d+\s*(?:years?|yrs?)',
            # Simple name followed by skills
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[,-]?\s*(?:experienced|skilled|proficient)',
            # Name followed by numbers (years of experience)
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+\d+',
            # Just a name at the start (fallback)
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        
        name = "Candidate"
        print(f"🔍 Debug: Extracting name from user_input: {user_input[:200]}...")
        for i, pattern in enumerate(name_patterns):
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                extracted_name = match.group(1).strip()
                print(f"🔍 Debug: Pattern {i+1} matched: {extracted_name}")
                # Validate that it looks like a real name (2+ letters, starts with capital)
                if len(extracted_name) >= 2 and extracted_name[0].isupper():
                    name = extracted_name
                    print(f"🔍 Debug: Name extracted successfully: {name}")
                    break
                else:
                    print(f"🔍 Debug: Name validation failed: {extracted_name}")
            else:
                print(f"🔍 Debug: Pattern {i+1} no match: {pattern}")
        
        print(f"🔍 Debug: Final name result: {name}")
        
        # Extract experience - improved patterns
        experience_patterns = [
            r'(\d+)\s*(?:years?|yr)s?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\s*\+\s*(?:years?|yr)s?\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]+(\d+)\s*(?:years?|yr)s?',
            r'(\d+)\s*(?:years?|yr)s?\s*(?:of\s*)?(?:professional|work|software)',
            r'(?:have|with|possess)\s+(\d+)\s*(?:years?|yr)s?',
            r'(\d+)\s*(?:years?|yr)s?\s+(?:of\s*)?(?:experience|exp|work|practice)'
        ]
        
        years = "0 years"
        for pattern in experience_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                years = match.group(1) + " years"
                print(f"🔍 Debug: Experience extracted - Pattern: {pattern}, Match: {match.group(1)}, Years: {years}")
                break
        else:
            print(f"🔍 Debug: No experience found in user_input: {user_input[:100]}...")
        
        # Extract skills
        skills = []
        for category, skill_list in self.skill_database.items():
            for skill in skill_list:
                if skill.lower() in user_input.lower():
                    skills.append(skill)
        
        # Extract achievements
        achievement_keywords = ['developed', 'created', 'implemented', 'led', 'managed', 'achieved', 'improved', 'optimized']
        achievements = []
        for keyword in achievement_keywords:
            if keyword.lower() in user_input.lower():
                achievements.append(keyword)
        
        return {
            'name': name,
            'years': years,
            'skills': ', '.join(skills[:5]) if skills else 'relevant technologies',
            'achievements': ', '.join(achievements[:3]) if achievements else 'delivering successful projects',
            'experience_level': self._determine_experience_level(years)
        }
    
    def debug_extract_user_info(self, user_input: str) -> Dict:
        """Debug version to see what's being extracted."""
        result = self.extract_user_info(user_input)
        print(f"🔍 Generator Debug - Extracted: {result}")
        return result
    
    def _determine_experience_level(self, years: str) -> str:
        """Determine experience level from years string."""
        try:
            years_num = int(re.findall(r'\d+', years)[0])
            if years_num < 2:
                return 'fresher'
            elif years_num < 5:
                return 'mid-level'
            else:
                return 'experienced'
        except:
            return 'mid-level'
    
    def _determine_tone(self, job_info: Dict, user_info: Dict) -> str:
        """Determine appropriate tone based on context."""
        if not job_info or not user_info:
            return 'professional'
        
        # Analyze job description for tone indicators
        jd_lower = str(job_info).lower()
        
        if any(word in jd_lower for word in ['innovative', 'dynamic', 'fast-paced', 'startup']):
            return 'enthusiastic'
        elif any(word in jd_lower for word in ['corporate', 'enterprise', 'formal', 'professional']):
            return 'formal'
        else:
            return 'professional'
    
    def _generate_dynamic_content(self, job_info: Dict, user_info: Dict) -> str:
        """Generate dynamic content based on context."""
        if not job_info or not user_info:
            return "professional growth and development"
        
        user_skills = user_info.get('skills', '').lower()
        job_skills = job_info.get('skills', '').lower()
        
        # Find common skills
        common_skills = []
        if user_skills and job_skills:
            user_skill_list = [skill.strip().lower() for skill in user_skills.split(',')]
            job_skill_list = [skill.strip().lower() for skill in job_skills.split(',')]
            common_skills = list(set(user_skill_list) & set(job_skill_list))
        
        if common_skills:
            return f"expertise in {', '.join(common_skills[:3])}"
        else:
            return "professional growth and development"
    
    def _enhance_natural_flow(self, text: str) -> str:
        """Enhance natural flow and readability."""
        # Remove repetitive phrases
        text = re.sub(r'\b(I am|I have|I believe)\s+\1+', r'\1', text, flags=re.IGNORECASE)
        
        # Clean up trailing 'and' in signatures and other places
        text = re.sub(r'([A-Z][a-z\s]+)\s+and\s*$', r'\1', text, flags=re.MULTILINE)
        text = re.sub(r'([A-Z][a-z]+)\s+and\s*$', r'\1', text, flags=re.MULTILINE)
        
        # Remove duplicate closing sentences
        lines = text.split('\n')
        cleaned_lines = []
        seen_lines = set()
        
        for line in lines:
            line = line.strip()
            if line and line not in seen_lines:
                cleaned_lines.append(line)
                seen_lines.add(line)
            elif not line:  # Keep empty lines for paragraph breaks
                cleaned_lines.append(line)
        
        text = '\n'.join(cleaned_lines)
        
        # Only add transitions where appropriate (not too many)
        # This was adding too many "Additionally" - let's remove it for now
        # text = re.sub(r'\. ([A-Z])', r'. Additionally, \1', text)
        
        return text
    
    def _clean_generated_text(self, text: str) -> str:
        """Clean and format generated text."""
        # First, preserve all newlines by temporarily replacing them
        text = text.replace('\n\n', '<<PARAGRAPH_BREAK>>')
        text = text.replace('\n', '<<LINE_BREAK>>')
        
        # Remove extra whitespace but preserve paragraph breaks
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Restore paragraph breaks first, then line breaks
        text = text.replace('<<PARAGRAPH_BREAK>>', '\n\n')
        text = text.replace('<<LINE_BREAK>>', '\n')
        
        # Clean up any extra spaces around newlines
        text = re.sub(r' \n', '\n', text)
        text = re.sub(r'\n ', '\n', text)
        
        # Fix common text issues
        text = re.sub(r'\b(for for|the the|and and|in in)\b', lambda m: m.group(0).split()[0], text, flags=re.IGNORECASE)
        
        # Ensure proper spacing around punctuation, but preserve paragraphs
        # First preserve paragraphs
        text = text.replace('\n\n', '<<TEMP_PARAGRAPH>>')
        text = re.sub(r'\s*([,.!?])\s*', r'\1 ', text)
        text = text.replace('<<TEMP_PARAGRAPH>>', '\n\n')
        
        # Remove duplicate sentences while preserving paragraphs
        # Split into paragraphs first
        paragraphs = text.split('\n\n')
        unique_paragraphs = []
        
        for paragraph in paragraphs:
            # Process each paragraph for duplicate sentences
            sentences = paragraph.split('. ')
            unique_sentences = []
            seen = set()
            
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence and sentence not in seen:
                    unique_sentences.append(sentence)
                    seen.add(sentence)
            
            # Reconstruct the paragraph
            reconstructed_paragraph = '. '.join(unique_sentences)
            unique_paragraphs.append(reconstructed_paragraph)
        
        # Rejoin paragraphs
        return '\n\n'.join(unique_paragraphs)
    
    def generate_cover_letter(self, job_description: str, user_input: str, 
                            best_match_content: str = "", company: str = "", experience_level: str = "", target_role: str = "") -> str:
        """Generate a personalized cover letter."""
        job_info = self.extract_job_info(job_description)
        user_info = self.extract_user_info(user_input)
        
        # Determine experience level if not provided
        if not experience_level:
            experience_level = user_info.get('experience_level', 'mid-level')
        
        # Select appropriate template
        template = random.choice(self.templates.get(experience_level, self.templates['mid-level']))
        
        # Determine tone
        tone = self._determine_tone(job_info, user_info)
        
        # Process user skills
        user_skills = user_info.get('skills', 'relevant technologies')
        if 'go' in user_skills.lower():
            skills_list = [skill for skill in user_skills.split(',') if skill.strip().lower() != 'go']
            user_skills = ', '.join(skills_list) if skills_list else 'relevant technologies'
        
        # Shuffle skills for variety
        skills_list = user_skills.split(', ')
        if len(skills_list) > 4:
            random.shuffle(skills_list)
            user_skills = ', '.join(skills_list[:6])
        
        # Prepare template variables
        template_vars = {
            'hiring_manager': 'Hiring Manager',
            'position': target_role or job_info.get('position', 'Professional position'),
            'company': company or job_info.get('company', 'the Company'),
            'key_skills': job_info.get('skills', user_skills),
            'matched_content': best_match_content or self._generate_dynamic_content(job_info, user_info),
            'years_experience': user_info.get('years', '0 years'),
            'candidate_name': user_info.get('name', 'Candidate'),
            'company_values': job_info.get('company_values', 'innovation and excellence'),
            'key_achievements': user_info.get('achievements', 'delivering successful projects'),
            'professional_values': 'professional excellence',
            'specialized_skills': user_skills,
            'opening_phrase': random.choice(self.opening_phrases),
            'closing_phrase': random.choice(self.closing_phrases),
            'tone': tone,
            'dynamic_content': self._generate_dynamic_content(job_info, user_info)
        }
        
        try:
            # Generate cover letter
            cover_letter = template.format(**template_vars)
            
            # Extract experience from user_input to override if needed
            exp_match = re.search(r'I have (\d+\+?)\s*years', user_input, re.IGNORECASE)
            if exp_match:
                # Replace the experience in the generated letter
                cover_letter = re.sub(r'\b\d+\+?\s*years', exp_match.group(1) + ' years', cover_letter, flags=re.IGNORECASE)
            else:
                # Also try to extract from user_info
                user_exp = user_info.get('years', '3+')
                if user_exp != '3+':
                    cover_letter = re.sub(r'\b3\+\s*years', user_exp, cover_letter, flags=re.IGNORECASE)
            
            # Enhance and clean
            cover_letter = self._enhance_natural_flow(cover_letter)
            cover_letter = self._clean_generated_text(cover_letter)
            
            # Final cleanup - remove trailing 'and' from signature
            cover_letter = re.sub(r'([A-Z][a-z\s]+)\s+and\s*$', r'\1', cover_letter, flags=re.MULTILINE)
            cover_letter = re.sub(r'([A-Z][a-z]+)\s+and\s*$', r'\1', cover_letter, flags=re.MULTILINE)
            
            # Aggressive cleanup for any trailing 'and' after names
            lines = cover_letter.split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                # Check if line looks like a name (2+ words, starts with capital letters)
                if re.match(r'^[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+', line):
                    # Remove trailing 'and'
                    line = re.sub(r'\s+and\s*$', '', line)
                    lines[i] = line
            
            cover_letter = '\n'.join(lines)
            
            # Ultimate cleanup - remove 'and' from the very end of the document
            cover_letter = cover_letter.rstrip()
            if cover_letter.endswith(' and'):
                cover_letter = cover_letter[:-4].rstrip()
            elif cover_letter.endswith(' and '):
                cover_letter = cover_letter[:-5].rstrip()
            
            return cover_letter
            
        except Exception as e:
            # Fallback cover letter
            return f"""Dear Hiring Manager,

I am excited to apply for the {template_vars['position']} position at {template_vars['company'] or 'your company'}.

Based on my background in {user_info.get('skills', 'relevant technologies')} and the requirements outlined in your job description, I believe I would be a valuable addition to your team.

I look forward to discussing how my qualifications can benefit your organization.

Thank you for your consideration.

Sincerely,
{user_info.get('name', 'Candidate')}"""
