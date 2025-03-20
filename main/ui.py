import streamlit as st
import requests

# Set page title and layout
st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

# Title and Branding
st.markdown(
    "<h2 style='text-align: left; color: #007bff;'>📄 Resume Analyzer</h2>", 
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar - File Upload
st.sidebar.header("📂 Upload Your Resume")
uploaded_file = st.sidebar.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

# Sidebar - Job Description Input
job_desc = st.sidebar.text_area("📄 Paste Job Description (Optional)", height=150)

# Process Button
if st.sidebar.button("Analyze Resume"):
    if uploaded_file:
        files = {"file": uploaded_file.getvalue()}
        data = {"job_desc": job_desc}
        
        # Call backend API (Assuming FastAPI or Flask)
        response = requests.post("http://127.0.0.1:5000/analyze", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ Resume Match Score: **{result['match_score']}%**")
        else:
            st.error("❌ Error analyzing resume. Please try again.")
    else:
        st.warning("⚠️ Please upload a resume.")

# UI Sections - Why Choose Us?
st.markdown("### 🚀 Why Choose Our AI Resume Analyzer?")
col1, col2 = st.columns(2)

with col1:
    st.info("🔍 **Tailored Scoring for Job Descriptions**\n\nYour resume is scored based on alignment with job descriptions.")

    st.success("💡 **Continuous AI Innovation**\n\nWe use cutting-edge AI models to provide accurate resume analysis.")

with col2:
    st.warning("🧠 **Multiple AI Perspectives**\n\nOur AI uses different models to provide diverse feedback.")

    st.error("📊 **Understanding Variability**\n\nResumes are evaluated from multiple lenses for a better perspective.")

# UI Sections - Features
st.markdown("### 🔥 Features of Our Resume Analyzer")
st.markdown("""
✅ **Smart Resume Analysis** - Instantly get insights on resume effectiveness.  
✅ **Detailed Insights** - Understand readability, impact, and industry benchmarks.  
✅ **Actionable Recommendations** - Improve wording, formatting, and optimization.  
""")







# import streamlit as st
# from PIL import Image

# def main():
#     # Page Configuration
#     st.set_page_config(page_title="Resume Analyzer", layout="wide")
    
#     # Header
#     st.markdown("""
#         <h1 style='text-align: left; color: #2C3E50;'>Resume Analyzer</h1>
#         <hr style='border: 1px solid #ddd;'>
#     """, unsafe_allow_html=True)
    
#     # Layout - File Upload & Job Description
#     col1, col2 = st.columns([2, 1])
#     with col1:
#         st.subheader("Upload Your Resume")
#         file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"], help="Only PDF or DOCX files are supported.")
    
#     with col2:
#         st.subheader("Enter Job Description")
#         job_desc = st.text_area("Paste the job description for better matching (optional)")
    
#     # Submit Button
#     if st.button("Analyze Resume", use_container_width=True):
#         if file:
#             st.success("Resume uploaded successfully. Processing...")
#         else:
#             st.error("Please upload a resume file before analyzing.")
    
#     # Feature Sections
#     st.markdown("""
#     <h2 style='text-align: center;'>Why Choose Our AI Resume Analyzer?</h2>
#     """, unsafe_allow_html=True)
    
#     # Features Grid
#     col1, col2 = st.columns(2)
#     with col1:
#         st.info("**Tailored Scoring for Job Descriptions**\n\nOur AI evaluates how well your resume aligns with job descriptions.")
#         st.info("**Continuous Innovation for Better Results**\n\nWe integrate the latest AI models to stay ahead.")
#     with col2:
#         st.info("**Multiple AI Perspectives**\n\nDiverse AI models provide comprehensive resume feedback.")
#         st.info("**Understanding Variability in Results**\n\nAI models interpret resumes differently, offering varied insights.")
    
#     st.markdown("""
#     <h2 style='text-align: center;'>How It Works</h2>
#     """, unsafe_allow_html=True)
    
#     st.markdown("""
#     1. **Upload Your Resume** - Supported formats: PDF, DOCX.
#     2. **Add Job Description (Optional)** - Paste the job description to improve analysis.
#     3. **Get Instant Analysis** - AI evaluates your resume for key insights.
#     """, unsafe_allow_html=True)
    
# if __name__ == "__main__":
#     main()

