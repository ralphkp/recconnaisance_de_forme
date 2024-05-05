import streamlit as st

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

def analyze_documents(cv, job_desc):
    # Cette fonction est un placeholder pour votre logique d'analyse de documents
    # Ici, retourner une liste de questions simulées
    return [
        "Décrivez une situation où vous avez dû travailler en équipe.",
        "Quels sont vos points forts qui correspondent à ce poste ?",
        "Pouvez-vous donner un exemple de défi professionnel et comment vous l'avez surmonté ?"
    ]

if __name__ == "__main__":
    main()
