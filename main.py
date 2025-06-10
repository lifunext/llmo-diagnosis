from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],  # ← POSTを含む
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

        prompt = f"以下はとあるWebページのHTML構造です。...（省略）...=== URL ===\n{url}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response['choices'][0]['message']['content']
        return {"answer": result}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
