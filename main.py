from fastapi import FastAPI, File, UploadFile
import fitz
from resume_parser import extract_entities

app = FastAPI()

@app.get("/")
async def main():
  return {"Test": "Server"}

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
  if not file.filename.endswith(".pdf"):
    return {"error": "Only PDF files are supported"}
  
  contents = await file.read()

  with fitz.open(stream=contents, filetype="pdf") as doc:
    text = ""
    for page in doc: 
      text += page.get_text()
    
    structured_data = extract_entities(text)

    return {"extracted_text": structured_data }