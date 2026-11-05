from lenguajes import prefijos, sufijos

def test_prefijos_cadena_vacia():
    assert prefijos("") == [""]

def test_sufijos_cadena_vacia():
    assert sufijos("") == [""]