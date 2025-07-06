from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os, json
from ibm_watson_machine_learning import APIClient
from ibm_watson_machine_learning.foundation_models import Model
import sys
print("⚙️ Python Version:", sys.version)


# IBM Watson setup
wml_credentials = {
    "url": "https://eu-de.ml.cloud.ibm.com",
    "apikey": "BPxaCfjggmxPQzbt-Djeit7Kk4cypyxZ5r7mrfvgp6v4"
}
project_id = "01a3988e-e085-4942-930e-181e9c90081d"

client = APIClient(wml_credentials)
client.set.default_project(project_id)

gen_model = Model(
    model_id="ibm/granite-3-3-8b-instruct",
    params={"decoding_method": "greedy", "max_new_tokens": 50},
    credentials=wml_credentials,
    project_id=project_id
)

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Pydantic Models ==========
class ChatRequest(BaseModel):
    message: str

class CodeRequest(BaseModel):
    prompt: str

# ========== IBM Watsonx Inference Logic ==========
def watson_respond(prompt: str) -> str:
    result = gen_model.generate(prompt=prompt)
    return result["results"][0]["generated_text"]

# ========== API Endpoints ==========

@app.get("/")
def root():
    return {"message": "✅ Watsonx AI Backend with Code Tools is running."}

@app.post("/chat")
def chat_ai(request: ChatRequest):
    prompt = f"You are an AI project assistant. {request.message}"
    response = watson_respond(prompt)
    return {"response": response}

@app.post("/generate-code")
def generate_code(request: CodeRequest):
    prompt = f"Generate Python code for the following task: {request.prompt}"
    code = watson_respond(prompt)
    return {"code": code}

@app.post("/debug-code")
def debug_code(request: CodeRequest):
    prompt = f"Debug the following Python code and explain the issues: {request.prompt}"
    debugged = watson_respond(prompt)
    return {"debugged_code": debugged}

@app.post("/compile-code")
def compile_code(request: CodeRequest):
    prompt = f"What will be the output of this Python code? Also mention any issues: {request.prompt}"
    result = watson_respond(prompt)
    return {"result": result}

@app.post("/generate-requirements")
def generate_requirements(request: CodeRequest):
    prompt = f"List functional and non-functional requirements for this project: {request.prompt}"
    requirements = watson_respond(prompt)
    return {"requirements": requirements}
