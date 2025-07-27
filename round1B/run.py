import os
import json
import fitz
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        if text:
            pages.append((page_number, text))
    return pages

def rank_relevance(pages, query, top_k=5):
    texts = [text for _, text in pages]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([query] + texts)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    ranked = sorted(zip(pages, cosine_similarities), key=lambda x: x[1], reverse=True)[:top_k]
    return ranked

def main():
    input_dir = "/app/input"
    output_dir = "/app/output"

    # Load persona and job
    with open(os.path.join(input_dir, "persona.json")) as f:
        persona_info = json.load(f)
    persona = persona_info["persona"]
    job = persona_info["job_to_be_done"]
    query = f"{persona} needs to {job}"

    metadata = {
        "input_documents": [],
        "persona": persona,
        "job_to_be_done": job,
        "timestamp": datetime.datetime.now().isoformat()
    }
    extracted_sections = []
    subsection_analysis = []

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, filename)
            metadata["input_documents"].append(filename)
            pages = extract_text_by_page(pdf_path)
            ranked_pages = rank_relevance(pages, query, top_k=3)

            for rank, ((page_num, text), score) in enumerate(ranked_pages, start=1):
                lines = text.strip().split("\n")
                title = lines[0] if lines else "Relevant Section"
                extracted_sections.append({
                    "document": filename,
                    "page_number": page_num,
                    "section_title": title.strip(),
                    "importance_rank": rank
                })
                subsection_analysis.append({
                    "document": filename,
                    "page_number": page_num,
                    "refined_text": text.strip()[:1000]
                })

    result = {
        "metadata": metadata,
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(os.path.join(output_dir, "final_output.json"), "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()