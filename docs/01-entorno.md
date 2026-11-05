# Ejercicio 1: Entorno de trabajo (Control de versiones y contenedores)

## Justificación de los tres entornos de Python

Para la realización de esta práctica se seleccionaron tres versiones distintas del intérprete de Python en contenedores independientes:

1. **py311 (`python:3.11-slim`):** Es la versión mínima compatible que continúa en soporte activo y admite las dependencias requeridas (como Flet).
2. **py312 (`python:3.12-slim`):** Es la versión de referencia del curso, encargada de servir la interfaz gráfica del sistema.
3. **py313 (`python:3.13-slim`):** Es una de las versiones más recientes, utilizada para verificar que el programa no presente incompatibilidades o fallos por cambios en el intérprete.

### ¿Por qué tres contenedores y no uno solo?
Un entorno virtual reutiliza el intérprete del sistema operativo sobre el que fue creado y no modifica la versión base de Python. Para contar con tres versiones en un solo contenedor se requeriría instalar manualmente tres intérpretes distintos dentro de la misma imagen. La arquitectura basada en tres contenedores garantiza aislamiento completo y reproducibilidad independiente en cada versión.

---

## Explicación del Dockerfile y Compose

- **`ARG PYTHON_VERSION=3.12`**: Declara una variable de construcción para seleccionar la imagen base dinámicamente.
- **`RUN python -m venv /opt/venv`**: Crea el entorno virtual en `/opt/venv`, manteniéndolo fuera de `/app` para evitar que sea sobrescrito por volúmenes montados.
- **`ENV PATH="/opt/venv/bin:$PATH"`**: Agrega el entorno virtual al `PATH` para activarlo por defecto.
- **`compose.yml`**: Configura los tres servicios (`py311`, `py312`, `py313`) pasando el argumento de versión correspondiente a cada uno.