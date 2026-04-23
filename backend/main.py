from fastapi import FastAPI, UploadFile, File
from storage import upload_pdf, get_pdf_url
import uuid

app = FastAPI()

@app.post("/upload-paper")
async def upload_paper(file: UploadFile = File(...)):
    contents = await file.read()
    filename = f"{uuid.uuid4()}.pdf"
    upload_pdf(contents, filename)
    return {"filename": filename}

@app.get("/paper-url/{filename}")
def paper_url(filename: str):
    url = get_pdf_url(filename)
    return {"url": url}