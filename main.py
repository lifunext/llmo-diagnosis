import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# 環境変数からOpenAI APIキーを取得
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # HTMLの取得とテキスト抽出
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        # OpenAIで診断コメント生成
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # 最新モデル
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいWebマーケターです。ページの構成、見出し、文章、UX改善などの観点からフィードバックしてください。"},
                {"role": "user", "content": f"以下のWebページの内容を診断してください：\n{text}"}
            ]
        )

        comment = response['choices'][0]['message']['content']
        return jsonify({"comment": comment})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Render用のポート設定
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
