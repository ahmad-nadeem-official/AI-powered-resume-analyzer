from flask import Flask, request, jsonify
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import google.generativeai as genai
from dotenv import load_dotenv
from docx import Document
import fitz 
import os

# load_dotenv("api.env")
# gemini_api_key = os.getenv("GEMINI_API_KEY")

try:
    nltk.data.find("corpora/stopwords")
    nltk.data.find("tokenizers/punkt")
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download("wordnet")

app = Flask(__name__)    

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

prompt = '''
You are an AI assistant. Extract the candidate's Name, Email, and Phone Number from the resume.
Then, compare the resume with the job description and provide a percentage match based on skills, experience, and relevance.
Strictly format the output as: 

<Name> <Email> <Phone> <Score%>

Example:
John Doe johndoe@gmail.com 1234567890 75.32%
'''

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    """Analyze Resume Match Score"""
    if "file" not in request.files or "job_desc" not in request.form:
        return jsonify({"error": "File and Job Description are required"}), 400
    
    file = request.files["file"]
    job_desc = request.form["job_desc"].strip()

    # Extract resume text
    if file.filename.endswith(".pdf"):
        resume_text = extract_pdf(file)
    elif file.filename.endswith(".docx"):
        resume_text = extract_docx(file)
    else:
        return jsonify({"error": "Unsupported file format"}), 400

    # Preprocess text
    resume_text = preprocess_text(resume_text)
    job_desc = preprocess_text(job_desc)

    # Generate AI Score
    data = f"Resume:\n{resume_text}\n\nJob Description:\n{job_desc}\n\n{prompt}"

    gemini_api_key ="AIzaSyAa-DKhqGewqHMEYYA2SnbgJK73zRh-EFA"
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(data)

    # Extract percentage score
    score = response.text.strip()

    return jsonify({"match_score": score})

if __name__ == "__main__":
    app.run(debug=True)


# genai.configure(api_key=gemini_api_key)
# model = genai.GenerativeModel("gemini-1.5-flash")
# response = model.generate_content(data)