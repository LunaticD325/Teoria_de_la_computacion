import pytest
from automata import Automata

def test_afd_aceptacion():
    # AFD que acepta cadenas sobre {a, b} que terminan en 'a'
    af = Automata(
        alfabeto=["a", "b"],
        estados=["q0", "q1"],
        inicial="q0",
        aceptacion=["q1"],
        transiciones=[
            {"desde": "q0", "lee": "a", "hacia": "q1"},
            {"desde": "q0", "lee": "b", "hacia": "q0"},
            {"desde": "q1", "lee": "a", "hacia": "q1"},
            {"desde": "q1", "lee": "b", "hacia": "q0"},
        ]
    )
    ok_a, _ = af.simular("ba")
    ok_b, _ = af.simular("ab")
    assert ok_a is True
    assert ok_b is False

def test_afnd_lambda_clausura():
    # AFND-lambda con transiciones espontáneas
    af = Automata(
        alfabeto=["a", "b"],
        estados=["q0", "q1", "q2"],
        inicial="q0",
        aceptacion=["q2"],
        transiciones=[
            {"desde": "q0", "lee": "", "hacia": "q1"},
            {"desde": "q1", "lee": "a", "hacia": "q2"},
        ],
        tipo="AFND-lambda"
    )
    clausura_q0 = af.lambda_clausura({"q0"})
    assert clausura_q0 == {"q0", "q1"}
    
    ok, traza = af.simular("a")
    assert ok is True