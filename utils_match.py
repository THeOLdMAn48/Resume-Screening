# src/utils_match.py
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

def tfidf_similarity(resume_text: str, jd_text: str, top_n: int = 6) -> Tuple[float, List[Tuple[str, float]]]:
    """
    Returns (score_percent, top_terms_list[(term, weight)]) using TF-IDF.
    """
    a = resume_text or ""
    b = jd_text or ""
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=5000)
    X = vectorizer.fit_transform([a, b])
    cos = cosine_similarity(X[0], X[1])[0][0]
    terms = vectorizer.get_feature_names_out()
    v0 = X[0].toarray().ravel()
    v1 = X[1].toarray().ravel()
    prod = v0 * v1
    if prod.size == 0:
        return 0.0, []
    top_idx = np.argsort(prod)[::-1][:top_n]
    top_terms = []
    for i in top_idx:
        if prod[i] > 0:
            top_terms.append((terms[i], float(prod[i])))
    return round(float(cos) * 100, 2), top_terms

def load_skills_from_csv(csv_path: str) -> List[str]:
    """Load skill list from a CSV with header 'skill' (one per row)."""
    import pandas as pd
    try:
        df = pd.read_csv(csv_path)
        if 'skill' in df.columns:
            return [str(s).strip().lower() for s in df['skill'].dropna().unique().tolist()]
    except Exception:
        pass
    return []

def extract_skills_from_text(text: str, skills_list: List[str]) -> List[str]:
    """Return skills found in text using simple word boundary matching."""
    if not text:
        return []
    txt = text.lower()
    found = set()
    for skill in skills_list:
        sk = skill.lower().strip()
        if not sk:
            continue
        # escape special characters for regex
        pattern = r'\b' + re.escape(sk) + r'\b'
        if re.search(pattern, txt):
            found.add(skill)
    return sorted(list(found))
