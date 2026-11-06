from src.automata import Automata

class RegexNode:
    pass

class SymbolNode(RegexNode):
    def __init__(self, symbol):
        self.symbol = symbol

class UnionNode(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ConcatNode(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class StarNode(RegexNode):
    def __init__(self, child):
        self.child = child

class RegexParser:
    """Parser descendente recursivo para notación del curso (+, yuxtaposición, *)."""
    def __init__(self, pattern):
        self.pattern = pattern
        self.pos = 0

    def parse(self):
        if not self.pattern:
            return SymbolNode('')  # Expresión vacía -> lambda
        node = self._parse_union()
        if self.pos < len(self.pattern):
            raise ValueError(f"Símbolo inesperado '{self.pattern[self.pos]}' en posición {self.pos}")
        return node

    def _parse_union(self):
        left = self._parse_concat()
        while self.pos < len(self.pattern) and self.pattern[self.pos] == '+':
            self.pos += 1  # consumir '+'
            right = self._parse_concat()
            left = UnionNode(left, right)
        return left

    def _parse_concat(self):
        nodes = []
        while self.pos < len(self.pattern) and self.pattern[self.pos] not in ')+':
            nodes.append(self._parse_star())
        if not nodes:
            return SymbolNode('')
        result = nodes[0]
        for nxt in nodes[1:]:
            result = ConcatNode(result, nxt)
        return result

    def _parse_star(self):
        base = self._parse_atom()
        while self.pos < len(self.pattern) and self.pattern[self.pos] == '*':
            self.pos += 1
            base = StarNode(base)
        return base

    def _parse_atom(self):
        if self.pos >= len(self.pattern):
            raise ValueError("Expresión incompleta al final del patrón")
        ch = self.pattern[self.pos]
        if ch == '(':
            self.pos += 1  # consumir '('
            expr = self._parse_union()
            if self.pos >= len(self.pattern) or self.pattern[self.pos] != ')':
                raise ValueError(f"Se esperaba ')' correspondiente a posición {self.pos}")
            self.pos += 1  # consumir ')'
            return expr
        elif ch in '+*)':
            raise ValueError(f"Operador inesperado '{ch}' en posición {self.pos}")
        else:
            self.pos += 1
            return SymbolNode(ch)

class ThompsonBuilder:
    """Construye un AFN-lambda utilizando las construcciones de Thompson."""
    def __init__(self):
        self.state_counter = 0

    def _new_state(self):
        st = f"q{self.state_counter}"
        self.state_counter += 1
        return st

    def build(self, node):
        if isinstance(node, SymbolNode):
            s_init, s_final = self._new_state(), self._new_state()
            alphabet = {node.symbol} if node.symbol and node.symbol not in ['', 'λ', 'lambda'] else set()
            sym_trans = node.symbol if node.symbol else 'lambda'
            trans = {s_init: {sym_trans: {s_final}}}
            return Automata(
                states={s_init, s_final},
                alphabet=alphabet,
                transitions=trans,
                initial_state=s_init,
                final_states={s_final},
                tipo="AFN-lambda"
            )

        elif isinstance(node, UnionNode):
            left_afn = self.build(node.left)
            right_afn = self.build(node.right)
            s_init, s_final = self._new_state(), self._new_state()

            states = left_afn.states | right_afn.states | {s_init, s_final}
            alphabet = left_afn.alphabet | right_afn.alphabet
            
            trans = {}
            for st, tdict in list(left_afn.transitions.items()) + list(right_afn.transitions.items()):
                trans[st] = {sym: set(dsts) for sym, dsts in tdict.items()}

            trans[s_init] = {'lambda': {left_afn.initial_state, right_afn.initial_state}}
            
            for f_st in left_afn.final_states:
                trans.setdefault(f_st, {}).setdefault('lambda', set()).add(s_final)
            for f_st in right_afn.final_states:
                trans.setdefault(f_st, {}).setdefault('lambda', set()).add(s_final)

            return Automata(
                states=states,
                alphabet=alphabet,
                transitions=trans,
                initial_state=s_init,
                final_states={s_final},
                tipo="AFN-lambda"
            )

        elif isinstance(node, ConcatNode):
            left_afn = self.build(node.left)
            right_afn = self.build(node.right)

            states = left_afn.states | right_afn.states
            alphabet = left_afn.alphabet | right_afn.alphabet

            trans = {}
            for st, tdict in list(left_afn.transitions.items()) + list(right_afn.transitions.items()):
                trans[st] = {sym: set(dsts) for sym, dsts in tdict.items()}

            for f_st in left_afn.final_states:
                trans.setdefault(f_st, {}).setdefault('lambda', set()).add(right_afn.initial_state)

            return Automata(
                states=states,
                alphabet=alphabet,
                transitions=trans,
                initial_state=left_afn.initial_state,
                final_states=right_afn.final_states,
                tipo="AFN-lambda"
            )

        elif isinstance(node, StarNode):
            child_afn = self.build(node.child)
            s_init, s_final = self._new_state(), self._new_state()

            states = child_afn.states | {s_init, s_final}
            alphabet = child_afn.alphabet

            trans = {}
            for st, tdict in child_afn.transitions.items():
                trans[st] = {sym: set(dsts) for sym, dsts in tdict.items()}

            trans[s_init] = {'lambda': {child_afn.initial_state, s_final}}
            for f_st in child_afn.final_states:
                trans.setdefault(f_st, {}).setdefault('lambda', set()).update({child_afn.initial_state, s_final})

            return Automata(
                states=states,
                alphabet=alphabet,
                transitions=trans,
                initial_state=s_init,
                final_states={s_final},
                tipo="AFN-lambda"
            )

def regex_to_automata(pattern):
    """Parsea el patrón de ER y retorna el AFN-lambda de Thompson y su AFD Mínimo."""
    parser = RegexParser(pattern)
    ast = parser.parse()
    builder = ThompsonBuilder()
    afn_lambda = builder.build(ast)
    dfa, _ = afn_lambda.subset_construction()
    dfa_min = dfa.minimize()
    return afn_lambda, dfa_min