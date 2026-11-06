import pytest
import random
import string
from src.automata import Automata
from src.regex_parser import regex_to_automata, RegexParser
from src.automata_to_regex import StateEliminationRegex
from src.validators import SystemValidator

def test_regex_parser_valid():
    pattern = "(a+b)*ab"
    afn_lambda, dfa_min = regex_to_automata(pattern)
    assert dfa_min.simulate_direct("ab")[0] is True
    assert dfa_min.simulate_direct("aab")[0] is True
    assert dfa_min.simulate_direct("bab")[0] is True
    assert dfa_min.simulate_direct("a")[0] is False

def test_state_elimination_regex():
    trans = {'q0': {'a': {'q1'}}}
    aut = Automata({'q0', 'q1'}, {'a'}, trans, 'q0', {'q1'})
    converter = StateEliminationRegex(aut)
    regex, steps = converter.convert_to_regex_steps()
    assert "a" in regex
    assert len(steps) > 1

def generate_500_test_strings():
    """Generador procedimental de 500+ cadenas para validación cruzada."""
    test_cases = []
    
    # 1. Emails
    for i in range(100):
        user = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=5))
        test_cases.append(("email", f"{user}@gmail.com"))
        test_cases.append(("email", f"{user}@invalid.org"))

    # 2. Teléfonos
    for i in range(100):
        digits = "".join(random.choices(string.digits, k=10))
        test_cases.append(("phone", digits))
        test_cases.append(("phone", digits[:8])) # Inválido (8 dígitos)

    # 3. URLs
    for i in range(100):
        domain = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=6))
        test_cases.append(("url", f"http://{domain}.com"))
        test_cases.append(("url", f"https://{domain}.org")) # Inválido

    return test_cases

def test_congruence_500_strings():
    test_cases = generate_500_test_strings()
    assert len(test_cases) >= 500

    validators = {
        "email": SystemValidator("email"),
        "phone": SystemValidator("phone"),
        "url": SystemValidator("url")
    }

    for v_type, test_str in test_cases:
        v = validators[v_type]
        automata_res = v.validate_with_automata(test_str)
        re_res = v.validate_with_re(test_str)
        assert automata_res == re_res, f"Discrepancia en {v_type} con cadena '{test_str}'"