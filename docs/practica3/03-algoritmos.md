# Ejercicio 3: Documentación Teórica y Análisis de Algoritmos

## 1. Cerradura Lambda ($\lambda$-closure) y Simulación Directa

* **Fundamento Teórico:** Hopcroft, Motwani & Ullman (2007), Sección 3.7. La $\lambda$-clausura de un conjunto de estados $S$, denotada $\text{CL}_{\lambda}(S)$, es el conjunto mínimo de estados alcanzables desde $S$ mediante cero o más transiciones espontáneas ($\lambda$).
* **Pseudocódigo:**
  ```text
  Función LambdaClosure(states):
      closure = set(states)
      stack = list(states)
      mientras stack no esté vacío:
          curr = stack.pop()
          para cada estado nxt en transitions[curr]['lambda']:
              si nxt no está en closure:
                  closure.add(nxt)
                  stack.append(nxt)
      retornar closure