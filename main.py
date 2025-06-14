from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
import fitz
from sqlalchemy.orm import Session
from resume_parser import extract_entities

# Models
from validation.schemas import UploadResumeOut,UploadResume
from models.resumes import Resume

# db
from db import get_session, Base, engine

# .env
from dotenv import load_dotenv
import os



# SQL

load_dotenv()


app = FastAPI()

@app.post("/upload-resume/", response_model= UploadResumeOut)
async def upload_resume(file: UploadFile = File(...), db:Session=Depends(get_session)):
  if not file.filename.endswith(".pdf"):
    return {"error": "Only PDF files are supported"}
  
  contents = await file.read()

  with fitz.open(stream=contents, filetype="pdf") as doc:
    text = ""
    for page in doc: 
      text += page.get_text()
    
    structured_data = extract_entities(text)

    db_resume = db.query(Resume).filter(Resume.email == structured_data.email).first()

    if db_resume:
      raise HTTPException(status_code=400, detail="Email already exists")
    
    # new_resume=Resume(
    #   name=structured_data.name.strip().title(), 
    #   email=structured_data.email,
    #   phone=structured_data.phone,
    #   skills=structured_data.skills,
    #   education=structured_data.education,
    #   experience=structured_data.experience,
    #   raw_text=structured_data.raw_text,
    # )
    # db.add(new_resume)
    # db.commit()
    # db.refresh(new_resume)

    return {"extracted_text": structured_data }