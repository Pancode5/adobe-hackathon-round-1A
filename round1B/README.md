# Round 1B - Persona-Driven Document Intelligence

## 📁 Folder Structure
- `input/` - Place PDFs and `persona.json` here
- `output/` - Generated output JSON will appear here

## 👤 persona.json format
```
{
  "persona": "PhD Researcher in Computational Biology",
  "job_to_be_done": "Prepare a literature review on GNNs for drug discovery"
}
```

## ⚙️ How to Run

### Build Docker Image
```
docker build --platform=linux/amd64 -t round1b-solution:latest .
```

### Run Container
```
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none round1b-solution:latest
```

(Use `%cd%` instead of `$(pwd)` on Windows CMD)