import flet as ft
from lenguajes import prefijos, sufijos, subcadenas, generar_kleene, generar_positiva

def main(page: ft.Page):
    page.title = "Operaciones Básicas sobre Cadenas y Lenguajes"
    page.scroll = ft.ScrollMode.AUTO

    # Campos Operación 1 (Cadenas)
    input_cadena = ft.TextField(label="Ingrese una cadena", value="ab")
    txt_prefijos = ft.Text("Prefijos: -")
    txt_sufijos = ft.Text("Sufijos: -")
    txt_subcadenas = ft.Text("Subcadenas: -")

    def operacion_cadenas(e):
        cad = input_cadena.value
        txt_prefijos.value = f"Prefijos ({len(prefijos(cad))}): {', '.join(prefijos(cad))}"
        txt_sufijos.value = f"Sufijos ({len(sufijos(cad))}): {', '.join(sufijos(cad))}"
        txt_subcadenas.value = f"Subcadenas ({len(subcadenas(cad))}): {', '.join(subcadenas(cad))}"
        page.update()

    # Campos Operación 2 (Cerraduras)
    input_alfabeto = ft.TextField(label="Alfabeto (separado por comas)", value="a,b")
    input_max_len = ft.TextField(label="Longitud máxima (n)", value="2")
    txt_kleene = ft.Text("Sigma*: -")
    txt_positiva = ft.Text("Sigma+: -")
    txt_error = ft.Text("", color="red")

    def operacion_cerraduras(e):
        txt_error.value = ""
        alfabeto = [s.strip() for s in input_alfabeto.value.split(",") if s.strip()]
        try:
            n = int(input_max_len.value)
        except ValueError:
            txt_error.value = "La longitud debe ser un número entero."
            page.update()
            return

        # Validación del límite de 200,000 cadenas
        k = len(alfabeto)
        total_estimado = sum(k**i for i in range(n + 1)) if k > 1 else (n + 1)
        if total_estimado > 200000:
            txt_error.value = f"Operación rechazada: generaría aproximadamente {total_estimado:,} cadenas (Límite: 200,000)."
            txt_kleene.value = "Sigma*: -"
            txt_positiva.value = "Sigma+: -"
            page.update()
            return

        res_k = generar_kleene(alfabeto, n)
        res_p = generar_positiva(alfabeto, n)

        txt_kleene.value = f"Sigma* ({len(res_k)} cadenas): {', '.join(res_k)}"
        txt_positiva.value = f"Sigma+ ({len(res_p)} cadenas): {', '.join(res_p)}"
        page.update()

    page.add(
        ft.Text("Operación 1: Prefijos, Sufijos y Subcadenas", size=20, weight=ft.FontWeight.BOLD),
        input_cadena,
        ft.Button("Calcular sobre cadena", on_click=operacion_cadenas),
        txt_prefijos,
        txt_sufijos,
        txt_subcadenas,
        ft.Divider(),
        ft.Text("Operación 2: Cerradura de Kleene y Positiva", size=20, weight=ft.FontWeight.BOLD),
        input_alfabeto,
        input_max_len,
        ft.Button("Calcular cerraduras", on_click=operacion_cerraduras),
        txt_error,
        txt_kleene,
        txt_positiva,
    )

ft.run(main)