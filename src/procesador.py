import cv2
import numpy as np

class Procesador:
    """
    Clase responsable del procesamiento de imágenes para extraer características de los jeroglíficos.
    """
    
    def procesar_imagen(self, imagen_path):
        """
        Procesa una imagen para extraer características de los jeroglíficos.
        
        Args:
            imagen_path (str): Ruta de la imagen a procesar.
            
        Returns:
            list: Lista de diccionarios con características de cada jeroglífico encontrado.
        """
        # Leer imagen
        imagen = cv2.imread(imagen_path)
        if imagen is None:
            raise ValueError(f"No se pudo leer la imagen en {imagen_path}")
        
        # Preprocesamiento
        gris = self._convertir_a_grises(imagen)
        binaria = self._binarizar_imagen(gris)
        
        # Encontrar contornos
        contornos = self._encontrar_contornos(binaria)
        
        # Extraer características
        caracteristicas = []
        for contorno in contornos:
            mascara = self._crear_mascara(binaria.shape, contorno)
            caracteristicas.append(self._extraer_caracteristicas(mascara))
        
        return caracteristicas
    
    def _convertir_a_grises(self, imagen):
        """
        Convierte una imagen a escala de grises.
        
        Args:
            imagen (numpy.ndarray): Imagen en color BGR.
            
        Returns:
            numpy.ndarray: Imagen en escala de grises.
        """
        if len(imagen.shape) == 3 and imagen.shape[2] == 3:
            return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        return imagen
    
    def _binarizar_imagen(self, imagen_gris):
        """
        Binariza una imagen en escala de grises.
        
        Args:
            imagen_gris (numpy.ndarray): Imagen en escala de grises.
            
        Returns:
            numpy.ndarray: Imagen binarizada (blanco y negro).
        """
        _, binaria = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY_INV)
        return binaria
    
    def _encontrar_contornos(self, imagen_binaria):
        """
        Encuentra contornos en una imagen binarizada.
        
        Args:
            imagen_binaria (numpy.ndarray): Imagen binarizada.
            
        Returns:
            list: Lista de contornos encontrados.
        """
        contornos, _ = cv2.findContours(
            imagen_binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return [c for c in contornos if cv2.contourArea(c) > 10]  # Filtrar pequeños
    
    def _crear_mascara(self, shape, contorno):
        """
        Crea una máscara binaria para un contorno dado.
        
        Args:
            shape (tuple): Dimensiones de la imagen original.
            contorno (numpy.ndarray): Contorno del jeroglífico.
            
        Returns:
            numpy.ndarray: Máscara binaria del jeroglífico.
        """
        mascara = np.zeros(shape, dtype=np.uint8)
        cv2.drawContours(mascara, [contorno], -1, 255, thickness=cv2.FILLED)
        return mascara
    
    def _extraer_caracteristicas(self, mascara):
        """
        Extrae características topológicas de un jeroglífico.
        
        Args:
            mascara (numpy.ndarray): Máscara binaria del jeroglífico.
            
        Returns:
            dict: Diccionario con características del jeroglífico.
        """
        # Calcular número de agujeros (Euler number)
        contornos, _ = cv2.findContours(
            255 - mascara, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        num_agujeros = len(contornos) - 1 if contornos else 0
        
        # Calcular convexidad
        contorno_original = cv2.findContours(
            mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0][0]
        hull = cv2.convexHull(contorno_original, returnPoints=False)
        defects = cv2.convexityDefects(contorno_original, hull) if len(hull) > 3 else None
        
        return {
            'num_agujeros': num_agujeros,
            'defectos_convexidad': defects,
            'area': cv2.contourArea(contorno_original),
            'perimetro': cv2.arcLength(contorno_original, True)
        }