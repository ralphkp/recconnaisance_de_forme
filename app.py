import nltk
nltk.download('stopwords')

from flask import Flask, render_template, request, send_from_directory
import os
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text
from utils import compare_similarity
from fuzzywuzzy import fuzz
import re

app = Flask(__name__)

UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_text_from_pdf(pdf_path):
    """Extrait le texte d'un fichier PDF."""
    return extract_text(pdf_path)

def segment_text_into_sections(text, doc_type):
    """Segmenter le texte en sections prédéfinies en fonction du type de document."""
    if doc_type == "cv":
        sections_regex = {
            re.compile(r"(expérience[s]? professionnelle[s]?|professional experience)", re.IGNORECASE): "expérience professionnelle / professional experience",
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
        }
    elif doc_type == "job_offer":
        sections_regex = {
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
    else:
        raise ValueError("Type de document non pris en charge")

    sections_content = {value: "" for key, value in sections_regex.items()}
    current_section = None
    
    for line in text.split('\n'):
        line = line.strip()
        if line:  # S'assurer que la ligne n'est pas vide
            found = False
            for regex, section_name in sections_regex.items():
                if regex.search(line):
                    current_section = section_name
                    found = True
                    break
            if current_section and found:
                sections_content[current_section] += "\n"
            elif current_section:
                sections_content[current_section] += line + " "

    # Ajouter des déclarations d'impression pour vérifier le contenu de section_text
    for section_name, section_text in sections_content.items():
        print(f"Section name: {section_name}")
        print(f"Section text: {section_text}")

    return sections_content

# Le reste du code reste inchangé...


def save_text_to_json(file_path, content):
    """Sauvegarde le contenu dans un fichier JSON."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    cv_file = request.files['cv']
    job_offer_file = request.files['job_offer']

    cv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'CV.pdf')
    job_offer_path = os.path.join(app.config['UPLOAD_FOLDER'], 'JobOffer.pdf')

    cv_file.save(cv_path)
    job_offer_file.save(job_offer_path)

    cv_text = extract_text(cv_path)
    job_offer_text = extract_text(job_offer_path)

   # cv_text = remove_stopwords(cv_text)  # Supprimer les mots vides du texte CV
   # job_offer_text = remove_stopwords(job_offer_text)  # Supprimer les mots vides du texte de l'offre d'emploi

    cv_sections = segment_text_into_sections(cv_text, "cv")
    job_offer_sections = segment_text_into_sections(job_offer_text, "job_offer")

    save_text_to_json(os.path.join(app.config['UPLOAD_FOLDER'], "cv_content.json"), cv_sections)
    save_text_to_json(os.path.join(app.config['UPLOAD_FOLDER'], "job_offer_content.json"), job_offer_sections)

    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'cv_content.json'), 'r', encoding='utf-8') as cv_file:
        cv_content = json.load(cv_file)

    with open(os.path.join(app.config['UPLOAD_FOLDER'], 'job_offer_content.json'), 'r', encoding='utf-8') as job_offer_file:
        job_offer_content = json.load(job_offer_file)

    similarity_score = compare_similarity(cv_content, job_offer_content)
    return render_template('index.html', similarity_score=similarity_score)


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True,port=5001)