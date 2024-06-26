import google.generativeai as genai
import json
import os
import sys
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

def configure_api():
    api_key = "AIzaSyB27wQtaCxAN3sQY_eMI02M0No2FCPt4g4"
    genai.configure(api_key=api_key)

def load_json_data(session_id, data_type):
    file_path = os.path.join('data', session_id, f"{data_type}")
    print(f"Tentative de chargement depuis : {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f"Données chargées pour {data_type} avec succès.")
            return data
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} n'a pas été trouvé.")
        return None
    except json.JSONDecodeError:
        print(f"Erreur : Le contenu du fichier JSON {file_path} est corrompu ou mal formé.")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON {file_path}: {e}")
        return None

def setup_model():
    return genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config={"temperature": 0.9, "top_p": 1, "top_k": 1, "max_output_tokens": 2048},
        safety_settings=[{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}]
    )

def generate_questions(model, data, data_type):
    if not data:
        print(f"Aucune donnée disponible pour générer des questions pour {data_type}.")
        return []
    questions_list = []
    convo = model.start_chat(history=[])
    
    # Envoyer le JSON au modèle
    convo.send_message(json.dumps(data, indent=4))
    
    for i in range(10):
        # Prompt amélioré avec un exemple du JSON d'entrée
        prompt = f"""
        Utilise les informations du document {data_type} (format JSON) pour générer une paire question-réponse dans le format JSON suivant:
        {{
          "question": "Question ici?",
          "answer": "Réponse ici."
        }}

        Exemple de données JSON: {json.dumps(data, indent=4)}

        Génère la paire question-réponse sous forme de JSON valide. 
        """
        convo.send_message(prompt)
        response = convo.last.text.strip()

        try:
            question_response = json.loads(response)
            questions_list.append(question_response)
        except json.JSONDecodeError:
            # Amélioration de la gestion des erreurs
            print(f"Erreur de décodage JSON pour la réponse {i+1}: {response}")
            questions_list.append({"question": "Erreur de formatage", "answer": "Aucune réponse générée correctement"})

    return questions_list

def save_questions(questions, session_id, data_type):
    output_path = f'data/{session_id}/{data_type}_questions.json'
    if not questions:
        print(f"Aucune question à enregistrer pour {data_type}.")
        return
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(questions, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des questions dans {output_path}: {e}")

def main(session_id):
    configure_api()
    model = setup_model()
    job_offer_data = load_json_data(session_id, "job_offer_results.json")
    cv_data = load_json_data(session_id, "cv_results.json")
    job_offer_questions = generate_questions(model, job_offer_data, "job_offer")
    cv_questions = generate_questions(model, cv_data, "cv")
    save_questions(job_offer_questions, session_id, "job_offer")
    save_questions(cv_questions, session_id, "cv")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gemini.py <session_id>")
        sys.exit(1)
    main(sys.argv[1])