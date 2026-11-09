from fetchers.rss_fetcher import RSSFetcher
from cleaner.text_cleaner import TextCleaner

def main():
    print("=== Iniciando Agregador de Noticias sin Anuncios ===")
    
    # URL de ejemplo para un feed RSS de noticias
    sample_feed_url = "https://news.google.com/rss?hl=es-419&gl=AR&ceid=AR:es-419"
    
    # Inicializar el conector RSS
    fetcher = RSSFetcher(source_name="Google News RSS", endpoint_url=sample_feed_url)
    
    print(f"Conectando a la fuente: {fetcher.source_name}...")
    
    # Simulación de obtención de datos crudos (en futuras iteraciones traerá los ítems reales)
    # raw_articles = fetcher.fetch()
    
    # Ejemplo de prueba de limpieza sobre un contenido HTML simulado con banners y scripts
    sample_raw_html = """
    <div class="article-body">
        <script>alert('malicious tracking script');</script>
        <p>Esta es una noticia de prueba muy importante sobre tecnología y desarrollo en Argentina.</p>
        <div class="banner-ads" style="background: red;">¡Compre aquí con 50% de descuento!</div>
        <p>El sistema de análisis de datos continúa procesando los reportes económicos oficiales.</p>
    </div>
    """
    
    print("\n[+] Procesando y limpiando contenido...")
    cleaned_output = TextCleaner.remove_ads_and_banners(sample_raw_html)
    
    print("\n--- CONTENIDO LIMPIO RESULTANTE ---")
    print(cleaned_output)
    print("-----------------------------------")
    print("\nEsqueleto del main.py ejecutado con éxito en la nube.")

if __name__ == "__main__":
    main()
