import streamlit as st
import requests
import pandas as pd  # Importer pandas pour la manipulation de données

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
            with st.spinner('Le processus peut prendre quelques minutes. Veuillez patienter...'):
                session_data = simulate_interview(uploaded_cv, uploaded_job_description)
                if session_data:
                    cv_questions_path = session_data.get('cv_questions_file')
                    job_offer_questions_path = session_data.get('job_offer_questions_file')
                    
                    # Récupérer et afficher les questions du CV
                    cv_questions = requests.get(f'http://127.0.0.1:5000/download/{cv_questions_path}').json()
                    job_offer_questions = requests.get(f'http://127.0.0.1:5000/download/{job_offer_questions_path}').json()
                   
                    questions_df = pd.DataFrame({
                        "Questions CV": cv_questions,
                        "Questions Offre": job_offer_questions,
                       
                    })
                    st.table(questions_df)
                    st.success('Traitement terminé!')
                else:
                    st.error("Aucune question n'a été générée.")
    else:
        st.warning("Veuillez télécharger un CV et une description de poste pour générer des questions.")

def simulate_interview(cv, job_desc):
    url = 'http://127.0.0.1:5000/upload'  # Assurez-vous que cette URL est correcte
    files = {
        'cv': (cv.name, cv, cv.type),
        'job_offer': (job_desc.name, job_desc, job_desc.type)
    }

    try:
        response = requests.post(url, files=files)
        response.raise_for_status()  # Ceci lèvera une exception si la réponse est une erreur
        return response.json()  # Assumant que le serveur renvoie les chemins des fichiers JSON
    except requests.exceptions.RequestException as e:  # Gérer les exceptions liées aux requêtes
        st.error(f"Erreur de communication avec le serveur: {str(e)}")
        return None

if __name__ == "__main__":
    main()
