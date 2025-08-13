# Resume Screening App (MVP)

A fast, lightweight **Applicant-side ATS** tool to match resumes against a Job Description (JD).  
It calculates **similarity score (TF-IDF + cosine)**, extracts **matched & missing skills**, and lets you **download a CSV report**.

> Built for quick screening by applicants and recruiters. Runs locally with Streamlit — no heavyweight ML required.

---

## ✨ Features
- 📄 **Upload Multiple Resumes** — PDF/TXT supported
- 📝 **Paste or Upload JD** — Text area + `.txt` upload
- 🧠 **TF-IDF Similarity** — Cosine score in %
- 🎯 **Skill Matching** — Uses customizable `data/skills_master.csv`
- 🔍 **Top Matched Terms** — Quick view of strongest overlaps
- 📊 **Results Table + CSV Export** — Shareable and sortable
- 🧵 **Clean UI** — Streamlit app with expanders and optional raw text view

---

## 🧱 Tech Stack
- Python, Streamlit
- scikit-learn (TfidfVectorizer, cosine_similarity)
- pandas, numpy
- PyPDF (via `pypdf`) or PyPDF2 (for text extraction)

---

## 📂 Project Structure

```
resume-screening/
|
|─ streamlit_app.py # Main Streamlit application
├─ utils_text.py # PDF/TXT extraction + cleaning
└─ utils_matching.py
│
├─ data/
│ └─ skills_master.csv # One skill per line (CSV with header: skill)
|
├─ screenshots/
├─ requirements.txt
└─ README.md
```

> ⚠️ Note: Keep module/file names consistent with imports used inside `streamlit_app.py`.  
> If you import `from src.utils_match import ...`, then keep files under `src/` and update imports accordingly.

---

## 🚀 Quick Start

### 1) Clone & setup
```bash
git clone https://github.com/<your-username>/resume-screening.git
cd resume-screening
```
### (optional) create venv
```bash
python -m venv .venv
```

### Windows
```bash
.venv\Scripts\activate
```
### Mac/Linux
```bash
source .venv/bin/activate
```
### install deps
```bash
pip install -r requirements.txt
```
### Run the app
```bash
streamlit run streamlist_app.py
```
Open the local URL shown in the terminal (e.g., http://localhost:8501).
## 🧩 Usage
- **Paste JD** in the text area (or upload a .txt).
- **Upload one or more resumes** (.pdf or .txt).
- (Optional) Ensure ``data/skills_master.csv`` exists for better skill matching.-
- Click Run Screening.
- See:
1. score_tfidf (0–100%)
2. matched_skills and missing_skills
3.  top_terms (from TF-IDF overlaps)
- Download CSV with one click.
## 🩺 Troubleshooting
- **ModuleNotFoundError: No module named 'utils_text'**
Ensure app/utils_text.py exists in the same folder as streamlit_app.py, or update imports.

- **No module named 'plotly'**
Install missing dependency: pip install plotly

- **PDF text not extracting**
If scanned, convert to text or upload .txt instead.

- **Low scores**
Add synonyms to skills_master.csv (e.g., ml, machine learning).

## 🗺️ Roadmap
- Semantic Match (SBERT) toggle
- Multiple JDs ranking view
- Highlight matched terms inside resume text
- PDF report export
- Deployed demo on Streamlit Cloud
## 🤝 Contributing
- Pull requests welcome. For major changes, open an issue first.
