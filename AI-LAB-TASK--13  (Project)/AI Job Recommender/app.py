from flask import Flask, render_template, request, jsonify
from recommender import JobRecommender

app = Flask(__name__)

# Initialize recommender once at startup
recommender = JobRecommender(data_path='data/pakistan_jobs.csv')

@app.route('/')
def index():
    """Home page with input form"""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """Handle form submission and return recommendations"""
    # Get form data
    skills     = request.form.get('skills', '').strip()
    experience = request.form.get('experience', '0').strip()
    location   = request.form.get('location', '').strip()
    job_type   = request.form.get('job_type', '').strip()

    # Validate inputs
    if not skills:
        return render_template('index.html',
                               error="Please enter at least one skill.")

    # Get recommendations
    jobs = recommender.recommend(
        skills=skills,
        experience=experience,
        location=location,
        job_type=job_type,
        top_n=10
    )

    return render_template('results.html',
                           jobs=jobs,
                           user_skills=skills,
                           user_location=location,
                           user_experience=experience)

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """JSON API endpoint (optional)"""
    data = request.get_json()
    jobs = recommender.recommend(
        skills=data.get('skills', ''),
        experience=data.get('experience', 0),
        location=data.get('location', ''),
        top_n=10
    )
    return jsonify({'recommendations': jobs})

if __name__ == '__main__':
    app.run(debug=True, port=5000)