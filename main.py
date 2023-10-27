from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from mechanics.storage import list_files_in_folder, get_file_in_folder, upload_file, download_file
from mechanics.processor import extract_text_from_pdf, ans_question_from_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # accept only PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    try:
        # upload file to storage
        upload_result = upload_file(file)
    except Exception as _:
        raise HTTPException(status_code=500, detail="Error uploading file")
    return {"url": upload_result}

@app.get("/list")
async def list_files():
    try:
        files = list_files_in_folder()
        # remove the storage folder name from the file name
        files = [file.split("/")[-1] for file in files]
    except Exception as _:
        raise HTTPException(status_code=500, detail="Error getting files")
    return {"files": files}

class InquiryData(BaseModel):
    question: str
    doc_ids: Optional[List[str]] = None

@app.post("/inquire")
async def inquire(data: InquiryData):
    question = data.question
    doc_ids = data.doc_ids
    
    # check is doc_ids is empty
    if not doc_ids:
        # doc_ids is empty, get all pdfs from the storage folder
        try:
            files = list_files_in_folder()
        except Exception as _:
            raise HTTPException(status_code=500, detail="Error getting files")
    
    else:
        # doc_ids is not empty, get the specified pdfs
        files = []
        for doc_id in doc_ids:
            try:
                files.append(get_file_in_folder(doc_id))
            except Exception as _:
                raise HTTPException(status_code=500, detail="Error getting doc file")
            
    if not files:
        raise HTTPException(status_code=400, detail="You need to upload at least one PDF file")
            
    full_text = ""
    for file in files:
        try:
            file_path = download_file(file)
            text = extract_text_from_pdf(file_path)
            full_text += text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file, {str(e)}")
        
    try:
        answer = ans_question_from_text(full_text, question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error answering question, {str(e)}")
            
    return {"answer": answer}