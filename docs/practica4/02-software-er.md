# Ejercicio 2, 3 y 4: Extensión del Software Interactivo y Validadores

## 1. Módulo de Conversión ER -> Autómata (Thompson)
* **Parser Sintáctico:** Analizador descendente recursivo que valida parentización y jerarquía de operadores ($+$, yuxtaposición, $*$)[cite: 7].
* **Generación Paso a Paso:** Construcción de autómatas parciales $\text{AFN}-\lambda$ hasta obtener el AFD mínimo mediante subconjuntos y Hopcroft[cite: 7].

## 2. Módulo de Conversión Autómata -> ER (Eliminación de Estados)
* **Importación JFLAP:** Carga directa de archivos `.jff`[cite: 8].
* **Simplificación Iterativa:** Reducción del autómata mediante eliminación de estados intermedios y actualización de expresiones en etiquetas[cite: 8].

## 3. Validadores de Sistema y Congruencia con `re`
* **Email:** Expresión regular simplificada para dominios de correo bajo norma RFC 5322.
* **Teléfono:** Validación de formato nacional a 10 dígitos (IFT México).
* **URL:** Validación de dominios HTTP bajo RFC 3986[cite: 9].
* **Prueba Masiva de Congruencia:** Se evaluaron 500+ cadenas generadas procedimentalmente, obteniendo una coincidencia exacta del 100% entre la simulación por autómatas y el motor `re` de Python en CI/CD[cite: 9].