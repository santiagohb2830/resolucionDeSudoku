# Proyecto IA – Resolución de Sudoku con Restricciones Adicionales

## Descripción general

Este proyecto implementa un **agente inteligente basado en búsqueda con restricciones (CSP)** para resolver tableros de **Sudoku** clásicos y una **versión extendida** que incorpora **nuevas restricciones**. El propósito es aplicar técnicas de resolución sistemática, mostrando cómo los algoritmos de Inteligencia Artificial pueden adaptarse a problemas combinatorios complejos.

El programa está desarrollado en **Python** y utiliza **búsqueda con retroceso (backtracking)**, combinada con **verificación de restricciones** y **propagación de consistencia**.

---

## Objetivos del proyecto

* Representar el Sudoku como un **problema de satisfacción de restricciones (CSP)**.
* Implementar un **algoritmo de búsqueda con retroceso** eficiente.
* Integrar una **nueva restricción adicional** que complemente las reglas clásicas del Sudoku.
* Analizar el comportamiento del algoritmo ante distintos tableros.

---

## Marco teórico resumido

El Sudoku se modela como un **CSP (Constraint Satisfaction Problem)**, donde:

* **Variables:** cada celda del tablero.
* **Dominios:** los posibles valores (1–9).
* **Restricciones:**

  * No repetir números en filas.
  * No repetir números en columnas.
  * No repetir números en subcuadrantes 3×3.
  * **Restricción adicional:** definida en este proyecto (por ejemplo, diagonales, regiones coloreadas, o sumas específicas entre celdas).

El algoritmo de resolución combina:

* **Selección de variables no asignadas.**
* **Prueba de valores válidos (consistencia local).**
* **Retroceso** cuando no existen opciones válidas.

---

## Estructura del proyecto

```
SudokuIA
├── Sudoku con nueva restriccion.py   # Código principal del proyecto
└── Documentación Segundo Proyecto.pdf # Informe explicativo del desarrollo
```

---


### Comando de ejecución

```bash
python3 "Sudoku con nueva restriccion.py"
```

El programa muestra:

* El **tablero inicial** (con ceros o espacios vacíos).
* El **proceso de resolución** (si está habilitado).
* El **tablero final completo**, validado con todas las restricciones.

---

## Ejemplo de entrada

```python
sudoku = [
    [0, 0, 3, 0, 2, 0, 6, 0, 0],
    [9, 0, 0, 3, 0, 5, 0, 0, 1],
    [0, 0, 1, 8, 0, 6, 4, 0, 0],
    [0, 0, 8, 1, 0, 2, 9, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 8],
    [0, 0, 6, 7, 0, 8, 2, 0, 0],
    [0, 0, 2, 6, 0, 9, 5, 0, 0],
    [8, 0, 0, 2, 0, 3, 0, 0, 9],
    [0, 0, 5, 0, 1, 0, 3, 0, 0]
]
```

El código procesa el tablero, aplica las restricciones y devuelve la solución completa.

---

## Lógica del algoritmo

1. Buscar una **celda vacía**.
2. Probar valores del 1 al 9.
3. Verificar si el valor cumple todas las restricciones:

   * Fila, columna, cuadrante, y restricción adicional.
4. Si cumple, asignarlo y continuar con la siguiente celda.
5. Si ninguna opción es válida, retroceder (backtrack).
6. Terminar cuando el tablero esté completo o no exista solución.

---

## Restricción adicional

Dependiendo de la versión, la nueva regla puede ser:

* **Diagonal:** los números en las diagonales principales no se repiten.
* **Killer Sudoku:** las sumas dentro de regiones deben igualar un valor específico.
* **Sudoku en cruz:** el centro debe cumplir restricciones de simetría.

(El detalle exacto se explica en el documento PDF adjunto.)

---

## Resultados y análisis

* El algoritmo resolvió correctamente los tableros de prueba.
* El tiempo de ejecución varía según el número de celdas vacías y la nueva restricción.
* Se demuestra que el enfoque de **búsqueda con retroceso + restricciones** es efectivo para resolver CSP pequeños.

---

## Mejoras futuras

* Implementar **heurísticas MRV** (Minimum Remaining Values) para elegir celdas más restrictivas.
* Incorporar **propagación de restricciones** (Forward Checking, AC-3).
* Crear una interfaz gráfica para visualizar el proceso.

---

## Autor

**Santiago Hernández Barbosa**
Pontificia Universidad Javeriana
Curso: *Introducción a Inteligencia Artificial*
Profesor: Julio Omar Palacio Niño
Octubre 2025

---

## Referencias

* Russell & Norvig, *Artificial Intelligence: A Modern Approach*.
* Apuntes de clase – Introducción a IA (Pontificia Universidad Javeriana).
* Documentación oficial de Python (`itertools`, `copy`).
