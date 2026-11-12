# Simulación de mitosis en Python (`mitosis.py`)

Programa sencillo en **Python 3** que muestra una simulación gráfica de la **mitosis** de dos células iniciales. La animación representa, de forma didáctica, las etapas principales del proceso hasta obtener cuatro células hijas.

## Descripción

- **Células iniciales:** 2
- **Células finales:** 4 (cada célula madre se divide en dos)
- **Interfaz:** ventana gráfica con animación en `tkinter`
- **Etapas representadas:**
  1. **Interfase**: la célula crece y duplica su ADN; el núcleo es visible.
  2. **Profase**: la cromatina se condensa en cromosomas y el núcleo se desorganiza.
  3. **Metafase**: los cromosomas se alinean en el ecuador de la célula.
  4. **Anafase**: las cromátidas hermanas se separan hacia polos opuestos.
  5. **Telofase**: se forman dos núcleos y los cromosomas se descondensan.
  6. **Citocinesis**: el citoplasma se divide y se originan las células hijas.

> Nota: es una simulación simplificada con fines educativos/ilustrativos, no un modelo biológico detallado.

## Requisitos

- **Python 3.x**
- **Tkinter** (incluido normalmente en las instalaciones estándar de Python)

En algunas distribuciones Linux puede ser necesario instalar Tkinter por separado, por ejemplo:

```bash
# Debian/Ubuntu
sudo apt-get install python3-tk
```

## Uso

1. Clona o descarga este repositorio.
2. Abre una terminal en el directorio del proyecto.
3. Ejecuta:

```bash
python3 mitosis.py
```

También puedes darle permisos de ejecución y lanzarlo directamente (opcional):

```bash
chmod +x mitosis.py
./mitosis.py
```

## Controles

- **Reiniciar**: botón en la parte inferior de la ventana para volver a ejecutar la simulación desde el inicio.

## Archivos del proyecto

- `mitosis.py`: código fuente de la simulación.
- `README.md`: información y guía de uso del programa.
- `.gitignore`: exclusiones comunes de Python (por ejemplo, `__pycache__/`).
