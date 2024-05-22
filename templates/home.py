import streamlit as st
import requests
import pandas as pd

def main():
    st.set_page_config(page_title="Simulateur d'Interview", page_icon=":briefcase:")
    
    with st.sidebar:
        st.header('Navigation')
        page = st.selectbox("Choisissez une page", ["Utilisateur", "Administrateur"])

    if page == "Utilisateur":
        show_user_interface()
    elif page == "Administrateur":
        show_admin_interface()

def show_user_interface():
    st.title('Simulateur d\'Interview Groupe 1')

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
                    similarity_score = session_data.get('similarity_score')
                    st.write(f"Score de similarité: {similarity_score}")
                    
                    cv_questions_path = session_data.get('cv_questions_file')
                    job_offer_questions_path = session_data.get('job_offer_questions_file')

                    try:
                        cv_questions = requests.get(f'http://127.0.0.1:5000/download/{cv_questions_path}').json()
                        job_offer_questions = requests.get(f'http://127.0.0.1:5000/download/{job_offer_questions_path}').json()

                        cv_df = pd.DataFrame(cv_questions)
                        job_offer_df = pd.DataFrame(job_offer_questions)

                        # Affichage des DataFrame avec style
                        display_dataframe_with_style(cv_df)
                        display_dataframe_with_style(job_offer_df)

                        st.success('Traitement terminé!')
                    except Exception as e:
                        st.error(f"Erreur lors de la récupération des questions. Veuillez réessayer. {e}")
                else:
                    st.error("Aucune question n'a été générée.")
    else:
        st.warning("Veuillez télécharger un CV et une description de poste pour générer des questions.")

def display_dataframe_with_style(df):
    st.write(df.to_html(escape=False), unsafe_allow_html=True)  # Modification ici pour utiliser correctement le HTML

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
        st.error(f"Erreur de communication avec le serveur lors de la simulation de l'interview. {e}")
        return None

def show_admin_interface():
    st.title("Interface Administrateur")
    st.write("Bienvenue dans l'interface administrateur.")

if __name__ == "__main__":
    main()
