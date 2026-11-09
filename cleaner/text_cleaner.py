import re
from bs4ounded import BeautifulSoup if 'BeautifulSoup' in globals() else None

class TextCleaner:
    """
    Módulo encargado de limpiar el contenido de las noticias,
    eliminando etiquetas no deseadas, scripts, banners y publicidad.
    """
    @staticmethod
    def remove_ads_and_banners(raw_html: str) -> str:
        if not raw_html:
            return ""
        
        # Limpieza básica de etiquetas usando expresiones regulares 
        # (o BeautifulSoup si se agrega en las dependencias)
        clean_text = re.sub(r'<script.*?</script>', '', raw_html, flags=re.DOTALL)
        clean_text = re.sub(r'<style.*?</style>', '', clean_text, flags=re.DOTALL)
        
        # Remover tags HTML genéricos para dejar texto plano legible
        clean_text = re.sub(r'<[^>]+>', '', clean_text)
        
        # Normalizar espacios en blanco y saltos de línea excesivos
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        return clean_text
