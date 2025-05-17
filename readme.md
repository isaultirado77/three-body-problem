# Simulación del Problema de los Tres Cuerpos – Punto L4

Este proyecto simula un sistema de tres cuerpos (Tierra, Luna y un asteroide) con el objetivo de estudiar la estabilidad alrededor del punto de Lagrange L4. Se integran las ecuaciones de movimiento y se generan animaciones, gráficos de trayectoria, energía, momento angular y espacio fase.

## Análisis y Resultados

Los resultados están disponibles en el siguiente notebook:

- `three_body_analysis.ipynb` [![Ver Análisis en Jupyter](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/isaultirado77/three-body-problem/blob/main/three_body_analysis.ipynb)

## Ejecución de la Simulación

### 1. Generar datos:

```bash
python three_body_system.py
```

### 2. Animar resultados:

```bash
python animate.py
```

### 3. Visualizar análisis (opcional):

```bash
jupyter notebook three_body_analysis.ipynb
```

## Requisitos

* **Python 3.7+**
* Instalar dependencias:

  ```bash
  pip install numpy matplotlib
  ```

---

¿Deseas que genere también el badge de GitHub Actions o colab para autoabrir el notebook?
