import streamlit as st
import feedparser
from fetchers.rss_fetcher import RSSFetcher
from cleaner.text_cleaner import TextCleaner

# Configuración de la página
st.set_page_config(
    page_title="Agregador de Noticias sin Anuncios",
    page_icon="📰",
    layout="wide"
)

# Diccionario optimizado con los mejores diarios globales de referencia por categoría (Feeds RSS directos)
CATEGORIES = {
    "Tecnología": {
        "TechCrunch": "https://techcrunch.com/feed/",
        "The Verge": "https://www.theverge.com/rss/index.xml",
        "Wired": "https://www.wired.com/feed/rss",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index"
    },
    "Finanzas y Economía": {
        "Financial Times": "https://www.ft.com/news-feed?format=rss",
        "CNBC Markets": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15838421",
        "MarketWatch": "https://feeds.marketwatch.com/marketwatch/topstories/"
    },
    "Política": {
        "BBC News (World)": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "Reuters": "https://www.reutersagency.com/feed/?best-regions=global&post_type=best",
        "The Guardian": "https://www.theguardian.com/world/rss"
    },
    "Espectáculos": {
        "Variety": "https://variety.com/feed/",
        "The Hollywood Reporter": "https://www.hollywoodreporter.com/feed/",
        "Deadline": "https://deadline.com/feed/"
    }
}

def main():
    st.title("📰 Agregador de Noticias sin Anuncios")
    st.markdown("Un espacio optimizado de alta velocidad para leer contenido global de referencia sin distracciones ni publicidad.")

    # Panel lateral para seleccionar la categoría y el diario específico
    st.sidebar.header("Panel de Navegación")
    selected_category = st.sidebar.selectbox("Seleccioná una categoría:", list(CATEGORIES.keys()))
    
    sources_dict = CATEGORIES[selected_category]
    selected_source_name = st.sidebar.selectbox("Seleccioná el medio/fuente:", list(sources_dict.keys()))

    feed_url = sources_dict[selected_source_name]

    # Botón para limpiar caché y actualizar
    if st.sidebar.button("Actualizar Feed"):
        st.cache_data.clear()

    # Instanciamos el conector RSS optimizado
    fetcher = RSSFetcher(source_name=selected_source_name, endpoint_url=feed_url)

    with st.spinner(f"Descargando y parseando feed de {selected_source_name}..."):
        raw_data = fetcher.fetch()

    if raw_data:
        # Usamos feedparser para estructurar las noticias en formato de tarjetas individuales
        feed = feedparser.parse(raw_data)
        
        st.success(f"¡Se encontraron {len(feed.entries)} artículos en {selected_source_name}!")
        st.markdown(f"### 📋 Artículos Recientes: {selected_source_name}")

        # Recorremos cada entrada del RSS y la mostramos como una tarjeta limpia
        for entry in feed.entries:
            title = getattr(entry, 'title', 'Sin título')
            published = getattr(entry, 'published', 'Fecha no disponible')
            link = getattr(entry, 'link', '#')
            summary_raw = getattr(entry, 'summary', getattr(entry, 'description', ''))
            
            # Limpiamos el resumen de HTML con nuestro TextCleaner
            clean_summary = TextCleaner.remove_ads_and_banners(summary_raw)

            with st.expander(f"📌 {title}"):
                st.caption(f"📅 Publicado: {published}")
                st.write(clean_summary if clean_summary else "No hay descripción disponible.")
                st.markdown(f"[Leer artículo completo en la fuente original]({link})", unsafe_allow_html=True)
    else:
        st.error(f"No se pudo conectar con el feed de {selected_source_name}. Verificá el enlace o tu conexión.")

if __name__ == "__main__":
    main()
