import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity

# Ensure necessary NLTK components are available
nltk.download("punkt")
nltk.download("stopwords")

# Function to preprocess text (Tokenization + Stopword Removal)
def preprocess_text(text):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text.lower())  # Tokenize and lowercase
    words = [word for word in words if word.isalnum() and word not in stop_words]  # Remove punctuation and stopwords
    return words

# Function to compute TF-IDF vectors manually
def compute_tfidf_vector(text, corpus):
    words = preprocess_text(text)
    word_counts = Counter(words)  # Count word frequency
    total_words = sum(word_counts.values())

    # Compute Term Frequency (TF)
    tf_vector = {word: count / total_words for word, count in word_counts.items()}

    # Compute Inverse Document Frequency (IDF)
    idf_vector = {}
    num_docs = len(corpus)
    for word in set(words):
        doc_count = sum(1 for doc in corpus if word in doc)
        idf_vector[word] = np.log((1 + num_docs) / (1 + doc_count)) + 1  # Smoothing

    # Compute TF-IDF scores
    tfidf_vector = {word: tf_vector[word] * idf_vector[word] for word in words}

    return tfidf_vector

# Convert dictionary to vector for cosine similarity
def vectorize(tfidf_dict, all_words):
    return np.array([tfidf_dict.get(word, 0) for word in all_words])

# Example texts
resume_text = "I am a Python Developer with expertise in Flask, Machine Learning, and NLP."
job_description = "Looking for a skilled developer with Python, Flask, and AI experience."

# Create corpus for IDF calculations
corpus = [preprocess_text(resume_text), preprocess_text(job_description)]

# Compute TF-IDF vectors
resume_tfidf = compute_tfidf_vector(resume_text, corpus)
job_tfidf = compute_tfidf_vector(job_description, corpus)

# Get all unique words across both texts
all_words = list(set(resume_tfidf.keys()).union(set(job_tfidf.keys())))

# Convert to numerical vectors
resume_vector = vectorize(resume_tfidf, all_words)
job_vector = vectorize(job_tfidf, all_words)

# Compute cosine similarity
similarity_score = cosine_similarity([resume_vector], [job_vector])[0][0]

# Print similarity score
print(f"Resume Match Score: {similarity_score * 100:.2f}%")