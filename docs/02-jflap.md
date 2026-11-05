# Ejercicio 2: AFND y AFND-λ en JFLAP

## 2.1 Clasificación y Cobertura de Ejercicios

### Lista 2 (Ejercicios 94 a 150)
- **Directorio:** `automatas/lista2-afd/`
- **Clasificación:** AFD (Autómatas Finitos Deterministas).
- **Justificación:** Para cada estado y cada símbolo del alfabeto existe exactamente una transición bien definida, determinando de forma única el siguiente estado sin bifurcaciones.

### Lista 3 (Ejercicios 151 a 207)
- **Directorio:** `automatas/lista3-afnd/`
- **Clasificación:** AFND estándar (Autómatas Finitos No Deterministas).
- **Justificación:** Contienen estados donde un mismo símbolo de entrada permite la transición hacia múltiples estados destino, permitiendo rutas de cómputo paralelas sin uso de transiciones $\lambda$.

### Lista 3 (Ejercicios 208 a 263)
- **Directorio:** `automatas/lista3-afnd-lambda/`
- **Clasificación:** AFND-$\lambda$ (Autómatas Finitos No Deterministas con Transiciones Lambda).
- **Justificación:** Utilizan transiciones espontáneas ($\lambda$ o $\epsilon$) que permiten cambiar de estado sin consumir símbolos de la cadena de entrada, facilitando la unión y concatenación de subautómatas.

---

## 2.2 Conversiones y Análisis Comparativo de la Cota $2^n$

### Tabla Comparativa de Conversiones (AFND $\to$ AFD)

| Caso de Prueba | Descripción del Lenguaje | Estados AFND ($n$) | Estados AFD Resultante | Cota Teórica ($2^n$) | Observaciones |
|---|---|---|---|---|---|
| **Caso 1** | Cadenas sobre $\{a, b\}$ que contienen la subcadena `ab` | 3 | 3 | $2^3 = 8$ | Los estados inalcanzables son descartados por la construcción de subconjuntos. |
| **Caso 2** | Cadenas sobre $\{a, b\}$ con el segundo símbolo desde el final igual a 'a' | 3 | 4 | $2^3 = 8$ | Mantiene un registro limitado de la memoria reciente. |
| **Caso 3** | Cadenas que terminan en `aba` | 4 | 4 | $2^4 = 16$ | El AFD resultante coincide casi exactamente en número de estados. |
| **Caso 4** | Cadenas sobre $\{a, b\}$ con número par de 'a' y de 'b' | 4 | 4 | $2^4 = 16$ | El modelo original era un AFD estricto. |
| **Caso 5 (Peor Caso)** | Cadenas donde el $k$-ésimo símbolo desde el final es 'a' ($k=n-1$) | 4 | 15 | $2^4 = 16$ | **Caso crítico:** El AFD requiere un estado por cada combinación posible de los últimos $k$ símbolos. |

---

## 2.3 Explicación Teórica de la Cota $2^n$

1. **¿Por qué rara vez se alcanza la cota $2^n$?**
   En la práctica, la mayoría de los subconjuntos del conjunto potencia $\mathcal{P}(Q)$ no son alcanzables a partir de la $\lambda$-clausura del estado inicial. Muchas combinaciones de estados son físicamente imposibles de activar simultáneamente durante la lectura de cualquier cadena válida.

2. **Familia de Lenguajes donde SÍ se alcanza la cota:**
   Tomada de la literatura (Hopcroft et al., 2008), la familia $L_k = \{w \in \{0, 1\}^* \mid \text{el } k\text{-ésimo símbolo desde el final es } 1\}$ requiere exactamente $n = k + 1$ estados en un AFND, pero cualquier AFD equivalente necesita estrictamente $2^k = 2^{n-1}$ estados para memorizar todos los posibles sufijos de longitud $k$.