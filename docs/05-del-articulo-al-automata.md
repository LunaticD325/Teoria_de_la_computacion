# Ejercicio 5: Del Artículo al Autómata

## 5.1 Definición Formal del Autómata (Pac-Man Ghost AI)

Modelamos el comportamiento ampliado de un fantasma en el juego Pac-Man mediante un Autómata Finito Determinista (AFD) de 6 estados: $M = (Q, \Sigma, \delta, q_0, F)$.

### Componentes de la Quíntupla:
- **Estados ($Q$):**
  - `q0` (Scatter/Dispersión): El fantasma se dirige a su esquina asignada.
  - `q1` (Chase/Persecución): El fantasma persigue activamente a Pac-Man.
  - `q2` (Frightened/Asustado): Pac-Man comió una píldora de poder; el fantasma huye.
  - `q3` (Eaten/Eaten): El fantasma fue comido y regresa al centro como ojos.
  - `q4` (Ambush/Emboscada - Estado Nuevo 1): Intenta interceptar la trayectoria futura de Pac-Man.
  - `q5` (Respawning/Reaparición - Estado Nuevo 2): Regeneración temporal en la casa central antes de salir.
- **Alfabeto ($\Sigma$):**
  - `t`: Timer expira.
  - `p`: Pac-Man come Píldora de Poder.
  - `c`: Fantasma es colisionado/comido por Pac-Man.
  - `h`: Fantasma llega a la casa central (Home).
  - `d`: Distancia corta a Pac-Man alcanzada.
  - `r`: Regeneración completada.
- **Estado Inicial ($q_0$):** `q0`
- **Estados de Aceptación ($F$):** `{q0, q1, q2, q3, q4, q5}` (Todos los estados representan comportamientos válidos).

---

## 5.2 Tabla de Transiciones ($\delta$)

| Estado | Evento `t` | Evento `p` | Evento `c` | Evento `h` | Evento `d` | Evento `r` |
|---|---|---|---|---|---|---|
| **q0** | q1 | q2 | - | - | q4 | - |
| **q1** | q0 | q2 | - | - | q4 | - |
| **q2** | q0 | - | q3 | - | - | - |
| **q3** | - | - | - | q5 | - | - |
| **q4** | q1 | q2 | - | - | - | - |
| **q5** | - | - | - | - | - | q0 |

---

## 5.3 Abstracción y Límites del Modelo

### Qué captura el modelo:
Captura la lógica de decisión de alto nivel y los modos de IA del fantasma en respuesta a eventos concretos del juego (tiempo transcurrido, consumo de ítems e interacciones físicas).

### Qué deja fuera:
No incluye las coordenadas espaciales $(x, y)$, la búsqueda de caminos mínimos (algoritmos como $A^*$), ni la velocidad continua de movimiento en píxeles por segundo.