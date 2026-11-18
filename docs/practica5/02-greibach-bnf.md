# Ejercicio 2: Forma Normal de Greibach (FNG) y Forma de Backus-Naur (BNF)

**Autor:** Garduño Ibarra Uriel  
**Referencia Bibliográfica Oficial:** Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2007). *Introducción a la Teoría de Autómatas, Lenguajes y Computación* (3.ª ed.). Pearson Educación, Capítulo 7 (Secciones 7.1 y Teorema de Greibach).  

---

## 1. Definición de Forma Normal de Greibach (FNG)
Una Gramática Independiente del Contexto $G = (V, \Sigma, R, S)$ está en **Forma Normal de Greibach** si todas sus producciones tienen la forma:
$$A \to a \alpha$$
donde $a \in \Sigma$ es un **símbolo terminal** y $\alpha \in V^*$ es una cadena (posiblemente vacía) de **variables**. (Si $\lambda \in L(G)$, se permite $S \to \lambda$ siempre que $S$ no aparezca en el lado derecho de ninguna regla).

---

## 2. Transformación Manual a FNG: Gramática Propia del Ejercicio 1

### 2.1 Partimos de la gramática limpia (sin $\lambda$, unitarias ni inútiles)
$$S \to A B \mid b B \mid b \mid a b$$
$$A \to a A \mid a$$
$$B \to b B \mid b$$

### 2.2 Método Seguido (Sustitución de Primeras Variables y Eliminación de Recursión Izquierda)
1. **Ordenamiento de variables:** $A_1 = S, \; A_2 = A, \; A_3 = B$.
2. **Verificar que cada regla de $A_i$ inicie con terminal o con $A_j$ tal que $j > i$:**
   * Para $A_2 = A$: $A \to aA \mid a$ (ya inicia con terminal $a$).
   * Para $A_3 = B$: $B \to bB \mid b$ (ya inicia con terminal $b$).
   * Para $A_1 = S$: la regla $S \to AB$ inicia con la variable $A$ ($2 > 1$).
3. **Sustitución de la variable inicial $A$ en $S \to AB$:**
   * Reemplazamos $A$ por sus producciones $\{aA, a\}$:
     $$S \to a A B \mid a B \mid b B \mid b \mid a b$$
4. **Resultado Final en Forma Normal de Greibach:**
   $$S \to a A B \mid a B \mid b B \mid a b \mid b$$
   $$A \to a A \mid a$$
   $$B \to b B \mid b$$

> Todas las producciones comienzan exactamente con un terminal ($a$ o $b$) seguido de cero o más variables. Al capturarse en JFLAP (`gramaticas/practica5/propia_fng.jff`), `Test -> Test for Grammar Type` la reconoce directamente como **Greibach Normal Form** y `Multiple Brute Force Parse` valida el mismo conjunto de 5 cadenas aceptadas (`b`, `ab`, `bb`, `aab`, `abb`) y 5 rechazadas.

* **Evidencia JFLAP (FNG Propia):**
  * ![FNG Propia JFLAP](../../evidencias/practica5/propia_fng.png) *(Adjuntar captura de Test for Grammar Type)*

---

## 3. Transformación Manual a FNG: Ejercicio 344 (Lista 5)

* **Gramática Original (Ejercicio 344):** *(Capturar producciones originales de tu Lista 5)*
* **Pasos de Transformación:**
  1. Eliminación de producciones $\lambda$, unitarias y símbolos inútiles.
  2. Ordenamiento de variables $A_1, A_2, \dots, A_m$ y eliminación de recursión izquierda inmediata ($A \to A\alpha \mid \beta \implies A \to \beta \mid \beta Z, \; Z \to \alpha \mid \alpha Z$).
  3. Sustitución hacia atrás (*back-substitution*) para que toda producción comience con un terminal $a \in \Sigma$.
* **Archivo JFLAP:** `gramaticas/practica5/ej344_fng.jff`
* **Evidencia JFLAP (FNG 344):**
  * ![FNG 344 JFLAP](../../evidencias/practica5/ej344_fng.png) *(Adjuntar captura de JFLAP)*

---

## 4. Forma de Backus-Naur (BNF) de la Gramática Propia

En notación **BNF** estándar (encerrando los no terminales entre `< >`, usando `::=` para definir reglas, `|` para alternancia y $\varepsilon$ para cadena vacía):

```bnf
<S> ::= <A> <B> | <C>
<A> ::= "a" <A> | ε
<B> ::= "b" <B> | "b"
<C> ::= "a" "b"
<D> ::= "a" <D> "b"