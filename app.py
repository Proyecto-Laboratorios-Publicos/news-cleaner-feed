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

# Diccionario maestro ampliado con los mejores diarios globales por categoría
CATEGORIES = {
    "Tecnología": {
        "TechCrunch": "https://techcrunch.com/feed/",
        "The Verge": "https://www.theverge.com/rss/index.xml",
        "Wired": "https://www.wired.com/feed/rss",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index"
    },
    "Finanzas y Economía": {
        "CNBC Markets": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15838421",
        "Business Insider (Markets)": "https://markets.businessinsider.com/rss/news"
    },
    "Política": {
        "BBC News (World)": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "The Guardian": "https://www.theguardian.com/world/rss",
        "Al Jazeera English": "https://www.aljazeera.com/xml/rss/all.xml",
        "France 24": "https://www.france24.com/en/rss",
        "UN News": "https://news.un.org/feed/subscribe/en/news/all/rss.xml",
        "Euronews": "https://www.euronews.com/rss?format=mrss",
        "The Conversation": "https://theconversation.com/global/articles.atom",
        "RFI": "https://www.rfi.fr/en/rss",
        "The Diplomat": "https://thediplomat.com/feed/"
    },
    "Espectáculos": {
        "Variety": "https://variety.com/feed/",
        "The Hollywood Reporter": "https://www.hollywoodreporter.com/feed/",
        "Deadline": "https://deadline.com/feed/",
        "Rolling Stone": "https://www.rollingstone.com/feed/",
        "IndieWire": "https://www.indiewire.com/feed/",
        "Collider": "https://collider.com/feed/",
        "Billboard": "https://www.billboard.com/feed/",
        "E! Online": "https://www.eonline.com/syndication/feeds/rss/topstories.xml"
    },
    "Ciencia y Salud": {
        "Nature": "https://www.nature.com/nature.rss",
        "Live Science": "https://www.livescience.com/feeds/all",
        "New Scientist": "https://www.newscientist.com/feed/home/",
        "Scientific American": "https://rss.sciam.com/ScientificAmerican-Global",
        "MIT Technology Review": "https://www.technologyreview.com/feed/",
        "ScienceDaily": "https://www.sciencedaily.com/rss/top/science.xml",
        "Phys.org": "https://phys.org/rss-feed/",
        "EurekAlert!": "https://www.eurekalert.org/rss/technology_engineering.xml"
    },
    "Deportes": {
        "BBC Sport": "https://feeds.bbci.co.uk/sport/rss.xml",
        "Marca": "https://e00-marca.uecdn.es/rss/portada.xml",
    },
    "Cultura": {
        "The Guardian (Culture)": "https://www.theguardian.com/culture/rss",
        "Smithsonian Magazine": "https://www.smithsonianmag.com/rss/arts-culture/",
        "Hyperallergic": "https://hyperallergic.com/feed/",
        "ARTnews": "https://www.artnews.com/feed/",
        "Open Culture": "https://www.openculture.com/feed",
    },
    "Videojuegos / Gaming": {
        "IGN": "https://feeds.ign.com/ign/all",
        "Polygon": "https://www.polygon.com/rss/index.xml",
        "PC Gamer": "https://www.pcgamer.com/rss/",
        "Eurogamer": "https://www.eurogamer.net/feed",
        "Kotaku": "https://kotaku.com/rss",
        "Destructoid": "https://www.destructoid.com/feed/",
    }
}

@st.cache_data(ttl=3600)
def fetch_full_article(url: str):
    """
    Función optimizada para extraer la imagen principal y una lista ordenada 
    de párrafos limpios del artículo de origen.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Compatible; NewsCleanerBot/1.0)'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return [], []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Eliminar elementos molestos comunes
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "iframe", "noscript"]):
            tag.decompose()

        # Extraer la imagen principal
        images = []
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            images.append(og_image["content"])
        else:
            img_tag = soup.find("img")
            if img_tag and img_tag.get("src"):
                images.append(img_tag["src"])

        # Recolectar párrafos conservando la estructura individual
        paragraphs = soup.find_all('p')
        clean_paragraphs = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 40:
                cleaned_p = TextCleaner.remove_ads_and_banners(text)
                if cleaned_p:
                    clean_paragraphs.append(cleaned_p)

        return clean_paragraphs, images

    except Exception as e:
        return [], []

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
                
                # Botón para cargar el artículo completo formateado en párrafos
                if st.button(f"📥 Cargar artículo completo", key=link):
                    with st.spinner("Extrayendo texto completo e imágenes..."):
                        paragraphs_list, images = fetch_full_article(link)
                        
                        # Mostrar la imagen principal si se encontró
                        for img_url in images:
                            try:
                                st.image(img_url, use_column_width=True)
                            except Exception:
                                pass

                        # Renderizar cada párrafo por separado para mantener el formato visual
                        if paragraphs_list:
                            for p in paragraphs_list:
                                st.write(p)
                        else:
                            st.write(clean_summary)
                else:
                    st.write(clean_summary if clean_summary else "Hacé clic en 'Cargar artículo completo' para ver el desarrollo.")

                st.markdown(f"[Leer artículo en la fuente original]({link})", unsafe_allow_html=True)
    else:
        st.error(f"No se pudo conectar con el feed de {selected_source_name}. Verificá el enlace o tu conexión.")

if __name__ == "__main__":
    main()
