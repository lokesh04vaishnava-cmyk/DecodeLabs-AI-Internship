import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import os

# Create raw_skills.csv if it doesn't exist
if not os.path.exists("raw_skills.csv"):
    data = """role,skills
Data Scientist,Python SQL Machine Learning Data Analysis Statistics Pandas NumPy
DevOps Engineer,AWS Docker Kubernetes CI/CD Automation Cloud Linux Git
Backend Developer,Java Python SQL APIs Spring Boot Databases Git
Cloud Architect,AWS Cloud Computing Automation Docker Kubernetes Networking Security
Frontend Developer,JavaScript React CSS HTML UI Design Web Design Git
Data Engineer,Python SQL ETL Data Pipelines Spark Cloud AWS
ML Engineer,Python Machine Learning TensorFlow PyTorch Data Structures Algorithms
System Administrator,Linux Networking Automation Security Cloud Bash Scripting
Full Stack Developer,JavaScript Python React Node.js SQL APIs Git
Cybersecurity Analyst,Security Networking Linux Python Risk Assessment Cloud"""
    with open("raw_skills.csv", "w") as f:
        f.write(data)
    print("Created raw_skills.csv")

df = pd.read_csv("raw_skills.csv")

print("Loaded job roles:")
print(df['role'].tolist())
print()

# Get user input — minimum 3 skills required (per spec)
def get_user_skills():
    print("Enter 3 skills you have (e.g. Python, Cloud, Automation):")
    skills = []
    for i in range(1, 4):
        skill = input(f"Skill {i}: ").strip()
        skills.append(skill)
    return " ".join(skills)   # join into one string, same format as dataset

user_input = get_user_skills()

# ── STEP 2: VECTOR MAPPING (TF-IDF) ───────────────────
# Combine user profile + all job roles into one corpus
# so they share the same vocabulary space
corpus = df['skills'].tolist() + [user_input]

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

# Last row = user vector, everything before = job role vectors
job_vectors = tfidf_matrix[:-1]
user_vector = tfidf_matrix[-1]

# ── STEP 3: SCORING (Cosine Similarity) ───────────────
similarity_scores = cosine_similarity(user_vector, job_vectors).flatten()

df['similarity_score'] = similarity_scores

# ── STEP 4: SORTING + FILTERING ───────────────────────
top_matches = df.sort_values(by='similarity_score', ascending=False).head(3)

# ── OUTPUT ─────────────────────────────────────────────
print("\n" + "=" * 50)
print("   TOP 3 RECOMMENDED CAREER PATHS")
print("=" * 50)
for i, row in enumerate(top_matches.itertuples(), 1):
    match_percent = row.similarity_score * 100
    print(f"{i}. {row.role}  —  {match_percent:.1f}% match")
print()

def validate_skills(user_skills_list, vectorizer):
    vocab = vectorizer.vocabulary_.keys() if hasattr(vectorizer, 'vocabulary_') else []
    unknown = [s for s in user_skills_list if s.lower() not in vocab]
    if unknown:
        print(f"Note: {unknown} not recognized in our skill database — recommendations may be less accurate.")