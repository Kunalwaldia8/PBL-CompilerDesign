from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample Job Description
job_description = """Looking for a software engineer with skills in Machine Learning Python, Java, SQL, React and Node.js."""

f=open("json_output.txt","r")
file_data=f.read()

# Sample Resumes
resumes = [
    file_data
]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform([job_description] + resumes)

# Compute Cosine Similarity
cosine_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

# Rank Resumes
ranked_resumes = sorted(enumerate(cosine_scores[0]), key=lambda x: x[1], reverse=True)

# Display Ranked Resumes
for rank, (index, score) in enumerate(ranked_resumes, start=1):
    print(f"Rank {rank}: Resume {index+1} - Score: {score*100:.2f}%")
