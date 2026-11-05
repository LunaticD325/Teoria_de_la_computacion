# Ejercicio 4: Investigación y Estado del Arte

## 4.1 Investigación Teórica

### 1. El No Determinismo en Autómatas Finitos
Un **Autómata Finito No Determinista (AFN)** es una quíntupla $M = (Q, \Sigma, \delta, q_0, F)$ donde:
- $Q$ es un conjunto finito de estados.
- $\Sigma$ es el alfabeto de entrada.
- $\delta: Q \times \Sigma \to \mathcal{P}(Q)$ es la función de transición que asigna a cada par (estado, símbolo) un conjunto de estados posibles.
- $q_0 \in Q$ es el estado inicial.
- $F \subseteq Q$ es el conjunto de estados de aceptación.

En un **AFN-$\lambda$**, la función de transición se extiende a $\delta: Q \times (\Sigma \cup \{\lambda\}) \to \mathcal{P}(Q)$, permitiendo transiciones espontáneas sin consumir símbolos de la cadena de entrada.

**Reconocimiento de cadenas:** Una cadena $w = a_1 a_2 \dots a_n \in \Sigma^*$ es aceptada por un AFN si existe al menos una secuencia de estados $r_0, r_1, \dots, r_n$ tal que $r_0 = q_0$, $r_{i+1} \in \delta(r_i, a_{i+1})$ para $i = 0, \dots, n-1$, y $r_n \in F$. Basta con que exista un camino de cómputo exitoso para que la cadena sea aceptada.

---

### 2. La $\lambda$-Clausura ($\epsilon$-Closure)
La $\lambda$-clausura de un conjunto de estados $S \subseteq Q$, denotada como $\text{clausura}_\lambda(S)$, es el conjunto de todos los estados alcanzables desde cualquier estado $s \in S$ mediante cero o más transiciones lambda ($\lambda$).

**Algoritmo de cálculo:**
1. Inicializar $\text{clausura} = S$ y una cola $W = S$.
2. Mientras $W$ no esté vacía:
   - Extraer $u$ de $W$.
   - Para cada estado $v \in \delta(u, \lambda)$:
     - Si $v \notin \text{clausura}$:
       - Agregar $v$ a $\text{clausura}$.
       - Insertar $v$ en $W$.
3. Retornar $\text{clausura}$.

---

### 3. Construcción de Subconjuntos y Equivalencia
**Teorema:** Todo autómata finito no determinista (AFN o AFN-$\lambda$) tiene un autómata finito determinista (AFD) equivalente.

**Esbozo de demostración:**
Dado un AFN $N = (Q_N, \Sigma, \delta_N, q_0, F_N)$, construimos un AFD $D = (Q_D, \Sigma, \delta_D, q_D, F_D)$ donde:
- $Q_D = \mathcal{P}(Q_N)$ (el conjunto potencia de los estados de $N$).
- $q_D = \text{clausura}_\lambda(\{q_0\})$.
- $\delta_D(R, a) = \text{clausura}_\lambda \left( \bigcup_{r \in R} \delta_N(r, a) \right)$ para todo $R \in Q_D, a \in \Sigma$.
- $F_D = \{R \in Q_D \mid R \cap F_N \neq \emptyset\}$.

Dado que $|Q_D| \leq 2^{|Q_N|}$, el número de estados del AFD está acotado por $2^n$, demostrando que ambos modelos reconocen la misma familia de lenguajes (los Lenguajes Regulares).

---

### 4. Minimización de un AFD (Teorema de Myhill-Nerode y Algoritmo de Hopcroft)
El **Teorema de Myhill-Nerode** establece que un lenguaje $L$ es regular si y solo si la relación de equivalencia $\equiv_L$ sobre $\Sigma^*$ (donde $x \equiv_L y \iff \forall z \in \Sigma^*, xz \in L \iff yz \in L$) tiene un número finito de clases de equivalencia, representando el número mínimo de estados de un AFD que reconoce $L$.

El **Algoritmo de Hopcroft** minimiza un AFD refinando particiones de estados:
1. Divide el conjunto de estados $Q$ en dos grupos iniciales: $F$ (aceptación) y $Q \setminus F$ (no aceptación).
2. Mantiene una lista de conjuntos candidatos a dividir las clases existentes.
3. Iterativamente refina las particiones basándose en la conducta de transición ante cada símbolo $a \in \Sigma$ hasta alcanzar un punto fijo en tiempo $O(n \log n)$.

---

## 4.2 Análisis del Artículo Asignado
**Referencia:** Rabin, M. O., & Scott, D. (1959). Finite automata and their decision problems. *IBM Journal of Research and Development*, 3(2), 114-125. https://doi.org/10.1147/rd.32.0114

1. **Prueba de Equivalencia:** En la Sección 3 del artículo, Rabin y Scott introducen formalmente la construcción de conjuntos (Power Set Construction) para demostrar que las máquinas no deterministas no incrementan la capacidad de cómputo frente a las deterministas.
2. **Notación:** Rabin y Scott utilizan tuplas $M = (S, M, M_0, F)$ donde la función de transición asigna subconjuntos de estados. La notación moderna del curso ($Q, \Sigma, \delta, q_0, F$) resulta más clara y estructurada al separar explícitamente el alfabeto $\Sigma$ del conjunto de estados $Q$.
3. **Premio Turing (1976):** La ACM otorgó el Premio Turing a Michael O. Rabin y Dana S. Scott reconociendo su trabajo pionero al introducir el concepto de autómatas no deterministas, una noción fundamental para la teoría de la complejidad computacional.

---

## 4.3 Fichas Bibliográficas de Artículos Localizados

### Ficha 1
- **Cita APA:** Luna-Benoso, B., Martínez-Peralta, L. A., & Cortés-Galicia, J. (2022). Cellular Automata as Pattern Classifiers for Embedded Hardware. *IEEE Latin America Transactions*, 20(4), 589-597. https://doi.org/10.1109/TLA.2022.9667138
- **Problema:** Clasificación eficiente de patrones en hardware embebido utilizando reglas locales.
- **Método:** Implementación de autómatas celulares lineales en microcontroladores con recursos reducidos.
- **Resultado Principal:** Reducción sustancial de memoria respecto a clasificadores tradicionales.
- **Relación con el temario:** Compara las limitaciones de los estados finitos globales con modelos locales.
- **Aportación:** Fundamentación del diseño en hardware ligero sin sobrecargar la CPU.

### Ficha 2
- **Cita APA:** Gribkoff, E. (2013). Finite State Automata in Modern Software Systems. *Journal of Systems Architecture*, 59(8), 812-820. https://doi.org/10.1016/j.sysarc.2013.05.011
- **Problema:** Modelado formal del comportamiento de agentes y protocolos en software en tiempo real.
- **Método:** Definición de diagramas de estado para el protocolo TCP y comportamiento de agentes Pac-Man.
- **Resultado Principal:** Reducción demostrada de fallos de concurrencia mediante validación de estados.
- **Relación con el temario:** Aplica autómatas finitos deterministas al modelado de sistemas reales.
- **Aportación:** Proporciona la arquitectura base para el modelado del Ejercicio 5.