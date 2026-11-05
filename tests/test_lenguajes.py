from lenguajes import prefijos, sufijos, subcadenas, generar_kleene, generar_positiva

def test_cadena_vacia():
    assert prefijos("") == [""]
    assert sufijos("") == [""]
    assert subcadenas("") == []

def test_alfabeto_un_simbolo():
    assert generar_kleene(["a"], 2) == ["λ", "a", "aa"]
    assert generar_positiva(["a"], 2) == ["a", "aa"]

def test_prefijos_sufijos_longitud_uno():
    assert prefijos("a") == ["", "a"]
    assert sufijos("a") == ["a", ""]

def test_diferencia_kleene_positiva_longitud_cero():
    assert generar_kleene(["a", "b"], 0) == ["λ"]
    assert generar_positiva(["a", "b"], 0) == []