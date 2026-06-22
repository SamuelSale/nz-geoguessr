# NZ GeoGuessr Agent

A hybrid vision-language (VLM) + CNN agent that predicts where in New Zealand
a street-level photo was taken. It combines a CNN region-classifier, a VLM that
extracts visual clues from the image, and a retrieval step over a hand-built
knowledge base of NZ "metas" — then fuses them into a final location guess with
a written rationale.

The work yields two projects:
1. **CNN image-geolocation model** — a standalone computer-vision classifier.
2. **VLM + RAG agent** — reasons over the metas knowledge base and fuses the
   CNN's prediction, benchmarked against the CNN alone.

## Status

In development. Building in phases (dataset → CNN → metas/RAG → fusion →
evaluation → deployment).

## Architecture

- **CNN geolocator** — predicts a region probability prior from the image.
- **VLM perception** — extracts structured visual clues (driving side, plate
  colour, pole/bollard type, road markings, vegetation, signage).
- **Metas knowledge base (RAG)** — retrieves NZ region clues matching the clues.
- **Fusion** — combines CNN prior + observations + retrieved metas into a final
  guess, confidence, and rationale.
- **Evaluation** — benchmarks CNN-alone vs VLM+metas-alone vs hybrid.

## Tech stack

Python 3.11 · PyTorch · scikit-learn · pandas · Mapillary API · Chroma/FAISS ·
Streamlit / Hugging Face Spaces · Power BI

## Setup

```bash
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Project structure

​```
data/        raw, interim, processed datasets
src/         data · cnn · vlm · rag · eval
metas/       hand-written NZ meta notes
app/         Streamlit / HF Spaces app
reports/     figures, dashboards, writeups
​```

## Acknowledgements

Metas compiled in my own words from public GeoGuessr learning resources
(e.g. Plonkit), with sources attributed.