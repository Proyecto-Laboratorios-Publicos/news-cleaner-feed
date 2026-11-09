import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup
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

@st.cache_data(ttl=3600)
def fetch_full_article(url: str):
    """
    Función optimizada con caché para realizar scraping bajo demanda del artículo completo
    y extraer su texto principal e imágenes al expandir la noticia.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Compatible; NewsCleanerBot/1.0)'}
        response = requests.get(url, headers=headers, timeout=8)
        if response.status_code != 200:
            return "", []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Eliminar elementos molestos comunes (anuncios, navegación, scripts, footers)
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
            tag.decompose()

        # Intentar extraer la imagen principal de la noticia
        images = []
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            images.append(og_image["content"])
        else:
            # Buscar la primera imagen relevante dentro del contenido
            img_tag = soup.find("img")
            if img_tag and img_tag.get("src"):
                images.append(img_tag["src"])

        # Intentar aislar el cuerpo principal del artículo para no traer ruido
        article_body = soup.find("article") or soup.find("div", class_=lambda x: x and ('content' in x.lower() or 'body' in x.lower()))
        
        if article_body:
            paragraphs = article_body.find_all(['p', 'h2', 'h3'])
        else:
            paragraphs = soup.find_all(['p', 'h2', 'h3'])

        full_text = "\n\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30])
        
        # Limpieza final de anuncios y banners
        clean_text = TextCleaner.remove_ads_and_banners(full_text)
        return clean_text, images

    except Exception as e:
        return "", []

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

    with st.spinner(f"Cargando artículos de {selected_source_name}..."):
        raw_data = fetcher.fetch()

    if raw_data:
        feed = feedparser.parse(raw_data)
        
        st.markdown(f"### 📋 Artículos Recientes: {selected_source_name}")

        for entry in feed.entries:
            title = getattr(entry, 'title', 'Sin título')
            published = getattr(entry, 'published', 'Fecha no disponible')
            link = getattr(entry, 'link', '#')
            summary = getattr(entry, 'summary', getattr(entry, 'description', ''))
            
            clean_summary = TextCleaner.remove_ads_and_banners(summary)

            with st.expander(f"📌 {title}"):
                st.caption(f"📅 Publicado: {published}")
                
                # Mostramos un botón o cargamos el contenido completo al abrir
                if st.button(f"📥 Cargar artículo completo", key=link):
                    with st.spinner("Extrayendo texto completo e imágenes..."):
                        full_text, images = fetch_full_article(link)
                        
                        # Mostrar imágenes si se encontraron
                        for img_url in images:
                            try:
                                st.image(img_url, use_column_width=True)
                            except Exception:
                                pass

                        if full_text:
                            st.write(full_text)
                        else:
                            st.write(clean_summary)
                else:
                    st.write(clean_summary if clean_summary else "Hacé clic en 'Cargar artículo completo' para ver el desarrollo.")

                st.markdown(f"[Leer artículo en la fuente original]({link})", unsafe_allow_html=True)
    else:
        st.error(f"No se pudo conectar con el feed de {selected_source_name}. Verificá el enlace o tu conexión.")

if __name__ == "__main__":
    main()
