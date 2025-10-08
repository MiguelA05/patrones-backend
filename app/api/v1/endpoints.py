from fastapi import APIRouter
from pydantic import BaseModel
from app.services.extractor import extract_all

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.post("/extract")
def extract(req: TextRequest):
    return extract_all(req.text)
