# Conclusiones Generales

A lo largo del desarrollo de las Prácticas 3 y 4 de Teoría de la Computación, se lograron integrar exitosamente los algoritmos fundamentales de la teoría de autómatas y lenguajes formales:

1. **Equivalencia de Modelos:** Se demostró de manera práctica el Teorema de Kleene mediante la Construcción de Thompson ($\text{ER} \to \text{AFN}-\lambda$), la Construcción de Subconjuntos ($\text{AFN}-\lambda \to \text{AFD}$), el Algoritmo de Hopcroft (Minimización) y el Método de Eliminación de Estados ($\text{AFD} \to \text{ER}$).
2. **Congruencia y Validación:** Se verificó la consistencia del motor de autómatas desarrollado frente al motor estándar `re` de Python mediante una suite masiva de más de 500 cadenas de prueba en integración continua (Docker / Pytest), obteniendo un 100% de coincidencia.
3. **Aplicación Práctica:** La implementación de validadores de uso cotidiano (correos, teléfonos y URLs) demuestra la relevancia teórica y computacional de las expresiones regulares en el desarrollo de software actual.
