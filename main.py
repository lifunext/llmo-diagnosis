from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# CORS設定（Makeなど外部サービスからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて制限
    allow_credentials=True,
    allow_methods=["POST"],  # 明示的にPOSTだけ許可
    allow_headers=["*"],
)

# OpenAI APIキーを環境変数から取得
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/fetch")
async def fetch(request: Request):
    try:
        data = await request.json()
        url = data.get("url", "")

        if not url:
            return JSONResponse(content={"error": "No URL provided"}, status_code=400)

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

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
