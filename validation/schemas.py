from typing import Dict
from pydantic import BaseModel

class UploadResume(BaseModel):
  name: str
  email:str
  phone:str
  skills: Dict[str, str]  # or Dict[str, Any] for mixed types
  education: Dict[str, str]  # or Dict[str, Any] for mixed types
  experience: Dict[str, str]  # or Dict[str, Any] for mixed types
  raw_text:str

class UploadResumeOut(BaseModel):
  msg: str
  
  class Config:
    orm_mode=True