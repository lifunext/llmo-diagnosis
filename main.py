from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

openai.api_key = 'sk-あなたのAPIキー'  # 本番では環境変数で管理推奨

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # HTMLを取得してテキスト化
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        # OpenAI に渡して診断コメント生成
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいWebマーケターです。ページの構成、見出し、文章、UX改善などの観点からフィードバックしてください。"},
                {"role": "user", "content": f"以下のWebページの内容を診断してください：\n{text}"}
            ]
        )

        comment = response['choices'][0]['message']['content']
        return jsonify({"comment": comment})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
