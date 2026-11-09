
import requests
from fetchers.base_fetcher import BaseFetcher

class RSSFetcher(BaseFetcher):
    """
    Conector especializado para extraer feeds RSS de noticias utilizando requests.
    Hereda de BaseFetcher para cumplir con la interfaz unificada.
    """
    
    def __init__(self, source_name: str, endpoint_url: str):
        super().__init__(source_name, endpoint_url)

    def fetch(self) -> str:
        """
        Realiza una petición HTTP GET al endpoint RSS y devuelve el contenido crudo (XML/HTML).
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Compatible; NewsCleanerBot/1.0)'}
            response = requests.get(self.endpoint_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"[-] Error al conectar con {self.source_name} ({self.endpoint_url}): {e}")
            return ""

    def clean_content(self, raw_data: str) -> str:
        """
        Implementación específica de limpieza si se requiere un filtrado previo a nivel de conector.
        """
        return raw_data
