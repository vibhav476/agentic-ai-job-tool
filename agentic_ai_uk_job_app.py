import streamlit as st
import openai
import pandas as pd

# --------------------------
# Config / API Key
# --------------------------
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("OpenAI API Key missing in secrets. Add it in Streamlit Cloud > App Settings > Secrets.")
    st.stop()

st.title("Agentic AI: UK Job Assistant")

# --------------------------
# Section: Input for CV + Cover Letter
# --------------------------
st.header("📄 Tailored CV & Cover Letter")

candidate_background = st.text_area("Your Background", height=200)
job_description = st.text_area("Job Description", height=300)
target_role = st.text_input("Job Title")
location = st.text_input("Location (e.g. London, Remote)")
sector = st.text_input("Sector / Industry")

if st.button("Generate Application"):
    with st.spinner("Generating..."):
        prompt = f"""
You are an expert UK career coach. Write:
1. 5 tailored CV bullet points
2. A UK-style cover letter

Based on:
- Candidate: {candidate_background}
- Job: {job_description}
- Role: {target_role}
- Location: {location}
- Sector: {sector}

Keep it direct, clear, and impact-driven.
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        st.markdown("### ✍️ Generated Output")
        st.write(response['choices'][0]['message']['content'])

# --------------------------
# Section: LinkedIn Message Generator
# --------------------------
st.header("💬 LinkedIn Message Draft")

if st.button("Generate LinkedIn Message"):
    linkedin_prompt = f"""
Write a short LinkedIn message under 500 characters for:
- Role: {target_role}
- Sector: {sector}
- Location: {location}
- Candidate: {candidate_background}

Goal: Reach out to a recruiter or hiring manager to express interest and ask for a referral.
Tone: Warm, concise, professional.
"""
    linkedin_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": linkedin_prompt}],
        temperature=0.7
    )
    st.markdown("### 📬 LinkedIn Message")
    st.code(linkedin_response['choices'][0]['message']['content'], language="text")

# --------------------------
# Section: Dummy UK Job Search + Visa Sponsor Filter
# --------------------------
st.header("🔎 UK Job Listings (Prototype)")

query = st.text_input("Search Role (e.g. PEGA)", "")
location_filter = st.text_input("Filter by Location", "")
sponsored_only = st.checkbox("Only show UK visa-sponsoring companies")

@st.cache_data(ttl=86400)
def load_sponsor_list():
    try:
        url = "https://assets.publishing.service.gov.uk/media/662251e5e0c72f000cd7f34a/register-of-licensed-sponsors-workers.csv"
        df = pd.read_csv(url)
        return df["Organisation Name"].str.lower().tolist()
    except:
        return []

sponsor_companies = load_sponsor_list()

dummy_jobs = [
    {"title": "PEGA Business Analyst", "company": "Amazon", "location": "London", "apply": "https://amazon.jobs"},
    {"title": "PEGA Consultant", "company": "StartupX", "location": "Remote", "apply": "https://startupx.io"},
    {"title": "Senior Insurance Analyst", "company": "PwC", "location": "London", "apply": "https://pwc.co.uk"},
    {"title": "Digital BA", "company": "ABC Tech", "location": "Hybrid", "apply": "https://abctech.com/careers"},
]

filtered_jobs = []
for job in dummy_jobs:
    if query.lower() in job["title"].lower() and location_filter.lower() in job["location"].lower():
        if not sponsored_only or job["company"].lower() in sponsor_companies:
            filtered_jobs.append(job)

st.subheader("📋 UK Job Results")
if filtered_jobs:
    for job in filtered_jobs:
        st.markdown(f"**{job['title']}** at **{job['company']}** – {job['location']}  
[Apply Here]({job['apply']})")
else:
    st.info("No jobs matched. Try changing search or location.")

# --------------------------
# Section: UAE Job Search (Real-time)
# --------------------------
st.header("🇦🇪 UAE Job Search (Real-time)")

sponsor_companies_uae = [
    "emirates", "etisalat", "microsoft", "ibm", "pwc", 
    "majid al futtaim", "noon", "careem", "deloitte", "kpmg", "ey"
]

query_uae = st.text_input("UAE Role", "")
location_uae = st.text_input("UAE Location", "Dubai")
filter_sponsored_uae = st.checkbox("Only show UAE visa-sponsoring companies")

if query_uae and location_uae:
    with st.spinner("Fetching UAE jobs..."):
        import requests
        payload = {
            "keywords": query_uae,
            "location": location_uae,
            "page": 1
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "b12225f66amsh7f5512744f52de8p1c9875jsn8c93cdded318",
            "X-RapidAPI-Host": "jooble.org"
        }
        response = requests.post("https://jooble.org/api/ab23bda5-9c07-409a-bc38-742f8b0c86f1", json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            st.subheader("🔍 UAE Jobs")
            count = 0
            for job in jobs:
                company = job.get("company", "").lower()
                if not filter_sponsored_uae or any(s in company for s in sponsor_companies_uae):
                    st.markdown(f"**{job.get('title')}** at **{job.get('company')}**  \n{job.get('location')}  \n[Apply]({job.get('link')})")
                    st.markdown("---")
                    count += 1
            if count == 0:
                st.info("No matching UAE jobs found.")
        else:
            st.error("Failed to fetch UAE jobs. Check API or try later.")