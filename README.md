# Diagnostic Interview Ingestion Engine

This Python-based ingestion engine analyzes transcribed diagnostic interviews and calculates key reasoning metrics. It uses a curated list of clinical features with associated likelihood ratios (LRs) organized by diagnostic neighborhoods (e.g., Cardiac, Dysphagia, Autoimmune).

## 🔍 Features

- Parses interview transcripts (PDF)
- Identifies captured diagnostic features
- Calculates:
  - Entropy reduction per diagnostic neighborhood
  - Geodesic distance to expert centroid
  - Number of diagnostic questions asked
  - Diagnostic efficiency score (questions / distance)

## 📂 Input

1. A PDF transcript of a diagnostic interview
2. A `cleaned_features.csv` file with columns:
   - `Feature`: clinical statement or cue
   - `Neighborhood`: diagnostic context (e.g., Cardiac)
   - `FeatureType`: MAJOR or minor
   - `Cleaned_LR`: likelihood ratio (empirical or consensus)
   - `Log_LR`: natural log of the LR

## 🧠 Output

The function `analyze_interview(pdf_path)` returns a dictionary with:
- `entropy_by_neighborhood`: DataFrame with entropy changes by region
- `geodesic_distance`: how far the reasoning path is from expert centroid
- `num_questions`: number of diagnostic questions (approximated by `?`)
- `efficiency_score`: reasoning efficiency

## 🛠 Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
