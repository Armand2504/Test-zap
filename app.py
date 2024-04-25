from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/generate-email', methods=['POST', 'GET'])
def generate_email():
    # Extraire la transcription de la réunion du corps de la requête
    data = request.get_json()
    transcription = data.get('transcription')

    if not transcription:
        return jsonify({"error": "No transcription provided"}), 400

    # Préparer la requête pour l'API OpenAI
    api_url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-davinci-003",  # Utilisez le modèle OpenAI approprié
        "prompt": f"Résumez la réunion et proposez des étapes suivantes basées sur les notes suivantes: {transcription}",
        "max_tokens": 1024
    }

    # Envoyer la requête à OpenAI
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        generated_text = response.json()['choices'][0]['text']
        return jsonify({"email": generated_text})
    else:
        return jsonify({"error": "Failed to generate email"}), response.status_code
