# Ejercicio 3: Visualización de Autómatas y Simulación Gráfica en Flet

**Autor:** Garduño Ibarra Uriel  
**Grupo:** 4CM2  

---

## 1. Arquitectura Modular (Separación Cálculo vs. Renderizado)
Para cumplir con las pruebas automatizadas y mantener el código limpio en Python puro:
* **`src/visualizer_core.py`:** Contiene `AutomatonLayout` (cálculo geométrico de coordenadas únicas $(x,y)$ y control de movimiento) y `StepSimulator` (traza paso a paso con cerradura $\lambda$, estados activos y transiciones disparadas).
* **`src/canvas_drawer.py`:** Implementa `AutomatonVisualizerWidget` directamente sobre `flet.canvas.Canvas` y `flet.GestureDetector` sin librerías externas de grafos.

## 2. Características Visuales Implementadas
1. **Soporte Universal:** Dibuja cualquier **AFD, AFN o AFN-$\lambda$** cargado desde `.jff` o generado desde las conversiones de las Prácticas 3 y 4 (mostrando en paralelo el autómata original y el convertido).
2. **Elementos Gráficos:**
   * **Estado inicial:** Flecha entrante en color cian.
   * **Estados de aceptación:** Doble círculo concéntrico.
   * **Auto-ciclos ($q \to q$):** Curva Bézier cúbica superior con etiqueta centrada.
   * **Transiciones bidireccionales ($p \to q$ y $q \to p$):** Curvas Bézier cuadráticas separadas perpendicularmente para evitar superposición de flechas y etiquetas.
3. **Interactividad (Drag & Drop):** Permite arrastrar cualquier estado con el ratón recalibrando todas sus aristas en tiempo real.
4. **Simulación Paso a Paso:**
   * Controles de navegación (`Cargar cadena`, `Anterior`, `Siguiente`, `Reiniciar`).
   * Iluminación en ámbar/dorado del estado actual (o conjunto de estados activos en AFN/AFN-$\lambda$) y de las transiciones utilizadas.
   * Visualización del prefijo leído, cadena restante y veredicto final (`ACEPTADA` / `RECHAZADA`).

## 3. Evidencia del Software en Funcionamiento
* ![Visualizador Flet Práctica 5](../../evidencias/practica5/visualizador_flet.png) *(Colocar captura de pantalla de la app Flet dibujando un autómata)*