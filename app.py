from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/generate-email', methods=['POST'])
def generate_email():
    # Extraire la transcription de la réunion du corps de la requête
    data = request.get_json()
    transcription = data['transcription']

    # Préparer la requête pour l'API OpenAI
    api_url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer votre_clé_api",  # Remplacez 'votre_clé_api' par votre clé API réelle
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-davinci-003",  # Utilisez le modèle OpenAI approprié
        "prompt": f"Résumez la réunion et proposez des étapes suivantes basées sur les notes suivantes: {transcription}",
        "max_tokens": 1024
    }

    # Envoyer la requête à OpenAI
    response = requests.post(api_url, headers=headers, json=payload)
    generated_text = response.json()['choices'][0]['text']

    # Retourner le texte généré en réponse
    return jsonify({"email": generated_text})

if __name__ == '__main__':
    app.run(debug=True)
