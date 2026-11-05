def prefijos(cadena: str):
    return [cadena[:i] for i in range(len(cadena) + 1)]

def sufijos(cadena: str):
    return [cadena[i:] for i in range(len(cadena) + 1)]

def subcadenas(cadena: str):
    res = set()
    n = len(cadena)
    for i in range(n):
        for j in range(i + 1, n + 1):
            res.add(cadena[i:j])
    return sorted(list(res))