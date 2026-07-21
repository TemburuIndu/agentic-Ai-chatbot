from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
import json
import tempfile
import os
from models import QueryResponse
from graph_builder import jarvis

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/style.css")
async def get_css():
    return FileResponse("static/style.css", media_type="text/css")

@app.get("/script.js")
async def get_js():
    return FileResponse("static/script.js", media_type="application/javascript")

@app.post("/run")
async def process_document(
    document: UploadFile = File(...),
    questions: str = Form(...)
):
    try:
        # Parse questions
        questions_list = json.loads(questions)
        
        # Save uploaded file temporarily
        file_ext = os.path.splitext(document.filename)[1] if document.filename else '.tmp'
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await document.read()
            tmp_file.write(content)
            file_path = tmp_file.name
        
        # Process with jarvis
        final_state = await jarvis.ainvoke({
            "doc_url": file_path, 
            "questions": questions_list
        })
        
        # Clean up temp file
        os.unlink(file_path)
        
        answers = final_state.get("answers", ["No answer could be generated."])
        return QueryResponse(answers=answers)
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)