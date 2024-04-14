"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
import json
genai.configure(api_key="AIzaSyB27wQtaCxAN3sQY_eMI02M0No2FCPt4g4")


# Charger les informations depuis un fichier JSON
with open(r'D:\projet_RDF\recconnaisance_de_forme\data\job_offer_content.json') as f:
    data = json.load(f)
    
# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[])

convo.send_message(json.dumps(data))
result = convo.last.text

# Générer 10 questions d'entretien en fonction des informations du fichier JSON
for i in range(10):
    convo.send_message("Quelle est votre question suivante?")
    print(convo.last.text)
    