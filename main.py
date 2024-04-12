import json

# Chemins des fichiers JSON
file_path_1 = "data/cv_content.json"
file_path_2 = "data/job_offer_content.json"

def ask_interview_questions(file_path):
    """Pose des questions d'entretien basées sur le contenu d'un fichier JSON."""
    with open(file_path) as f:
        data = json.load(f)
    # Analyser les données et formuler des questions en fonction du contenu
    questions = []
    if "expérience professionnelle" in data:
        questions.append("Pouvez-vous nous en dire plus sur votre expérience professionnelle ?")
    if "compétences" in data:
        questions.append("Quelles sont vos compétences principales ?")
    # Ajoutez d'autres conditions en fonction de votre contenu JSON
    return questions

# Poser des questions pour le fichier 1
questions_1 = ask_interview_questions(file_path_1)

# Poser des questions pour le fichier 2
questions_2 = ask_interview_questions(file_path_2)

# Afficher les questions
print("Questions d'entretien pour le fichier 1 :")
for question in questions_1:
    print(question)

print("\nQuestions d'entretien pour le fichier 2 :")
for question in questions_2:
    print(question)
