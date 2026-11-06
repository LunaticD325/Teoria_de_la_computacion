# Ejercicio 1: Investigación sobre Expresiones Regulares

**Autor:** Garduño Ibarra Uriel  
**Materia:** Teoría de la Computación (ESCOM - IPN)  
**Grupo:** 4CM2  

---

## 1. Definición Formal de Lenguaje Regular y Expresión Regular

### 1.1 Lenguaje Regular
Un lenguaje $L \subseteq \Sigma^*$ se define como **regular** si existe un Autómata Finito Determinista (AFD), un Autómata Finito No Determinista (AFN o $\text{AFN}-\lambda$), o una Expresión Regular (ER) que lo reconozca o genere.

### 1.2 Expresión Regular (Definición Inductiva)
Dado un alfabeto finito $\Sigma$, una **Expresión Regular** sobre $\Sigma$ se define inductivamente como sigue:

1. **Casos Base:**
   * $\emptyset$ es una ER que denota el lenguaje vacío $L(\emptyset) = \emptyset$.
   * $\lambda$ (o $\epsilon$) es una ER que denota el lenguaje $L(\lambda) = \{\lambda\}$.
   * Para todo $a \in \Sigma$, $a$ es una ER que denota el lenguaje $L(a) = \{a\}$.

2. **Paso Inductivo:** Si $r$ y $s$ son expresiones regulares que denotan los lenguajes $L(r)$ y $L(s)$ respectivamente, entonces:
   * **Unión ($+$):** $(r + s)$ es una ER que denota $L(r + s) = L(r) \cup L(s)$.
   * **Concatenación (yuxtaposición):** $(r s)$ es una ER que denota $L(r s) = L(r) \cdot L(s) = \{x y \mid x \in L(r), y \in L(s)\}$.
   * **Cerradura de Kleene ($*$):** $(r^*)$ es una ER que denota $L(r^*) = \bigcup_{i=0}^{\infty} L(r)^i$.

---

## 2. Jerarquía de Chomsky

En la Jerarquía de Gramáticas de Noam Chomsky (1956), los lenguajes regulares ocupan el nivel más restringido:

| Tipo | Gramática | Autómata Reconocedor | Forma de las Reglas |
|---|---|---|---|
| **Tipo 3** | **Regular** | **Autómata Finito (AFD / AFN)** | $A \to aB$ o $A \to a$ |
| **Tipo 2** | Libre del Contexto | Autómata con Pila (PDA) | $A \to \alpha$ |
| **Tipo 1** | Sensible al Contexto | Autómata Linealmente Acotado (LBA) | $\alpha A \beta \to \alpha \gamma \beta$ |
| **Tipo 0** | Sin Restricciones | Máquina de Turing (TM) | $\alpha \to \beta$ |

---

## 3. Teorema de Kleene

### Enunciado General
Un lenguaje $L \subseteq \Sigma^*$ es regular si y solo si es aceptado por un Autómata Finito (determinista o no determinista) o puede ser descrito mediante una Expresión Regular.

### Las Dos Direcciones del Teorema
1. **Primera Dirección ($\text{ER} \to \text{Autómata}$):** Dada cualquier expresión regular $r$, existe un $\text{AFN}-\lambda$ equivalente $M$ tal que $L(M) = L(r)$. Se demuestra mediante la **Construcción de Thompson**.
2. **Segunda Dirección ($\text{Autómata} \to \text{ER}$):** Dado cualquier Autómata Finito $M$, existe una expresión regular $r$ tal que $L(r) = L(M)$. Se demuestra mediante el **Método de Eliminación de Estados** o la **Construcción $R_{ij}^{(k)}$**.

**Referencia Bibliográfica Oficial:**  
Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2007). *Introducción a la Teoría de Autómatas, Lenguajes y Computación* (3.ª ed.). Pearson Educación. Capítulos 3.1 y 3.2.

---

## 4. Leyes Algebraicas de las Expresiones Regulares

Las leyes utilizadas para la simplificación de expresiones regulares en la Práctica 3 son:

1. **Conmutatividad de la Unión:** $R + S = S + R$
2. **Asociatividad de la Unión y Concatenación:**
   * $(R + S) + T = R + (S + T)$
   * $(R S) T = R (S T)$
3. **Distributividad:**
   * $L (R + S) = L R + L S$ (Distributividad a izquierda)
   * $(R + S) L = R L + S L$ (Distributividad a derecha)
4. **Identidades y Anuladores:**
   * $R + \emptyset = R$
   * $R \lambda = \lambda R = R$
   * $R \emptyset = \emptyset R = \emptyset$
5. **Idempotencia de la Unión:** $R + R = R$
6. **Leyes de Kleene:**
   * $(R^*)^* = R^*$
   * $\emptyset^* = \lambda$
   * $\lambda^* = \lambda$
   * $R^* = \lambda + R R^* = \lambda + R^* R$

---

## 5. Expresiones Regulares Teóricas vs. Motores de Lenguajes de Programación

### 5.1 Diferencia Fundamental
Las **ER teóricas** se basan en operaciones puras de lenguajes regulares reconocibles por Autómatas Finitos sin memoria persistente.  
Los **motores modernos de ER** (Python `re`, PCRE, JavaScript) añaden extensiones como *backreferences* (referencias hacia atrás, ej. `\1`), *lookaheads* y cuantificadores perezosos, lo que permite reconocer lenguajes **No Regulares** (incluso Libres del Contexto o Sensibles al Contexto).

### 5.2 Demostración mediante el Lema de Bombeo

Consideremos el lenguaje $L = \{ (a^n) b a^n \mid n \ge 0 \}$, el cual es descrito en sintaxis de motor moderno por el patrón `(a*)b\1`.

**Teorema:** El lenguaje $L = \{ a^n b a^n \mid n \ge 0 \}$ no es regular.

**Demostración por Contradicción mediante el Lema de Bombeo:**
1. Supongamos que $L$ es regular. Por el Lema de Bombeo, existe una constante de bombeo $p \ge 1$.
2. Seleccionamos la cadena $w = a^p b a^p \in L$. Se cumple $|w| = 2p + 1 \ge p$.
3. Por el Lema de Bombeo, $w$ se puede descomponer en $w = xyz$ tal que:
   * $|xy| \le p$
   * $|y| > 0$
   * Para todo $i \ge 0$, $x y^i z \in L$.
4. Como $|xy| \le p$, la subcadena $y$ consta únicamente de símbolos $a$ pertenecientes al primer bloque de $a$'s ($y = a^k$ con $k \ge 1$).
5. Evaluemos la cadena bombeada para $i = 2$:
   $$w' = x y^2 z = a^{p+k} b a^p$$
6. Como $k \ge 1$, tenemos $p + k \neq p$. Por lo tanto, $w' \notin L$, lo cual **contradice** el Lema de Bombeo.
7. **Conclusión:** $L$ no es un lenguaje regular, por lo que patrones con retro-referencias como `(a*)b\1` exceden la potencia formal de las expresiones regulares teóricas.

---

## 6. Aplicaciones de las Expresiones Regulares en Computación

1. **Análisis Léxico en Compiladores (Lex / Flex):**
   * **Expresión:** `[a-zA-R_][a-zA-R0-9_]*`
   * **Explicación:** Define el patrón de identificadores de variables en C/Python (debe iniciar con letra o guion bajo, seguido de letras, dígitos o guiones bajos).

2. **Búsqueda de Patrones en Texto (grep / ripgrep):**
   * **Expresión:** `^ERROR \[[0-9]{4}-[0-9]{2}-[0-9]{2}\]:`
   * **Explicación:** Filtra líneas de logs de servidores que inicien con la etiqueta `ERROR` seguida de una fecha en formato ISO (`YYYY-MM-DD`).

3. **Validación de Formatos de Entrada:**
   * **Expresión:** `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
   * **Explicación:** Valida direcciones de correo electrónico asegurando la estructura `usuario@dominio.extensión`.

4. **Filtrado y Limpieza de Datos (Pandas / Data Engineering):**
   * **Expresión:** `^\+52\s?\d{2}\s?\d{4}\s?\d{4}$`
   * **Explicación:** Valida y normaliza números telefónicos en México con clave internacional `+52` y 10 dígitos locales.

5. **Automatización en Sistemas Operativos (Sed / Awk / Bash):**
   * **Expresión:** `s/https?:\/\/[^\/]+/https:\/\/localhost/g`
   * **Explicación:** Reemplaza URLs de producción por la dirección local `localhost` en archivos de configuración de despliegue.