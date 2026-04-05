from vinted_scraper import VintedScraper

# Inizializza lo scraper con l'URL della piattaforma (es. vinted.it)
scraper = VintedScraper("https://www.vinted.it")

def analizza_quadri(keyword="quadri", limite=20):
    print(f"🔍 Ricerca in corso per: {keyword}...")
    
    # Esegue la ricerca
    params = {
        "search_text": keyword,
        "catalog_ids": "1124", # ID categoria Arredamento/Decorazioni (opzionale)
        "order": "newest"       # Ordiniamo per i più recenti per vedere il trend attuale
    }
    
    items = scraper.search(params)
    
    # Lista per memorizzare i dati estratti
    risultati = []

    for item in items[:limite]:
        dati_quadro = {
            "titolo": item.title,
            "prezzo": item.price,
            "preferiti": item.favourite_count,
            "visualizzazioni": item.view_count,
            "url": item.url
        }
        risultati.append(dati_quadro)

    # Ordina la lista per numero di preferiti (dal più alto al più basso)
    classifica = sorted(risultati, key=lambda x: x['preferiti'], reverse=True)

    print(f"\n🏆 I {limite} QUADRI PIÙ APPREZZATI DEL MOMENTO:\n")
    for i, q in enumerate(classifica, 1):
        print(f"{i}. {q['titolo']}")
        print(f"   ❤️ Preferiti: {q['preferiti']} | 👀 Visualizzazioni: {q['visualizzazioni']}")
        print(f"   💰 Prezzo: {q['prezzo']}€")
        print(f"   🔗 Link: {q['url']}\n")

if __name__ == "__main__":
    analizza_quadri("quadri olio", limite=15)
