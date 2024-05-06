import streamlit as st
import requests

def main():
    st.title('Simulateur d\'Interview Groupe 1')

    # Utilisation du sidebar pour les uploads de fichiers
    with st.sidebar:
        st.header('Téléchargez vos fichiers')
        uploaded_cv = st.file_uploader("Télécharger le CV", type=['pdf', 'docx', 'txt'], key="cv")
        uploaded_job_description = st.file_uploader("Télécharger la description de poste", type=['pdf', 'docx', 'txt'], key="job")

    # Vérifier si les fichiers sont chargés
    if uploaded_cv and uploaded_job_description:
        st.success("Fichiers téléchargés avec succès! Veuillez simuler l'interview.")
        
        # Bouton pour simuler l'interview
        if st.button('Simuler l\'Interview'):
            st.header('Questions d\'Interview Suggérées')
            # Simuler une fonction d'analyse des fichiers
            questions = analyze_documents(uploaded_cv, uploaded_job_description)
            for question in questions:
                st.markdown(f"- {question}")
    else:
        st.warning("Veuillez télécharger un CV et une description de poste pour générer des questions.")

import requests

def analyze_documents(cv, job_desc):
    # Adresse de l'API du serveur Flask
    url = 'http://127.0.0.1:5000/upload'  # Assurez-vous que cette URL est correcte

    # Préparer les fichiers à envoyer
    files = {
        'cv': (cv.name, cv, cv.type),
        'job_offer': (job_desc.name, job_desc, job_desc.type)
    }

    # Effectuer la requête POST
    response = requests.post(url, files=files)

    if response.status_code == 200:
        # Traitement réussi, recevoir les données
        questions = response.json()  # Assumant que le serveur renvoie une liste de questions en JSON
        return questions
    else:
        # Gérer les erreurs
        return ["Erreur lors de la communication avec le serveur."]


if __name__ == "__main__":
    main()
