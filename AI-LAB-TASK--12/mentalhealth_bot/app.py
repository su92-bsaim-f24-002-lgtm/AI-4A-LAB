"""
Mental Health QnA Bot - Flask Backend
Pipeline: CSV → clean_text → MiniLM embeddings → FAISS → similarity search → Flask API
"""

from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import re
import os

app = Flask(__name__)

# ── Same clean_text function as HadithBot ─────────────────────
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)   # remove punctuations
    text = re.sub(r'\s+', ' ', text)               # remove extra spaces
    return text.strip()

# ── Load artifacts (built by build_pipeline.py) ───────────────
print("🔄 Loading model and index...")

model      = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
faiss_index = faiss.read_index('mh_faiss.index')
df         = pd.read_csv('cleaned_mental_health_data.csv')

print(f"✅ Ready — {faiss_index.ntotal} QnA vectors loaded")

# ── Same search function as HadithBot get_similar_hadith ──────
def get_similar_answers(query, count=3):
    cleaned_query  = clean_text(query)
    query_embedding = model.encode([cleaned_query])
    distances, indices = faiss_index.search(query_embedding, count)

    results = []
    for i in range(count):
        idx = indices[0][i]
        results.append({
            "question": df['question'].iloc[idx],
            "answer":   df['answer'].iloc[idx],
            "distance": round(float(distances[0][i]), 4)
        })
    return results

# ── Routes ────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('query', '').strip()

    if not query:
        return jsonify({'error': 'Empty question'}), 400

    results = get_similar_answers(query, count=3)

    # Primary answer = closest match (lowest L2 distance)
    best = results[0]

    return jsonify({
        'question': query,
        'answer':   best['answer'],
        'matched_q': best['question'],
        'distance': best['distance'],
        'related':  results[1:]    # 2 related answers
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
