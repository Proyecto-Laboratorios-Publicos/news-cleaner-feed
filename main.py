from fetchers.rss_fetcher import RSSFetcher
from cleaner.text_cleaner import TextCleaner

# Diccionario maestro de categorías y sus feeds RSS especializados
CATEGORIES = {
    "1": {
        "name": "Tecnología",
        "url": "https://news.google.com/rss/search?q=tecnologia&hl=es-419&gl=AR&ceid=AR:es-419"
    },
    "2": {
        "name": "Finanzas y Economía",
        "url": "https://news.google.com/rss/search?q=economia+finanzas&hl=es-419&gl=AR&ceid=AR:es-419"
    },
    "3": {
        "name": "Política",
        "url": "https://news.google.com/rss/search?q=politica+argentina&hl=es-419&gl=AR&ceid=AR:es-419"
    },
    "4": {
        "name": "Espectáculos",
        "url": "https://news.google.com/rss/search?q=espectaculos+cine+musica&hl=es-419&gl=AR&ceid=AR:es-419"
    }
}

def main():
    print("=== News without ads ===")
    print("Seleccione la categoría que desea consultar:\n")
    
    for key, cat in CATEGORIES.items():
        print(f"[{key}] {cat['name']}")
        
    choice = input("\nIngrese el número de la categoría: ").strip()
    
    if choice not in CATEGORIES:
        print("[-] Opción inválida. Ejecución finalizada.")
        return
        
    selected_category = CATEGORIES[choice]
    print(f"\n[+] Ha seleccionado: {selected_category['name']}")
    
    # Inicializar el conector RSS con la URL específica de la categoría seleccionada
    fetcher = RSSFetcher(source_name=selected_category['name'], endpoint_url=selected_category['url'])
    print(f"Conectando al feed de {fetcher.source_name}...")
    
    # Obtener el contenido crudo vía requests
    raw_rss_data = fetcher.fetch()
    
    if raw_rss_data:
        print(f"\n[+] ¡Conexión exitosa! Datos descargados ({len(raw_rss_data)} caracteres).")
        
        # Procesar y limpiar el contenido usando BeautifulSoup
        print("\n[+] Procesando y limpiando contenido del feed...")
        cleaned_output = TextCleaner.remove_ads_and_banners(raw_rss_data)
        
        print(f"\n--- CONTENIDO LIMPIO: {selected_category['name'].upper()} ---")
        print(cleaned_output[:800] + "...\n[Contenido truncado para visualización]")
        print("-------------------------------------------------------------")
    else:
        print("[-] No se pudieron obtener datos del feed RSS.")

    print("\nEjecución del main.py finalizada con éxito.")

if __name__ == "__main__":
    main()
