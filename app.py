import nltk
nltk.download('stopwords')
import subprocess
from flask import Flask, render_template, request, send_from_directory, jsonify, abort
import os
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
from utils import compare_similarity, remove_stopwords
from fuzzywuzzy import fuzz
import re
import uuid
from werkzeug.utils import secure_filename
import warnings
from urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

app = Flask(__name__)
UPLOAD_FOLDER_BASE = 'data'

# Création des dossiers si nécessaire
if not os.path.exists(UPLOAD_FOLDER_BASE):
    os.makedirs(UPLOAD_FOLDER_BASE)

app.config['UPLOAD_FOLDER_BASE'] = UPLOAD_FOLDER_BASE

def extract_text_from_pdf(pdf_path):
    """Extrait le texte d'un fichier PDF."""
    return extract_text(pdf_path)


def segment_text_into_sections(text, doc_type):
    """Segmenter le texte en sections prédéfinies en fonction du type de document."""
    sections_regex = {
        "cv": {
            re.compile(r"(expérience[s]? professionnelle[s]?|professional experience)", re.IGNORECASE): "expérience professionnelle",
            re.compile(r"(éducation|education|formation[s]?|training)", re.IGNORECASE): "éducation / education",
            re.compile(r"(compétence[s]?|skills)", re.IGNORECASE): "compétences / skills",
            re.compile(r"(langue[s]?|languages)", re.IGNORECASE): "langues / languages",
            re.compile(r"(projet[s]?|projects)", re.IGNORECASE): "projets / projects",
            re.compile(r"(intérêt[s]?|interests)", re.IGNORECASE): "intérêts / interests",
            re.compile(r"(référence[s]?|references)", re.IGNORECASE): "références / references",
            re.compile(r"(objectif[s]?|objectives)", re.IGNORECASE): "objectifs / objectives",
            re.compile(r"(qualité[s]?|qualities)", re.IGNORECASE): "qualités / qualities",
            re.compile(r"(formation[s]?|training[s]?)", re.IGNORECASE): "formations / training",
            re.compile(r"(réseaux\s*sociaux|social\s*media)", re.IGNORECASE): "réseaux sociaux / social media",
            re.compile(r"(atouts)", re.IGNORECASE): "strengths",
            re.compile(r"(stages)", re.IGNORECASE): "stages",
            re.compile(r"(projets\s*académique|academic\s*projects)", re.IGNORECASE): "projets académiques / academic projects",
        },
        "job_offer": {
            re.compile(r"(description\s*du\s*poste|job\s*description)", re.IGNORECASE): "description du poste / job description",
            re.compile(r"(profil\s*recherché|profile\s*searched)", re.IGNORECASE): "profil recherché / profile searched",
            re.compile(r"(compétence[s]?|skills)", re.IGNORECASE): "compétences / skills",
            re.compile(r"(formation[s]?|training[s]?)", re.IGNORECASE): "formations / training",
            re.compile(r"(avantages|benefits)", re.IGNORECASE): "avantages / benefits",
            re.compile(r"(responsabilit[ée]s|responsibilities)", re.IGNORECASE): "responsabilités / responsibilities",
            re.compile(r"(salaire|salary)", re.IGNORECASE): "salaire / salary",
            re.compile(r"(conditions\s*de\s*travail|working\s*conditions)", re.IGNORECASE): "conditions de travail / working conditions",
            re.compile(r"(motivation\s*et\s*contexte|motivation\s*and\s*context)", re.IGNORECASE): "motivation et contexte / motivation and context",
            re.compile(r"(objectif[s]?|objectives)", re.IGNORECASE): "objectifs / objectives",
        }
}.get(doc_type, {})
    if not sections_regex:
        raise ValueError("Type de document non pris en charge")
    sections_content = {value: "" for value in sections_regex.values()}
    current_section = None
    for line in text.split('\n'):
        line = line.strip()
        if line:
            for regex, section_name in sections_regex.items():
                if regex.search(line):
                    current_section = section_name
                    break
            if current_section:
                sections_content[current_section] += line + " "
    return sections_content

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'cv' not in request.files or 'job_offer' not in request.files:
        return jsonify({'error': 'Fichiers manquants'}), 400
    session_id = str(uuid.uuid4())
    session_folder = os.path.join(UPLOAD_FOLDER_BASE, session_id)
    os.makedirs(session_folder, exist_ok=True)
    cv_file = request.files['cv']
    job_offer_file = request.files['job_offer']
    cv_path = os.path.join(session_folder, 'cv.pdf')
    job_offer_path = os.path.join(session_folder, 'job_offer.pdf')
    cv_file.save(cv_path)
    job_offer_file.save(job_offer_path)
    cv_text = extract_text_from_pdf(cv_path)
    job_offer_text = extract_text_from_pdf(job_offer_path)
    cv_sections = segment_text_into_sections(cv_text, "cv")
    job_offer_sections = segment_text_into_sections(job_offer_text, "job_offer")
    # Calcul de la similarité
    similarity_score = compare_similarity(cv_sections, job_offer_sections)
    

  
    cv_json_path = os.path.join(session_folder, 'cv_results.json')
    job_offer_json_path = os.path.join(session_folder, 'job_offer_results.json')
    with open(cv_json_path, 'w', encoding='utf-8') as cv_f:
        json.dump(cv_sections, cv_f, ensure_ascii=False, indent=4)
    with open(job_offer_json_path, 'w', encoding='utf-8') as job_f:
        json.dump(job_offer_sections, job_f, ensure_ascii=False, indent=4)
    command = ['python', 'gemini.py', session_id]
    subprocess.run(command, cwd=os.path.dirname(os.path.abspath(__file__)))
     # Chemins vers les fichiers de questions
    cv_questions_path = os.path.join(session_folder, 'cv_questions.json')
    job_offer_questions_path = os.path.join(session_folder, 'job_offer_questions.json')

    return jsonify({
        'session_id': session_id,
        'cv_json_file': cv_json_path,
        'job_offer_json_file': job_offer_json_path,
        'cv_questions_file': cv_questions_path,
        'job_offer_questions_file': job_offer_questions_path,
        'similarity_score': similarity_score
    })
    
@app.route('/download/<path:filename>')
def download_file(filename):
    # Supprimer le préfixe redondant si présent
    if filename.startswith('data/'):
        filename = filename[5:]  # Retirer le préfixe 'data/'

    filepath = os.path.join(UPLOAD_FOLDER_BASE, filename)
    print(f"Tentative d'accès au fichier : {filepath}")  # Log pour vérification

    # Vérifier si le fichier existe
    if not os.path.exists(filepath):
        print("Fichier non trouvé")
        abort(404, description="Fichier non trouvé")  # Envoyer une erreur 404 si le fichier n'existe pas

    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    return send_from_directory(directory, filename, as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True, port=5000)