"""
Advanced Interactive Cover Letter Generator
Supports uploading custom job descriptions and resume-based generation.
"""

import os
import sys
from pathlib import Path
import re

# Add backend directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from generator import CoverLetterGenerator
from document_reader import extract_text_from_document


def advanced_interactive_generator():
    """Advanced interactive cover letter generator with file upload support."""
    
    print("🚀 Advanced Cover Letter Generator")
    print("=" * 50)
    print("Choose how you want to generate your cover letter:")
    print()
    
    while True:
        print("1️⃣  Upload Custom Job Description")
        print("2️⃣  Use Existing Job Description File")
        print("3️⃣  Enter Job Description Manually")
        print("4️⃣  Resume-Based Generation")
        print("5️⃣  Skills-Based Generation")
        print("6️⃣  Exit")
        print()
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            upload_custom_jd()
            break
        elif choice == '2':
            generate_from_jd_file()
            break
        elif choice == '3':
            generate_from_manual_jd()
            break
        elif choice == '4':
            generate_from_resume()
            break
        elif choice == '5':
            generate_from_skills()
            break
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")
            print()


def upload_custom_jd():
    """Upload and use custom job description."""
    print("\n📤 Upload Custom Job Description")
    print("-" * 35)
    
    print("📁 Options to provide your job description:")
    print("1. Paste job description text directly")
    print("2. Specify path to job description file")
    print("3. Upload from file (drag and drop path)")
    print()
    
    upload_choice = input("Choose option (1-3): ").strip()
    
    if upload_choice == '1':
        paste_job_description()
    elif upload_choice == '2':
        specify_jd_file()
    elif upload_choice == '3':
        upload_jd_file()
    else:
        print("❌ Invalid choice. Returning to main menu.")
        return


def paste_job_description():
    """Paste job description directly."""
    print("\n📋 Paste Job Description")
    print("-" * 25)
    print("Paste the job description below (press Enter twice to finish):")
    print()
    
    job_description_lines = []
    empty_line_count = 0
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
                if empty_line_count >= 2:
                    break
            else:
                empty_line_count = 0
            job_description_lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break
    
    job_description = "\n".join(job_description_lines)
    
    if not job_description.strip():
        print("❌ No job description entered.")
        return
    
    process_job_description(job_description)


def specify_jd_file():
    """Specify path to job description file."""
    print("\n📂 Specify Job Description File")
    print("-" * 30)
    print("Supported formats: .txt, .pdf, .docx")
    print()
    
    file_path = input("Enter the full path to your job description file: ").strip().strip('"')
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    try:
        # Extract text from job description file (supports PDF, DOCX, TXT)
        job_description = extract_text_from_document(file_path)
        
        print(f"✅ Successfully loaded: {os.path.basename(file_path)}")
        print(f"📄 File type: {Path(file_path).suffix}")
        print(f"📏 Extracted text length: {len(job_description)} characters")
        process_job_description(job_description)
        
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        print("💡 Supported formats: .txt, .pdf, .docx")
        print("💡 Make sure the file is not corrupted")


def upload_jd_file():
    """Upload job description file (drag and drop support)."""
    print("\n📤 Upload Job Description File")
    print("-" * 30)
    print("Drag and drop your job description file here, or enter the path:")
    print("Supported formats: .txt, .pdf, .docx")
    print()
    
    file_path = input("File path: ").strip().strip('"')
    
    if not file_path:
        print("❌ No file path provided.")
        return
    
    # Handle Windows path formatting and clean up
    file_path = file_path.replace('\\', '/')
    # Remove PowerShell command character and quotes
    if file_path.startswith('&'):
        file_path = file_path[1:].strip()
    if file_path.startswith("'"):
        file_path = file_path[1:].strip()
    if file_path.startswith('"'):
        file_path = file_path[1:].strip()
    
    # Remove any remaining quotes
    file_path = file_path.strip("'").strip('"').strip()
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    try:
        job_description = extract_text_from_document(file_path)
        print(f"✅ Successfully uploaded: {os.path.basename(file_path)}")
        process_job_description(job_description)
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")


def process_job_description(job_description):
    """Process job description and generate cover letter."""
    print("\n📄 Job Description Loaded")
    print("-" * 25)
    print(f"Length: {len(job_description)} characters")
    print(f"Lines: {len(job_description.splitlines())}")
    print()
    
    # Get user input
    user_input = input("📝 Enter your details (name, experience, skills): ").strip()
    
    # Extract company name from job description or ask user
    target_company = input("🏢 Company name (optional - press Enter to skip): ").strip()
    if not target_company:
        target_company = ""
    
    # Get output filename
    output_file = input("💾 Enter output filename (e.g., my_cover_letter.txt): ").strip()
    if not output_file:
        output_file = "custom_jd_cover_letter.txt"
    
    # Generate cover letter
    print("\n🚀 Generating cover letter...")
    
    try:
        generator = CoverLetterGenerator()
        
        # Generate cover letter
        cover_letter = generator.generate_cover_letter(
            job_description=job_description,
            user_input=user_input,
            company=target_company
        )
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        
        print(f"✅ Cover letter saved to: {output_file}")
        print(f"\n📄 Generated Cover Letter:")
        print("=" * 50)
        print(cover_letter)
        
    except Exception as e:
        print(f"❌ Error generating cover letter: {str(e)}")


def generate_from_resume():
    """Generate cover letter based on resume information."""
    print("\n📄 Resume-Based Generation")
    print("-" * 30)
    
    print("📁 Options to provide your resume:")
    print("1. Paste resume text directly")
    print("2. Specify path to resume file")
    print("3. Upload resume file (drag and drop)")
    print()
    
    resume_choice = input("Choose option (1-3): ").strip()
    
    if resume_choice == '1':
        paste_resume()
    elif resume_choice == '2':
        specify_resume_file()
    elif resume_choice == '3':
        upload_resume_file()
    else:
        print("❌ Invalid choice. Returning to main menu.")
        return


def paste_resume():
    """Paste resume text directly."""
    print("\n📋 Paste Resume Text")
    print("-" * 20)
    print("Paste your resume below (press Enter twice to finish):")
    print()
    
    resume_lines = []
    empty_line_count = 0
    
    while True:
        try:
            line = input()
            if line.strip() == "":
                empty_line_count += 1
                if empty_line_count >= 2:
                    break
            else:
                empty_line_count = 0
            resume_lines.append(line)
        except (EOFError, KeyboardInterrupt):
            break
    
    resume_text = "\n".join(resume_lines)
    
    if not resume_text.strip():
        print("❌ No resume text entered.")
        return
    
    process_resume(resume_text)


def specify_resume_file():
    """Specify path to resume file."""
    print("\n📂 Specify Resume File")
    print("-" * 20)
    print("Supported formats: .txt, .pdf, .docx")
    print()
    
    file_path = input("Enter the full path to your resume file: ").strip().strip('"')
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    try:
        # Extract text from resume (supports PDF, DOCX, TXT)
        resume_text = extract_text_from_document(file_path)
        
        print(f"✅ Successfully loaded: {os.path.basename(file_path)}")
        print(f"📄 File type: {Path(file_path).suffix}")
        print(f"📏 Extracted text length: {len(resume_text)} characters")
        process_resume(resume_text)
        
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        print("💡 Supported formats: .txt, .pdf, .docx")
        print("💡 Make sure the file is not corrupted")


def upload_resume_file():
    """Upload resume file (drag and drop support)."""
    print("\n📤 Upload Resume File")
    print("-" * 20)
    print("Drag and drop your resume file here, or enter the path:")
    print("Supported formats: .txt, .pdf, .docx")
    print()
    
    file_path = input("File path: ").strip().strip('"')
    
    if not file_path:
        print("❌ No file path provided.")
        return
    
    # Handle Windows path formatting
    file_path = file_path.replace('\\', '/')
    # Remove PowerShell command character and quotes
    if file_path.startswith('&'):
        file_path = file_path[1:].strip()
    if file_path.startswith("'"):
        file_path = file_path[1:].strip()
    if file_path.startswith('"'):
        file_path = file_path[1:].strip()
    
    # Remove any remaining quotes
    file_path = file_path.strip("'").strip('"').strip()
    
    try:
        # Extract text from resume (supports PDF, DOCX, TXT)
        resume_text = extract_text_from_document(file_path)
        
        print(f"✅ Successfully uploaded: {os.path.basename(file_path)}")
        print(f"📄 File type: {Path(file_path).suffix}")
        print(f"📏 Extracted text length: {len(resume_text)} characters")
        process_resume(resume_text)
        
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        print("💡 Supported formats: .txt, .pdf, .docx")
        print("💡 Make sure the file is not corrupted")


def process_resume(resume_text):
    """Process resume and generate cover letter."""
    print("\n📄 Resume Loaded")
    print("-" * 15)
    print(f"Length: {len(resume_text)} characters")
    print(f"Lines: {len(resume_text.splitlines())}")
    print()
    
    # Extract key information from resume
    extracted_info = extract_resume_info(resume_text)
    
    print("🔍 Extracted Information:")
    print(f"Name: {extracted_info.get('name', 'Not found')}")
    print(f"Experience: {extracted_info.get('experience', 'Not found')}")
    print(f"Skills: {extracted_info.get('skills', 'Not found')}")
    print()
    
    # Get target job information
    target_role = input("🎯 What type of position are you applying for? ").strip()
    target_company = input("🏢 Company name (optional - e.g., TCS, Cognizant, Deloitte): ").strip()
    if not target_company:
        target_company = "the Company"
    
    # Generate job description based on target role
    job_description = generate_job_description_from_role(target_role, target_company)
    
    # If name found in resume, use it directly
    if extracted_info.get('name', 'Not found') != 'Not found' and extracted_info.get('name', 'Not found') != 'Linkedin Profile':
        name = extracted_info.get('name', 'Candidate')
        experience = extracted_info.get('experience', 'Not found')
        skills = extracted_info.get('skills', 'various technologies')
        print(f"\n✅ Resume Analysis Complete:")
        print(f"Name: {name}")
        print(f"Experience: {experience}")
        print(f"Skills: {skills}")
        print()
        
        # Ask for experience if not found
        if experience == 'Not found':
            experience = input("Experience not found in resume. Please enter your years of experience: ").strip()
        
    else:
        # Ask for confirmation only if extraction failed
        print(f"\n🔍 Extracted Information:")
        print(f"Name: {extracted_info.get('name', 'Not found')}")
        print(f"Experience: {extracted_info.get('experience', 'Not found')}")
        print(f"Skills: {extracted_info.get('skills', 'Not found')}")
        print()
        
        name = input(f"Name detected: {extracted_info.get('name', 'Not found')}. Press Enter to accept or enter correct name: ").strip()
        experience = input(f"Experience detected: {extracted_info.get('experience', 'Not found')}. Press Enter to accept or enter correct experience: ").strip()
        skills = input(f"Skills detected: {extracted_info.get('skills', 'Not found')}. Press Enter to accept or enter correct skills: ").strip()
    
    # Create user input from resume
    user_input = f"My name is {name or extracted_info.get('name', 'Candidate')} and I have {experience or extracted_info.get('experience', 'relevant experience')}. I am skilled in {skills or extracted_info.get('skills', 'various technologies')}."

    # Get output filename
    output_file = input("💾 Enter output filename (e.g., resume_based_cover_letter.txt): ").strip()
    if not output_file:
        output_file = "resume_based_cover_letter.txt"
    
    # Generate cover letter
    print("\n🚀 Generating cover letter...")
    
    try:
        generator = CoverLetterGenerator()
        
        # Generate cover letter
        cover_letter = generator.generate_cover_letter(
            job_description=job_description,
            user_input=user_input,
            company=target_company
        )
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        
        print(f"✅ Cover letter saved to: {output_file}")
        print(f"\n📄 Generated Cover Letter:")
        print("=" * 50)
        print(cover_letter)
        
    except Exception as e:
        print(f"❌ Error generating cover letter: {str(e)}")


def extract_resume_info(resume_text: str) -> dict:
    """Extract information from resume text with enhanced name detection."""
    info = {}
    
    # Enhanced name extraction - more comprehensive patterns
    name_patterns = [
        r'NILADRI\s+BHANDARI',  # Specific pattern first
        r'AYAK\s+MANNA',  # Another specific pattern
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',  # First Last or First Middle Last
        r'Name[:\s]*([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'(?:my name is|i am|i\'m)\s+([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'([A-Z][a-z]+)\s+([A-Z][a-z]+)',  # Simple First Last
        r'([A-Z]{2,}\s+[A-Z]{2,})',  # All caps names
    ]
    
    for pattern in name_patterns:
        try:
            match = re.search(pattern, resume_text, re.IGNORECASE)
            if match:
                # Use group(0) for full match, group(1) for captured group
                if pattern in [r'NILADRI\s+BHANDARI', r'AYAK\s+MANNA']:
                    potential_name = match.group(0).strip()
                elif pattern == r'([A-Z]{2,}\s+[A-Z]{2,})':
                    potential_name = match.group(0).strip()
                else:
                    potential_name = match.group(1).strip()
                
                # Filter out common false positives
                false_positives = ['resume', 'profile', 'candidate', 'experience', 'my name is', 'linkedin', 'github', 'portfolio', 'email', 'contact', 'phone']
                if not any(word.lower() in potential_name.lower() for word in false_positives):
                    # Additional validation: should have at least 2 parts and reasonable length
                    name_parts = potential_name.split()
                    if len(name_parts) >= 2 and len(potential_name) >= 5:
                        info['name'] = potential_name
                        break
        except Exception as e:
            continue
    
    # Enhanced experience extraction - simple patterns
    years_patterns = [
        r'(\d+)\s*years?',
        r'(\d+)\s*yrs?',
        r'(\d+)\s*year',
    ]
    
    for pattern in years_patterns:
        try:
            match = re.search(pattern, resume_text, re.IGNORECASE)
            if match:
                info['experience'] = f"{match.group(1)} years"
                break
        except:
            continue
    
    # Extract skills
    skill_keywords = [
        'python', 'java', 'javascript', 'react', 'nodejs', 'sql', 'aws', 'azure', 'gcp',
        'docker', 'kubernetes', 'git', 'agile', 'scrum', 'machine learning',
        'data analysis', 'tensorflow', 'pytorch', 'django', 'flask', 'spring',
        'mongodb', 'postgresql', 'mysql', 'restful api', 'microservices',
        'html', 'css', 'typescript', 'vue', 'angular', 'express', 'c++', 'c#',
        'linux', 'windows', 'ubuntu', 'communication', 'leadership', 'project management'
    ]
    
    found_skills = []
    resume_lower = resume_text.lower()
    for skill in skill_keywords:
        if skill in resume_lower:
            found_skills.append(skill)
    
    if found_skills:
        info['skills'] = ', '.join(found_skills[:10])
    
    return info


def generate_job_description_from_role(role, company=""):
    """Generate job description based on role."""
    job_descriptions = {
        'frontend developer': f"""
    We are looking for a Frontend Developer to join our innovative team at {company or 'our company'}. The ideal candidate should have a strong foundation in web technologies and a passion for creating exceptional user experiences.
    
    Responsibilities:
    • Develop responsive and interactive web applications using React and modern JavaScript
    • Collaborate with UX/UI designers to implement pixel-perfect designs
    • Optimize applications for maximum speed and scalability
    • Work with backend developers to integrate APIs and services
    • Ensure cross-browser compatibility and responsive design
    
    Requirements:
    • Strong knowledge of HTML5, CSS3, and JavaScript (ES6+)
    • Experience with React or similar modern frontend frameworks
    • Understanding of responsive design and mobile-first development
    • Familiarity with version control systems (Git)
    • Excellent problem-solving skills and attention to detail
    """,
        
        'backend developer': f"""
    We are seeking a Backend Developer to join our growing team at {company or 'our company'}. The ideal candidate should have strong server-side development skills and experience building scalable applications.
    
    Responsibilities:
    • Design and develop robust server-side applications
    • Create and maintain RESTful APIs and microservices
    • Work with databases and optimize query performance
    • Implement security best practices and data protection
    • Collaborate with frontend teams to integrate services
    
    Requirements:
    • Strong experience with server-side programming languages
    • Experience with database design and optimization
    • Knowledge of cloud platforms and deployment
    • Understanding of security and scalability
    • Experience with version control and collaborative development
    """,
        
        'full stack developer': f"""
    We are looking for a Full Stack Developer to join our dynamic team at {company or 'our company'}. This role requires expertise in both frontend and backend technologies.
    
    Responsibilities:
    • Develop both frontend and backend components of web applications
    • Design and implement RESTful APIs and database schemas
    • Create responsive user interfaces using modern frameworks
    • Work with cloud services for deployment and scaling
    • Participate in the full software development lifecycle
    
    Requirements:
    • Experience with both frontend and backend technologies
    • Strong foundation in computer science fundamentals
    • Knowledge of web technologies (HTML, CSS, JavaScript)
    • Familiarity with databases (SQL or NoSQL)
    • Understanding of software development principles
    """,
        
        'data scientist': f"""
    We are seeking a Data Scientist to join our analytics team at {company or 'our company'}. The ideal candidate should have strong analytical skills and experience with machine learning.
    
    Responsibilities:
    • Develop and implement machine learning models
    • Analyze large datasets and extract actionable insights
    • Create data visualizations and reports
    • Work with cross-functional teams on data-driven projects
    • Communicate findings to stakeholders
    
    Requirements:
    • Strong background in statistics and mathematics
    • Experience with Python and data science libraries
    • Knowledge of machine learning algorithms
    • Experience with data visualization tools
    • Strong analytical and problem-solving skills
    """,
        
        'software engineer': f"""
    We are looking for a Software Engineer to join our engineering team at {company or 'our company'}. The ideal candidate should have strong programming skills and a passion for building quality software.
    
    Responsibilities:
    • Design, develop, and maintain software applications
    • Write clean, efficient, and well-documented code
    • Participate in code reviews and technical discussions
    • Troubleshoot and debug applications
    • Collaborate with cross-functional teams
    
    Requirements:
    • Strong programming skills in one or more languages
    • Understanding of software development principles
    • Experience with version control systems
    • Good problem-solving and analytical skills
    • Ability to work in a team environment
    """
    }
    
    # Return matching job description or default
    role_lower = role.lower()
    for key, jd in job_descriptions.items():
        if key in role_lower:
            return jd
    
    # Default job description
    return f"""
    We are looking for a {role} to join our team at {company or 'our company'}. The ideal candidate should have relevant experience and a passion for innovation.
    
    Responsibilities:
    • Develop and maintain high-quality solutions
    • Collaborate with cross-functional teams
    • Contribute to technical decisions and best practices
    • Continuously learn and adapt to new technologies
    
    Requirements:
    • Strong problem-solving skills
    • Good communication and teamwork abilities
    • Attention to detail and quality focus
    • Eagerness to learn and grow professionally
    """


def generate_from_jd_file():
    """Generate cover letter from existing job description file."""
    print("\n📁 Existing Job Description File Method")
    print("-" * 40)
    
    # List available JD files
    jd_dir = Path("sample_data/job_description_data")
    jd_files = list(jd_dir.glob("*.txt"))
    
    if not jd_files:
        print("❌ No job description files found in sample_data/job_description_data/")
        return
    
    print("Available job description files:")
    for i, file in enumerate(jd_files, 1):
        print(f"{i}. {file.name}")
    
    while True:
        try:
            file_choice = input(f"\nSelect file (1-{len(jd_files)}): ").strip()
            file_index = int(file_choice) - 1
            
            if 0 <= file_index < len(jd_files):
                selected_file = jd_files[file_index]
                break
            else:
                print("❌ Invalid file number. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    print(f"\n📄 Selected: {selected_file.name}")
    
    # Get user input
    user_input = input("\n📝 Enter your details (name, experience, skills): ").strip()
    
    # Get output filename
    output_file = input("💾 Enter output filename (e.g., my_cover_letter.txt): ").strip()
    if not output_file:
        output_file = "generated_cover_letter.txt"
    
    # Generate cover letter
    print("\n🚀 Generating cover letter...")
    
    try:
        generator = CoverLetterGenerator()
        
        # Read job description
        with open(selected_file, 'r', encoding='utf-8') as f:
            job_description = f.read()
        
        # Generate cover letter
        cover_letter = generator.generate_cover_letter(
            job_description=job_description,
            user_input=user_input,
            company=target_company
        )
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        
        print(f"✅ Cover letter saved to: {output_file}")
        print(f"\n📄 Generated Cover Letter:")
        print("=" * 50)
        print(cover_letter)
        
    except Exception as e:
        print(f"❌ Error generating cover letter: {str(e)}")


def generate_from_manual_jd():
    """Generate cover letter from manually entered job description."""
    print("\n⌨️  Manual Job Description Method")
    print("-" * 35)
    
    print("📄 Enter the job description (press Enter twice to finish):")
    print("(You can copy and paste the job description here)")
    print()
    
    # Read job description
    job_description_lines = []
    empty_line_count = 0
    
    while True:
        line = input()
        if line.strip() == "":
            empty_line_count += 1
            if empty_line_count >= 2:
                break
        else:
            empty_line_count = 0
        job_description_lines.append(line)
    
    job_description = "\n".join(job_description_lines)
    
    if not job_description.strip():
        print("❌ No job description entered.")
        return
    
    # Get user input
    user_input = input("\n📝 Enter your details (name, experience, skills): ").strip()
    
    # Get output filename
    output_file = input("💾 Enter output filename (e.g., my_cover_letter.txt): ").strip()
    if not output_file:
        output_file = "generated_cover_letter.txt"
    
    # Generate cover letter
    print("\n🚀 Generating cover letter...")
    
    try:
        generator = CoverLetterGenerator()
        
        # Generate cover letter
        cover_letter = generator.generate_cover_letter(
            job_description=job_description,
            user_input=user_input,
            company=target_company
        )
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        
        print(f"✅ Cover letter saved to: {output_file}")
        print(f"\n📄 Generated Cover Letter:")
        print("=" * 50)
        print(cover_letter)
        
    except Exception as e:
        print(f"❌ Error generating cover letter: {str(e)}")


def generate_from_skills():
    """Generate cover letter based on skills only."""
    print("\n🛠️  Skills-Based Generation Method")
    print("-" * 35)
    
    # Get user input
    user_input = input("📝 Enter your details (name, experience, skills): ").strip()
    
    # Ask for target role
    target_role = input("🎯 What type of position are you applying for? (e.g., Frontend Developer, Data Scientist, etc.): ").strip()
    
    # Get output filename
    output_file = input("💾 Enter output filename (e.g., my_cover_letter.txt): ").strip()
    if not output_file:
        output_file = "generated_cover_letter.txt"
    
    # Generate job description based on role
    job_description = generate_job_description_from_role(target_role)
    
    # Generate cover letter
    print("\n🚀 Generating cover letter...")
    
    try:
        generator = CoverLetterGenerator()
        
        # Generate cover letter
        cover_letter = generator.generate_cover_letter(
            job_description=job_description,
            user_input=user_input,
            company=target_company
        )
        
        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(cover_letter)
        
        print(f"✅ Cover letter saved to: {output_file}")
        print(f"\n📄 Generated Cover Letter:")
        print("=" * 50)
        print(cover_letter)
        
    except Exception as e:
        print(f"❌ Error generating cover letter: {str(e)}")


import webbrowser

def offer_download(filepath):
    abs_path = os.path.abspath(filepath)
    print(f"\n📥 To open/download your cover letter, copy this path or click below (if supported):\n{abs_path}")
    try:
        webbrowser.open(f'file:///{abs_path}')
    except Exception:
        pass

if __name__ == "__main__":
    advanced_interactive_generator()

