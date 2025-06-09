from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# CORS設定（Makeからのアクセス許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/fetch")
async def fetch(request: Request):
    data = await request.json()
    url = data.get("url")

    prompt = f"""以下はとあるWebページのHTML構造です。
下記URLページがGoogleの「AI概要（AI Overview）」に引用されやすいかどうかを100点満点で評価してください。

【分析項目】
- タイトルと見出しが明確か？
- 構造化されたQ&A形式があるか？
- 専門性や信頼性が感じられるか？
- HTML内に著者や運営者、監修者の情報はあるか？

以下の点をもとに、点数（100点満点）＋改善アドバイスをください。

=== URL ===
{url}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response['choices'][0]['message']['content']
    return {"answer": result}
