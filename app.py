import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI

# Charger variables d'environnement
# load_dotenv()
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)


st.set_page_config(page_title="Assistant Documents Auto", page_icon="🚘", layout="wide")
st.title("🚘 Assistant Carte Grise & Factures")

# === Upload fichiers ===
uploaded_files = st.file_uploader("📂 Importez vos fichiers (carte grise + factures)", type="pdf", accept_multiple_files=True)

docs_text = {}

if uploaded_files:
    for file in uploaded_files:
        reader = PdfReader(file)
        texte = " ".join([page.extract_text() for page in reader.pages])
        docs_text[file.name] = texte

    st.success(f"{len(uploaded_files)} fichier(s) chargé(s) ✅")

    # === Interrogation libre ===
    question = st.text_input("❓ Posez une question (ex: Quel est le numéro VIN ?)")

    if st.button("Interroger l'IA") and question:
        with st.spinner("Analyse en cours..."):
            all_text = "\n\n".join([f"--- {name} ---\n{text}" for name, text in docs_text.items()])
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Tu es un assistant qui analyse des cartes grises et factures automobiles."},
                    {"role": "user", "content": f"Voici les documents :\n{all_text}\n\nQuestion : {question}"}
                ]
            )
            st.write("### Réponse de l'IA :")
            st.write(response.choices[0].message.content)

