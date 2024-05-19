import streamlit as st
import requests
import pandas as pd  # Importer pandas pour la manipulation de données

def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ceci lèvera une exception si la réponse est une erreur
        return response.json()
    #except requests.exceptions.HTTPError as e:
     #   if e.response.status_code == 404:
      #      st.error("Les données demandées ne sont pas disponibles pour le moment. Veuillez vérifier que les fichiers ont été téléchargés correctement et réessayer.")
      #  else:
      #      st.error("Erreur lors de la récupération des données: " + str(e))
      #  return None
    except requests.exceptions.ConnectionError:
        st.error("Erreur de connexion. Veuillez vérifier votre connexion Internet.")
        return None
    except requests.exceptions.Timeout:
        st.error("Le serveur a mis trop de temps à répondre. Veuillez réessayer ultérieurement.")
        return None
    except requests.exceptions.RequestException as e:
        st.error("Erreur lors de la requête: " + str(e))
        return None

def simulate_interview(cv, job_desc):
    url = 'http://127.0.0.1:5000/upload'
    files = {
        'cv': (cv.name, cv, cv.type),
        'job_offer': (job_desc.name, job_desc, job_desc.type)
    }
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de communication avec le serveur: {str(e)}")
        return None

def main():
    st.title('Simulateur d\'Interview Groupe 1')

    # Style pour les bordures de table
    st.markdown("""
        <style>
        .dataframe th, .dataframe td {
            border: 1px solid black !important;
            text-align: left !important;
        }
        </style>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.header('Téléchargez vos fichiers')
        uploaded_cv = st.file_uploader("Télécharger le CV", type=['pdf', 'docx', 'txt'], key="cv")
        uploaded_job_description = st.file_uploader("Télécharger la description de poste", type=['pdf', 'docx', 'txt'], key="job")

    if uploaded_cv and uploaded_job_description:
        st.success("Fichiers téléchargés avec succès! Veuillez simuler l'interview.")
        if st.button('Simuler l\'Interview'):
            with st.spinner('Le processus peut prendre quelques minutes. Veuillez patienter...'):
                session_data = simulate_interview(uploaded_cv, uploaded_job_description)
                if session_data:
                    cv_questions_path = session_data.get('cv_questions_file')
                    job_offer_questions_path = session_data.get('job_offer_questions_file')
                    cv_questions = fetch_data(f'http://127.0.0.1:5000/download/{cv_questions_path}')
                    job_offer_questions = fetch_data(f'http://127.0.0.1:5000/download/{job_offer_questions_path}')
                    if cv_questions and job_offer_questions:
                        # Affichage des questions et réponses
                        st.subheader("Questions et Réponses pour le CV")
                        for question, answer in cv_questions.items():
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                st.text("Question: " + question)
                            with col2:
                                st.text("Réponse: " + answer)
                        
                        st.subheader("Questions et Réponses pour l'Offre d'Emploi")
                        for question, answer in job_offer_questions.items():
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                st.text("Question: " + question)
                            with col2:
                                st.text("Réponse: " + answer)
                        
                        st.success('Traitement terminé!')
                    else:
                        st.error("Erreur lors de la récupération des questions. Veuillez réessayer.")
                else:
                    st.error("Aucune question n'a été générée.")
    else:
        st.warning("Veuillez télécharger un CV et une description de poste pour générer des questions.")

if __name__ == "__main__":
    main()
