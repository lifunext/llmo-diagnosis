import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# OpenAI API Key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is missing'}), 400

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "あなたはSEOに詳しいWebマーケターです。"},
            {"role": "user", "content": f"このページを分析してコメントしてください：\n{text}"}
        ]
    )

    comment = response['choices'][0]['message']['content']
    return jsonify({'comment': comment})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
