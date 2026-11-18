import flet as ft
import xml.etree.ElementTree as ET
from src.automata import Automata
from src.regex_parser import regex_to_automata
from src.automata_to_regex import StateEliminationRegex
from src.validators import SystemValidator
from src.canvas_drawer import AutomatonVisualizerWidget

Icons = getattr(ft, "Icons", getattr(ft, "icons", None))
Colors = getattr(ft, "Colors", getattr(ft, "colors", None))
PrimaryButton = getattr(ft, "ElevatedButton", getattr(ft, "Button", None))


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


def register_picker(page: ft.Page, picker: ft.FilePicker):
    if hasattr(page, "services"):
        page.services.append(picker)
    elif hasattr(page, "overlay"):
        page.overlay.append(picker)


def build_sim_and_conversions_tab(page: ft.Page):
    """Pestaña unificada: Carga .jff, conversiones Práctica 3 y visualización doble."""
    file_picker = ft.FilePicker()
    register_picker(page, file_picker)

    status_text = ft.Text("Cargue un archivo .jff para visualizarlo y convertirlo", color=Colors.GREY_400)
    current_automaton = {"obj": None}

    vis_original = AutomatonVisualizerWidget(title="1. Autómata Original")
    vis_converted = AutomatonVisualizerWidget(title="2. Autómata Transformado (Práctica 3)")

    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            try:
                with open(e.files[0].path, "r", encoding="utf-8") as f:
                    content = f.read()
                aut = parse_jff_content(content)
                current_automaton["obj"] = aut
                status_text.value = f"Cargado: {e.files[0].name} ({aut.tipo}, {len(aut.states)} estados)"
                status_text.color = Colors.GREEN_400
                vis_original.set_automata(aut, title=f"1. Autómata Original ({e.files[0].name})")
            except Exception as err:
                status_text.value = f"Error al cargar JFF: {str(err)}"
                status_text.color = Colors.RED_400
            status_text.update()

    file_picker.on_result = on_file_result

    def on_remove_lambda(e):
        if current_automaton["obj"]:
            afn = current_automaton["obj"].remove_lambda_transitions()
            vis_converted.set_automata(afn, title="2. AFN sin transiciones λ")

    def on_subset(e):
        if current_automaton["obj"]:
            afd, _ = current_automaton["obj"].subset_construction()
            vis_converted.set_automata(afd, title="2. AFD (Construcción de Subconjuntos)")

    def on_minimize(e):
        if current_automaton["obj"]:
            afd, _ = current_automaton["obj"].subset_construction()
            afd_min = afd.minimize()
            vis_converted.set_automata(afd_min, title="2. AFD Mínimo (Hopcroft)")

    return ft.Column(
        [
            ft.Row(
                [
                    PrimaryButton(
                        "Cargar .jff",
                        icon=Icons.UPLOAD_FILE,
                        on_click=lambda _: file_picker.pick_files(allowed_extensions=["jff"]),
                    ),
                    ft.OutlinedButton("Eliminar λ", on_click=on_remove_lambda),
                    ft.OutlinedButton("Subconjuntos (AFD)", on_click=on_subset),
                    ft.OutlinedButton("Minimizar AFD", on_click=on_minimize),
                    status_text,
                ],
                wrap=True,
            ),
            ft.Divider(),
            vis_original,
            ft.Divider(),
            vis_converted,
        ],
        spacing=12,
    )


def build_regex_to_automata_tab():
    """Práctica 4 + Práctica 5: Muestra visualmente el AFN-lambda de Thompson y el AFD Mínimo."""
    regex_input = ft.TextField(label="Expresión Regular (Ej. (a+b)*ab)", expand=True)
    result_text = ft.Text(weight=ft.FontWeight.BOLD)

    vis_thompson = AutomatonVisualizerWidget(title="1. AFN-λ (Construcción de Thompson)")
    vis_dfa_min = AutomatonVisualizerWidget(title="2. AFD Mínimo Equivalente")

    def on_convert(e):
        try:
            afn, dfa_min = regex_to_automata(regex_input.value)
            result_text.value = (
                f"AFN-λ: {len(afn.states)} estados | AFD Mínimo: {len(dfa_min.states)} estados."
            )
            result_text.color = Colors.GREEN_400
            vis_thompson.set_automata(afn, title=f"1. AFN-λ de Thompson ({regex_input.value})")
            vis_dfa_min.set_automata(dfa_min, title=f"2. AFD Mínimo ({regex_input.value})")
        except Exception as err:
            result_text.value = f"Error en la expresión: {str(err)}"
            result_text.color = Colors.RED_400
        result_text.update()

    return ft.Column(
        [
            ft.Text(
                "Conversión de ER a Autómata y Visualización (Prácticas 4 y 5)",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Row([regex_input, PrimaryButton("Generar y Dibujar", on_click=on_convert)]),
            result_text,
            ft.Divider(),
            vis_thompson,
            ft.Divider(),
            vis_dfa_min,
        ],
        spacing=12,
    )


def build_automata_to_regex_tab(page: ft.Page):
    file_picker = ft.FilePicker()
    register_picker(page, file_picker)

    status_text = ft.Text("Cargue un archivo .jff para extraer su ER", color=Colors.GREY_400)
    regex_result = ft.Text(size=16, weight=ft.FontWeight.BOLD)
    vis_aut = AutomatonVisualizerWidget(title="Autómata Cargado")

    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            try:
                with open(e.files[0].path, "r", encoding="utf-8") as f:
                    content = f.read()
                aut = parse_jff_content(content)
                converter = StateEliminationRegex(aut)
                regex_str, steps = converter.convert_to_regex_steps()
                status_text.value = f"Autómata procesado ({len(steps)} pasos de eliminación)"
                status_text.color = Colors.GREEN_400
                regex_result.value = f"Expresión Regular Obtenida: {regex_str}"
                regex_result.color = Colors.BLUE_400
                vis_aut.set_automata(aut, title=f"Autómata: {e.files[0].name}")
            except Exception as err:
                status_text.value = f"Error al procesar: {str(err)}"
                status_text.color = Colors.RED_400
                regex_result.value = ""
            status_text.update()
            regex_result.update()

    file_picker.on_result = on_file_result

    return ft.Column(
        [
            ft.Text(
                "Conversión de Autómata a ER (Eliminación de Estados)",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            ft.Row(
                [
                    PrimaryButton(
                        "Cargar .jff para ER",
                        icon=Icons.UPLOAD_FILE,
                        on_click=lambda _: file_picker.pick_files(allowed_extensions=["jff"]),
                    ),
                    status_text,
                ]
            ),
            regex_result,
            ft.Divider(),
            vis_aut,
        ],
        spacing=12,
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
            color = Colors.GREEN_400 if res_aut else Colors.RED_400

            output_text.value = (
                f"Resultado Autómata: {verdict} | "
                f"Resultado Python `re`: {'ACEPTADO' if res_re else 'RECHAZADO'}"
            )
            output_text.color = color
        except Exception as err:
            output_text.value = f"Error: {str(err)}"
            output_text.color = Colors.RED_400
        output_text.update()

    return ft.Column(
        [
            ft.Text(
                "Validadores de Aplicación y Congruencia (Ejercicio 4)",
                size=18,
                weight=ft.FontWeight.BOLD,
            ),
            validator_dropdown,
            ft.Row([input_text, PrimaryButton("Validar Cadena", on_click=on_validate)]),
            output_text,
        ]
    )

def main(page: ft.Page):
    page.title = "Teoría de la Computación - Software Interactivo (Prácticas 3, 4 y 5)"
    page.scroll = ft.ScrollMode.AUTO

    views = [
        build_sim_and_conversions_tab(page),
        build_regex_to_automata_tab(),
        build_automata_to_regex_tab(page),
        build_validators_tab(),
    ]

    content_container = ft.Container(content=views[0], padding=10)

    def switch_tab(idx: int):
        content_container.content = views[idx]
        for i, btn in enumerate(nav_buttons):
            btn.style = ft.ButtonStyle(
                bgcolor=Colors.BLUE_700 if i == idx else None,
                color=Colors.WHITE if i == idx else None,
            )
        page.update()

    nav_buttons = [
        ft.OutlinedButton("1. Visualizador & Conversiones (.jff)", on_click=lambda _: switch_tab(0)),
        ft.OutlinedButton("2. ER -> Autómata (Visual)", on_click=lambda _: switch_tab(1)),
        ft.OutlinedButton("3. Autómata -> ER", on_click=lambda _: switch_tab(2)),
        ft.OutlinedButton("4. Validadores", on_click=lambda _: switch_tab(3)),
    ]
    nav_buttons[0].style = ft.ButtonStyle(bgcolor=Colors.BLUE_700, color=Colors.WHITE)

    page.add(
        ft.Row(nav_buttons, wrap=True),
        ft.Divider(),
        content_container,
    )


if __name__ == "__main__":
    if hasattr(ft, "run"):
        ft.run(main)
    else:
        ft.app(target=main)