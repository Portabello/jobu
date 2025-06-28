from fastapi import FastAPI
from pydantic import BaseModel
from openai_services import get_gpt_response
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles



# Load environment variables (optional here since openai_services.py already does)
load_dotenv()

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"  # Optional: allow overriding the model

@app.post("/chat")
async def chat(request: ChatRequest):
    response = get_gpt_response(request.message, model=request.model)
    return {"response": response}

#configure FastAPI to serve static files (index.html)
app.mount("/", StaticFiles(directory="C:/Users/Jasmit/Documents/GitHub/jobu/frontend" , html=True), name="static")
