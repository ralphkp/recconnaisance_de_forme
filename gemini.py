import google.generativeai as genai
import json

# Configuration de l'API Google generative AI
genai.configure(api_key="AIzaSyB27wQtaCxAN3sQY_eMI02M0No2FCPt4g4")

# Fonction pour charger les données JSON
def load_json_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON {file_path}: {e}")
        exit()

# Charger le contenu des fichiers JSON
job_offer_data = load_json_data(r'data/job_offer_content.json')
cv_data = load_json_data(r'data/cv_content.json')

# Configuration du modèle de génération AI
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Démarrage de la conversation avec le modèle
convo = model.start_chat(history=[])

# Fonction pour générer des questions pour un fichier donné
def generate_questions(data, data_type):
    questions_dict = {}
    convo.send_message(json.dumps(data))  # Envoi des données initiales pour contexte
    for i in range(10):
        prompt = f"Quelle est votre question d'entretien suivante basée sur les technologies présentées dans le {data_type}?"
        convo.send_message(prompt)
        response = convo.last.text.strip()
        # Nettoyage de la réponse
        clean_response = response.replace("Question d'entretien suivante possible basée sur les technologies présentées dans le CV :", "").strip()
        clean_response = clean_response.replace("**Question d'entretien possible basée sur les technologies présentées dans l'offre d'emploi :", "").strip()
        questions_dict[f"{data_type}_question_{i+1}"] = clean_response
    return questions_dict

# Générer des questions pour chaque fichier
job_offer_questions = generate_questions(job_offer_data, "job_offer")
cv_questions = generate_questions(cv_data, "cv")

# Sauvegarde des questions dans des fichiers JSON avec une structure clé-valeur
def save_questions(questions, output_path):
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des questions: {e}")

# Chemins pour sauvegarder les questions générées
save_questions(job_offer_questions, r'data/job_offer_questions.json')
save_questions(cv_questions, r'data/cv_questions.json')

# Affichage des questions pour vérification
print("Questions basées sur l'offre d'emploi:")
for key, question in job_offer_questions.items():
    print(f"{key}: {question}")

print("\nQuestions basées sur le CV:")
for key, question in cv_questions.items():
    print(f"{key}: {question}")