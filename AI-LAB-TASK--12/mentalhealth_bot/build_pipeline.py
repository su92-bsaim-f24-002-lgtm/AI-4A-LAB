import re
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os

# ── Step 1: Load dataset ──────────────────────────────────────
print("📂 Loading dataset...")
df = pd.read_csv('mental_health_qna.csv')
print(f"   Loaded {len(df)} QnA pairs")
print(df.head(2))

# ── Step 2: Preprocess (same clean_text as HadithBot) ─────────
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)   # remove punctuations
    text = re.sub(r'\s+', ' ', text)               # remove extra spaces
    return text.strip()

print("\n🧹 Preprocessing text...")
df['Cleaned_Question'] = df['question'].astype(str).apply(clean_text)
df['Cleaned_Answer']   = df['answer'].astype(str).apply(clean_text)

df.to_csv('cleaned_mental_health_data.csv', index=False)
print(f"   Saved cleaned_mental_health_data.csv")

# ── Step 3: Embed with MiniLM (same model as HadithBot) ───────
print("\n🤖 Loading SentenceTransformer model (all-MiniLM-L6-v2)...")
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

print("   Encoding questions...")
embeddings = model.encode(df['Cleaned_Question'].tolist(), show_progress_bar=True)
embeddings = np.array(embeddings)
print(f"   Embeddings shape: {embeddings.shape}")

np.save('mh_embeddings.npy', embeddings)
print("   Saved mh_embeddings.npy")

# ── Step 4: Build FAISS index (same as HadithBot) ─────────────
print("\n📦 Building FAISS index...")
dimensions = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dimensions)   # Euclidean Distance (same as HadithBot)
faiss_index.add(embeddings)
print(f"   Index contains {faiss_index.ntotal} vectors")

faiss.write_index(faiss_index, 'mh_faiss.index')
print("   Saved mh_faiss.index")

# ── Step 5: Quick test (same as get_similar_hadith) ───────────
print("\n🔍 Test search: 'How do I deal with stress?'")
query = 'How do I deal with stress?'
q_emb = model.encode([clean_text(query)])
distances, indices = faiss_index.search(q_emb, 3)

for i in range(3):
    print(f"\n  Result {i+1} | Distance: {distances[0][i]:.4f}")
    print(f"  Q: {df['question'].iloc[indices[0][i]]}")
    print(f"  A: {df['answer'].iloc[indices[0][i]][:120]}...")

print("\n✅ Pipeline complete! Run 'python app.py' to start the Flask app.")
