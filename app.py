# app.py
import streamlit as st
import json
import os

st.set_page_config(page_title="Tender Tracker", layout="wide")

st.title("📄 Government Tender Tracker & Recommender")

# Sidebar
st.sidebar.header("Upload Company Profile")
uploaded_profile = st.sidebar.file_uploader("Choose a company profile (PDF/TXT)", type=["pdf", "txt"])

# Main Area
st.header("Aggregated Tenders")

# Load tenders
if os.path.exists("data/tenders.json"):
    with open("data/tenders.json", "r") as f:
        tenders = json.load(f)
    for tender in tenders:
        st.subheader(tender['title'])
        st.write(f"**Deadline:** {tender['deadline']}")
        st.write(f"**EMD Amount:** {tender['emd']}")
        st.write(f"**Scope of Work:** {tender['scope']}")
        st.divider()
else:
    st.info("No tenders found. Please run the scrapers.")

