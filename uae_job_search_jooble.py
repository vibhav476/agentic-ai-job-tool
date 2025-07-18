
import streamlit as st
import requests

st.header("🇦🇪 UAE Job Search (Real-time)")

# Sponsor companies list (static)
sponsor_companies_uae = [
    "emirates", "etisalat", "microsoft", "ibm", "pwc", 
    "majid al futtaim", "noon", "careem", "deloitte", "kpmg", "ey"
]

# User inputs
query = st.text_input("Search Role (e.g. PEGA Consultant)", "")
location = st.text_input("Location (Default: Dubai)", "Dubai")
filter_sponsored = st.checkbox("Only show jobs from UAE visa-sponsoring companies")

# API Key
API_KEY = "b12225f66amsh7f5512744f52de8p1c9875jsn8c93cdded318"
url = "https://jooble.org/api/"
headers = {
    "content-type": "application/json",
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "jooble.org"
}

if query and location:
    with st.spinner("Fetching jobs..."):
        payload = {
            "keywords": query,
            "location": location,
            "page": 1
        }
        response = requests.post("https://jooble.org/api/ab23bda5-9c07-409a-bc38-742f8b0c86f1", json=payload)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            st.subheader("🔍 Results")
            count = 0
            for job in jobs:
                company = job.get("company", "").lower()
                if not filter_sponsored or any(s in company for s in sponsor_companies_uae):
                    st.markdown(f"**{job.get('title')}** at **{job.get('company')}**  
{job.get('location')}  
[Apply]({job.get('link')})")
                    st.markdown("---")
                    count += 1
            if count == 0:
                st.info("No matching jobs found. Try a different keyword or remove the sponsor filter.")
        else:
            st.error("Failed to fetch jobs. Check API limits or try later.")
