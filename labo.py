import json
from ibm_watson import AssistantV2

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('6BMZghZy5HNM5NcawcNGNRtDhG0OUTUrEsD1UU7z6hjQ')

assistant = AssistantV2(
    version="2021-06-14",
    authenticator=authenticator
)

# Chargez le contenu JSON
with open('data/cv_content.json') as f:
    content = json.load(f)

# Créez un service Watson Assistant
assistant = AssistantV2(
    version="2021-06-14",
    authenticator=authenticator
)

# Générez des questions à partir du contenu JSON
questions = assistant.generate_question(
    
    content=content
)

# Affichez les questions
for question in questions:
    print(question)