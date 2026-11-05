import os
import flet as ft
from lenguajes import prefijos, sufijos, subcadenas, generar_kleene, generar_positiva
from automata import Automata
from formatos import (
    cargar_jff, guardar_jff,
    cargar_json, guardar_json,
    cargar_xml, guardar_xml
)

def main(page: ft.Page):
    page.title = "Simulador de Autómatas y Lenguajes"
    page.scroll = ft.ScrollMode.AUTO

    automata_actual = None

    # --- PESTAÑA 1: Operaciones sobre Cadenas y Lenguajes ---
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

    input_alfabeto = ft.TextField(label="Alfabeto (separado por comas)", value="a,b")
    input_max_len = ft.TextField(label="Longitud máxima (n)", value="2")
    txt_kleene = ft.Text("Sigma*: -")
    txt_positiva = ft.Text("Sigma+: -")
    txt_error_lenguajes = ft.Text("", color="red")

    def operacion_cerraduras(e):
        txt_error_lenguajes.value = ""
        alfabeto = [s.strip() for s in input_alfabeto.value.split(",") if s.strip()]
        try:
            n = int(input_max_len.value)
        except ValueError:
            txt_error_lenguajes.value = "La longitud debe ser un número entero."
            page.update()
            return

        k = len(alfabeto)
        total_estimado = sum(k**i for i in range(n + 1)) if k > 1 else (n + 1)
        if total_estimado > 200000:
            txt_error_lenguajes.value = f"Rechazado: generaría {total_estimado:,} cadenas (Límite: 200,000)."
            page.update()
            return

        res_k = generar_kleene(alfabeto, n)
        res_p = generar_positiva(alfabeto, n)
        txt_kleene.value = f"Sigma* ({len(res_k)}): {', '.join(res_k)}"
        txt_positiva.value = f"Sigma+ ({len(res_p)}): {', '.join(res_p)}"
        page.update()

    tab_lenguajes = ft.Column([
        ft.Text("Operación 1: Prefijos, Sufijos y Subcadenas", size=18, weight=ft.FontWeight.BOLD),
        input_cadena,
        ft.Button("Calcular sobre cadena", on_click=operacion_cadenas),
        txt_prefijos, txt_sufijos, txt_subcadenas,
        ft.Divider(),
        ft.Text("Operación 2: Cerradura de Kleene y Positiva", size=18, weight=ft.FontWeight.BOLD),
        input_alfabeto, input_max_len,
        ft.Button("Calcular cerraduras", on_click=operacion_cerraduras),
        txt_error_lenguajes, txt_kleene, txt_positiva
    ])

    # --- PESTAÑA 2: Simulador de Autómatas ---
    input_ruta_archivo = ft.TextField(label="Ruta del archivo (.jff, .json, .xml)", value="automata.jff")
    txt_info_automata = ft.Text("Autómata no cargado.", weight=ft.FontWeight.BOLD)
    txt_tabla_transiciones = ft.Text("-")

    def cargar_archivo(e):
        nonlocal automata_actual
        ruta = input_ruta_archivo.value.strip()
        if not os.path.exists(ruta):
            txt_info_automata.value = f"Error: El archivo '{ruta}' no existe."
            page.update()
            return

        try:
            if ruta.endswith(".jff"):
                automata_actual = cargar_jff(ruta)
            elif ruta.endswith(".json"):
                automata_actual = cargar_json(ruta)
            elif ruta.endswith(".xml"):
                automata_actual = cargar_xml(ruta)
            else:
                txt_info_automata.value = "Formato no soportado (use .jff, .json o .xml)."
                page.update()
                return

            txt_info_automata.value = (
                f"Tipo: {automata_actual.tipo} | Estados: {sorted(list(automata_actual.estados))} | "
                f"Inicial: {automata_actual.inicial} | Aceptación: {sorted(list(automata_actual.aceptacion))}"
            )
            
            # Construir resumen de transiciones
            lineas = []
            for orig, mapa in automata_actual.transiciones.items():
                for sim, dests in mapa.items():
                    sim_s = sim if sim else "λ"
                    lineas.append(f"  δ({orig}, '{sim_s}') -> {sorted(list(dests))}")
            txt_tabla_transiciones.value = "Transiciones:\n" + "\n".join(lineas)
        except Exception as err:
            txt_info_automata.value = f"Error al cargar archivo: {err}"
        page.update()

    input_cadena_sim = ft.TextField(label="Cadena a simular", value="a")
    txt_resultado_sim = ft.Text("Resultado: -", size=16, weight=ft.FontWeight.BOLD)
    txt_traza_sim = ft.Text("Traza de ejecución: -")

    def simular_cadena(e):
        if not automata_actual:
            txt_resultado_sim.value = "Error: Primero debe cargar un autómata."
            page.update()
            return

        cadena = input_cadena_sim.value
        aceptada, traza = automata_actual.simular(cadena)
        txt_resultado_sim.value = f"Resultado: {'ACEPTADA' if aceptada else 'RECHAZADA'}"
        txt_traza_sim.value = "Traza paso a paso:\n" + "\n".join(traza)
        page.update()

    tab_simulador = ft.Column([
        ft.Text("Importación y Simulación de Autómatas", size=18, weight=ft.FontWeight.BOLD),
        input_ruta_archivo,
        ft.Button("Cargar Autómata", on_click=cargar_archivo),
        txt_info_automata,
        txt_tabla_transiciones,
        ft.Divider(),
        ft.Text("Simulación Paso a Paso", size=18, weight=ft.FontWeight.BOLD),
        input_cadena_sim,
        ft.Button("Simular Cadena", on_click=simular_cadena),
        txt_resultado_sim,
        txt_traza_sim
    ])

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Lenguajes",
                content=tab_lenguajes,
            ),
            ft.Tab(
                text="Simulador AFND/AFD",
                content=tab_simulador,
            ),
        ],
        expand=1,
    )

    page.add(tabs)

ft.run(main)