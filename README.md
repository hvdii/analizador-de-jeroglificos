# Decodificador de Jeroglíficos Egipcios

Este programa identifica y decodifica jeroglíficos egipcios basándose en el número de espacios internos que contienen.

## Requisitos
- Python 3.6+
- OpenCV (cv2)
- NumPy
- scikit-image

## Instalación
1. Clona el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_REPOSITORIO]
```

2. (Opcional) Crea entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. Instala dependencias:
```bash
pip install opencv-python numpy scikit-image
```

## Uso
1. Ejecutar:
```bash
python main.py
```

## Agregar más imágenes
1. Añade imágenes (JPG/PNG) a `input/`
2. Edita `main.py` agregando:
```python
archivo_entrada = "input/nueva_imagen.jpg"
imagen_gris = cv2.imread(archivo_entrada, cv2.IMREAD_GRAYSCALE)
_, imagen_binaria = cv2.threshold(imagen_gris, 127, 255, cv2.THRESH_BINARY_INV)
resultado = procesar_imagen(imagen_binaria)
print(resultado)
```