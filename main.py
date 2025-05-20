from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

        # タイトル
        title = soup.title.string if soup.title else ''

        # 見出し h1〜h3
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]

        # 本文（先頭3000文字）
        body = soup.get_text(strip=True)[:3000]

        return jsonify({
            'title': title,
            'headings': headings,
            'body': body
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# RenderのFreeプラン対応：ポート固定＆外部アクセス可能設定
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
