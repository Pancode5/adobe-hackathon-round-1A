# Connecting the Dots - Round 1A

## 📌 Overview
This solution extracts structured outlines (Title, H1, H2, H3 with page numbers) from PDFs using PyMuPDF.

## 📁 Folder Structure
- `/input` — Place your PDF files here before running.
- `/output` — The corresponding JSON files will be saved here.

## ⚙️ How to Build and Run

### 1. Build Docker Image
```
docker build --platform linux/amd64 -t pdf-outliner:latest .
```

### 2. Run Container
```
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outliner:latest
```

## ✅ Output Format (Example)
```
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```