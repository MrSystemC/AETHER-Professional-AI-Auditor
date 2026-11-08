"""
AETHER — Web interface
"""

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
import tempfile
import os

from aether.core import Aether

app = FastAPI(title="AETHER", description="Система фундаментальной инженерии цифрового мира")
engine = Aether()

# Full HTML content would go here; for this call we include a minimal version
HTML = """<!DOCTYPE html><html><head><title>AETHER</title></head><body><h1>AETHER</h1><p>Web interface</p></body></html>"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML

@app.post("/process")
async def process(text: str = Form(None), file: UploadFile = File(None)):
    if file:
        content = await file.read()
        filename = file.filename
    elif text:
        content = text
        filename = "text"
    else:
        return JSONResponse({"error": "no input"}, status_code=400)
    root = engine.process(content, filename)
    return root.to_dict()

@app.post("/audit")
async def audit(payload: dict):
    text = payload.get("text", "")
    if not text:
        return JSONResponse({"error": "no text"}, status_code=400)
    report = engine.audit_ai(text)
    return report
