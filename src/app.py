import flet as ft
from src.automata import Automata
import os

def main(page: ft.Page):
    page.title = "Simulador de Autómatas - Práctica 3"
    page.padding = 20
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.DARK

    # Estado global del autómata cargado
    current_automata = [None]

    # Componentes de interfaz
    status_text = ft.Text("No hay autómata cargado", color=ft.Colors.GREY_400)
    
    # -------------------------------------------------------------------
    # Tab 1: Carga y Simulación Directa
    # -------------------------------------------------------------------
    input_string = ft.TextField(label="Cadena a evaluar", width=300)
    sim_result = ft.Text(weight=ft.FontWeight.BOLD)
    sim_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Paso / Símbolo")),
            ft.DataColumn(ft.Text("Transición Directa")),
            ft.DataColumn(ft.Text("Estados Activos (con λ-clausura)")),
        ],
        rows=[]
    )

    def on_simulate(e):
        if not current_automata[0]:
            sim_result.value = "Error: Carga un autómata primero."
            sim_result.color = ft.Colors.RED
            page.update()
            return

        word = input_string.value or ""
        accepted, history = current_automata[0].simulate_direct(word)
        
        sim_result.value = f"Resultado: {'¡ACEPTADA!' if accepted else 'RECHAZADA'}"
        sim_result.color = ft.Colors.GREEN if accepted else ft.Colors.RED

        sim_table.rows.clear()
        for step, (sym, step_st, closure_st) in enumerate(history):
            st_str = "{" + ", ".join(sorted(step_st)) + "}" if step_st else "∅"
            cl_str = "{" + ", ".join(sorted(closure_st)) + "}" if closure_st else "∅"
            sim_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(f"Paso {step}: '{sym}'")),
                    ft.DataCell(ft.Text(st_str)),
                    ft.DataCell(ft.Text(cl_str)),
                ])
            )
        page.update()

    # -------------------------------------------------------------------
    # Tab 2: Transformaciones (Subconjuntos, Minimización, Sin λ)
    # -------------------------------------------------------------------
    transform_info = ft.Markdown()
    
    def on_run_subset(e):
        if not current_automata[0]:
            return
        dfa, table_log = current_automata[0].subset_construction()
        
        log_md = "### Tabla de Construcción de Subconjuntos (AFN -> AFD)\n\n"
        log_md += "| Estado AFD | Símbolo | Subconjunto Alcanzado |\n|---|---|---|\n"
        for src, sym, dst in table_log:
            src_str = "{" + ", ".join(src) + "}"
            dst_str = "{" + ", ".join(dst) + "}" if dst else "∅"
            log_md += f"| `{src_str}` | `{sym}` | `{dst_str}` |\n"
        
        log_md += f"\n**AFD Resultante:** {len(dfa.states)} estados. Inicial: `{dfa.initial_state}`, Finales: `{dfa.final_states}`"
        transform_info.value = log_md
        page.update()

    def on_run_minimize(e):
        if not current_automata[0]:
            return
        dfa_min = current_automata[0].minimize()
        
        log_md = "### Minimización de AFD (Algoritmo de Hopcroft)\n\n"
        log_md += f"* **Estados del autómata original:** {len(current_automata[0].states)}\n"
        log_md += f"* **Estados del AFD mínimo:** {len(dfa_min.states)}\n"
        log_md += f"* **Estado Inicial:** `{dfa_min.initial_state}`\n"
        log_md += f"* **Estados Finales:** `{dfa_min.final_states}`\n\n"
        log_md += "#### Transiciones del AFD Mínimo:\n"
        for st, trans in dfa_min.transitions.items():
            for sym, targets in trans.items():
                log_md += f"- `{st}` -- `{sym}` --> `{list(targets)[0]}`\n"
        
        transform_info.value = log_md
        page.update()

    # -------------------------------------------------------------------
    # Tab 3: Carga Masiva desde Archivo TXT
    # -------------------------------------------------------------------
    file_path_input = ft.TextField(label="Ruta del archivo de cadenas (.txt)", width=400, value="cadenas.txt")
    batch_results_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Cadena")),
            ft.DataColumn(ft.Text("Resultado")),
        ],
        rows=[]
    )

    def on_run_batch(e):
        if not current_automata[0]:
            return
        path = file_path_input.value
        if not os.path.exists(path):
            status_text.value = f"Archivo no encontrado: {path}"
            status_text.color = ft.Colors.RED
            page.update()
            return

        results = current_automata[0].validate_file(path)
        batch_results_table.rows.clear()
        for word, accepted in results:
            batch_results_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(word if word != "" else "λ (vacía)")),
                    ft.DataCell(ft.Text("ACEPTADA" if accepted else "RECHAZADA", 
                                       color=ft.Colors.GREEN if accepted else ft.Colors.RED)),
                ])
            )
        status_text.value = f"Validación masiva completada ({len(results)} cadenas)."
        status_text.color = ft.Colors.GREEN
        page.update()

    # Autómata de demostración inicial
    demo_transitions = {
        'q0': {'lambda': {'q1'}},
        'q1': {'a': {'q2'}, 'b': {'q1'}},
        'q2': {'a': {'q2'}, 'b': {'q2'}}
    }
    current_automata[0] = Automata({'q0', 'q1', 'q2'}, {'a', 'b'}, demo_transitions, 'q0', {'q2'})
    status_text.value = "Autómata de prueba cargado (Acepta cadenas que contienen 'a')"

    # Layout Principal
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Simulación Directa",
                content=ft.Column([
                    ft.Row([input_string, ft.ElevatedButton("Simular", on_click=on_simulate)]),
                    sim_result,
                    sim_table
                ], spacing=15)
            ),
            ft.Tab(
                text="Transformaciones",
                content=ft.Column([
                    ft.Row([
                        ft.ElevatedButton("Construcción de Subconjuntos", on_click=on_run_subset),
                        ft.ElevatedButton("Minimizar AFD", on_click=on_run_minimize),
                    ]),
                    transform_info
                ], spacing=15)
            ),
            ft.Tab(
                text="Validación Masiva",
                content=ft.Column([
                    ft.Row([file_path_input, ft.ElevatedButton("Procesar Archivo", on_click=on_run_batch)]),
                    batch_results_table
                ], spacing=15)
            )
        ]
    )

    page.add(
        ft.Text("Práctica 3 - Simulador e Integración de Autómatas", size=22, weight=ft.FontWeight.BOLD),
        status_text,
        tabs
    )

if __name__ == "__main__":
    ft.app(target=main)