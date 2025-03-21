import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import fitz
from docx import Document
import streamlit as st
import google.generativeai as genai

genai_api_key = "AIzaSyAa-DKhqGewqHMEYYA2SnbgJK73zRh-EFA"
genai.configure(api_key=genai_api_key)


try:
    nltk.data.find("corpora/stopwords")
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download("wordnet")


def extract_pdf(file):
    text = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")  
    for page in doc:
        text += page.get_text("text") + "\n"
    return text.strip()


def extract_docx(file):
    text = ""
    document = Document(file)
    for para in document.paragraphs:
        text += para.text + "\n"
    return text.strip()


def preprocess_text(text):
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text.lower())
    words = [lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words]
    return " ".join(words)


st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")


st.markdown("""
    <style>
        .title {
            text-align: center; 
            font-size: 34px; /* Slightly larger */
            font-weight: bold; 
            color: #007bff;
        }
        .sub-title {
            text-align: center; 
            font-size: 22px; /* Slightly larger */
            color: gray;
        }
        .score {
            font-size: 22px;
            font-weight: bold;
        }
        .stButton button {
            width: 100%;
            background-color: #007bff !important;
            color: white !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("<p class='title'>📄 AI-Powered Resume Analyzer</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Effortlessly analyze resumes and get instant insights.</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


st.sidebar.header("📂 Upload Resume & Job Description")
uploaded_file = st.sidebar.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])
job_desc = st.sidebar.text_area("📄 Paste Job Description", height=150)


if st.sidebar.button("Analyze Resume"):
    if uploaded_file:
        resume_text = ""


        if uploaded_file.type == "application/pdf":
            resume_text = extract_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_docx(uploaded_file)
        else:
            st.error("❌ Unsupported file format. Please upload a PDF or DOCX.")
            st.stop()


        if not job_desc.strip():
            st.warning("⚠️ No job description provided. Analysis will be based only on resume.")
            job_desc = "No job description provided."

        
        prompt = """
        You are an AI assistant. Extract the candidate's Name, Email, and Phone Number from the resume.
        Then, compare the resume with the job description and provide a percentage match based on skills, experience, and relevance.
        Strictly format the output as: <Name> <Email> <Phone> <Score%>
        """
        data = f"Resume:\n{resume_text}\n\nJob Description:\n{job_desc}\n\n{prompt}"

        
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(data)

        
        if response and response.text:
            st.success("✅ Resume Analysis Complete!")
            
        
            result_lines = response.text.strip().split("\n")
            last_line = result_lines[-1]  # Assuming last line has score
            parts = last_line.split()
            
            if parts and parts[-1].endswith("%"):
                score = int(parts[-1].replace("%", ""))  # Convert to integer
                
                # Assign color based on score threshold
                score_color = "green" if score > 50 else "red"
                score_html = f"<p class='score' style='color: {score_color};'>Score: {score}%</p>"
                
                # Display the formatted score
                st.markdown(score_html, unsafe_allow_html=True)
            
            st.write(response.text)
        else:
            st.error("❌ Failed to analyze the resume. Please try again.")

    else:
        st.warning("⚠️ Please upload a resume.")

# Key Features Section
st.markdown("## Why Choose Our AI Resume Analyzer?")
st.markdown("""
- **AI-Powered, Not Just Keywords:** Unlike traditional ATS, our AI doesn't reject resumes based on missing keywords. Instead, it **understands context** and evaluates skills fairly.
- **Supports Both PDF & DOCX Formats:** No need to open resumes manually. Our AI automatically processes both **PDF and DOCX** files.
- **Instantly Extracts Candidate Details:** It extracts **Name, Email, and Phone Number** directly from resumes for quick HR review.
- **Unbiased & Fair Evaluation:** ATS systems can unfairly filter resumes, but our AI **objectively** assesses based on experience and skills, eliminating biases.
- **Fast & Efficient Resume Analysis:** Get **instant** feedback, job-match scores, and resume insights in **seconds**.
- **No Fear of Keyword Manipulation:** Candidates no longer need to **stuff** keywords—our AI analyzes **true skill relevance**, not just text-matching.
- **Industry-Grade Accuracy:** Our AI uses **cutting-edge NLP** to deliver accurate resume evaluations that help recruiters make **better hiring decisions**.
""")


st.markdown("### Benefits for HR Professionals")
col1, col2 = st.columns(2)

with col1:
    st.success("**Faster Hiring Process**\n\nSave **hours** of resume screening with AI automation.")
    st.info("**Eliminates Bias**\n\nEvaluates resumes fairly without ATS-style keyword discrimination.")
    
with col2:
    st.warning("**More Accurate Candidate Matches**\n\nAI **scores resumes based on actual skills** rather than keyword frequency.")
    st.error("**Seamless Resume Extraction**\n\nExtracts essential candidate details instantly.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>© 2025 AI Resume Analyzer | made by MUHAMMAD AHMAD NADEEM</p>", unsafe_allow_html=True)
