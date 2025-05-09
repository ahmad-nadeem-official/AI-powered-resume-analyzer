import fitz
from docx import Document
import streamlit as st
import google.generativeai as genai
import pandas as pd
import smtplib
from email.message import EmailMessage

# Setup Gemini API
genai_api_key = "AIzaSyClwV_FGE6CWL0RA5v68UZwKIidGPNYdsY"
genai.configure(api_key=genai_api_key)

# Functions
def extract_pdf(file):
    text = ""
    pdf_bytes = file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page in doc:
        text += page.get_text("text") + "\n"
    doc.close()
    return text.strip()

def extract_docx(file):
    text = ""
    document = Document(file)
    for para in document.paragraphs:
        text += para.text + "\n"
    return text.strip()

# UI setup
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")
st.markdown("<h1>📄 AI-Powered Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p>Effortlessly analyze resumes and get instant insights.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📂 Upload Resume & Job Description")
uploaded_files = st.sidebar.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"], accept_multiple_files=True)
job_desc = st.sidebar.text_area("📄 Paste Job Description", height=150)

# Analyze button
if st.sidebar.button("Analyze Resume"):
    if uploaded_files:
        if not job_desc.strip():
            st.warning("⚠️ No job description provided. Analysis will be based only on resume.")
            job_desc = "No job description provided."

        model = genai.GenerativeModel("gemini-1.5-flash")
        names, emails, phones, scores = [], [], [], []

        for file in uploaded_files:
            if file.name.endswith(".pdf"):
                resume_text = extract_pdf(file)
            elif file.name.endswith(".docx"):
                resume_text = extract_docx(file)
            else:
                st.error(f"❌ Unsupported file format: {file.name}")
                continue

            prompt = """
            You are an AI assistant. Extract the candidate's Name, Email, and Phone Number from the resume.
            Then, compare the resume with the job description and provide a percentage match based on skills, experience, and relevance.
            Strictly format the output as: <Name>, <Email>, <Phone>, <Score>
            """

            data = f"Resume:\n{resume_text}\n\nJob Description:\n{job_desc}\n\n{prompt}"
            response = model.generate_content(data)

            if response and response.text:
                last_line = response.text.strip().split("\n")[-1]
                parts = [x.strip() for x in last_line.split(",")]
                if len(parts) == 4:
                    name, email, phone, score_str = parts
                    try:
                        score = int(score_str.replace("%", "").strip())
                        names.append(name)
                        emails.append(email)
                        phones.append(phone)
                        scores.append(score)
                    except ValueError:
                        st.warning(f"⚠️ Could not parse score for file {file.name}")
                else:
                    st.warning(f"⚠️ Unexpected format for file {file.name}")
            else:
                st.error(f"❌ Failed to analyze {file.name}")

        st.session_state.df = pd.DataFrame({
            "Name": names,
            "Email": emails,
            "Phone": phones,
            "Score": scores
        })
        st.success("✅ Resume Analysis Complete!")

# Show analysis if available
if "df" in st.session_state:
    df = st.session_state.df
    st.dataframe(df)

    st.markdown("### 📬 Send Emails to Eligible Candidates")

    # Minimum score filter
    min_score = st.number_input("🎯 Minimum Eligibility Score (%)", min_value=0, max_value=100, value=50)

    # Email form inputs
    st.text_input("📧 Email Subject", key="email_subject")
    st.text_area("📄 Email Body", key="email_body")
    st.text_input("🔒 Enter your email password", type="password", key="email_password")

    if st.button("📨 Send Interview Emails"):
        subject = st.session_state["email_subject"]
        body = st.session_state["email_body"]
        smtp_password = st.session_state["email_password"]

        if not subject or not body or not smtp_password:
            st.warning("⚠️ Please fill in all email fields.")
        else:
            eligible_df = df[df["Score"] >= min_score]
            try:
                sender_email = "ahmadnadeem701065@gmail.com"
                smtp_server = "smtp.gmail.com"
                smtp_port = 587

                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, smtp_password)

                for _, row in eligible_df.iterrows():
                    msg = EmailMessage()
                    msg["From"] = sender_email
                    msg["To"] = row["Email"]
                    msg["Subject"] = subject
                    msg.set_content(body)
                    server.send_message(msg)

                server.quit()
                st.success(f"📨 Emails sent to {len(eligible_df)} eligible candidates!")
            except Exception as e:
                st.error(f"❌ Failed to send emails. Error: {e}")
else:
    st.info("ℹ️ Upload and analyze resumes to enable the email feature.")
