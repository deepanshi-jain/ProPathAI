from typing import List, Dict, Any

def create_rag_resume_feedback_prompt(resume_text: str, retrieved_context: List[Dict[str, Any]]) -> str:
    """Create a RAG-enhanced prompt for resume feedback"""
    
    # Extract relevant examples and job descriptions
    resume_examples = [ctx for ctx in retrieved_context if ctx.get('type') == 'resume_example']
    job_descriptions = [ctx for ctx in retrieved_context if ctx.get('type') == 'job_description']
    
    context_str = ""
    if resume_examples:
        context_str += "\n\nRELEVANT RESUME EXAMPLES:\n"
        for i, example in enumerate(resume_examples[:3], 1):
            context_str += f"{i}. {example.get('title', 'Example')}:\n"
            context_str += f"   Skills: {', '.join(example.get('skills', []))}\n"
            context_str += f"   Experience: {example.get('experience_years', 'N/A')} years\n"
            context_str += f"   Success Rate: {example.get('success_rate', 'N/A')}\n\n"
    
    if job_descriptions:
        context_str += "\n\nRELEVANT JOB DESCRIPTIONS:\n"
        for i, job in enumerate(job_descriptions[:3], 1):
            context_str += f"{i}. {job.get('title', 'Job')} at {job.get('company', 'Company')}:\n"
            context_str += f"   Required Skills: {', '.join(job.get('skills', []))}\n"
            context_str += f"   Level: {job.get('experience_level', 'N/A')}\n\n"
    
    prompt = f"""
You are an expert resume reviewer with access to a database of successful resumes and job descriptions. 
Analyze the following resume and provide comprehensive feedback based on the relevant examples and job requirements.

{context_str}

RESUME TO ANALYZE:
{resume_text}

Please provide:

1. **Overall Assessment** (2-3 sentences)
2. **Strengths** (3-4 bullet points)
3. **Areas for Improvement** (3-4 specific suggestions)
4. **Skill Gap Analysis** (compare with relevant job requirements)
5. **Formatting & Structure** (ATS-friendly recommendations)
6. **Action Items** (3 specific next steps)

Base your recommendations on the successful examples and job requirements provided above.
"""
    return prompt

def create_rag_ats_score_prompt(resume_text: str, job_description: str, retrieved_context: List[Dict[str, Any]]) -> str:
    """Create a RAG-enhanced prompt for ATS scoring"""
    
    # Find similar job descriptions and successful resumes
    similar_jobs = [ctx for ctx in retrieved_context if ctx.get('type') == 'job_description']
    successful_resumes = [ctx for ctx in retrieved_context if ctx.get('type') == 'resume_example' and ctx.get('success_rate') == 'High']
    
    context_str = ""
    if similar_jobs:
        context_str += "\n\nSIMILAR JOB REQUIREMENTS:\n"
        for i, job in enumerate(similar_jobs[:2], 1):
            context_str += f"{i}. {job.get('title', 'Job')}: {', '.join(job.get('skills', []))}\n"
    
    if successful_resumes:
        context_str += "\n\nSUCCESSFUL RESUME PATTERNS:\n"
        for i, resume in enumerate(successful_resumes[:2], 1):
            context_str += f"{i}. {resume.get('title', 'Resume')}: {', '.join(resume.get('skills', []))}\n"
    
    prompt = f"""
You are an advanced ATS (Applicant Tracking System) simulator with access to successful resume patterns and job requirements.

{context_str}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide a detailed ATS analysis:

**ATS Score: [0-100]**

**Keyword Analysis:**
- Matched Keywords: [list]
- Missing Critical Keywords: [list]
- Keyword Density Score: [0-100]

**Formatting Assessment:**
- ATS-Friendly Format: [Yes/No]
- Issues Found: [list any formatting problems]
- Header Structure: [Good/Fair/Poor]

**Content Quality:**
- Quantified Achievements: [count and examples]
- Action Verbs: [count and examples]
- Skills Alignment: [percentage match]

**Final Verdict:**
- ATS Status: [Pass/Borderline/Fail]
- Confidence Level: [High/Medium/Low]
- Priority Improvements: [top 3 actions needed]

Use the successful patterns and job requirements above to provide accurate scoring.
"""
    return prompt

def create_career_advice_prompt(resume_text: str, retrieved_context: List[Dict[str, Any]]) -> str:
    """Create a RAG-enhanced prompt for career advice"""
    
    # Analyze the resume to understand career trajectory
    resume_examples = [ctx for ctx in retrieved_context if ctx.get('type') == 'resume_example']
    job_descriptions = [ctx for ctx in retrieved_context if ctx.get('type') == 'job_description']
    
    context_str = ""
    if resume_examples:
        context_str += "\n\nCAREER PATH EXAMPLES:\n"
        for i, example in enumerate(resume_examples[:3], 1):
            context_str += f"{i}. {example.get('title', 'Career Path')}:\n"
            context_str += f"   Experience: {example.get('experience_years', 'N/A')} years\n"
            context_str += f"   Key Skills: {', '.join(example.get('skills', []))}\n"
            context_str += f"   Success Indicators: {example.get('success_rate', 'N/A')}\n\n"
    
    if job_descriptions:
        context_str += "\n\nMARKET DEMAND:\n"
        for i, job in enumerate(job_descriptions[:3], 1):
            context_str += f"{i}. {job.get('title', 'Role')} ({job.get('experience_level', 'N/A')}):\n"
            context_str += f"   Required Skills: {', '.join(job.get('skills', []))}\n\n"
    
    prompt = f"""
You are a career development expert with access to successful career paths and current market demands.
Analyze this resume and provide strategic career advice.

{context_str}

RESUME:
{resume_text}

Provide comprehensive career guidance:

**Career Trajectory Analysis:**
- Current Position: [assess level and role]
- Career Progression: [next logical steps]
- Market Positioning: [competitive analysis]

**Skill Development Roadmap:**
- Immediate Skills (3 months): [list]
- Short-term Skills (6 months): [list]
- Long-term Skills (1 year): [list]

**Career Opportunities:**
- Recommended Roles: [3-4 positions]
- Target Companies: [types/sectors]
- Salary Expectations: [range based on experience]

**Networking & Branding:**
- Professional Brand: [key differentiators]
- Networking Strategy: [specific actions]
- Online Presence: [recommendations]

**Action Plan:**
- 30-Day Goals: [specific actions]
- 90-Day Goals: [milestones]
- 6-Month Vision: [career objectives]

Base recommendations on successful career paths and current market demands shown above.
"""
    return prompt

def create_job_matching_prompt(resume_text: str, retrieved_context: List[Dict[str, Any]]) -> str:
    """Create a RAG-enhanced prompt for job matching"""
    
    job_descriptions = [ctx for ctx in retrieved_context if ctx.get('type') == 'job_description']
    
    context_str = ""
    if job_descriptions:
        context_str += "\n\nAVAILABLE OPPORTUNITIES:\n"
        for i, job in enumerate(job_descriptions[:5], 1):
            context_str += f"{i}. {job.get('title', 'Position')} at {job.get('company', 'Company')}\n"
            context_str += f"   Level: {job.get('experience_level', 'N/A')}\n"
            context_str += f"   Skills: {', '.join(job.get('skills', []))}\n\n"
    
    prompt = f"""
You are a job matching specialist with access to current job opportunities.
Match this resume with the most suitable positions.

{context_str}

RESUME:
{resume_text}

Provide job matching analysis:

**Best Matches (Top 3):**
1. [Job Title] - [Company] - [Match Score %]
   - Why it's a good fit: [explanation]
   - Application readiness: [Ready/Needs Work]

2. [Job Title] - [Company] - [Match Score %]
   - Why it's a good fit: [explanation]
   - Application readiness: [Ready/Needs Work]

3. [Job Title] - [Company] - [Match Score %]
   - Why it's a good fit: [explanation]
   - Application readiness: [Ready/Needs Work]

**Skill Alignment:**
- Perfect Matches: [skills that align perfectly]
- Partial Matches: [skills that need development]
- Missing Skills: [critical gaps to address]

**Application Strategy:**
- Resume Customization: [specific changes needed]
- Cover Letter Focus: [key selling points]
- Interview Preparation: [areas to emphasize]

**Alternative Paths:**
- Related Roles: [similar positions to consider]
- Industry Transitions: [other sectors to explore]
- Skill Pivots: [how to leverage current skills]

Base recommendations on the available opportunities and skill requirements shown above.
"""
    return prompt

