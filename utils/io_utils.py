import os
from docx import Document

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def save_docx(text: str, path: str):
    ensure_dir(os.path.dirname(path))
    doc = Document()
    for para in text.split("\n"):
        doc.add_paragraph(para)
    doc.save(path)

def save_text(text: str, path: str):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
