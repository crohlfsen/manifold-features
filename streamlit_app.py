# Prototype Diagnostic Interview Ingestion Engine
# Assumes preprocessed feature list with Log_LR and diagnostic neighborhoods

import fitz  # PyMuPDF for PDF reading
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
import umap

# Load cleaned feature definitions (assume already preprocessed)
FEATURES_PATH = "cleaned_features.csv"  # from earlier step
features_df = pd.read_csv(FEATURES_PATH)

# Load interview transcript PDF and extract text
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = " ".join([page.get_text() for page in doc])
    return text.lower()

# Match features in transcript
def match_features(transcript_text, features_df):
    matched = []
    for _, row in features_df.iterrows():
        if isinstance(row['Feature'], str) and row['Feature'].lower() in transcript_text:
            matched.append(row)
    return pd.DataFrame(matched)

# Entropy reduction per neighborhood
def compute_entropy_by_neighborhood(matched_df):
    grouped = matched_df.groupby('Neighborhood')['Log_LR'].sum().reset_index()
    grouped.columns = ['Neighborhood', 'EntropyReduction']
    return grouped

# Geodesic distance to expert centroid (simulated here as origin)
def compute_geodesic_distance(feature_vector, expert_vector=None):
    if expert_vector is None:
        expert_vector = np.zeros_like(feature_vector)
    return np.linalg.norm(feature_vector - expert_vector)

# Reasoning efficiency = number of questions / geodesic distance
def compute_efficiency(num_questions, geodesic_distance):
    return num_questions / geodesic_distance if geodesic_distance > 0 else np.nan

# Count number of questions in the transcript (approximate by '?')
def count_questions(transcript_text):
    return transcript_text.count("?")

# Main runner
def analyze_interview(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    matched = match_features(text, features_df)
    entropy_by_neigh = compute_entropy_by_neighborhood(matched)

    # Create binary feature vector
    all_features = features_df['Feature'].tolist()
    vector = np.array([1 if feat in matched['Feature'].values else 0 for feat in all_features])

    geodesic = compute_geodesic_distance(vector)
    num_questions = count_questions(text)
    efficiency = compute_efficiency(num_questions, geodesic)

    return {
        "entropy_by_neighborhood": entropy_by_neigh,
        "geodesic_distance": geodesic,
        "num_questions": num_questions,
        "efficiency_score": efficiency
    }
