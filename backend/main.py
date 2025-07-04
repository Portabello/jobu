from fastapi import FastAPI
from pydantic import BaseModel
from backend.openai_services import get_gpt_response
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File
from fastapi.responses import JSONResponse
import pdfplumber
from backend.openai_services import get_gpt_response, embed_texts, add_resume_to_store, get_resume_context
import os




# Load environment variables (optional here since openai_services.py already does)
load_dotenv()

app = FastAPI()

def extract_text(file: UploadFile):
    if file.filename.endswith(".pdf"):
        with pdfplumber.open(file.file) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif file.filename.endswith(".txt"):
        return file.file.read().decode("utf-8")
    else:
        raise ValueError("Unsupported file type")

def chunk_text(text, max_words=150):
    paragraphs = text.split("\n")
    chunks, current = [], ""
    for p in paragraphs:
        words = p.strip().split()
        if len(current.split()) + len(words) < max_words:
            current += " " + " ".join(words)
        else:
            chunks.append(current.strip())
            current = " ".join(words)
    if current:
        chunks.append(current.strip())
    return chunks

class ChatRequest(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo"  # Optional: allow overriding the model

@app.post("/chat")
async def chat(request: ChatRequest):
    context = get_resume_context(request.message)
    if context:
        full_prompt = f"Use the following resume context to answer the question:\n\n{context}\n\nQuestion: {request.message}"
    else:
        full_prompt = request.message
    response = get_gpt_response(full_prompt, model=request.model)
    return {"response": response}

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        text = extract_text(file)
        chunks = chunk_text(text)
        embeddings = embed_texts(chunks)
        add_resume_to_store(chunks, embeddings)

        return JSONResponse({"message": f"Uploaded and embedded {len(chunks)} chunks from resume."})
    except Exception as e:
        return JSONResponse({"message": f"Upload failed: {str(e)}"}, status_code=400)


#configure FastAPI to serve static files (index.html)
#app.mount("/", StaticFiles(directory="C:/Users/Jasmit/Documents/GitHub/jobu/frontend" , html=True), name="static")
# Get current file directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(BASE_DIR, "../frontend")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
