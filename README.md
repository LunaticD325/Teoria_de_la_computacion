# Teoría de la Computación

**Nombre completo:** Garduño Ibarra Uriel  
**Boleta:** 2024630286  
**Grupo:** 4CM2  
**Carrera:** Ingeniería en Computación  
**Institución:** Escuela Superior de Cómputo - Instituto Politécnico Nacional  

---

## Índice General de Prácticas

1. **Práctica 3 - Algoritmos de Autómatas y Software Interactivo**
   * [Documentación Teórica y Análisis de Algoritmos](docs/practica3/03-algoritmos.md)
2. **Práctica 4 - Uso de Expresiones Regulares y Extensión de Software**
   * [Ejercicio 1: Investigación sobre Expresiones Regulares](docs/practica4/01-investigacion.md)
   * [Ejercicios 2, 3 y 4: Software Interactivo, Algoritmos y Validadores](docs/practica4/02-software-er.md)
3. **Práctica 5 - Formas Normales (Chomsky/Greibach) y Visualizador Gráfico**
   * [Ejercicio 1: Forma Normal de Chomsky con JFLAP](docs/practica5/01-forma-normal-chomsky.md)
   * [Ejercicio 2: Forma Normal de Greibach y Forma de Backus-Naur](docs/practica5/02-greibach-bnf.md)
   * [Ejercicio 3: Visualización de Autómatas y Simulación Gráfica en Flet](docs/practica5/03-visualizador-flet.md)

---

## Práctica 5: Especificaciones Técnicas y Nuevas Funciones

### Nuevas Funciones en el Software Interactivo
* **Lienzo Gráfico Interactivo (`ft.canvas.Canvas`):** Renderizado propio de AFD, AFN y AFN-$\lambda$ con soporte para ciclos, aristas bidireccionales curvas y reubicación de nodos mediante arrastre (*drag & drop*).
* **Comparativa Visual:** Visualización simultánea del autómata original y el transformado para todas las operaciones de las Prácticas 3 y 4.
* **Simulación Gráfica Paso a Paso:** Navegación símbolo por símbolo (adelante y atrás) resaltando estados activos y transiciones disparadas.

---

## Práctica 4: Especificaciones Técnicas

### Notación Aceptada por el Analizador de ER
El motor de expresiones regulares acepta la notación estándar del curso respetando la jerarquía de operadores (Cerradura $>$ Concatenación $>$ Unión):

* **Unión:** Símbolo `+` (ejemplo: `a+b`)
* **Concatenación:** Yuxtaposición explícita o implícita (ejemplo: `ab`)
* **Cerradura de Kleene:** Símbolo `*` (ejemplo: `a*`)
* **Agrupación y Precedencia:** Paréntesis `()` (ejemplo: `(a+b)*ab`)

### Validadores del Sistema (Ejercicio 4)
* **Correo Electrónico:** Formato simplificado basado en RFC 5322 (`user@gmail.com`).
* **Teléfono Nacional:** Validación a 10 dígitos según la normativa del IFT México.
* **URL:** Formato de dominio Web HTTP basado en RFC 3986 (`http://domain.com`).

---

## Instrucciones para Ejecutar el Entorno y Pruebas

### Requisitos
* Docker y Docker Compose V2

### 1. Ejecutar las Pruebas Unitarias (Pytest en CI/CD)
Para correr la suite completa de pruebas (incluyendo los 500+ casos de congruencia de modelos entre autómatas y el módulo `re`, así como la validación del layout y simulación paso a paso):

```bash
cd entorno
docker compose run --rm