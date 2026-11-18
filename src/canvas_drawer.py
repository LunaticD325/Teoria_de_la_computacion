import math
import flet as ft
import flet.canvas as cv
from typing import Dict, List, Set, Tuple, Optional
from src.automata import Automata
from src.visualizer_core import AutomatonLayout, StepSimulator


class AutomatonVisualizerWidget(ft.Column):
    """Widget interactivo con lienzo Flet puro para dibujar y simular autómatas paso a paso."""

    NODE_RADIUS = 24.0

    def __init__(self, automata: Optional[Automata] = None, title: str = "Visualizador de Autómata"):
        super().__init__(spacing=10)
        self.title_text = title
        self.automata: Optional[Automata] = automata
        self.layout = AutomatonLayout(width=780.0, height=420.0)
        self.simulator: Optional[StepSimulator] = None
        self.dragging_state: Optional[str] = None

        self.active_states: Set[str] = set()
        self.active_edges: Set[Tuple[str, str]] = set()  # pares (u, v) iluminados

        # Controles de simulación
        self.chain_input = ft.TextField(label="Cadena a simular paso a paso", width=260, dense=True)
        self.btn_load_chain = ft.ElevatedButton("Cargar cadena", icon=ft.icons.PLAY_ARROW, on_click=self._on_load_chain)
        self.btn_prev = ft.IconButton(icon=ft.icons.SKIP_PREVIOUS, tooltip="Paso anterior", on_click=self._on_prev, disabled=True)
        self.btn_next = ft.IconButton(icon=ft.icons.SKIP_NEXT, tooltip="Siguiente paso", on_click=self._on_next, disabled=True)
        self.btn_reset = ft.IconButton(icon=ft.icons.REPLAY, tooltip="Reiniciar", on_click=self._on_reset, disabled=True)
        self.btn_relayout = ft.OutlinedButton("Reordenar nodos", icon=ft.icons.REFRESH, on_click=self._on_relayout)

        self.step_info = ft.Text("Cargue o genere un autómata para visualizarlo.", size=13, weight=ft.FontWeight.W_500)
        self.verdict_badge = ft.Text("", size=14, weight=ft.FontWeight.BOLD)

        self.canvas = cv.Canvas(
            shapes=[],
            width=self.layout.width,
            height=self.layout.height,
        )

        self.gesture_detector = ft.GestureDetector(
            content=ft.Container(
                content=self.canvas,
                width=self.layout.width,
                height=self.layout.height,
                bgcolor=ft.colors.SURFACE_VARIANT,
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=8,
            ),
            on_pan_start=self._on_pan_start,
            on_pan_update=self._on_pan_update,
            on_pan_end=self._on_pan_end,
        )

        self.controls = [
            ft.Row(
                [
                    ft.Text(self.title_text, size=16, weight=ft.FontWeight.BOLD),
                    self.btn_relayout,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Row(
                [
                    self.chain_input,
                    self.btn_load_chain,
                    self.btn_prev,
                    self.btn_next,
                    self.btn_reset,
                    self.verdict_badge,
                ],
                wrap=True,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            self.step_info,
            self.gesture_detector,
        ]

        if automata is not None:
            self.set_automata(automata, auto_update=False)

    def set_automata(self, automata: Automata, title: Optional[str] = None, auto_update: bool = True):
        self.automata = automata
        if title:
            self.title_text = title
            self.controls[0].controls[0].value = title

        self.layout.compute_initial_positions(automata)
        self.simulator = StepSimulator(automata)
        self.active_states = {automata.initial_state} if automata.initial_state else set()
        self.active_edges = set()
        self.verdict_badge.value = ""
        self.step_info.value = (
            f"Tipo: {automata.tipo} | Estados: {len(automata.states)} | "
            f"Inicial: {automata.initial_state} | Finales: {', '.join(sorted(automata.final_states)) or 'Ninguno'} "
            "(Arrastre cualquier nodo con el mouse)"
        )
        self.btn_prev.disabled = True
        self.btn_next.disabled = True
        self.btn_reset.disabled = True
        self._redraw(auto_update=auto_update)

    # --- Eventos de arrastre (Drag & Drop) ---

    def _on_pan_start(self, e: ft.DragStartEvent):
        if not self.automata:
            return
        px, py = e.local_x, e.local_y
        for state, (sx, sy) in self.layout.positions.items():
            if math.hypot(px - sx, py - sy) <= self.NODE_RADIUS + 6:
                self.dragging_state = state
                break

    def _on_pan_update(self, e: ft.DragUpdateEvent):
        if self.dragging_state and self.automata:
            self.layout.move_state(self.dragging_state, e.local_x, e.local_y, margin=self.NODE_RADIUS + 10)
            self._redraw(auto_update=True)

    def _on_pan_end(self, e: ft.DragEndEvent):
        self.dragging_state = None

    def _on_relayout(self, e):
        if self.automata:
            self.layout.compute_initial_positions(self.automata)
            self._redraw(auto_update=True)

    # --- Eventos de simulación paso a paso ---

    def _on_load_chain(self, e):
        if not self.automata or not self.simulator:
            return
        text = self.chain_input.value or ""
        self.simulator.load_string(text)
        self._sync_step_state(auto_update=True)

    def _on_next(self, e):
        if self.simulator:
            self.simulator.next_step()
            self._sync_step_state(auto_update=True)

    def _on_prev(self, e):
        if self.simulator:
            self.simulator.prev_step()
            self._sync_step_state(auto_update=True)

    def _on_reset(self, e):
        if self.simulator:
            self.simulator.reset()
            self._sync_step_state(auto_update=True)

    def _sync_step_state(self, auto_update: bool = True):
        if not self.simulator:
            return
        st = self.simulator.current_step
        self.active_states = set(st["active_states"])
        self.active_edges = {(u, v) for (u, _, v) in st["active_transitions"]}

        total_steps = len(self.simulator.steps) - 1
        cur = st["step"]
        self.btn_prev.disabled = cur <= 0
        self.btn_next.disabled = cur >= total_steps
        self.btn_reset.disabled = total_steps == 0 and cur == 0

        read_txt = st["read_prefix"] if st["read_prefix"] else "λ (inicio)"
        rem_txt = st["remaining"] if st["remaining"] else "∅ (fin)"
        act_list = ", ".join(sorted(self.active_states)) if self.active_states else "∅ (Estado muerto)"

        self.step_info.value = (
            f"Paso {cur}/{total_steps} | Leído: [{read_txt}] | Restante: [{rem_txt}] | "
            f"Estados activos: {{{act_list}}}"
        )

        if st["is_final_step"]:
            if st["accepted"]:
                self.verdict_badge.value = "✔ CADENA ACEPTADA"
                self.verdict_badge.color = ft.colors.GREEN_400
            else:
                self.verdict_badge.value = "✘ CADENA RECHAZADA"
                self.verdict_badge.color = ft.colors.RED_400
        else:
            self.verdict_badge.value = ""

        self._redraw(auto_update=auto_update)

    # --- Renderizado geométrico en Canvas ---

    def _group_transitions(self) -> Dict[Tuple[str, str], List[str]]:
        grouped: Dict[Tuple[str, str], List[str]] = {}
        if not self.automata:
            return grouped
        for u, tdict in self.automata.transitions.items():
            for sym, targets in tdict.items():
                disp = "λ" if sym in ("lambda", "λ", "") else sym
                for v in targets:
                    grouped.setdefault((u, v), []).append(disp)
        for pair in grouped:
            grouped[pair] = sorted(set(grouped[pair]))
        return grouped

    def _draw_arrowhead(self, shapes: list, tip_x: float, tip_y: float, angle: float, color: str):
        arrow_len = 10.0
        spread = math.pi / 7.0
        x1 = tip_x - arrow_len * math.cos(angle - spread)
        y1 = tip_y - arrow_len * math.sin(angle - spread)
        x2 = tip_x - arrow_len * math.cos(angle + spread)
        y2 = tip_y - arrow_len * math.sin(angle + spread)
        shapes.append(
            cv.Path(
                elements=[
                    cv.Path.MoveTo(tip_x, tip_y),
                    cv.Path.LineTo(x1, y1),
                    cv.Path.LineTo(x2, y2),
                    cv.Path.Close(),
                ],
                paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
            )
        )

    def _redraw(self, auto_update: bool = True):
        shapes = []
        if not self.automata:
            self.canvas.shapes = shapes
            if auto_update:
                self.update()
            return

        positions = self.layout.positions
        grouped = self._group_transitions()
        r = self.NODE_RADIUS

        # 1. Flecha de estado inicial
        init_st = self.automata.initial_state
        if init_st in positions:
            ix, iy = positions[init_st]
            start_x = ix - r - 28.0
            end_x = ix - r - 2.0
            shapes.append(
                cv.Line(start_x, iy, end_x, iy, paint=ft.Paint(color=ft.colors.CYAN_400, stroke_width=2.5))
            )
            self._draw_arrowhead(shapes, end_x, iy, 0.0, ft.colors.CYAN_400)

        # 2. Aristas (transiciones)
        for (u, v), symbols in grouped.items():
            if u not in positions or v not in positions:
                continue
            label = ", ".join(symbols)
            is_active = (u, v) in self.active_edges
            edge_color = ft.colors.AMBER_400 if is_active else ft.colors.ON_SURFACE_VARIANT
            stroke_w = 3.0 if is_active else 1.6
            paint = ft.Paint(color=edge_color, stroke_width=stroke_w, style=ft.PaintingStyle.STROKE)

            x1, y1 = positions[u]
            x2, y2 = positions[v]

            if u == v:
                # Auto-ciclo sobre el mismo estado (bucle superior)
                loop_top = y1 - r - 38.0
                c1x, c1y = x1 - 24.0, loop_top
                c2x, c2y = x1 + 24.0, loop_top
                sx, sy = x1 - 10.0, y1 - r + 2.0
                ex, ey = x1 + 10.0, y1 - r + 2.0

                shapes.append(
                    cv.Path(
                        elements=[
                            cv.Path.MoveTo(sx, sy),
                            cv.Path.CubicTo(c1x, c1y, c2x, c2y, ex, ey),
                        ],
                        paint=paint,
                    )
                )
                self._draw_arrowhead(shapes, ex, ey, math.pi / 2.5, edge_color)
                shapes.append(
                    cv.Text(
                        x=x1,
                        y=loop_top - 6.0,
                        text=label,
                        alignment=ft.alignment.center,
                        style=ft.TextStyle(size=12, weight=ft.FontWeight.BOLD, color=edge_color),
                    )
                )
            else:
                dx = x2 - x1
                dy = y2 - y1
                dist = math.hypot(dx, dy)
                if dist < 1e-3:
                    continue
                ux, uy = dx / dist, dy / dist
                # Vector perpendicular para separar aristas bidireccionales u <-> v
                px, py = -uy, ux
                has_reverse = (v, u) in grouped
                curve_offset = 28.0 if has_reverse else 0.0

                mid_x = (x1 + x2) / 2.0 + px * curve_offset
                mid_y = (y1 + y2) / 2.0 + py * curve_offset

                # Puntos de inicio y fin en el borde de cada círculo
                ang_start = math.atan2(mid_y - y1, mid_x - x1)
                ang_end = math.atan2(y2 - mid_y, x2 - mid_x)

                sx = x1 + r * math.cos(ang_start)
                sy = y1 + r * math.sin(ang_start)
                ex = x2 - r * math.cos(ang_end)
                ey = y2 - r * math.sin(ang_end)

                if has_reverse:
                    shapes.append(
                        cv.Path(
                            elements=[
                                cv.Path.MoveTo(sx, sy),
                                cv.Path.QuadraticTo(mid_x, mid_y, ex, ey),
                            ],
                            paint=paint,
                        )
                    )
                else:
                    shapes.append(cv.Line(sx, sy, ex, ey, paint=paint))

                self._draw_arrowhead(shapes, ex, ey, ang_end, edge_color)

                # Etiqueta desplazada ligeramente del centro de la curva
                lbl_x = (x1 + x2) / 2.0 + px * (curve_offset * 0.65 + 12.0)
                lbl_y = (y1 + y2) / 2.0 + py * (curve_offset * 0.65 + 12.0)
                shapes.append(
                    cv.Text(
                        x=lbl_x,
                        y=lbl_y,
                        text=label,
                        alignment=ft.alignment.center,
                        style=ft.TextStyle(size=12, weight=ft.FontWeight.BOLD, color=edge_color),
                    )
                )

        # 3. Nodos (estados)
        for state, (sx, sy) in positions.items():
            is_active = state in self.active_states
            is_final = state in self.automata.final_states

            fill_color = ft.colors.AMBER_700 if is_active else ft.colors.BLUE_GREY_900
            border_color = ft.colors.AMBER_300 if is_active else ft.colors.LIGHT_BLUE_300

            shapes.append(
                cv.Circle(
                    x=sx,
                    y=sy,
                    radius=r,
                    paint=ft.Paint(color=fill_color, style=ft.PaintingStyle.FILL),
                )
            )
            shapes.append(
                cv.Circle(
                    x=sx,
                    y=sy,
                    radius=r,
                    paint=ft.Paint(color=border_color, stroke_width=2.5, style=ft.PaintingStyle.STROKE),
                )
            )
            if is_final:
                shapes.append(
                    cv.Circle(
                        x=sx,
                        y=sy,
                        radius=r - 5.0,
                        paint=ft.Paint(color=border_color, stroke_width=1.8, style=ft.PaintingStyle.STROKE),
                    )
                )

            shapes.append(
                cv.Text(
                    x=sx,
                    y=sy,
                    text=state,
                    alignment=ft.alignment.center,
                    style=ft.TextStyle(size=12, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                )
            )

        self.canvas.shapes = shapes
        if auto_update:
            self.update()