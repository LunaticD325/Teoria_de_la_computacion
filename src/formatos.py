import json
import xml.etree.ElementTree as ET
from automata import Automata

def cargar_jff(ruta):
    """Carga un autómata desde un archivo .jff (JFLAP)."""
    tree = ET.parse(ruta)
    root = tree.getroot()
    automaton = root.find("automaton")

    estados = []
    inicial = None
    aceptacion = []
    mapa_estados = {}

    for state in automaton.findall("state"):
        sid = state.get("id")
        name = state.get("name") or f"q{sid}"
        estados.append(name)
        mapa_estados[sid] = name

        if state.find("initial") is not None:
            inicial = name
        if state.find("final") is not None:
            aceptacion.append(name)

    transiciones = []
    alfabeto = set()
    es_lambda = False

    for trans in automaton.findall("transition"):
        origen = mapa_estados[trans.find("from").text]
        destino = mapa_estados[trans.find("to").text]
        read_elem = trans.find("read")
        simbolo = read_elem.text if (read_elem is not None and read_elem.text) else ""

        if simbolo == "":
            es_lambda = True
        else:
            alfabeto.add(simbolo)

        transiciones.append({"desde": origen, "lee": simbolo, "hacia": destino})

    tipo = "AFND-lambda" if es_lambda else ("AFND" if len(transiciones) > len(set((t["desde"], t["lee"]) for t in transiciones)) else "AFD")

    return Automata(
        alfabeto=list(alfabeto),
        estados=estados,
        inicial=inicial,
        aceptacion=aceptacion,
        transiciones=transiciones,
        tipo=tipo
    )

def guardar_jff(automata, ruta):
    """Guarda un autómata en formato .jff (JFLAP)."""
    structure = ET.Element("structure")
    ET.SubElement(structure, "type").text = "fa"
    automaton = ET.SubElement(structure, "automaton")

    estado_to_id = {}
    for i, est in enumerate(sorted(list(automata.estados))):
        estado_to_id[est] = str(i)
        st = ET.SubElement(automaton, "state", id=str(i), name=est)
        ET.SubElement(st, "x").text = str(100.0 + i * 100)
        ET.SubElement(st, "y").text = "100.0"
        if est == automata.inicial:
            ET.SubElement(st, "initial")
        if est in automata.aceptacion:
            ET.SubElement(st, "final")

    for origen, map_trans in automata.transiciones.items():
        for simbolo, destinos in map_trans.items():
            for dest in destinos:
                tr = ET.SubElement(automaton, "transition")
                ET.SubElement(tr, "from").text = estado_to_id[origen]
                ET.SubElement(tr, "to").text = estado_to_id[dest]
                read_elem = ET.SubElement(tr, "read")
                read_elem.text = simbolo if simbolo not in ['', 'lambda'] else ""

    tree = ET.ElementTree(structure)
    ET.indent(tree, space="  ")
    tree.write(ruta, encoding="utf-8", xml_declaration=True)

def cargar_json(ruta):
    """Carga un autómata desde un archivo .json."""
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    return Automata(
        alfabeto=data.get("alfabeto", []),
        estados=data.get("estados", []),
        inicial=data.get("inicial", ""),
        aceptacion=data.get("aceptacion", []),
        transiciones=data.get("transiciones", []),
        tipo=data.get("tipo", "AFD")
    )

def guardar_json(automata, ruta):
    """Guarda un autómata en formato .json."""
    trans_list = []
    for origen, map_trans in automata.transiciones.items():
        for simbolo, destinos in map_trans.items():
            trans_list.append({
                "desde": origen,
                "lee": simbolo,
                "hacia": sorted(list(destinos))
            })

    data = {
        "tipo": automata.tipo,
        "alfabeto": sorted(list(automata.alfabeto)),
        "estados": sorted(list(automata.estados)),
        "inicial": automata.inicial,
        "aceptacion": sorted(list(automata.aceptacion)),
        "transiciones": trans_list
    }

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def cargar_xml(ruta):
    """Carga un autómata desde un archivo .xml personalizado."""
    tree = ET.parse(ruta)
    root = tree.getroot()

    tipo = root.get("tipo", "AFD")
    alfabeto = [s.text for s in root.find("alfabeto").findall("simbolo")]
    
    estados = []
    inicial = None
    aceptacion = []

    for est in root.find("estados").findall("estado"):
        nombre = est.get("nombre")
        estados.append(nombre)
        if est.get("inicial") == "true":
            inicial = nombre
        if est.get("aceptacion") == "true":
            aceptacion.append(nombre)

    transiciones = []
    for tr in root.find("transiciones").findall("transicion"):
        transiciones.append({
            "desde": tr.get("desde"),
            "lee": tr.get("lee") or "",
            "hacia": tr.get("hacia")
        })

    return Automata(
        alfabeto=alfabeto,
        estados=estados,
        inicial=inicial,
        aceptacion=aceptacion,
        transiciones=transiciones,
        tipo=tipo
    )

def guardar_xml(automata, ruta):
    """Guarda un autómata en formato .xml personalizado."""
    root = ET.Element("automata", tipo=automata.tipo)
    
    alf_elem = ET.SubElement(root, "alfabeto")
    for sim in sorted(list(automata.alfabeto)):
        ET.SubElement(alf_elem, "simbolo").text = sim

    est_elem = ET.SubElement(root, "estados")
    for est in sorted(list(automata.estados)):
        attribs = {"nombre": est}
        if est == automata.inicial:
            attribs["inicial"] = "true"
        if est in automata.aceptacion:
            attribs["aceptacion"] = "true"
        ET.SubElement(est_elem, "estado", **attribs)

    trans_elem = ET.SubElement(root, "transiciones")
    for origen, map_trans in automata.transiciones.items():
        for simbolo, destinos in map_trans.items():
            for dest in destinos:
                ET.SubElement(trans_elem, "transicion", desde=origen, lee=simbolo, hacia=dest)

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(ruta, encoding="utf-8", xml_declaration=True)