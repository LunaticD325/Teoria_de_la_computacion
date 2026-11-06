from collections import deque
import json
import xml.etree.ElementTree as ET

class Automata:
    def __init__(self, estados=None, alfabeto=None, transiciones=None, estado_inicial=None, estados_finales=None,
                 states=None, alphabet=None, transitions=None, initial_state=None, final_states=None,
                 inicial=None, finales=None, aceptacion=None, tipo="AFD"):
        
        # Resolver estado inicial y estados finales
        init_st = initial_state if initial_state is not None else (estado_inicial if estado_inicial is not None else inicial)
        fin_st = final_states if final_states is not None else (estados_finales if estados_finales is not None else (finales if finales is not None else aceptacion))

        self.states = set(states if states is not None else (estados if estados is not None else []))
        self.alphabet = set(alphabet if alphabet is not None else (alfabeto if alfabeto is not None else []))
        self.initial_state = init_st
        self.final_states = set(fin_st if fin_st is not None else [])
        self.tipo = tipo

        # Parsear transiciones (si vienen como lista de diccionarios o como diccionario anidado)
        raw_trans = transitions if transitions is not None else (transiciones if transiciones is not None else {})
        if isinstance(raw_trans, list):
            parsed_trans = {}
            for t in raw_trans:
                src = t.get("desde")
                sym = t.get("lee", "")
                dst = t.get("hacia")
                if src not in parsed_trans:
                    parsed_trans[src] = {}
                if sym not in parsed_trans[src]:
                    parsed_trans[src][sym] = set()
                
                # Manejar destino si viene como lista o elemento único
                if isinstance(dst, list):
                    parsed_trans[src][sym].update(dst)
                elif isinstance(dst, set):
                    parsed_trans[src][sym].update(dst)
                else:
                    parsed_trans[src][sym].add(dst)
            self.transitions = parsed_trans
        else:
            self.transitions = raw_trans

        # Alias para compatibilidad con pruebas anteriores
        self.estados = self.states
        self.alfabeto = self.alphabet
        self.transiciones = self.transitions
        self.estado_inicial = self.initial_state
        self.estados_finales = self.final_states
        self.inicial = self.initial_state
        self.finales = self.final_states
        self.aceptacion = self.final_states

    # Alias para compatibilidad con tests anteriores
    def simular(self, input_string):
        accepted, _ = self.simulate_direct(input_string)
        return accepted, None

    def lambda_clausura(self, states):
        return self.lambda_closure(states)

    # -------------------------------------------------------------------
    # 2.1 Cerradura Lambda y Simulación Directa
    # -------------------------------------------------------------------
    def lambda_closure(self, states):
        """Calcula la cerradura lambda de un conjunto de estados."""
        if isinstance(states, (str, int)):
            states = {states}
        closure = set(states)
        stack = list(states)

        while stack:
            curr = stack.pop()
            for l_sym in ['', 'lambda', 'λ', 'e', 'eps', 'epsilon']:
                next_states = self.transitions.get(curr, {}).get(l_sym, set())
                for nxt in next_states:
                    if nxt not in closure:
                        closure.add(nxt)
                        stack.append(nxt)
        return closure

    def simulate_direct(self, input_string):
        """Simula un AFN-lambda directamente paso a paso."""
        current_states = self.lambda_closure({self.initial_state})
        history = [("Inicio", set(), set(current_states))]

        for symbol in input_string:
            if symbol not in self.alphabet:
                return False, history
            
            next_step_states = set()
            for st in current_states:
                reached = self.transitions.get(st, {}).get(symbol, set())
                next_step_states.update(reached)
            
            closure_after = set()
            if next_step_states:
                closure_after = self.lambda_closure(next_step_states)
            
            history.append((symbol, next_step_states, closure_after))
            current_states = closure_after

        is_accepted = bool(current_states & self.final_states)
        return is_accepted, history

    # -------------------------------------------------------------------
    # 2.2 Eliminación de Transiciones Lambda
    # -------------------------------------------------------------------
    def remove_lambda_transitions(self):
        """Transforma AFN-lambda a AFN sin transiciones lambda."""
        new_transitions = {}
        new_final_states = set(self.final_states)

        for st in self.states:
            if self.lambda_closure({st}) & self.final_states:
                new_final_states.add(st)

        for st in self.states:
            new_transitions[st] = {}
            st_closure = self.lambda_closure({st})
            for sym in self.alphabet:
                reached_set = set()
                for c_st in st_closure:
                    reached_set.update(self.transitions.get(c_st, {}).get(sym, set()))
                
                full_reached = self.lambda_closure(reached_set)
                if full_reached:
                    new_transitions[st][sym] = full_reached

        return Automata(
            states=self.states,
            alphabet=self.alphabet,
            transitions=new_transitions,
            initial_state=self.initial_state,
            final_states=new_final_states
        )

    # -------------------------------------------------------------------
    # 2.3 Construcción de Subconjuntos (AFN -> AFD)
    # -------------------------------------------------------------------
    def subset_construction(self):
        """Convierte AFN/AFN-lambda a AFD equivalente."""
        start_closure = tuple(sorted(self.lambda_closure({self.initial_state})))
        
        dfa_states = {start_closure}
        unmarked = [start_closure]
        dfa_transitions = {}
        dfa_final_states = set()
        table_log = []

        while unmarked:
            current = unmarked.pop(0)
            dfa_transitions[current] = {}

            if any(st in self.final_states for st in current):
                dfa_final_states.add(current)

            for sym in sorted(self.alphabet):
                move_set = set()
                for st in current:
                    move_set.update(self.transitions.get(st, {}).get(sym, set()))
                
                closure_set = tuple(sorted(self.lambda_closure(move_set)))
                if closure_set:
                    dfa_transitions[current][sym] = closure_set
                    if closure_set not in dfa_states:
                        dfa_states.add(closure_set)
                        unmarked.append(closure_set)
                
                table_log.append((current, sym, closure_set))

        state_map = {st: f"q{i}" for i, st in enumerate(sorted(dfa_states))}
        
        named_transitions = {}
        for src, sub_dict in dfa_transitions.items():
            named_src = state_map[src]
            named_transitions[named_src] = {}
            for sym, target in sub_dict.items():
                named_transitions[named_src][sym] = {state_map[target]}

        named_initial = state_map[start_closure]
        named_finals = {state_map[st] for st in dfa_final_states}
        named_all = set(state_map.values())

        dfa = Automata(
            states=named_all,
            alphabet=self.alphabet,
            transitions=named_transitions,
            initial_state=named_initial,
            final_states=named_finals
        )
        return dfa, table_log

    # -------------------------------------------------------------------
    # 2.4 Minimización de AFD y Equivalencia
    # -------------------------------------------------------------------
    def remove_unreachable_states(self):
        """Elimina estados inaccesibles desde el estado inicial."""
        reachable = set()
        queue = [self.initial_state]
        reachable.add(self.initial_state)

        while queue:
            curr = queue.pop(0)
            for sym in self.alphabet:
                for nxt in self.transitions.get(curr, {}).get(sym, set()):
                    if nxt not in reachable:
                        reachable.add(nxt)
                        queue.append(nxt)

        new_transitions = {
            st: {sym: targets & reachable for sym, targets in self.transitions.get(st, {}).items() if targets & reachable}
            for st in reachable
        }
        return Automata(
            states=reachable,
            alphabet=self.alphabet,
            transitions=new_transitions,
            initial_state=self.initial_state,
            final_states=self.final_states & reachable
        )

    def minimize(self):
        """Minimiza un AFD eliminando inalcanzables y aplicando particiones."""
        cleaned = self.remove_unreachable_states()
        
        P = [set(cleaned.final_states), set(cleaned.states) - set(cleaned.final_states)]
        P = [p for p in P if p]
        W = [set(cleaned.final_states), set(cleaned.states) - set(cleaned.final_states)]
        W = [w for w in W if w]

        while W:
            A = W.pop(0)
            for c in cleaned.alphabet:
                X = set()
                for st in cleaned.states:
                    target = list(cleaned.transitions.get(st, {}).get(c, []))
                    if target and target[0] in A:
                        X.add(st)

                new_P = []
                for Y in P:
                    intersection = Y & X
                    difference = Y - X
                    if intersection and difference:
                        new_P.append(intersection)
                        new_P.append(difference)
                        if Y in W:
                            W.remove(Y)
                            W.append(intersection)
                            W.append(difference)
                        else:
                            if len(intersection) <= len(difference):
                                W.append(intersection)
                            else:
                                W.append(difference)
                    else:
                        new_P.append(Y)
                P = new_P

        block_map = {}
        for i, group in enumerate(P):
            for st in group:
                block_map[st] = f"q{i}"

        min_states = set(block_map.values())
        min_initial = block_map[cleaned.initial_state]
        min_finals = {block_map[st] for st in cleaned.final_states}

        min_transitions = {}
        for st in cleaned.states:
            src_name = block_map[st]
            if src_name not in min_transitions:
                min_transitions[src_name] = {}
            for sym in cleaned.alphabet:
                targets = cleaned.transitions.get(st, {}).get(sym, set())
                if targets:
                    target_st = list(targets)[0]
                    min_transitions[src_name][sym] = {block_map[target_st]}

        return Automata(
            states=min_states,
            alphabet=cleaned.alphabet,
            transitions=min_transitions,
            initial_state=min_initial,
            final_states=min_finals
        )

    def is_equivalent_to(self, other_automata, max_len=5):
        """Comprueba equivalencia entre dos autómatas."""
        symbols = list(self.alphabet | other_automata.alphabet)
        
        def generate_words(length):
            if length == 0:
                yield ""
                return
            for w in generate_words(length - 1):
                for s in symbols:
                    yield w + s

        for l in range(max_len + 1):
            for word in generate_words(l):
                acc1, _ = self.simulate_direct(word)
                acc2, _ = other_automata.simulate_direct(word)
                if acc1 != acc2:
                    return False
        return True