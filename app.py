import streamlit as st
import json
from matcher.ai_matcher import match_tenders
import base64
st.set_page_config(page_title="Tender Recommendation", page_icon="📝")
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background(r"pg.jpg")
def load_tenders(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def save_company_profile(uploaded_file):
    with open('data/company_profile.txt', 'wb') as f:
        f.write(uploaded_file.read())

st.set_page_config(page_title="Tender Tracker AI", layout="wide")

st.title("📑Tender Tracker & AI Bid Match Recommender")

st.sidebar.header("Upload Company Profile")
uploaded_profile = st.sidebar.file_uploader("Upload your company profile (.txt)", type=["txt"])

threshold = st.sidebar.slider("Matching Threshold", 0.3, 0.9, 0.5)

if uploaded_profile:
    save_company_profile(uploaded_profile)
    st.sidebar.success("✅ Profile uploaded successfully!")

tenders = load_tenders('data/tenders.json')

if uploaded_profile:
    matches, all_tenders = match_tenders('data/company_profile.txt', 'data/tenders.json', threshold=threshold)
    st.subheader(f"🎯 Tenders Matched to Your Profile (Threshold {threshold})")
    if matches:
        for tender in matches:
            with st.expander(f"🔎 {tender['title']} (Score: {tender['match_score']})"):
                st.write(f"**Scope:** {tender.get('scope', 'No scope available.')}")
                st.write(f"**Deadline:** {tender.get('deadline', 'N/A')}")
                st.write(f"**EMD:** {tender.get('emd', 'N/A')}")
    else:
        st.warning("😢 No tenders matched your profile based on the current threshold. Try lowering it.")

st.subheader("📋 All Available Tenders")
for tender in tenders:
    with st.expander(f"📝 {tender['title']}"):
        st.write(f"**Scope:** {tender.get('scope', 'No scope available.')}")
        st.write(f"**Deadline:** {tender.get('deadline', 'N/A')}")
        st.write(f"**EMD:** {tender.get('emd', 'N/A')}")
