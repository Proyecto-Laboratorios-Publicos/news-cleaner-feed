import streamlit as st
from fetchers.rss_fetcher import RSSFetcher
from cleaner.text_cleaner import TextCleaner

# Configuración de la página
st.set_page_config(
    page_title="Agregador de Noticias sin Anuncios",
    page_icon="📰",
    layout="wide"
)

# Diccionario maestro de categorías y feeds RSS
CATEGORIES = {
    "Tecnología": {
        "url": "https://news.google.com/rss/search?q=tecnologia&hl=es-419&gl=AR&ceid=AR:es-419"
    },
    "Finanzas y Economía": {
        "url": "https://news.google.com/rss/search?q=economia+finanzas&hl=es-419&gl=AR&ceid=AR:es-419"
    },
    "Política": {
        "url": "https://news.google.com/rss/search?q=politica+argentina&hl=es-419&gl=AR&ceid=AR:es-419"
    },
    "Espectáculos": {
        "url": "https://news.google.com/rss/search?q=espectaculos+cine+musica&hl=es-419&gl=AR&ceid=AR:es-419"
    }
}

def main():
    st.title("📰 Agregador de Noticias sin Anuncios")
    st.markdown("Un espacio limpio para leer contenido actualizado sin distracciones, banners ni publicidad.")

    # Panel lateral para seleccionar la categoría
    st.sidebar.header("Panel de Navegación")
    selected_category = st.sidebar.radio("Seleccioná una categoría:", list(CATEGORIES.keys()))

    # Botón para actualizar / consultar el feed
    if st.sidebar.button("Actualizar Feed"):
        st.cache_data.clear()

    feed_url = CATEGORIES[selected_category]["url"]

    # Instanciamos el conector que ya tenemos probado
    fetcher = RSSFetcher(source_name=selected_category, endpoint_url=feed_url)

    with st.spinner(f"Conectando y descargando noticias de {selected_category}..."):
        raw_data = fetcher.fetch()

    if raw_data:
        # Limpiamos el contenido utilizando nuestra clase robusta con BeautifulSoup
        cleaned_content = TextCleaner.remove_ads_and_banners(raw_data)

        st.success(f"¡Contenido de {selected_category} obtenido y optimizado con éxito!")
        
        st.markdown("### 📋 Vista Limpia del Feed")
        
        # Mostramos el contenido limpio en un contenedor expandible o caja de texto estilizada
        st.text_area("Contenido procesado:", cleaned_content, height=450)
    else:
        st.error("No se pudo conectar con el feed RSS seleccionado. Verificá tu conexión a internet.")

if __name__ == "__main__":
    main()
