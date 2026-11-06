import re
from src.regex_parser import regex_to_automata

# Notación del curso (+ para unión) y equivalencias re
VALIDATOR_PATTERNS = {
    "email": {
        "course_regex": "(a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z+0+1+2+3+4+5+6+7+8+9+.)*@gmail.com",
        "python_re": r"^[a-z0-9.]+@gmail\.com$",
        "standard_ref": "RFC 5322 (Aproximación simplificada para dominios de correo)"
    },
    "phone": {
        "course_regex": "(0+1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)(0+1+2+3+4+5+6+7+8+9)",
        "python_re": r"^\d{10}$",
        "standard_ref": "IFT - Plan Nacional de Numeración (10 dígitos en México)"
    },
    "url": {
        "course_regex": "http://(a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v+w+x+y+z)*.com",
        "python_re": r"^http://[a-z]+\.com$",
        "standard_ref": "RFC 3986 (Sintaxis genérica de URIs)"
    }
}

class SystemValidator:
    def __init__(self, name):
        if name not in VALIDATOR_PATTERNS:
            raise ValueError(f"Validador '{name}' no soportado")
        self.info = VALIDATOR_PATTERNS[name]
        self.afn, self.dfa_min = regex_to_automata(self.info["course_regex"])
        self.re_pattern = re.compile(self.info["python_re"])

    def validate_with_automata(self, text: str) -> bool:
        accepted, _ = self.dfa_min.simulate_direct(text)
        return accepted

    def validate_with_re(self, text: str) -> bool:
        return bool(self.re_pattern.fullmatch(text))