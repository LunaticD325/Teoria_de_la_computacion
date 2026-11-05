import flet as ft
from lenguajes import prefijos

def main(page: ft.Page):
    page.title = "Operaciones básicas sobre lenguajes"
    entrada = ft.TextField(label="Cadena")
    salida = ft.Text()

    def calcular(e):
        salida.value = ", ".join(prefijos(entrada.value))
        page.update()

    page.add(entrada, ft.ElevatedButton("Prefijos", on_click=calcular), salida)

ft.app(target=main)