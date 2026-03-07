"""
Personality Profiling based on facial feature measurements.
Maps normalised measurements to MBTI personality types.
This is for educational/entertainment purposes only.
"""

# Full MBTI type descriptions
MBTI_PROFILES = {
    "INTJ": {
        "name": "The Architect",
        "description": "Strategic, independent, and determined. "
                       "INTJs are analytical problem-solvers who thrive on creating efficient systems.",
        "strengths": ["Strategic thinking", "Independence", "Determination", "High standards"],
        "challenges": ["May appear aloof", "Perfectionism", "Impatience with inefficiency"],
    },
    "INTP": {
        "name": "The Logician",
        "description": "Inventive, curious, and logical. "
                       "INTPs love abstract theories and seek to understand the universe.",
        "strengths": ["Analytical mind", "Objectivity", "Imagination", "Originality"],
        "challenges": ["Overthinking", "Social discomfort", "Absent-mindedness"],
    },
    "ENTJ": {
        "name": "The Commander",
        "description": "Bold, imaginative, and strong-willed leaders who always find a way.",
        "strengths": ["Leadership", "Efficiency", "Strategic vision", "Confidence"],
        "challenges": ["Impatience", "Stubbornness", "Intolerance of perceived incompetence"],
    },
    "ENTP": {
        "name": "The Debater",
        "description": "Smart, curious, and intellectually bold. ENTPs enjoy mental sparring.",
        "strengths": ["Quick thinking", "Charisma", "Creativity", "Energy"],
        "challenges": ["Argumentativeness", "Insensitivity", "Difficulty with follow-through"],
    },
    "INFJ": {
        "name": "The Advocate",
        "description": "Quiet, mystical, and inspiring. INFJs are idealists who act on their convictions.",
        "strengths": ["Insightfulness", "Determination", "Compassion", "Vision"],
        "challenges": ["Perfectionism", "Burnout", "Difficulty opening up"],
    },
    "INFP": {
        "name": "The Mediator",
        "description": "Poetic, kind, and altruistic. INFPs seek harmony and authenticity.",
        "strengths": ["Empathy", "Creativity", "Open-mindedness", "Passion"],
        "challenges": ["Over-idealism", "Self-isolation", "Emotional vulnerability"],
    },
    "ENFJ": {
        "name": "The Protagonist",
        "description": "Charismatic, inspiring leaders who mesmerise their followers.",
        "strengths": ["Natural leadership", "Empathy", "Reliability", "Charisma"],
        "challenges": ["Over-involvement", "Idealism", "Sensitivity to criticism"],
    },
    "ENFP": {
        "name": "The Campaigner",
        "description": "Enthusiastic, creative, and sociable free spirits.",
        "strengths": ["Enthusiasm", "Creativity", "Sociability", "Optimism"],
        "challenges": ["Difficulty focusing", "Over-thinking", "Emotional stress"],
    },
    "ISTJ": {
        "name": "The Logistician",
        "description": "Practical, fact-minded, and reliable. ISTJs value tradition and order.",
        "strengths": ["Integrity", "Practical logic", "Dedication", "Patience"],
        "challenges": ["Stubbornness", "Insensitivity", "Resistance to change"],
    },
    "ISFJ": {
        "name": "The Defender",
        "description": "Very dedicated and warm protectors, always ready to defend loved ones.",
        "strengths": ["Supportiveness", "Reliability", "Patience", "Observation"],
        "challenges": ["Shyness", "Overloading themselves", "Reluctance to change"],
    },
    "ESTJ": {
        "name": "The Executive",
        "description": "Excellent administrators. Unmatched at managing things and people.",
        "strengths": ["Organisation", "Dedication", "Strong will", "Direct honesty"],
        "challenges": ["Inflexibility", "Difficulty relaxing", "Judgmental"],
    },
    "ESFJ": {
        "name": "The Consul",
        "description": "Extraordinarily caring, social, and popular. Always eager to help.",
        "strengths": ["Loyalty", "Sensitivity", "Warmth", "Social skills"],
        "challenges": ["Worried about social status", "Inflexibility", "Vulnerability to criticism"],
    },
    "ISTP": {
        "name": "The Virtuoso",
        "description": "Bold, practical experimenters who master all kinds of tools.",
        "strengths": ["Optimistic energy", "Creativity", "Practicality", "Spontaneity"],
        "challenges": ["Stubbornness", "Insensitivity", "Risk-prone"],
    },
    "ISFP": {
        "name": "The Adventurer",
        "description": "Flexible, charming artists. Always ready to explore and experience.",
        "strengths": ["Charm", "Sensitivity", "Imagination", "Passion"],
        "challenges": ["Fiercely independent", "Easily stressed", "Unpredictability"],
    },
    "ESTP": {
        "name": "The Entrepreneur",
        "description": "Smart, energetic, and perceptive. Enjoys living on the edge.",
        "strengths": ["Bold", "Rational", "Practical", "Perceptive"],
        "challenges": ["Impatience", "Risk-prone", "Difficulty in academics"],
    },
    "ESFP": {
        "name": "The Entertainer",
        "description": "Spontaneous, energetic, and enthusiastic. Life is never boring around them.",
        "strengths": ["Bold", "Original", "Observant", "Excellent people skills"],
        "challenges": ["Sensitive", "Conflict-averse", "Easily bored"],
    },
}


class PersonalityProfiler:
    """Map normalised facial measurements to an MBTI personality type."""

    def __init__(self, normalized_measurements: dict):
        self.nm = normalized_measurements
        self._type = None
        self._scores = None

    # ------------------------------------------------------------------
    def _compute_scores(self):
        """Score each of the four MBTI dichotomies from measurements."""
        nm = self.nm

        face_ratio = nm.get("face_ratio", 1.2)
        eye_open = (nm.get("left_eye_openness", 0.3) + nm.get("right_eye_openness", 0.3)) / 2
        eye_space = nm.get("eye_spacing_ratio", 0.3)
        nose_w = nm.get("nose_width_ratio", 0.25)
        mouth_w = nm.get("mouth_width_ratio", 0.38)
        mouth_h = nm.get("mouth_height_ratio", 0.08)
        jaw_w = nm.get("jaw_width_ratio", 0.72)

        # E/I – wider jaw & wider mouth lean Extraverted
        ei = 0.5 + (jaw_w - 0.72) * 2 + (mouth_w - 0.38) * 1.5
        # S/N – higher face ratio & wider nose lean Sensing
        sn = 0.5 + (face_ratio - 1.25) * 1.5 + (nose_w - 0.25) * 2
        # T/F – narrow mouth & low eye openness lean Thinking
        tf = 0.5 - (mouth_h - 0.08) * 3 - (eye_open - 0.32) * 2
        # J/P – wide jaw & medium eye spacing lean Judging
        jp = 0.5 + (jaw_w - 0.72) * 1.5 - abs(eye_space - 0.30) * 2

        # Clamp to [0, 1]
        def clamp(v):
            return max(0.0, min(1.0, v))

        self._scores = {
            "E_I": clamp(ei),   # >0.5 → E, else I
            "S_N": clamp(sn),   # >0.5 → S, else N
            "T_F": clamp(tf),   # >0.5 → T, else F
            "J_P": clamp(jp),   # >0.5 → J, else P
        }
        return self._scores

    # ------------------------------------------------------------------
    def get_type(self) -> str:
        """Return the 4-letter MBTI code."""
        if self._type is not None:
            return self._type

        scores = self._compute_scores()
        letters = ""
        letters += "E" if scores["E_I"] >= 0.5 else "I"
        letters += "S" if scores["S_N"] >= 0.5 else "N"
        letters += "T" if scores["T_F"] >= 0.5 else "F"
        letters += "J" if scores["J_P"] >= 0.5 else "P"

        self._type = letters
        return self._type

    # ------------------------------------------------------------------
    def get_full_profile(self) -> dict:
        """Return the full personality profile."""
        mbti = self.get_type()
        scores = self._scores
        profile = MBTI_PROFILES.get(mbti, MBTI_PROFILES["INTJ"])

        confidence = 0
        for v in scores.values():
            confidence += abs(v - 0.5)
        confidence = min(1.0, confidence / 2) * 100  # percentage

        return {
            "type": mbti,
            "name": profile["name"],
            "description": profile["description"],
            "strengths": profile["strengths"],
            "challenges": profile["challenges"],
            "confidence": round(confidence, 1),
            "dimension_scores": {
                "E_vs_I": round(scores["E_I"] * 100, 1),
                "S_vs_N": round(scores["S_N"] * 100, 1),
                "T_vs_F": round(scores["T_F"] * 100, 1),
                "J_vs_P": round(scores["J_P"] * 100, 1),
            },
        }

    # ------------------------------------------------------------------
    def get_recommendations(self) -> list:
        """Return personalised recommendations based on the type."""
        mbti = self.get_type()
        recs = {
            "INTJ": ["Focus on strategic long-term planning", "Allow time for deep analytical work", "Practice patience with others"],
            "INTP": ["Explore creative problem-solving", "Set aside time for theoretical exploration", "Work on communicating ideas simply"],
            "ENTJ": ["Lead projects with confidence", "Delegate effectively", "Practice active listening"],
            "ENTP": ["Channel creativity into focused projects", "Build on your networking skills", "Follow through on ideas"],
            "INFJ": ["Trust your intuition", "Set healthy boundaries", "Use your vision to inspire others"],
            "INFP": ["Express yourself through creative outlets", "Connect with like-minded communities", "Balance idealism with pragmatism"],
            "ENFJ": ["Mentor and develop others", "Lead community initiatives", "Take time for self-care"],
            "ENFP": ["Pursue diverse interests", "Build meaningful connections", "Create structure for your ideas"],
            "ISTJ": ["Create reliable systems", "Document processes methodically", "Embrace gradual change"],
            "ISFJ": ["Support your team with dedication", "Create comfortable environments", "Speak up about your needs"],
            "ESTJ": ["Organise team efforts efficiently", "Set clear expectations", "Be open to alternative approaches"],
            "ESFJ": ["Build strong community bonds", "Support others generously", "Maintain healthy boundaries"],
            "ISTP": ["Pursue hands-on challenges", "Master practical skills", "Stay flexible and adaptable"],
            "ISFP": ["Express yourself artistically", "Stay true to your values", "Embrace new experiences"],
            "ESTP": ["Take calculated risks", "Use your energy to motivate others", "Develop long-term focus"],
            "ESFP": ["Bring enthusiasm to everything", "Connect people and ideas", "Plan for the future"],
        }
        return recs.get(mbti, ["Stay curious and keep exploring!"])
