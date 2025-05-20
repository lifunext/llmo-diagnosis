@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get('url')
    print("受信したURL:", url)

    if not url:
        return jsonify({'error': 'URL is missing'}), 400

    html = requests.get(url).text
    print("HTML取得成功（長さ）:", len(html))

    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    print("抽出テキスト（先頭100文字）:", text[:100])

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいWebマーケターです。"},
                {"role": "user", "content": f"このページを分析してコメントしてください：\n{text}"}
            ]
        )
        print("OpenAI応答:", response)
        comment = response['choices'][0]['message']['content']
        return jsonify({'result': comment})
    except Exception as e:
        print("OpenAIエラー:", e)
        return jsonify({'error': 'LLM生成エラー', 'details': str(e)}), 500
