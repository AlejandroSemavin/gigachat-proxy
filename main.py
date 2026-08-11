from fastapi import FastAPI, Request
import httpx
import uvicorn

if "PORT" in os.environ:  # Проверяем наличие именно от Railway
    uvicorn_config_port = int(os.getenv("PORT"))
else:
    uvicorn_config_port = 8000  # Дефолтный порт для локалки

app = FastAPI()
GIGACHAT_API_URL = "https://gigachat.api.sber.ru/v1/chat/completions"
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.0-turbo")
API_KEY = os.getenv("GIGACHAT_API_KEY")

@app.post("/api/gigachat") # <--- Точка входа для нашего запроса!
async def proxy_gigachat(request: Request):
    body = await request.json()
    
    if not any(msg["role"] == "system" for msg in body.get("messages", [])):
        body["messages"].insert(0, {"role": "system", "content": f"You are running as {MODEL_NAME}."})
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(GIGACHAT_API_URL, json=body, headers=headers)
        
    return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=uvicorn_config_port)
