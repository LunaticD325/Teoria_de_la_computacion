import pytest
from src.regex_parser import regex_to_automata, RegexParser

def test_regex_parser_valid():
    pattern = "(a+b)*ab"
    afn_lambda, dfa_min = regex_to_automata(pattern)
    
    # Probar cadenas aceptadas y rechazadas
    assert dfa_min.simulate_direct("ab")[0] is True
    assert dfa_min.simulate_direct("aab")[0] is True
    assert dfa_min.simulate_direct("bab")[0] is True
    assert dfa_min.simulate_direct("a")[0] is False
    assert dfa_min.simulate_direct("b")[0] is False

def test_regex_parser_invalid():
    with pytest.raises(ValueError) as excinfo:
        RegexParser("(a+b").parse()
    assert "Se esperaba ')'" in str(excinfo.value)