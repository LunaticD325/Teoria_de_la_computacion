import os
import pytest
from automata import Automata
from formatos import (
    guardar_jff, cargar_jff,
    guardar_json, cargar_json,
    guardar_xml, cargar_xml
)

@pytest.fixture
def automata_prueba():
    return Automata(
        alfabeto=["a", "b"],
        estados=["q0", "q1"],
        inicial="q0",
        aceptacion=["q1"],
        transiciones=[
            {"desde": "q0", "lee": "a", "hacia": "q1"},
            {"desde": "q0", "lee": "", "hacia": "q1"}
        ],
        tipo="AFND-lambda"
    )

def test_conversion_jff(tmp_path, automata_prueba):
    ruta = tmp_path / "test.jff"
    guardar_jff(automata_prueba, str(ruta))
    cargado = cargar_jff(str(ruta))

    assert cargado.inicial == automata_prueba.inicial
    assert set(cargado.estados) == set(automata_prueba.estados)
    assert set(cargado.aceptacion) == set(automata_prueba.aceptacion)

def test_conversion_json(tmp_path, automata_prueba):
    ruta = tmp_path / "test.json"
    guardar_json(automata_prueba, str(ruta))
    cargado = cargar_json(str(ruta))

    assert cargado.inicial == automata_prueba.inicial
    assert set(cargado.estados) == set(automata_prueba.estados)

def test_conversion_xml(tmp_path, automata_prueba):
    ruta = tmp_path / "test.xml"
    guardar_xml(automata_prueba, str(ruta))
    cargado = cargar_xml(str(ruta))

    assert cargado.inicial == automata_prueba.inicial
    assert set(cargado.estados) == set(automata_prueba.estados)