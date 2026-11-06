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
Para correr la suite completa de pruebas (incluyendo los 500+ casos de congruencia de modelos entre autómatas y el módulo `re`):

```bash
cd entorno
docker compose run --rm py312 pytest
cd ..