from sentence_transformers import SentenceTransformer, util
import json

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Light and fast

def load_company_profile(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def load_tenders(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def calculate_similarity(tender_scope, profile_text):
    tender_embedding = model.encode(tender_scope, convert_to_tensor=True)
    profile_embedding = model.encode(profile_text, convert_to_tensor=True)
    similarity = util.cos_sim(tender_embedding, profile_embedding)
    return float(similarity)

def match_tenders(profile_path, tenders_path, threshold=0.5):
    profile_text = load_company_profile(profile_path)
    tenders = load_tenders(tenders_path)

    matched = []
    for tender in tenders:
        scope = tender.get('scope', '')
        if scope:
            score = calculate_similarity(scope, profile_text)
            tender['match_score'] = round(score, 2)
            if score >= threshold:
                matched.append(tender)
    
    return matched, tenders
