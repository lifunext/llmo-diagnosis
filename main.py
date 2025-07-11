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

        prompt = f"""以下はとあるWebページです。
以下のURLを以下の評価ポイントをもとに、点数＋改善アドバイスをください。
（100点満点。各項目25点満点でトータルが総合点。）
各項目と返答内容は下記でお願いします。
「<br>」などを使い、HTMLメールで改行が反映されるように整えてください。
▲▲には一言でポイントを書いてください。
改行も一言ずつ改行し、各評価ポイントの間には1行開けてください。
改善アドバイスは箇条書きでお願いします。
URLの部分にURL出ないものが入っているときは診断できない旨伝えてください。

総合点：●●点/100点<br>

【評価ポイント】
- タイトルと見出しが明確か？（●●点/25点）<br>
└▲▲<br><br>
- 構造化されたQ&A形式があるか？（●●点/25点）<br>
└▲▲<br><br>
- 専門性や信頼性が感じられるか？（●●点/25点）<br>
└▲▲<br><br>
- HTML内に著者や運営者、監修者の情報はあるか？（●●点/25点）<br>
└▲▲<br><br>

【改善アドバイス】<br>

=== URL ===
{url}
"""


        response = openai.ChatCompletion.create(
            model="gpt-4",  # または gpt-4 / gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}]
        )
        result = response['choices'][0]['message']['content']
        return {"answer": result}

    except Exception as e:
        print("Exception occurred:", e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
