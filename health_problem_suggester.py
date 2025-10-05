import time

def print_slow(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

print_slow("🩺 Health Problem Suggester – Dynamic Version 🩺\n")

# Symptom database
problem_db = {
    "Heart Problem": {
        "symptoms": {"chest pain": 3, "shortness of breath": 3, "palpitations": 2, 
                     "high bp": 1, "irregular heartbeat": 2, "fatigue":1},
        "description": "Could indicate coronary artery disease, arrhythmia, or risk of heart attack.",
        "advice": "Consult a cardiologist immediately. ECG and checkups recommended."
    },
    "Respiratory Issue": {
        "symptoms": {"cough": 2, "shortness of breath": 2, "wheezing": 2, 
                     "asthma": 3, "lung infection": 2},
        "description": "Could indicate asthma, bronchitis, pneumonia, or viral infections.",
        "advice": "Consult a pulmonologist if symptoms persist. Rest and hydration recommended."
    },
    "Digestive Issue": {
        "symptoms": {"stomach pain": 2, "nausea": 2, "vomiting": 2, 
                     "diarrhea": 2, "acid reflux": 2, "bloating":1},
        "description": "Could indicate gastritis, indigestion, or gastrointestinal infection.",
        "advice": "Maintain a balanced diet and consult a gastroenterologist if persistent."
    },
    "Musculoskeletal Pain": {
        "symptoms": {"joint pain": 3, "back pain": 3, "muscle ache": 2, 
                     "swelling": 2, "stiffness": 2},
        "description": "Could indicate arthritis, muscle strain, or other musculoskeletal disorders.",
        "advice": "Exercise, physiotherapy, or orthopedist consultation recommended."
    },
    "Neurological Issue": {
        "symptoms": {"headache": 2, "dizziness": 2, "numbness": 3, 
                     "tingling": 2, "seizure": 3},
        "description": "Could indicate migraines, neuropathy, or other neurological conditions.",
        "advice": "Consult a neurologist if symptoms persist or worsen."
    },
}

# Normal/common symptom mapping
normal_db = {
    "Cold/Fever": ["cough", "sore throat", "mild fever", "runny nose", "fatigue"],
    "Viral Infection": ["fever", "body ache", "fatigue", "mild headache", "nausea"],
    "Indigestion": ["bloating", "stomach pain", "heartburn", "nausea"],
}

def suggest_problem(description):
    description = description.lower()
    suggestions = {}

    # Check serious problems
    for problem, data in problem_db.items():
        score = sum(weight for symptom, weight in data["symptoms"].items() if symptom in description)
        if score > 0:
            suggestions[problem] = score

    # If no serious symptoms or only 1 minor symptom, check normal problems
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
    print("\n📝 Suggested Problem Type(s)")
    print("-"*60)
    if suggestions:
        total_score = sum(suggestions.values())
        for problem, score in suggestions.items():
            confidence = round((score/total_score)*100, 2)
            if level == "serious":
                desc = problem_db[problem]["description"]
                advice = problem_db[problem]["advice"]
            else:
                desc = "Common minor health issue."
                advice = "Rest, hydrate, and consult a doctor if symptoms worsen."
            print(f"- {problem} (Confidence: {confidence}%)")
            print(f"  Description: {desc}")
            print(f"  Suggested Action: {advice}\n")
    else:
        print("No problem detected. Your health seems normal.")
    print("-"*60)

def main():
    print_slow("Describe your symptoms in detail.\n")
    while True:
        description = input("➡️ Enter your symptoms: ")
        suggestions, level = suggest_problem(description)
        display_suggestions(suggestions, level)

        retry = input("Do you want to enter another description? (yes/no): ").lower()
        if retry != "yes":
            print_slow("\nThank you for using Health Problem Suggester! Stay healthy ❤️")
            break
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
