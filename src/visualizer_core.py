import math
from typing import Dict, List, Set, Tuple, Optional
from src.automata import Automata


class AutomatonLayout:
    """Calcula y gestiona las coordenadas (x, y) de los estados de forma independiente a la GUI."""

    def __init__(self, width: float = 800.0, height: float = 480.0):
        self.width = width
        self.height = height
        self.positions: Dict[str, Tuple[float, float]] = {}

    def compute_initial_positions(self, automata: Automata) -> Dict[str, Tuple[float, float]]:
        """Asigna coordenadas únicas (x, y) a cada estado evitando colisiones."""
        states = sorted(list(automata.states))
        # Colocar el estado inicial primero para una lectura natural de izquierda a derecha
        if automata.initial_state in states:
            states.remove(automata.initial_state)
            states.insert(0, automata.initial_state)

        n = len(states)
        self.positions.clear()

        if n == 0:
            return self.positions

        cx = self.width / 2.0
        cy = self.height / 2.0

        if n == 1:
            self.positions[states[0]] = (round(cx, 2), round(cy, 2))
            return self.positions

        radius = min(self.width, self.height) * 0.34
        for i, state in enumerate(states):
            # Empezar desde la izquierda (pi radianes) e ir en sentido horario
            angle = math.pi + (2.0 * math.pi * i) / n
            x = round(cx + radius * math.cos(angle), 2)
            y = round(cy + radius * math.sin(angle), 2)
            self.positions[state] = (x, y)

        return self.positions

    def move_state(self, state: str, x: float, y: float, margin: float = 35.0) -> Tuple[float, float]:
        """Actualiza la posición de un estado al ser arrastrado dentro de los límites del lienzo."""
        clamped_x = max(margin, min(self.width - margin, round(x, 2)))
        clamped_y = max(margin, min(self.height - margin, round(y, 2)))
        self.positions[state] = (clamped_x, clamped_y)
        return self.positions[state]


class StepSimulator:
    """Simulador paso a paso para AFD, AFN y AFN-lambda con historial navegable."""

    def __init__(self, automata: Automata):
        self.automata = automata
        self.input_string: str = ""
        self.steps: List[Dict] = []
        self.current_index: int = 0
        self.accepted: bool = False

    def _lambda_closure(self, states: Set[str]) -> Tuple[Set[str], List[Tuple[str, str, str]]]:
        """Calcula la cerradura lambda y registra las transiciones lambda recorridas."""
        closure = set(states)
        stack = list(states)
        lambda_edges: List[Tuple[str, str, str]] = []

        while stack:
            curr = stack.pop()
            tdict = self.automata.transitions.get(curr, {})
            for sym in ("lambda", "λ", ""):
                for nxt in tdict.get(sym, set()):
                    lambda_edges.append((curr, "λ", nxt))
                    if nxt not in closure:
                        closure.add(nxt)
                        stack.append(nxt)

        return closure, lambda_edges

    def load_string(self, input_string: str) -> List[Dict]:
        """Precalcula toda la traza de ejecución símbolo por símbolo."""
        self.input_string = input_string
        self.steps = []
        self.current_index = 0

        init_set = {self.automata.initial_state} if self.automata.initial_state else set()
        current_states, init_lambda_edges = self._lambda_closure(init_set)

        self.steps.append({
            "step": 0,
            "symbol": None,
            "read_prefix": "",
            "remaining": input_string,
            "active_states": set(current_states),
            "active_transitions": init_lambda_edges,
            "is_final_step": len(input_string) == 0,
            "accepted": bool(current_states & self.automata.final_states) if len(input_string) == 0 else None,
        })

        for idx, ch in enumerate(input_string):
            next_raw: Set[str] = set()
            used_edges: List[Tuple[str, str, str]] = []

            for st in current_states:
                targets = self.automata.transitions.get(st, {}).get(ch, set())
                for dst in targets:
                    next_raw.add(dst)
                    used_edges.append((st, ch, dst))

            closed_next, lambda_edges = self._lambda_closure(next_raw)
            all_edges = used_edges + lambda_edges
            is_last = idx == len(input_string) - 1
            is_acc = bool(closed_next & self.automata.final_states) if is_last else None

            self.steps.append({
                "step": idx + 1,
                "symbol": ch,
                "read_prefix": input_string[: idx + 1],
                "remaining": input_string[idx + 1 :],
                "active_states": set(closed_next),
                "active_transitions": all_edges,
                "is_final_step": is_last,
                "accepted": is_acc,
            })
            current_states = closed_next

        self.accepted = bool(current_states & self.automata.final_states)
        return self.steps

    @property
    def current_step(self) -> Dict:
        if not self.steps:
            self.load_string("")
        return self.steps[self.current_index]

    def next_step(self) -> Dict:
        if self.current_index < len(self.steps) - 1:
            self.current_index += 1
        return self.current_step

    def prev_step(self) -> Dict:
        if self.current_index > 0:
            self.current_index -= 1
        return self.current_step

    def reset(self) -> Dict:
        self.current_index = 0
        return self.current_step