from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)

# OpenAI APIキーをここに貼り付けてください（セキュリティのため、後で環境変数にするのが望ましい）
openai.api_key = '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'

@app.route('/fetch', methods=['POST'])
def fetch():
    # 1. Makeから送られてきたJSONからURLを取得
    data = request.get_json()
    url = data.get('url')

    # 2. 指定URLのHTMLを取得し、テキストだけを抽出
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    # 3. OpenAI GPTに渡してフィードバックコメントを生成
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # GPT-4でも可
        messages=[
            {"role": "system", "content": "あなたはSEOに詳しいプロのWebマーケターです。"},
            {"role": "user", "content": f"以下のページを診断してください。\n{text}"}
        ]
    )

    comment = response['choices'][0]['message']['content']

    # 4. 診断結果コメントをJSON形式で返す（←ここが変更済み）
    return jsonify({'comment': comment})


