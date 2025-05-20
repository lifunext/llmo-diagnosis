from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai

app = Flask(__name__)
openai.api_key = 'sk-あなたのOpenAI APIキーをここに入れる'

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "URLが指定されていません"}), 400

    try:
        # WebページのHTMLを取得
        html = requests.get(url, timeout=5).text

        # テキストを抽出
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        # ChatGPTで診断コメント生成
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはWebサイトの改善点を提案するマーケターです。SEO・読みやすさ・CV導線などを見て改善ポイントをフィードバックしてください。"},
                {"role": "user", "content": f"以下はとあるWebページの内容です：\n{text}"}
            ]
        )

        result = response['choices'][0]['message']['content']
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
