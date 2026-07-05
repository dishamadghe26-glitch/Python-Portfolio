import streamlit as st
import pdfplumber
from openai import OpenAI

# 👉 Apni API key yahan daalna, ya fir streamlit secrets use karna
# Example: client = OpenAI
client = OpenAI(api_key=st.secrets["OPEAN_API_KEY"])

# ---------------------------
# PDF TEXT EXTRACTION
# ---------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text


# ---------------------------
# STREAMLIT UI
# ---------------------------
st.title("🧠 AI Smart Resume & Cover Letter Tailor")
st.write("Upload your resume and paste job description")

resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_desc = st.text_area("Paste Job Description")

if st.button("Generate AI Output"):

    if resume_file and job_desc:
        # Step 1: Extract resume text

        resume_text = extract_text_from_pdf(resume_file)

        # Step 2: Resume Tailoring Prompt
        resume_prompt = f"""
You are an expert resume writer.

Rewrite the resume according to the job description.
Make it ATS-friendly and highlight important skills.

Resume:
{resume_text}

Job Description:
{job_desc}
"""

        # Step 3: Cover Letter Prompt
        cover_prompt = f"""
Write a professional cover letter.

Resume:
{resume_text}

Job Description:
{job_desc}
"""

        # Step 4: Call AI
        with st.spinner("Generating AI response..."):
            try:
                resume_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": resume_prompt}]
                )

                cover_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": cover_prompt}]
                )

                # Step 5: Show Output (Using markdown for better formatting)
                st.subheader("📄 Optimized Resume")
                st.markdown(resume_response.choices[0].message.content)

                st.subheader("✉️ Cover Letter")
                st.markdown(cover_response.choices[0].message.content)

            except Exception as e:
                st.error(f"OpenAI API Error: {e}")

    else:
        st.error("Please upload resume and job description")
        