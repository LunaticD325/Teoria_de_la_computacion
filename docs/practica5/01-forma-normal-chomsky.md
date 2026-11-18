# Ejercicio 1: Forma Normal de Chomsky (FNC) con JFLAP

**Autor:** Garduño Ibarra Uriel  
**Boleta:** 2024630286  
**Grupo:** 4CM2  

---

## 1. Gramática Propia (Con Producciones $\lambda$, Unitarias y Símbolos Inútiles)

### 1.1 Definición Original $G = (V, \Sigma, R, S)$
* **Variables ($V$):** $\{S, A, B, C, D\}$
* **Terminales ($\Sigma$):** $\{a, b\}$
* **Símbolo Inicial:** $S$
* **Producciones ($R$):**
  $$S \to A B \mid C$$
  $$A \to a A \mid \lambda$$
  $$B \to b B \mid b$$
  $$C \to a b$$
  $$D \to a D b$$

> **Nota de diseño:** Esta gramática contiene la producción anulable $A \to \lambda$, la producción unitaria $S \to C$, el símbolo no alcanzable $D$ y cumple con ser Independiente del Contexto (Tipo 2) al verificarla con *Test for Grammar Type* en JFLAP.

### 1.2 Etapas de Transformación (`Convert -> Transform Grammar`)

1. **Eliminación de Producciones $\lambda$:**
   * Conjunto de variables anulables: $N = \{A\}$.
   * Al sustituir $A \to \lambda$ en $S \to AB$ y $A \to aA$:
     $$S \to A B \mid B \mid C$$
     $$A \to a A \mid a$$
     $$B \to b B \mid b$$
     $$C \to a b$$
     $$D \to a D b$$

2. **Eliminación de Producciones Unitarias:**
   * Pares unitarios detectados: $(S, B)$ y $(S, C)$.
   * Reemplazando las producciones de $B$ y $C$ directamente en $S$:
     $$S \to A B \mid b B \mid b \mid a b$$
     $$A \to a A \mid a$$
     $$B \to b B \mid b$$
     $$C \to a b$$
     $$D \to a D b$$

3. **Eliminación de Símbolos Inútiles (No generadores y no alcanzables):**
   * $D$ no genera cadenas terminales ni es alcanzable desde $S$; $C$ deja de ser alcanzable tras eliminar $S \to C$.
   * Gramática limpia resultante:
     $$S \to A B \mid b B \mid b \mid a b$$
     $$A \to a A \mid a$$
     $$B \to b B \mid b$$

4. **Paso a Forma Normal de Chomsky ($A \to BC$ o $A \to a$):**
   * Introduciendo variables auxiliares para terminales en producciones de longitud $\ge 2$: $T_a \to a$, $T_b \to b$.
   * **Gramática Final en FNC:**
     $$S \to A B \mid T_b B \mid T_a T_b \mid b$$
     $$A \to T_a A \mid a$$
     $$B \to T_b B \mid b$$
     $$T_a \to a, \quad T_b \to b$$

### 1.3 Validación y Árbol CYK en JFLAP (Gramática Propia)
* **Archivos JFLAP:** `gramaticas/practica5/propia_original.jff` y `gramaticas/practica5/propia_fnc.jff`.
* **Pruebas de Equivalencia (`Multiple Brute Force Parse`):**
  * **5 Cadenas Aceptadas:** `b`, `ab`, `bb`, `aab`, `abb` (Aceptadas tanto en original como en FNC).
  * **5 Cadenas Rechazadas:** `λ`, `a`, `ba`, `aba`, `baa` (Rechazadas en ambas).
* **Evidencia CYK Parse:**
  * ![CYK Gramática Propia](../../evidencias/practica5/propia_cyk.png) *(Colocar captura de CYK Parse aquí)*

---

## 2. Ejercicio 341 (Lista 5)

* **Archivos JFLAP:** `gramaticas/practica5/ej341_original.jff` y `gramaticas/practica5/ej341_fnc.jff`.
* **Etapas en JFLAP (`Transform Grammar`):**
  1. Verificación de Gramática Independiente del Contexto (*Test for Grammar Type*).
  2. Eliminación de producciones $\lambda$, unitarias y símbolos inútiles.
  3. Conversión final a FNC.
* **Pruebas de Equivalencia (5 aceptadas / 5 rechazadas):**
  * ![Multiple Brute Force 341](../../evidencias/practica5/ej341_mbf.png) *(Adjuntar captura de tabla de pruebas)*
* **Análisis CYK Parse:**
  * ![CYK 341](../../evidencias/practica5/ej341_cyk.png) *(Adjuntar captura del árbol de derivación)*

---

## 3. Ejercicio 343 (Lista 5)

* **Archivos JFLAP:** `gramaticas/practica5/ej343_original.jff` y `gramaticas/practica5/ej343_fnc.jff`.
* **Etapas en JFLAP (`Transform Grammar`):**
  1. Verificación de Gramática Independiente del Contexto (*Test for Grammar Type*).
  2. Eliminación de producciones $\lambda$, unitarias y símbolos inútiles.
  3. Conversión final a FNC.
* **Pruebas de Equivalencia (5 aceptadas / 5 rechazadas):**
  * ![Multiple Brute Force 343](../../evidencias/practica5/ej343_mbf.png) *(Adjuntar captura de tabla de pruebas)*
* **Análisis CYK Parse:**
  * ![CYK 343](../../evidencias/practica5/ej343_cyk.png) *(Adjuntar captura del árbol de derivación)*

---

## 4. ¿Qué ocurre con la cadena vacía ($\lambda$) en la Forma Normal de Chomsky?

Por definición estricta (Hopcroft, Motwani & Ullman, 2007, Sección 7.1.5), una gramática en **Forma Normal de Chomsky** solo admite producciones de la forma $A \to BC$ o $A \to a$, por lo que **ninguna variable puede derivar $\lambda$** y el lenguaje generado es $L(G) \setminus \{\lambda\}$.

* Si la gramática original $G$ genera la cadena vacía ($\lambda \in L(G)$), al transformarla a una FNC extendida que conserve exactamente el mismo lenguaje, se introduce un **nuevo símbolo inicial $S_0$** que **no aparece en el lado derecho de ninguna producción**, agregando exclusivamente la regla:
  $$S_0 \to S \mid \lambda$$
* De este modo, $\lambda$ se deriva en un único paso directo desde $S_0$, mientras que el resto de las derivaciones para cadenas de longitud $n \ge 1$ mantienen intacta la propiedad de árbol binario estricto de la FNC.