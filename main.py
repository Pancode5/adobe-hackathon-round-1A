import fitz  # PyMuPDF
import os
import json

def classify_heading(font_size):
    if font_size >= 16:
        return "H1"
    elif font_size >= 13:
        return "H2"
    elif font_size >= 11:
        return "H3"
    else:
        return None

def extract_outline_from_pdf(filepath):
    doc = fitz.open(filepath)
    outline = []
    title = os.path.basename(filepath).replace(".pdf", "")

    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    font_size = span["size"]
                    text = span["text"].strip()
                    heading_level = classify_heading(font_size)
                    if heading_level and len(text.split()) <= 15 and text.isprintable():
                        outline.append({
                            "level": heading_level,
                            "text": text,
                            "page": page_number
                        })
    return {"title": title, "outline": outline}

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            filepath = os.path.join(input_dir, filename)
            result = extract_outline_from_pdf(filepath)
            output_filename = filename.replace(".pdf", ".json")
            with open(os.path.join(output_dir, output_filename), "w") as f:
                json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()