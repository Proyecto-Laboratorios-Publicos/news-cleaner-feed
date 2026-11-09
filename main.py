from fetchers.rss_fetcher import RSSFetcher
from cleaner.text_cleaner import TextCleaner

def main():
    print("=== Iniciando Agregador de Noticias sin Anuncios ===")
    
    # URL del feed RSS de noticias de Google News (Argentina)
    sample_feed_url = "https://news.google.com/rss?hl=es-419&gl=AR&ceid=AR:es-419"
    
    # Inicializar el conector RSS
    fetcher = RSSFetcher(source_name="Google News RSS", endpoint_url=sample_feed_url)
    print(f"Conectando a la fuente: {fetcher.source_name}...")
    
    # Obtener contenido real del feed RSS vía requests
    raw_rss_data = fetcher.fetch()
    
    if raw_rss_data:
        print(f"\n[+] ¡Conexión exitosa! Datos descargados ({len(raw_rss_data)} caracteres).")
        
        # Ejemplo de limpieza aplicado al contenido crudo obtenido o a un fragmento
        print("\n[+] Procesando y limpiando contenido del feed...")
        cleaned_output = TextCleaner.remove_ads_and_banners(raw_rss_data[:1500]) # Mostramos un snippet inicial limpio
        
        print("\n--- CONTENIDO LIMPIO RESULTANTE (Muestra) ---")
        print(cleaned_output[:600] + "...\n[Contenido truncado para visualización]")
        print("---------------------------------------------")
    else:
        print("[-] No se pudieron obtener datos del feed RSS.")

    print("\nEjecución del main.py finalizada con éxito.")

if __name__ == "__main__":
    main()
