import nltk
nltk.download('stopwords')
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.metrics import edit_distance
import nltk
from fuzzywuzzy import fuzz
nltk.download('stopwords')




def compare_similarity(cv_content, job_offer_content):
    """Compare la similarité entre le contenu du CV et l'offre d'emploi en utilisant plusieurs approches."""
    # Convertir le contenu du CV et de l'offre d'emploi en textes uniques
    cv_text = ' '.join(cv_content.values())
    job_offer_text = ' '.join(job_offer_content.values())

    # Similarité cosinus avec TF-IDF
    vectorizer = TfidfVectorizer()
    cv_vector = vectorizer.fit_transform([cv_text])
    job_offer_vector = vectorizer.transform([job_offer_text])
    cosine_sim = cosine_similarity(cv_vector, job_offer_vector)[0][0]

    # Similarité de Levenshtein
    max_len = max(len(cv_text), len(job_offer_text))
    levenshtein_sim = 1 - edit_distance(cv_text, job_offer_text) / max_len

    # Similarité FuzzyWuzzy (par exemple, le ratio de similarité)
    fuzzy_sim = fuzz.ratio(cv_text, job_offer_text) / 100.0  # Convertir le score en une échelle de 0 à 1

    # Vous pouvez attribuer des poids différents à chaque mesure et les combiner selon vos besoins
    combined_similarity = 0.4 * cosine_sim + 0.4 * levenshtein_sim + 0.2 * fuzzy_sim  # Par exemple, attribuer des poids de 0.4, 0.4 et 0.2 respectivement

    return combined_similarity

def remove_stopwords(text):

    stop_words = set(stopwords.words('english'))
    word_tokens = nltk.word_tokenize(text)
    filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
    filtered_text = ' '.join(filtered_text)

    return filtered_text