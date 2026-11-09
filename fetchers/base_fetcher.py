
class BaseFetcher:
    """
    Clase base para la extracción de noticias de múltiples fuentes.
    Garantiza una interfaz unificada para procesar RSS o APIs de diarios.
    """
    def __init__(self, source_name: str, endpoint_url: str):
        self.source_name = source_name
        self.endpoint_url = endpoint_url

    def fetch(self):
        """Método principal para obtener los datos crudos."""
        raise NotImplementedError("Las clases hijas deben implementar el método fetch().")

    def clean_content(self, raw_data):
        """Lógica genérica para limpiar banners, anuncios y elementos no deseados."""
        pass
