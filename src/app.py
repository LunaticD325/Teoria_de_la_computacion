import flet as ft
import xml.etree.ElementTree as ET
from src.automata import Automata
from src.regex_parser import regex_to_automata
from src.automata_to_regex import StateEliminationRegex
from src.validators import SystemValidator, VALIDATOR_PATTERNS


def parse_jff_content(content_str: str) -> Automata:
    root = ET.fromstring(content_str)
    automaton_node = root.find("automaton")
    if automaton_node is None:
        raise ValueError("El archivo XML no contiene una etiqueta <automaton>.")

    states = set()
    initial_state = None
    final_states = set()
    state_id_to_name = {}

    for state_elem in automaton_node.findall("state"):
        sid = state_elem.attrib.get("id")
        sname = state_elem.attrib.get("name", f"q{sid}")
        state_id_to_name[sid] = sname
        states.add(sname)

        if state_elem.find("initial") is not None:
            initial_state = sname
        if state_elem.find("final") is not None:
            final_states.add(sname)

    transitions = {}
    alphabet = set()

    for trans_elem in automaton_node.findall("transition"):
        from_id = trans_elem.find("from").text
        to_id = trans_elem.find("to").text
        read_elem = trans_elem.find("read")

        sym = (
            read_elem.text
            if (read_elem is not None and read_elem.text is not None)
            else "lambda"
        )
        u = state_id_to_name[from_id]
        v = state_id_to_name[to_id]

        if sym not in ["lambda", "λ", ""]:
            alphabet.add(sym)

        transitions.setdefault(u, {}).setdefault(sym, set()).add(v)

    return Automata(
        states=states,
        alphabet=alphabet,
        transitions=transitions,
        initial_state=initial_state or "q0",
        final_states=final_states,
        tipo="AFN-lambda" if "lambda" in str(transitions) else "AFD",
    )


def build_sim_tab():
    file_picker = ft.FilePicker()
    status_text = ft.Text("Cargue un archivo .jff para iniciar", color=ft.colors.GREY_400)
    input_chain = ft.TextField(label="Cadena a simular", expand=True)
    sim_result = ft.Text(weight=ft.FontWeight.BOLD)
    current_automaton = {"obj": None}

    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            try:
                with open(e.files[0].path, "r", encoding="utf-8") as f:
                    content = f.read()
                aut = parse_jff_content(content)
                current_automaton["obj"] = aut
                status_text.value = f"Cargado: {e.files[0].name} ({len(aut.states)} estados)"
                status_text.color = ft.colors.GREEN_400
            except Exception as err:
                status_text.value = f"Error al cargar JFF: {str(err)}"
                status_text.color = ft.colors.RED_400
            status_text.update()

    file_picker.on_result = on_file_result

    def on_simulate(e):
        if not current_automaton["obj"]:
            sim_result.value = "Primero cargue un autómata (.jff)"
            sim_result.color = ft.colors.RED_400
        else:
            acc, path = current_automaton["obj"].simulate_direct(input_chain.value)
            res_str = "ACEPTADA" if acc else "RECHAZADA"
            sim_result.value = f"Resultado: {res_str} | Camino: {' -> '.join(path)}"
            sim_result.color = ft.colors.GREEN_400 if acc else ft.colors.RED_400
        sim_result.update()

    return ft.Column(
        [
            file_picker,
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Cargar .jff",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: file_picker.pick_files(
                            allowed_extensions=["jff"]
                        ),
                    ),
                    status_text,
                ]
            ),
            ft.Row(
                [
                    input_chain,
                    ft.ElevatedButton("Simular", on_click=on_simulate),
                ]
            ),
            sim_result,
        ]
    )


def build_regex_to_automata_tab():
    regex_input = ft.TextField(
        label="Expresión Regular (Ej. (a+b)*ab)", expand=True
    )
    result_text = ft.Text(weight=ft.FontWeight.BOLD)

    def on_convert(e):
        try:
            afn, dfa_min = regex_to_automata(regex_input.value)
            result_text.value = (
                f"AFN-λ construido con {len(afn.states)} estados.\n"
                f"AFD Mínimo generado con {len(dfa_min.states)} estados."
            )
            result_text.color = ft.colors.GREEN_400
        except Exception as err:
            result_text.value = f"Error en la expresión: {str(err)}"
            result_text.color = ft.colors.RED_400
        result_text.update()

    return ft.Column(
        [
            ft.Text(
                "Conversión de ER a Autómata (Construcción de Thompson)",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Row(
                [
                    regex_input,
                    ft.ElevatedButton(
                        "Generar Autómatas", on_click=on_convert
                    ),
                ]
            ),
            result_text,
        ]
    )


def build_automata_to_regex_tab():
    file_picker = ft.FilePicker()
    status_text = ft.Text("Cargue un archivo .jff para extraer su ER", color=ft.colors.GREY_400)
    regex_result = ft.Text(size=16, weight=ft.FontWeight.BOLD)

    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            try:
                with open(e.files[0].path, "r", encoding="utf-8") as f:
                    content = f.read()
                aut = parse_jff_content(content)
                converter = StateEliminationRegex(aut)
                regex_str, steps = converter.convert_to_regex_steps()
                status_text.value = f"Autómata procesado ({len(steps)} pasos de eliminación)"
                status_text.color = ft.colors.GREEN_400
                regex_result.value = f"Expresión Regular Obtenida: {regex_str}"
                regex_result.color = ft.colors.BLUE_400
            except Exception as err:
                status_text.value = f"Error al procesar: {str(err)}"
                status_text.color = ft.colors.RED_400
                regex_result.value = ""
            status_text.update()
            regex_result.update()

    file_picker.on_result = on_file_result

    return ft.Column(
        [
            file_picker,
            ft.Text(
                "Conversión de Autómata a ER (Eliminación de Estados)",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Cargar .jff para ER",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=lambda _: file_picker.pick_files(
                            allowed_extensions=["jff"]
                        ),
                    ),
                    status_text,
                ]
            ),
            regex_result,
        ]
    )


def build_validators_tab():
    validator_dropdown = ft.Dropdown(
        label="Seleccionar Validador",
        options=[
            ft.dropdown.Option("email", "Correo Electrónico (@gmail.com)"),
            ft.dropdown.Option("phone", "Teléfono Nacional (10 dígitos)"),
            ft.dropdown.Option("url", "URL Genérica (http://...com)"),
        ],
        value="email",
    )
    input_text = ft.TextField(label="Texto a validar", expand=True)
    output_text = ft.Text(weight=ft.FontWeight.BOLD)

    def on_validate(e):
        try:
            val = SystemValidator(validator_dropdown.value)
            res_aut = val.validate_with_automata(input_text.value)
            res_re = val.validate_with_re(input_text.value)

            verdict = "ACEPTADO" if res_aut else "RECHAZADO"
            color = ft.colors.GREEN_400 if res_aut else ft.colors.RED_400

            output_text.value = (
                f"Resultado Autómata: {verdict} | "
                f"Resultado Python `re`: {'ACEPTADO' if res_re else 'RECHAZADO'}"
            )
            output_text.color = color
        except Exception as err:
            output_text.value = f"Error: {str(err)}"
            output_text.color = ft.colors.RED_400
        output_text.update()

    return ft.Column(
        [
            ft.Text(
                "Validadores de Aplicación y Congruencia (Ejercicio 4)",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            validator_dropdown,
            ft.Row(
                [
                    input_text,
                    ft.ElevatedButton("Validar Cadena", on_click=on_validate),
                ]
            ),
            output_text,
        ]
    )


def main(page: ft.Page):
    page.title = "Teoría de la Computación - Software Interactivo"
    page.scroll = ft.ScrollMode.AUTO

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Simulador .jff", content=build_sim_tab()),
            ft.Tab(
                text="ER -> Autómata", content=build_regex_to_automata_tab()
            ),
            ft.Tab(
                text="Autómata -> ER", content=build_automata_to_regex_tab()
            ),
            ft.Tab(text="Validadores", content=build_validators_tab()),
        ],
        expand=1,
    )

    page.add(tabs)


if __name__ == "__main__":
    ft.app(target=main)