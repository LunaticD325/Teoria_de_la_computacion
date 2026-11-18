# Ejercicio 1: Forma Normal de Chomsky (FNC) y Algoritmo CYK

## 1. Definición Formal
Una Gramática Libre de Contexto $G = (V, \Sigma, R, S)$ se encuentra en **Forma Normal de Chomsky (FNC)** si todas sus reglas de producción tienen exclusivamente una de las siguientes dos formas:
* $A \to BC$, donde $A, B, C \in V$ y $B, C \notin \{S\}$.
* $A \to a$, donde $A \in V$ y $a \in \Sigma$.
* Se permite $S \to \lambda$ únicamente si $\lambda \in L(G)$ y $S$ no aparece en el lado derecho de ninguna producción.

---

## 2. Ejercicio 341 (Lista 5)
* **Archivos JFLAP:** `gramaticas/practica5/ej341_original.jff` y `gramaticas/practica5/ej341_fnc.jff`
* **Procedimiento de transformación aplicado:**
  1. Verificación de Gramática Independiente del Contexto mediante `Test for Grammar Type`.
  2. Eliminación de producciones anulables ($\lambda$), producciones unitarias ($A \to B$) y símbolos inaccesibles o no generadores.
  3. Sustitución de terminales en producciones de longitud $\ge 2$ por nuevas variables auxiliares $T_a \to a$ y binarización de lados derechos con más de dos variables.
* **Validación de equivalencia y análisis sintáctico:**
  * Equivalencia verificada con `Multiple Brute Force Parse` sobre 5 cadenas aceptadas y 5 rechazadas.
  * Árbol de derivación en tiempo polinómico $O(n^3)$ generado mediante `CYK Parse`.

---

## 3. Ejercicio 343 (Lista 5)
* **Archivos JFLAP:** `gramaticas/practica5/ej343_original.jff` y `gramaticas/practica5/ej343_fnc.jff`
* **Procedimiento de transformación aplicado:**
  1. Verificación de Gramática Independiente del Contexto mediante `Test for Grammar Type`.
  2. Eliminación de producciones $\lambda$, unitarias y símbolos inútiles.
  3. Binarización estricta de todas las reglas de producción hacia FNC.
* **Validación de equivalencia y análisis sintáctico:**
  * Equivalencia verificada con `Multiple Brute Force Parse` sobre 5 cadenas aceptadas y 5 rechazadas.
  * Análisis sintáctico ascendente ejecutado mediante `CYK Parse`.

---

## 4. Gramática Propia (Expresiones Aritméticas Balanceadas)
* **Archivos JFLAP:** `gramaticas/practica5/propia_original.jff` y `gramaticas/practica5/propia_fnc.jff`
* **Gramática Original $G_1$:**
  $$S \to S + T \mid T$$
  $$T \to T * F \mid F$$
  $$F \to (S) \mid a$$
* **Gramática Equivalente en FNC $G_1'$:**
  $$S \to S A_1 \mid T A_2 \mid L A_3 \mid a$$
  $$T \to T A_2 \mid L A_3 \mid a$$
  $$F \to L A_3 \mid a$$
  $$A_1 \to P S, \quad A_2 \to M T, \quad A_3 \to S R$$
  $$P \to +, \quad M \to *, \quad L \to (, \quad R \to )$$
* **Validación:** Equivalencia comprobada entre $G_1$ y $G_1'$ con `Multiple Brute Force Parse` y derivación de cadenas como `(a+a)*a` verificada mediante `CYK Parse`.