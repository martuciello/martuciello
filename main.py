import streamlit as st
import pandas as pd
from vinted_scraper import VintedScraper

# Configurazione Pagina
st.set_page_config(page_title="Vinted Art Analyzer", layout="wide")

st.title("🎨 Vinted Art Trend Analyzer")
st.write("Analizza quali quadri stanno ottenendo più successo su Vinted in tempo reale.")

# Sidebar per i filtri
with st.sidebar:
    st.header("Parametri di Ricerca")
    keyword = st.text_input("Cosa cerchi?", "quadro olio")
    limite = st.slider("Numero di articoli da analizzare", 10, 100, 30)
    st.info("Nota: Più articoli analizzi, più tempo potrebbe impiegare lo scraper.")

# Inizializzazione Scraper
@st.cache_data(ttl=600) # Salva i risultati per 10 minuti per evitare ban da Vinted
def get_data(query, limit):
    try:
        scraper = VintedScraper("https://www.vinted.it")
        params = {"search_text": query, "order": "newest"}
        items = scraper.search(params)
        
        data = []
        for item in items[:limit]:
            data.append({
                "Titolo": item.title,
                "Prezzo (€)": float(item.price),
                "❤️ Preferiti": item.favourite_count,
                "👀 Visite": item.view_count,
                "Link": item.url
            })
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Errore durante il recupero dati: {e}")
        return pd.DataFrame()

if st.button("Avvia Analisi"):
    df = get_data(keyword, limite)
    
    if not df.empty:
        # Ordina per preferiti di default
        df_sorted = df.sort_values(by="❤️ Preferiti", ascending=False)
        
        # Metriche riassuntive
        col1, col2, col3 = st.columns(3)
        col1.metric("Top Preferiti", int(df["❤️ Preferiti"].max()))
        col2.metric("Prezzo Medio", f"{round(df['Prezzo (€)'].mean(), 2)} €")
        col3.metric("Articoli Analizzati", len(df))

        # Tabella Interattiva
        st.subheader("📊 Classifica Risultati")
        st.dataframe(
            df_sorted, 
            column_config={"Link": st.column_config.LinkColumn("Link Prodotto")},
            use_container_width=True
        )

        # Grafico a dispersione: Prezzo vs Preferiti
        st.subheader("📈 Correlazione Prezzo / Popolarità")
        st.scatter_chart(data=df, x="Prezzo (€)", y="❤️ Preferiti", color="#ff4b4b")
        
    else:
        st.warning("Nessun risultato trovato. Prova a cambiare parola chiave.")


