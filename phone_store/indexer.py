import os
import fitz  # PyMuPDF
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StemmingAnalyzer

schema = Schema(
    title=TEXT(stored=True),
    path=ID(stored=True, unique=True),
    content=TEXT(analyzer=StemmingAnalyzer())
)

INDEX_DIR = "indexdir"
if not os.path.exists(INDEX_DIR):
    os.mkdir(INDEX_DIR)

ix = create_in(INDEX_DIR, schema)
writer = ix.writer()

PDF_DIR = "./media/specs"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

for filename in os.listdir(PDF_DIR):
    if filename.endswith(".pdf"):
        full_path = os.path.join(PDF_DIR, filename)
        text = extract_text_from_pdf(full_path)
        writer.add_document(title=filename, path=full_path, content=text)
        print(f"Indexat: {filename}")

writer.commit()
print("Done indexing")
