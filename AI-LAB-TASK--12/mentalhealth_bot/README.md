# 🧠 MindEase — Mental Health QnA Bot
**Lab 10 Project | Pipeline: MiniLM + FAISS + Flask**

---

## Pipeline (mirrors HadithBot.ipynb exactly)

```
mental_health_qna.csv
        ↓
   clean_text()          ← same function as HadithBot
        ↓
  MiniLM-L6-v2           ← same HuggingFace model
        ↓
  FAISS IndexFlatL2      ← same index type (L2/Euclidean)
        ↓
  similarity search      ← same .search(query_emb, k)
        ↓
  Flask + HTML UI        ← web interface added on top
```

---

## Project Structure

```
mentalhealth_bot/
├── mental_health_qna.csv         ← 80 QnA pairs (your dataset)
├── build_pipeline.py             ← Step 1-4: preprocess → embed → FAISS
├── app.py                        ← Flask backend
├── MentalHealthBot.ipynb         ← Notebook version (same as HadithBot style)
├── requirements.txt
└── templates/
    └── index.html                ← Chat UI frontend
```

After running build_pipeline.py, these files are generated:
```
├── cleaned_mental_health_data.csv   ← preprocessed dataset
├── mh_embeddings.npy                ← MiniLM vectors (384-dim)
└── mh_faiss.index                   ← FAISS index
```

---

## How to Run

### 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### 2 — Build the pipeline (run ONCE)
```bash
python build_pipeline.py
```
This will:
- Clean and preprocess all 80 QnA pairs
- Embed questions using `all-MiniLM-L6-v2` (384-dim vectors)
- Build and save a FAISS `IndexFlatL2` index

### 3 — Start the Flask app
```bash
python app.py
```

### 4 — Open in browser
```
http://localhost:5000
```

---

## HadithBot vs MentalHealthBot — Side by Side

| Step | HadithBot.ipynb | MentalHealthBot |
|------|----------------|-----------------|
| Dataset | LK-Hadith CSV files | mental_health_qna.csv |
| Preprocess | `clean_text()` | Same `clean_text()` |
| Model | `all-MiniLM-L6-v2` | Same model |
| Index | `faiss.IndexFlatL2` | Same index |
| Search | `faiss_index.search(q_emb, k)` | Same call |
| Output | `print()` in notebook | Flask + HTML chat UI |

---

## Features
- 🔍 Semantic similarity search (not keyword matching)
- 💬 Shows matched question + best answer
- 🔗 Shows 2 related topics per query
- 📊 Distance score displayed per result
- 🎨 Dark-themed responsive chat UI
- 📱 Mobile friendly

## Dataset Topics (80 QnA pairs)
Depression · Anxiety · Stress · PTSD · OCD · Bipolar · Therapy ·
CBT · Mindfulness · Sleep · Self-care · Coping · Boundaries ·
Trauma · Grief · Burnout · Panic attacks · Social anxiety · and more
