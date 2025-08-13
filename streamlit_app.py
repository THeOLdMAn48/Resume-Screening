# app/streamlit_app.py
import streamlit as st
import os
from utils_text import extract_text_from_pdf_file, read_text_file, clean_text
from utils_match import tfidf_similarity, load_skills_from_csv, extract_skills_from_text
import pandas as pd

st.set_page_config(page_title="Resume Matcher (MVP)", layout="wide")
st.title("🧾 Resume Matcher — MVP (TF-IDF)")

# Sidebar options
with st.sidebar:
    st.header("Options")
    st.markdown("Upload `data/skills_master.csv` for custom skill keywords.")
    show_raw = st.checkbox("Show parsed resume text", value=False)
    sample_jd = st.button("Load sample job description")

# Sample JD
SAMPLE_JD = """We are hiring a Data Scientist with strong Python, SQL and Machine Learning experience.
Responsibilities: build predictive models (scikit-learn, xgboost), create dashboards (Power BI), work with datasets and deploy models.
Preferred: NLP, transformers, cloud (AWS)."""

if sample_jd:
    st.session_state['jd_text'] = SAMPLE_JD

# Job Description input
st.subheader("1) Job Description (paste or upload .txt)")
jd_text = st.text_area("Paste Job Description here", value=st.session_state.get('jd_text', SAMPLE_JD), height=160)
uploaded_jd_file = st.file_uploader("Or upload job description (.txt)", type=['txt'])
if uploaded_jd_file:
    jd_text = read_text_file(uploaded_jd_file.read())

# Resume upload
st.subheader("2) Upload resume(s) (.pdf or .txt)")
uploaded_files = st.file_uploader("Upload resume files (you can select multiple)", type=['pdf', 'txt'],
                                  accept_multiple_files=True)

# Skills file (optional)
skills_csv_path = "data/skills_master.csv"
skills_list = []
if os.path.exists(skills_csv_path):
    skills_list = load_skills_from_csv(skills_csv_path)
else:
    st.sidebar.warning("Add data/skills_master.csv for skill matching (optional). Using built-in defaults.")
    # fallback default small list
    skills_list = ["python", "sql", "pandas", "numpy", "machine learning", "power bi", "tableau", "aws", "docker",
                   "flask"]

# Run button
if st.button("Run Screening"):
    if not jd_text or not uploaded_files:
        st.error("Please paste a job description and upload at least one resume file.")
    else:
        results = []
        for up in uploaded_files:
            name = up.name
            raw_text = ""
            if name.lower().endswith(".pdf"):
                raw_text = extract_text_from_pdf_file(up.read())
            else:
                try:
                    raw_text = up.read().decode('utf-8', errors='ignore')
                except Exception:
                    raw_text = ""

            if not raw_text:
                st.warning(f"Could not extract text from {name}. Try re-saving or using a TXT file.")

            # cleaning
            resume_clean = clean_text(raw_text)
            jd_clean = clean_text(jd_text)

            # tfidf
            score, top_terms = tfidf_similarity(resume_clean, jd_clean, top_n=8)
            top_term_str = ", ".join([t[0] for t in top_terms]) if top_terms else ""

            # skills
            matched_skills = extract_skills_from_text(resume_clean, skills_list)
            jd_skills = extract_skills_from_text(jd_clean, skills_list)
            missing_skills = sorted([s for s in jd_skills if s not in matched_skills])

            results.append({
                "filename": name,
                "score_tfidf": score,
                "top_terms": top_term_str,
                "matched_skills": ", ".join(matched_skills),
                "missing_skills": ", ".join(missing_skills),
                "raw_text": raw_text
            })

        df = pd.DataFrame(results).sort_values(by="score_tfidf", ascending=False).reset_index(drop=True)
        st.success("Screening complete ✅")
        st.dataframe(df[["filename", "score_tfidf", "matched_skills", "missing_skills", "top_terms"]],
                     use_container_width=True)

        # Download CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download results (CSV)", data=csv, file_name="screening_results.csv", mime="text/csv")

        # expanders for details
        for i, row in df.iterrows():
            with st.expander(f"Details — {row['filename']} (Score: {row['score_tfidf']}%)"):
                st.markdown(f"**Top matched terms:** {row['top_terms'] or '—'}")
                st.markdown(f"**Matched skills:** {row['matched_skills'] or '—'}")
                st.markdown(f"**Missing skills:** {row['missing_skills'] or '—'}")
                if show_raw:
                    st.text_area("Parsed resume text (first 20k chars)", value=row['raw_text'][:20000], height=240)
