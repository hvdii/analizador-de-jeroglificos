import cv2
import numpy as np
from skimage.measure import label

# Diccionario que relaciona cada jeroglífico con su número de espacios internos
diccionario_jeroglificos = {
    "A": 1,  # Ankh (Cruz egipcia)
    "J": 3,  # Wedjat (Ojo de Horus)
    "D": 5,  # Djed (Pilar de la estabilidad)
    "S": 4,  # Scarab (Escarabajo)
    "W": 0,  # Was (Cetro de poder)
    "K": 2,  # Akhet (Horizonte)
}


def decifrar_jeroglifico(mascara_jeroglifico):
    """
    Identifica un jeroglífico basado en el número de espacios internos que contiene.
    
    Args:
        mascara_jeroglifico (numpy.ndarray): Imagen binaria que representa el jeroglífico aislado
    
    Returns:
        str: Letra que representa el jeroglífico o None si no se encuentra coincidencia
    """
    # Invertir la máscara para detectar espacios internos (los blancos se convierten en negros y viceversa)
    mascara_invertida = cv2.bitwise_not(mascara_jeroglifico)
    
    # Etiquetar componentes conectados en la imagen invertida
    componentes_etiquetados = label(mascara_invertida > 0, connectivity=2)
    
    # Calcular espacios internos (excluyendo el fondo exterior)
    num_componentes = np.max(componentes_etiquetados)  # Número total de componentes
    espacios_internos = num_componentes - 1  # Restamos 1 para excluir el fondo
    
    # Buscar coincidencia en el diccionario
    for simbolo, cantidad_espacios in diccionario_jeroglificos.items():
        if cantidad_espacios == espacios_internos:
            return simbolo
    return None


def procesar_imagen(imagen_binaria):
    """
    Procesa una imagen binaria para identificar y decodificar todos los jeroglíficos presentes.
    
    Args:
        imagen_binaria (numpy.ndarray): Imagen binaria donde los jeroglíficos son regiones blancas
    
    Returns:
        str: Cadena concatenada con los jeroglíficos identificados, ordenados alfabéticamente
    """
    # Etiquetar componentes conectados en la imagen binaria
    imagen_etiquetada = label(imagen_binaria > 0, connectivity=2)
    total_jeroglificos = np.max(imagen_etiquetada)  # Número de jeroglíficos encontrados
    
    jeroglificos_detectados = []
    
    # Procesar cada jeroglífico individualmente
    for indice in range(1, total_jeroglificos + 1):
        # Crear máscara para el jeroglífico actual
        mascara_jeroglifico = np.where(imagen_etiquetada == indice, 255, 0).astype(np.uint8)
        
        # Decodificar el jeroglífico
        letra_jeroglifico = decifrar_jeroglifico(mascara_jeroglifico)
        if letra_jeroglifico:
            jeroglificos_detectados.append(letra_jeroglifico)
    
    # Ordenar alfabéticamente y generar cadena final
    jeroglificos_detectados.sort()
    return "".join(jeroglificos_detectados)


if __name__ == "__main__":
    # Procesar primera imagen de ejemplo
    archivo_entrada = "input/figura1.jpg"
    imagen_gris = cv2.imread(archivo_entrada, cv2.IMREAD_GRAYSCALE)
    _, imagen_binaria = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY_INV)
    
    resultado = procesar_imagen(imagen_binaria)
    print(resultado)
    
    # Procesar segunda imagen de ejemplo
    archivo_entrada = "input/figura2.png"
    imagen_gris = cv2.imread(archivo_entrada, cv2.IMREAD_GRAYSCALE)
    _, imagen_binaria = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY_INV)
    
    resultado = procesar_imagen(imagen_binaria)
    print(resultado)

    # Procesar tercera imagen de ejemplo
    archivo_entrada = "input/figura3.png"
    imagen_gris = cv2.imread(archivo_entrada, cv2.IMREAD_GRAYSCALE)
    _, imagen_binaria = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY_INV)
    
    resultado = procesar_imagen(imagen_binaria)
    print(resultado)