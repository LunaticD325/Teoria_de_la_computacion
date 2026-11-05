from collections import defaultdict, deque

class Automata:
    def __init__(self, alfabeto=None, estados=None, inicial=None, aceptacion=None, transiciones=None, tipo="AFD"):
        self.alfabeto = set(alfabeto) if alfabeto else set()
        self.estados = set(estados) if estados else set()
        self.inicial = inicial
        self.aceptacion = set(aceptacion) if aceptacion else set()
        # Estructura: dict[origen][simbolo] -> set(destinos)
        self.transiciones = defaultdict(lambda: defaultdict(set))
        self.tipo = tipo

        if transiciones:
            for t in transiciones:
                # t puede ser dict o tupla (desde, lee, hacia)
                if isinstance(t, dict):
                    origen = t["desde"]
                    simbolo = t["lee"]
                    destinos = t["hacia"] if isinstance(t["hacia"], list) else [t["hacia"]]
                else:
                    origen, simbolo, destinos = t[0], t[1], t[2] if isinstance(t[2], list) else [t[2]]
                
                for d in destinos:
                    self.transiciones[origen][simbolo].add(d)

    def lambda_clausura(self, estados_set):
        """Calcula la lambda-clausura (o epsilon-clausura) de un conjunto de estados."""
        if isinstance(estados_set, str):
            estados_set = {estados_set}
        
        clausura = set(estados_set)
        cola = deque(estados_set)

        while cola:
            estado = cola.popleft()
            # La transición lambda puede representarse como '' o 'lambda'
            for sim in ['', 'lambda']:
                if sim in self.transiciones[estado]:
                    for sig in self.transiciones[estado][sim]:
                        if sig not in clausura:
                            clausura.add(sig)
                            cola.append(sig)
        return clausura

    def mover(self, estados_set, simbolo):
        """Transición dado un conjunto de estados y un símbolo de entrada."""
        destinos = set()
        for estado in estados_set:
            if simbolo in self.transiciones[estado]:
                destinos.update(self.transiciones[estado][simbolo])
        return destinos

    def simular(self, cadena):
        """
        Simula el reconocimiento de una cadena en un AFD, AFND o AFND-lambda.
        Retorna (aceptada: bool, traza: list)
        """
        if not self.inicial:
            return False, ["Error: No hay estado inicial definido."]

        actuales = self.lambda_clausura({self.inicial})
        traza = [f"Inicio: {sorted(list(actuales))}"]

        for c in cadena:
            if c not in self.alfabeto:
                traza.append(f"Símbolo '{c}' no pertenece al alfabeto.")
                return False, traza

            siguientes = self.mover(actuales, c)
            actuales = self.lambda_clausura(siguientes)
            traza.append(f"Lee '{c}' -> Estados actuales: {sorted(list(actuales))}")

            if not actuales:
                break

        aceptada = bool(actuales.intersection(self.aceptacion))
        traza.append(f"Resultado: {'Aceptada' if aceptada else 'Rechazada'}")
        return aceptada, traza