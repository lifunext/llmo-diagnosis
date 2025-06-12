from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/fetch")
async def fetch(request: Request):
    try:
        data = await request.json()
        url = data.get("url")

        if not url:
            return JSONResponse(content={"error": "No URL provided"}, status_code=400)

        prompt = f"""以下はとあるWebページのHTML構造です。<br>
このURLがGoogleの「AI概要（AI Overview）」に引用されやすいか評価してください。<br>
以下の評価ポイントをもとに、点数（100点満点）＋改善アドバイスをください。<br>
各項目と返答の仕方は下記でお願いします。<br><br>
・返答は「<br>」などを使い、HTMLメールで改行が反映されるように整えてください。<br>
・改行も一言ずつ改行し、各評価ポイントの間には1行開けてください。<br>
・改善アドバイスは箇条書きでお願いします。<br>
・各項目25点満点でトータルが総合点。何点中何点かわかるように記載<br><br>

総合点：●●点/100点<br><br>

【評価ポイント】<br>
- タイトルと見出しが明確か？（●●点/25点）<br>
└概要<br><br>

- 構造化されたQ&A形式があるか？（●●点/25点）<br>
└概要<br><br>

- 専門性や信頼性が感じられるか？（●●点/25点）<br>
└概要<br><br>

- HTML内に著者や運営者、監修者の情報はあるか？（●●点/25点）<br>
└概要<br><br>

【改善アドバイス】<br><br>

=== URL ===<br>
{url}
"""


        response = openai.ChatCompletion.create(
            model="gpt-4o",  # または gpt-4 / gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}]
        )
        result = response['choices'][0]['message']['content']
        return {"answer": result}

    except Exception as e:
        print("Exception occurred:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
