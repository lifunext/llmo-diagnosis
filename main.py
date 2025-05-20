import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is missing'}), 400

    try:
        # Get HTML from URL
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        # Send text to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいプロのWebマーケターです。"},
                {"role": "user", "content": "このページを分析してコメントしてください：\n" + text}
            ]
        )

        comment = response['choices'][0]['message']['content']
        return jsonify({'comment': comment})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
