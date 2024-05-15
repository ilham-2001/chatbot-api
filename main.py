import google.generativeai as genai

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Prompt

import os
from dotenv import load_dotenv

load_dotenv('.env')

LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME")

genai.configure(api_key=LLM_API_KEY)
model = genai.GenerativeModel(LLM_MODEL_NAME)


origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/chat')
async def response_chat(prompt: Prompt):
    response = model.generate_content(f'{prompt}.Please provide a response in a plain structured JSON format').text.replace("`", "").strip('json')
    return response
