import itertools

def prefijos(cadena: str) -> list[str]:
    """Calcula todos los prefijos de una cadena."""
    return [cadena[:i] for i in range(len(cadena) + 1)]

def sufijos(cadena: str) -> list[str]:
    """Calcula todos los sufijos de una cadena."""
    return [cadena[i:] for i in range(len(cadena) + 1)]

def subcadenas(cadena: str) -> list[str]:
    """Calcula todas las subcadenas distintas de una cadena."""
    res = set()
    n = len(cadena)
    for i in range(n):
        for j in range(i + 1, n + 1):
            res.add(cadena[i:j])
    return sorted(list(res))

def generar_kleene(alfabeto: list[str], max_len: int) -> list[str]:
    """Genera la cerradura de Kleene (Sigma*) hasta una longitud máxima."""
    resultado = ["λ"]
    if max_len == 0:
        return resultado
    for n in range(1, max_len + 1):
        for p in itertools.product(alfabeto, repeat=n):
            resultado.append("".join(p))
    return resultado

def generar_positiva(alfabeto: list[str], max_len: int) -> list[str]:
    """Genera la cerradura positiva (Sigma+) hasta una longitud máxima."""
    resultado = []
    if max_len == 0:
        return resultado
    for n in range(1, max_len + 1):
        for p in itertools.product(alfabeto, repeat=n):
            resultado.append("".join(p))
    return resultado