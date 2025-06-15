from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
import fitz
from sqlalchemy.orm import Session
from resume_parser import extract_entities

# functions
from functions.scrape_web_pages import fetch_web_page

# Models
from validation.schemas import UploadResumeOut,UploadResume
from models.resumes import Resume

# db
from db import get_session, Base, engine

# Create Database
# Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/resumes")
async def get_all_resumes(db: Session = Depends(get_session)):
  db_resumes = db.query(Resume).all()  # Use .all() to fetch all records
  return {"resumes": db_resumes}

@app.get("/resume/{email}")
async def get_resume_by_email(email: str, db: Session = Depends(get_session)):
  db_resume_by_email = db.query(Resume).filter(Resume.email == email).first()
  if not db_resume_by_email:
    raise HTTPException(status_code=404, detail="Resume not found")
  return {"resume": db_resume_by_email}
  

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

    db_resume = db.query(Resume).filter(Resume.email == structured_data['email']).first()

    if db_resume:
      raise HTTPException(status_code=400, detail="Email already exists")
    
    new_resume=Resume(
      name=structured_data['name'].strip().title(), 
      email=structured_data['email'],
      phone=structured_data['phone'],
      skills=structured_data['skills'],
      education=structured_data['education'],
      experience=structured_data['experience'],
      # raw_text=structured_data['raw_text'],
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {"extracted_text": structured_data , "msg": "Success"}
  
@app.post("/fetch-web-pages")
async def fetch_web_pages(webPage: str):
  html_doc = """<html><head><title>The Dormouse's story</title></head>
  <body>
  <p class="title"><b>The Dormouse's story</b></p>

  <p class="story">Once upon a time there were three little sisters; and their names were
  <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
  <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
  <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
  and they lived at the bottom of a well.</p>

  <p class="story">...</p>
  """
  page = fetch_web_page(webPage) 
  print(page)
  return {"fetch_page", "Hello"}
