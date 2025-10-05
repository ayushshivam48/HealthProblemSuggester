import streamlit as st

# ---------------------------
# 🩺 Health Problem Suggester – Streamlit Version
# ---------------------------

st.set_page_config(page_title="🩺 Health Problem Suggester", page_icon="🩺", layout="centered")

# Symptom database
problem_db = {
    "Heart Problem": {
        "symptoms": {"chest pain": 3, "shortness of breath": 3, "palpitations": 2, 
                     "high bp": 1, "irregular heartbeat": 2, "fatigue":1},
        "description": "Could indicate coronary artery disease, arrhythmia, or risk of heart attack.",
        "advice": "⚠️ Consult a cardiologist immediately. ECG and medical checkups are recommended."
    },
    "Respiratory Issue": {
        "symptoms": {"cough": 2, "shortness of breath": 2, "wheezing": 2, 
                     "asthma": 3, "lung infection": 2},
        "description": "Could indicate asthma, bronchitis, pneumonia, or viral infections.",
        "advice": "💨 Consult a pulmonologist if symptoms persist. Rest and hydration are recommended."
    },
    "Digestive Issue": {
        "symptoms": {"stomach pain": 2, "nausea": 2, "vomiting": 2, 
                     "diarrhea": 2, "acid reflux": 2, "bloating":1},
        "description": "Could indicate gastritis, indigestion, or gastrointestinal infection.",
        "advice": "🍽️ Maintain a balanced diet and consult a gastroenterologist if symptoms persist."
    },
    "Musculoskeletal Pain": {
        "symptoms": {"joint pain": 3, "back pain": 3, "muscle ache": 2, 
                     "swelling": 2, "stiffness": 2},
        "description": "Could indicate arthritis, muscle strain, or other musculoskeletal disorders.",
        "advice": "🏃 Exercise, physiotherapy, or orthopedist consultation recommended."
    },
    "Neurological Issue": {
        "symptoms": {"headache": 2, "dizziness": 2, "numbness": 3, 
                     "tingling": 2, "seizure": 3},
        "description": "Could indicate migraines, neuropathy, or other neurological conditions.",
        "advice": "🧠 Consult a neurologist if symptoms persist or worsen."
    },
}

# Normal/common symptom mapping
normal_db = {
    "Cold/Fever": ["cough", "sore throat", "mild fever", "runny nose", "fatigue"],
    "Viral Infection": ["fever", "body ache", "fatigue", "mild headache", "nausea"],
    "Indigestion": ["bloating", "stomach pain", "heartburn", "nausea"],
}

# ---------------------------
# 🔍 Core logic functions
# ---------------------------

def suggest_problem(description):
    description = description.lower()
    suggestions = {}

    # Check serious problems
    for problem, data in problem_db.items():
        score = sum(weight for symptom, weight in data["symptoms"].items() if symptom in description)
        if score > 0:
            suggestions[problem] = score

    # If no serious or only minor symptoms, check normal problems
    if not suggestions or max(suggestions.values()) <= 2:
        normal_suggestions = {}
        for problem, keywords in normal_db.items():
            score = sum(1 for keyword in keywords if keyword in description)
            if score > 0:
                normal_suggestions[problem] = score
        if normal_suggestions:
            return dict(sorted(normal_suggestions.items(), key=lambda x: x[1], reverse=True)), "normal"

    return dict(sorted(suggestions.items(), key=lambda x: x[1], reverse=True)), "serious"

def display_suggestions(suggestions, level):
    if suggestions:
        total_score = sum(suggestions.values())
        for problem, score in suggestions.items():
            confidence = round((score/total_score)*100, 2)
            st.markdown(f"### 🩹 {problem} — Confidence: `{confidence}%`")
            if level == "serious":
                desc = problem_db[problem]["description"]
                advice = problem_db[problem]["advice"]
            else:
                desc = "Common minor health issue."
                advice = "🩺 Rest, hydrate, and consult a doctor if symptoms worsen."
            st.write(f"**Description:** {desc}")
            st.write(f"**Suggested Action:** {advice}")
            st.markdown("---")
    else:
        st.success("✅ No major problem detected. Your health seems normal.")

# ---------------------------
# 🌟 Streamlit Interface
# ---------------------------

st.title("🩺 Health Problem Suggester – AI Symptom Checker")
st.write("Describe your symptoms below, and this app will suggest possible causes and advice. ⚕️")

with st.form("symptom_form"):
    description = st.text_area("Enter your symptoms in detail:", placeholder="Example: I have chest pain and shortness of breath...")
    submitted = st.form_submit_button("🔍 Analyze Symptoms")

if submitted:
    if description.strip():
        suggestions, level = suggest_problem(description)
        st.markdown("---")
        if level == "serious":
            st.warning("⚠️ Serious or specific health issues detected!")
        else:
            st.info("💤 Seems like a common or minor condition.")
        display_suggestions(suggestions, level)
    else:
        st.error("Please enter a description of your symptoms before submitting.")

st.markdown("---")
st.caption("⚠️ Disclaimer: This tool is for informational purposes only and does not replace professional medical advice.")
