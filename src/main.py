import os
import cv2
from procesador import Procesador
from clasificador import Clasificador

class AnalizadorJeroglificos:
    """
    Clase principal que coordina el procesamiento y clasificación de imágenes con jeroglíficos.
    """
    
    def __init__(self, input_dir='input', output_dir='output'):
        """
        Inicializa el analizador con los directorios de entrada y salida.
        
        Args:
            input_dir (str): Directorio donde se encuentran las imágenes a procesar.
            output_dir (str): Directorio donde se guardarán los resultados.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.procesador = Procesador()
        self.clasificador = Clasificador()
        
        # Crear directorios si no existen
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def procesar_imagenes(self):
        """
        Procesa todas las imágenes válidas en el directorio de entrada y genera los resultados.
        """
        resultados = {}
        
        # Obtener lista de imágenes válidas
        imagenes = [f for f in os.listdir(self.input_dir) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not imagenes:
            print(f"No se encontraron imágenes válidas en {self.input_dir}")
            return
        
        print(f"Procesando {len(imagenes)} imagen(es)...")
        
        for imagen_nombre in imagenes:
            imagen_path = os.path.join(self.input_dir, imagen_nombre)
            
            try:
                # Procesar imagen
                caracteristicas = self.procesador.procesar_imagen(imagen_path)
                
                # Clasificar jeroglíficos
                letras = self.clasificador.clasificar(caracteristicas)
                
                # Ordenar alfabéticamente y guardar resultado
                letras_ordenadas = sorted(letras)
                resultados[imagen_nombre] = ''.join(letras_ordenadas)
                
                print(f"{imagen_nombre}: {len(letras)} jeroglíficos encontrados")
                
            except Exception as e:
                print(f"Error al procesar {imagen_nombre}: {str(e)}")
                continue
        
        # Guardar resultados en archivo
        self._guardar_resultados(resultados)
    
    def _guardar_resultados(self, resultados):
        """
        Guarda los resultados en un archivo de texto en el directorio de salida.
        
        Args:
            resultados (dict): Diccionario con los resultados por imagen.
        """
        output_path = os.path.join(self.output_dir, 'resultados.txt')
        
        with open(output_path, 'w') as f:
            for imagen, letras in resultados.items():
                f.write(f"{imagen}: {letras}\n")
        
        print(f"Resultados guardados en {output_path}")

if __name__ == "__main__":
    analizador = AnalizadorJeroglificos()
    analizador.procesar_imagenes()