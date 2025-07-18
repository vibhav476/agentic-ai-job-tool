import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Agentic AI: UK Job Application Assistant")

st.markdown("""
This tool generates tailored CV bullet points and a UK-style cover letter based on:
- Your background
- The job description
- The role and industry focus
""")

# Input fields
candidate_background = st.text_area("Your Background", height=200, placeholder="Summarize your experience, education, skills, visa status, etc.")
job_description = st.text_area("Job Description", height=300, placeholder="Paste the full job description here.")
target_role = st.text_input("Job Title", placeholder="e.g., Senior Business Analyst")
location = st.text_input("Location", placeholder="e.g., London, UK or Remote")
sector = st.text_input("Sector", placeholder="e.g., FinTech, Insurance, Consulting")

if st.button("Generate Application"):
    with st.spinner("Crafting your CV bullets and cover letter..."):
        prompt = f"""
You are an expert career assistant specialized in the UK job market. Your task is to generate a tailored CV bullet list and a personalized cover letter for a candidate applying to a specific job role.

Candidate Background:
{candidate_background}

Job Description:
{job_description}

Target Role:
{target_role}
Location: {location}
Sector: {sector}

Instructions:
- Tailor the CV bullets to emphasize achievements, tools, and domain experience relevant to this role.
- Structure the cover letter in a UK format: concise, targeted, professional tone (no generic fluff).
- Show cultural awareness of the UK hiring market: emphasize results, responsibility, and value to employer.
- Include a clear "value proposition" statement at the top of the cover letter.
- Highlight if the candidate needs visa sponsorship or already has the right to work in the UK.

Output Format:
1. Tailored CV Bullet Points (max 5)
2. Cover Letter (UK-style, 3-4 short paragraphs)

Respond only with the final text. No explanations.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        st.markdown("### Results")
        st.write(response['choices'][0]['message']['content'])