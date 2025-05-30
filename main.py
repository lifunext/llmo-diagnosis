import logging
logging.basicConfig(level=logging.INFO)

@app.route('/fetch', methods=['POST'])
def fetch():
    try:
        data = request.get_json()
        url = data.get('url')
        logging.info(f"Received URL: {url}")

        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()

        response = openai.ChatCompletion.create(
            model="gpt-4o",  # または "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "あなたはSEOに詳しいWebマーケターです。"},
                {"role": "user", "content": f"以下のWebページの内容を診断してください：\n{text}"}
            ]
        )

        comment = response['choices'][0]['message']['content']
        return jsonify({"comment": comment})
    
    except Exception as e:
        logging.exception("Error in /fetch")
        return jsonify({'error': str(e)}), 500
