from flask import Flask, request, jsonify, render_template
from groq import Groq
import os

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
#  GROQ API — 100% FREE, no credit card required
#  Get your free key at: https://console.groq.com  (takes 1 min)
#  Then set it:  GROQ_API_KEY=gsk_xxxx  (env var) or paste below
# ─────────────────────────────────────────────────────────────
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))

SYSTEM_PROMPT = """You are AdmissionBot, a friendly and knowledgeable University Admission Assistant for Greenfield University. You help prospective students with:

1. **Admission Requirements**: GPA thresholds, test scores (SAT/ACT), language requirements (IELTS/TOEFL), recommendation letters, essays.
2. **Application Deadlines**: 
   - Fall semester: Applications open Aug 1, Early Decision: Nov 1, Regular Decision: Jan 15
   - Spring semester: Applications open Feb 1, Deadline: Oct 1
   - Rolling admissions for some programs
3. **Programs & Departments**:
   - Engineering (CS, EE, Mechanical, Civil, Biomedical)
   - Business (MBA, Finance, Marketing, Accounting)
   - Arts & Sciences (Biology, Chemistry, Psychology, English, History)
   - Law School (JD, LLM)
   - Medical School (MD, Pre-Med track)
   - Education, Architecture, Fine Arts
4. **Tuition & Financial Aid**:
   - Undergraduate: $32,000/year domestic, $48,000/year international
   - Graduate: varies by program ($20,000–$55,000/year)
   - Scholarships: Merit-based, Need-based, Athletic, International Excellence Award
   - FAFSA deadline: March 1
5. **Campus Life**: Housing (guaranteed for freshmen), dining, clubs, sports, health center
6. **Transfer Students**: Min 30 credit hours, GPA 2.5+, transfer application deadline Feb 1
7. **International Students**: F-1 visa guidance, I-20 form, English proficiency requirements

Always be warm, helpful, and encouraging. If a question is outside your knowledge, politely suggest contacting admissions@greenfield.edu or calling (555) 123-4567. Keep responses concise but complete — use bullet points when listing multiple items. Never make up specific information not listed above; instead offer to connect them with the admissions office."""

conversation_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history
    
    data = request.json
    user_message = data.get("message", "").strip()
    reset = data.get("reset", False)
    
    if reset:
        conversation_history = []
        return jsonify({"response": "Conversation reset. How can I help you today?"})
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # Recommended replacement model on Groq
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history,
            max_tokens=1024,
            temperature=0.7,
        )

        assistant_message = response.choices[0].message.content

        # Add assistant response to history
        conversation_history.append({"role": "assistant", "content": assistant_message})

        # Keep history manageable (last 20 messages)
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]

        return jsonify({"response": assistant_message})

    except Exception as e:
        err = str(e)
        if "invalid_api_key" in err.lower() or "authentication" in err.lower():
            return jsonify({"error": "❌ Invalid Groq API key. Get your FREE key at https://console.groq.com"}), 401
        return jsonify({"error": f"Error: {err}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
