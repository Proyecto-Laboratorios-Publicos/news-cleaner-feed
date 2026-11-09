import re
from bs4 import BeautifulSoup

class TextCleaner:
    """
    Módulo encargado de limpiar el contenido de las noticias, eliminando etiquetas no deseadas, scripts, banners y publicidad.
    """
    
    @staticmethod
    def remove_ads_and_banners(raw_html: str) -> str:
        if not raw_html:
            return ""
            
        # Usamos BeautifulSoup para parsear el contenido XML/HTML de forma robusta
        soup = BeautifulSoup(raw_html, 'html.parser')
        
        # Eliminar etiquetas de scripts y estilos por completo
        for element in soup(["script", "style"]):
            element.decompose()
            
        # Extraer el texto plano ya limpio de tags y banners
        clean_text = soup.get_text()
        
        # Normalizar espacios en blanco y saltos de línea excesivos
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        return clean_text
