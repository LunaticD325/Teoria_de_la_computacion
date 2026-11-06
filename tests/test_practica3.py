import sys
import os
import pytest

# Añadir la raíz del proyecto al path para importar src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.automata import Automata

def test_lambda_closure():
    # AFN-lambda simple: q0 --lambda--> q1 --a--> q2
    transitions = {
        'q0': {'lambda': {'q1'}},
        'q1': {'a': {'q2'}}
    }
    afn_l = Automata({'q0', 'q1', 'q2'}, {'a'}, transitions, 'q0', {'q2'})
    
    assert afn_l.lambda_closure('q0') == {'q0', 'q1'}
    assert afn_l.lambda_closure({'q1'}) == {'q1'}

def test_equivalence_pipeline():
    # AFN-lambda de prueba: acepta cadenas que contienen 'a'
    transitions = {
        'q0': {'lambda': {'q1'}},
        'q1': {'a': {'q2'}, 'b': {'q1'}},
        'q2': {'a': {'q2'}, 'b': {'q2'}}
    }
    afn_lambda = Automata({'q0', 'q1', 'q2'}, {'a', 'b'}, transitions, 'q0', {'q2'})

    # 1. Simulación directa
    acc_direct, _ = afn_lambda.simulate_direct("ba")
    assert acc_direct is True

    # 2. Eliminación de lambda
    afn_no_lambda = afn_lambda.remove_lambda_transitions()
    
    # 3. Construcción de subconjuntos (AFD)
    afd, _ = afn_lambda.subset_construction()

    # 4. Minimización del AFD
    afd_min = afd.minimize()

    # Comprobar que el AFD mínimo no excede el número de estados del AFD
    assert len(afd_min.states) <= len(afd.states)

    # Comprobar equivalencia formal entre todos los modelos
    assert afn_lambda.is_equivalent_to(afn_no_lambda, max_len=4)
    assert afn_lambda.is_equivalent_to(afd, max_len=4)
    assert afn_lambda.is_equivalent_to(afd_min, max_len=4)