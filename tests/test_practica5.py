import pytest
from src.automata import Automata
from src.regex_parser import regex_to_automata
from src.visualizer_core import AutomatonLayout, StepSimulator


def test_unique_state_positions():
    _, dfa_min = regex_to_automata("(a+b)*abb")
    layout = AutomatonLayout(width=800, height=500)
    positions = layout.compute_initial_positions(dfa_min)

    assert len(positions) == len(dfa_min.states)
    # Verificar que no haya dos estados en exactamente la misma coordenada (x, y)
    coords = list(positions.values())
    assert len(set(coords)) == len(coords)


def test_step_simulator_matches_direct_simulation():
    # AFN-lambda construido por Thompson para (a+b)*ab
    afn_lambda, dfa_min = regex_to_automata("(a+b)*ab")
    test_strings = ["", "ab", "aab", "bab", "a", "b", "abba"]

    for aut in (afn_lambda, dfa_min):
        sim = StepSimulator(aut)
        for s in test_strings:
            expected_acc, _ = aut.simulate_direct(s)
            steps = sim.load_string(s)

            assert len(steps) == len(s) + 1
            assert sim.accepted == expected_acc
            assert steps[-1]["accepted"] == expected_acc


def test_step_navigation_forward_and_backward():
    trans = {
        "q0": {"a": {"q1"}},
        "q1": {"b": {"q2"}},
    }
    aut = Automata({"q0", "q1", "q2"}, {"a", "b"}, trans, "q0", {"q2"})
    sim = StepSimulator(aut)
    sim.load_string("ab")

    assert sim.current_step["step"] == 0
    assert sim.current_step["active_states"] == {"q0"}

    s1 = sim.next_step()
    assert s1["step"] == 1
    assert s1["read_prefix"] == "a"
    assert s1["active_states"] == {"q1"}
    assert ("q0", "a", "q1") in s1["active_transitions"]

    s2 = sim.next_step()
    assert s2["step"] == 2
    assert s2["accepted"] is True
    assert s2["active_states"] == {"q2"}

    # Retroceder un paso
    back = sim.prev_step()
    assert back["step"] == 1
    assert back["active_states"] == {"q1"}
    