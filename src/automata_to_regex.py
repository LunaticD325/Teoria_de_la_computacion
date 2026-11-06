from src.automata import Automata

class StateEliminationRegex:
    """Implementa el método de eliminación de estados para convertir un AFD/AFN a Expresión Regular."""
    def __init__(self, automata: Automata):
        self.automata = automata

    def convert_to_regex_steps(self):
        """Devuelve una tupla (expresión_final, pasos_historial) eliminando estados intermedios."""
        states = list(self.automata.states)
        init_st = self.automata.initial_state
        final_sts = list(self.automata.final_states)

        q_s, q_f = "q_s", "q_f"
        trans = {}

        def add_trans(u, v, expr):
            if expr is None:
                return
            if (u, v) in trans:
                old = trans[(u, v)]
                if old in ["λ", ""]:
                    trans[(u, v)] = expr if expr not in ["λ", ""] else "λ"
                elif expr in ["λ", ""]:
                    pass
                else:
                    trans[(u, v)] = f"({old}+{expr})"
            else:
                trans[(u, v)] = expr

        # Cargar transiciones originales
        for u, tdict in self.automata.transitions.items():
            for sym, targets in tdict.items():
                label = "" if sym in ['lambda', 'λ'] else sym
                for v in targets:
                    add_trans(u, v, label)

        # Conectar q_s a init_st y final_sts a q_f
        add_trans(q_s, init_st, "")
        for f_st in final_sts:
            add_trans(f_st, q_f, "")

        steps_log = []
        middle_states = [s for s in states]

        steps_log.append({
            'action': 'Inicio con q_s y q_f',
            'removed': None,
            'transitions': dict(trans)
        })

        for state in middle_states:
            preds = set(u for (u, v) in trans.keys() if v == state and u != state)
            succs = set(v for (u, v) in trans.keys() if u == state and v != state)
            
            loop_expr = trans.get((state, state), None)
            loop_str = f"({loop_expr})*" if loop_expr and loop_expr not in ["", "λ"] else ""

            for u in preds:
                r1 = trans.get((u, state), "")
                for v in succs:
                    r2 = trans.get((state, v), "")
                    
                    # Ignorar cadenas vacías y 'λ' para evitar contaminar la expresión resultante
                    parts = [p for p in [r1, loop_str, r2] if p not in ["", "λ"]]
                    new_expr = "".join(parts) if parts else ""
                    
                    add_trans(u, v, new_expr)

            keys_to_remove = [k for k in trans.keys() if k[0] == state or k[1] == state]
            for k in keys_to_remove:
                del trans[k]

            steps_log.append({
                'action': f"Estado {state} eliminado",
                'removed': state,
                'transitions': dict(trans)
            })

        final_regex = trans.get((q_s, q_f), "λ")
        if final_regex == "":
            final_regex = "λ"
        return final_regex, steps_log