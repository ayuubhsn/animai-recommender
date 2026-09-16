
import streamlit as st
import json
from data import df
from ai import analyser_dna, anbefalinger

st.set_page_config(page_title="AnimAI", page_icon="🎌", layout="wide")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp { background-color: #0d0d14; }
.stButton > button {
    background-color: #1a1a2e;
    color: white;
    border: 1px solid #2a2a3e;
    border-radius: 12px;
    padding: 10px 20px;
    width: 100%;
}
.stButton > button:hover {
    background-color: #E24B4A;
    border-color: #E24B4A;
    color: white;
}
.stTextInput > div > div > input {
    background-color: #1a1a2e;
    color: white;
    border: 1px solid #2a2a3e;
    border-radius: 12px;
}
.stTabs [data-baseweb="tab"] { color: #888; font-size: 15px; }
.stTabs [aria-selected="true"] { color: #E24B4A; }
.stTabs [data-baseweb="tab-highlight"] { background-color: #E24B4A; }
</style>

<div style="background:#12121f; border-bottom:1px solid #1e1e30; padding:0 2rem; height:56px; display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:1rem;">
    <div style="width:8px; height:8px; border-radius:50%; background:#E24B4A;"></div>
    <span style="color:white; font-size:16px; font-weight:500;">AnimAI</span>
    <span style="color:#666; font-size:13px; margin-left:8px;">Din personlige anime-guide</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🎯 Anbefalinger", "🧬 Anime DNA", "💬 Chat"])

with tab1:
    if "stemning" not in st.session_state:
        st.session_state.stemning = ""

    st.write("Velg stemning:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⚔️ Action"): st.session_state.stemning = "action og intense kamper"
        if st.button("💔 Drama"): st.session_state.stemning = "drama og følelsesmessige historier"
    with col2:
        if st.button("🧠 Thriller"): st.session_state.stemning = "psykologisk thriller og spenning"
        if st.button("🌸 Romance"): st.session_state.stemning = "romantikk og kjærlighet"
    with col3:
        if st.button("😂 Comedy"): st.session_state.stemning = "komedie og humor"
        if st.button("👻 Horror"): st.session_state.stemning = "horror og skumle elementer"

    bruker_input = st.text_input("Eller beskriv selv:", placeholder="F.eks. noe mørkt og action-fylt...", value=st.session_state.stemning)

    if st.button("Finn anime", key="finn"):
        if bruker_input:
            with st.spinner("Spør sensei..."):
                svar = anbefalinger(bruker_input, df)
            anbefalte = json.loads(svar)
            for anime in anbefalte:
                rad = df[df["tittel"] == anime["tittel"]]
                if not rad.empty:
                    st.markdown(f"""
                    <div style="background:#12121f; border:1px solid #1e1e30; border-radius:14px; padding:14px; display:flex; gap:14px; margin-bottom:10px;">
                        <img src="{rad.iloc[0]['bilde']}" style="width:80px; height:110px; border-radius:8px; object-fit:cover;">
                        <div>
                            <div style="color:white; font-size:15px; font-weight:500; margin-bottom:4px;">{anime['tittel']}</div>
                            <div style="color:#5DCAA5; font-size:12px; margin-bottom:6px;">⭐ {rad.iloc[0]['score']} · {rad.iloc[0]['genres']}</div>
                            <div style="color:#888; font-size:13px;">{anime['forklaring']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Velg en stemning eller skriv hva du er i stemning for!")

with tab2:
    st.write("Skriv 3 anime du liker:")
    
    anime1 = st.text_input("Anime 1", placeholder="F.eks. Death Note")
    anime2 = st.text_input("Anime 2", placeholder="F.eks. Attack on Titan")
    anime3 = st.text_input("Anime 3", placeholder="F.eks. Steins;Gate")
    
    if st.button("Analyser min smak", key="dna"):
        if anime1 and anime2 and anime3:
            with st.spinner("Analyserer din anime-DNA..."):
                svar = analyser_dna(anime1, anime2, anime3, df)
            
            resultat = json.loads(svar)
            
            st.subheader("Din anime-DNA 🧬")
            for trekk in resultat["profil"]:
                st.markdown(f"""
                <span style="background:#1a0f2e; border:1px solid #534AB7; color:#AFA9EC; padding:4px 12px; border-radius:20px; font-size:13px; margin-right:8px;">{trekk}</span>
                """, unsafe_allow_html=True)
            
            st.divider()
            st.subheader("Anbefalinger basert på din DNA")
            
            for anime in resultat["anbefalinger"]:
                rad = df[df["tittel"] == anime["tittel"]]
                if not rad.empty:
                    st.markdown(f"""
                    <div style="background:#12121f; border:1px solid #1e1e30; border-radius:14px; padding:14px; display:flex; gap:14px; margin-bottom:10px;">
                        <img src="{rad.iloc[0]['bilde']}" style="width:80px; height:110px; border-radius:8px; object-fit:cover;">
                        <div>
                            <div style="color:white; font-size:15px; font-weight:500; margin-bottom:4px;">{anime['tittel']}</div>
                            <div style="color:#5DCAA5; font-size:12px; margin-bottom:6px;">⭐ {rad.iloc[0]['score']}</div>
                            <div style="color:#888; font-size:13px;">{anime['forklaring']}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("Skriv inn alle tre anime!")

with tab3:
    from ai import chat_karakter
    
    karakterer = ["Naruto", "Light Yagami", "Levi", "Goku", "Luffy", "Eren"]
    valgt = st.selectbox("Velg karakter:", karakterer)
    
    if "historikk" not in st.session_state:
        st.session_state.historikk = []
    
    if "forrige_karakter" not in st.session_state:
        st.session_state.forrige_karakter = valgt
    
    if valgt != st.session_state.forrige_karakter:
        st.session_state.historikk = []
        st.session_state.forrige_karakter = valgt
    
    for msg in st.session_state.historikk:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
    
    melding = st.chat_input("Skriv til karakteren...")
    
    if melding:
        st.session_state.historikk.append({"role": "user", "content": melding})
        st.chat_message("user").write(melding)
        
        with st.spinner(f"{valgt} tenker..."):
            svar = chat_karakter(valgt, melding, st.session_state.historikk)
        
        st.session_state.historikk.append({"role": "assistant", "content": svar})
        st.chat_message("assistant").write(svar)