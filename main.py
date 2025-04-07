from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from chatbot import chatbot

app = FastAPI(
    title="Chatbot API",
    description="A simple chatbot API",
    version="0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ask")
def handle_question(question:str):
    response = chatbot(question)
    return JSONResponse(content={"response": response})