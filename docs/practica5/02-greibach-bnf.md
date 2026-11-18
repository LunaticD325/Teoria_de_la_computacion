# Ejercicio 2: Forma Normal de Greibach (FNG) y Forma de Backus-Naur (BNF)

## 1. Definición Formal de FNG
Una Gramática Libre de Contexto $G = (V, \Sigma, R, S)$ se encuentra en **Forma Normal de Greibach (FNG)** si todas sus reglas de producción tienen la forma:
$$A \to a\alpha$$
donde $A \in V$, $a \in \Sigma$ es un símbolo terminal y $\alpha \in V^*$ es una cadena (posiblemente vacía) compuesta únicamente por variables no terminales.

---

## 2. Gramática Propia en FNG
* **Archivo JFLAP:** `gramaticas/practica5/propia_fng.jff`
* **Definición de la Gramática ($L = \{a^n b^n \mid n \ge 1\}$):**
  $$S \to a S B \mid a B$$
  $$B \to b$$
* **Verificación:** Todas las producciones inician con un terminal seguido de cero o más variables, cumpliendo directamente la definición de FNG sin recursión izquierda. Validada mediante `Multiple Brute Force Parse` con 5 cadenas aceptadas (`ab`, `aabb`, `aaabbb`, `aaaabbbb`, `aaaaabbbbb`) y 5 rechazadas (`a`, `b`, `aab`, `abb`, `ba`).

---

## 3. Transformación Manual a FNG: Ejercicio 344 (Lista 5)
* **Archivo JFLAP:** `gramaticas/practica5/ej344_fng.jff`
* **Gramática Original $G_{344}$:**
  $$S \to A B \mid b$$
  $$A \to S a \mid a$$
  $$B \to b B \mid b$$
* **Pasos de Transformación:**
  1. **Eliminación de producciones $\lambda$, unitarias y símbolos inútiles:** La gramática no contiene producciones $\lambda$ ni unitarias, y todos sus símbolos son generadores y alcanzables.
  2. **Ordenamiento de variables ($A_1 = S, A_2 = A, A_3 = B$) y eliminación de recursión izquierda:**
     * Para $A_1 = S$: $S \to A B \mid b$.
     * Para $A_2 = A$: se sustituye $S$ en $A \to S a$ obteniendo $A \to A B a \mid b a \mid a$. Se elimina la recursión izquierda inmediata introduciendo $Z$:
       $$A \to b a \mid a \mid b a Z \mid a Z$$
       $$Z \to B a \mid B a Z$$
  3. **Sustitución hacia atrás (back-substitution):**
     * Sustituyendo $A$ en $S \to A B$:
       $$S \to b a B \mid a B \mid b a Z B \mid a Z B \mid b$$
     * Sustituyendo $B \to b B \mid b$ al inicio de $Z \to B a \mid B a Z$:
       $$Z \to b B a \mid b a \mid b B a Z \mid b a Z$$
* **Resultado Final en FNG:**
  $$S \to b a B \mid a B \mid b a Z B \mid a Z B \mid b$$
  $$A \to b a \mid a \mid b a Z \mid a Z$$
  $$B \to b B \mid b$$
  $$Z \to b B a \mid b a \mid b B a Z \mid b a Z$$

---

## 4. Notación de Backus-Naur (BNF)
La **Forma de Backus-Naur (BNF)** es una metalenguaje formal equivalente a las Gramáticas Libres de Contexto empleado para especificar la sintaxis de lenguajes de programación y protocolos. Sus metasímbolos principales son:
* `<no_terminal>`: delimita variables sintácticas.
* `::=`: indica definición de producción ("se define como").
* `|`: representa alternancia entre producciones.

### Representación en BNF del Ejercicio 344
```bnf
<S> ::= <A> <B> | "b"
<A> ::= <S> "a" | "a"
<B> ::= "b" <B> | "b"