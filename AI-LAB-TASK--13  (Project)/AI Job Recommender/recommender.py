import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

class JobRecommender:
    def __init__(self, data_path='data/pakistan_jobs.csv'):
        self.data_path = data_path
        self.df = None
        self.tfidf = None
        self.job_vectors = None
        self.load_and_prepare()

    def load_and_prepare(self):
        """Load dataset and build TF-IDF vectors"""
        self.df = pd.read_csv(self.data_path)

        # Combine all job features into one string for vectorization
        self.df['combined_features'] = (
            self.df['title'].fillna('') + ' ' +
            self.df['skills_required'].fillna('') + ' ' +
            self.df['description'].fillna('') + ' ' +
            self.df['job_type'].fillna('') + ' ' +
            self.df['location'].fillna('')
        )

        # Build TF-IDF matrix
        self.tfidf = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),   # Unigrams + bigrams
            max_features=5000
        )
        self.job_vectors = self.tfidf.fit_transform(
            self.df['combined_features']
        )

    def build_user_profile(self, skills, experience, location, job_type=''):
        """Convert user input into a text profile"""
        profile = f"{skills} {location} {job_type} experience {experience} years"
        return profile

    def recommend(self, skills, experience, location, job_type='', top_n=10):
        """Return top N job recommendations"""
        user_profile = self.build_user_profile(
            skills, experience, location, job_type
        )

        # Vectorize user profile
        user_vector = self.tfidf.transform([user_profile])

        # Calculate cosine similarity
        similarities = cosine_similarity(user_vector, self.job_vectors).flatten()

        # Get top N indices
        top_indices = similarities.argsort()[::-1][:top_n]

        results = []
        for idx in top_indices:
            job = self.df.iloc[idx]
            score = round(float(similarities[idx]) * 100, 1)

            if score > 0:  # Only show relevant results
                results.append({
                    'title': job['title'],
                    'company': job['company'],
                    'location': job['location'],
                    'skills': job['skills_required'],
                    'experience': job['experience_required'],
                    'salary_min': int(job['salary_min']),
                    'salary_max': int(job['salary_max']),
                    'job_type': job['job_type'],
                    'description': job['description'],
                    'apply_link': job['apply_link'],
                    'match_score': score
                })

        return results