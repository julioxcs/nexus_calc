"""
MÓDULO DE COMPATIBILIDADE: calculadora.py
PROJETO: NEXUS CALC
DESCRICAO:
    Reexporta as funções de 'engine.py' para manter compatibilidade total
    com a suíte de testes unitários existente (test_calculadora.py).
"""

from engine import (
    converter_para_decimal,
    formatar_numero,
    somar,
    subtrair,
    multiplicar,
    dividir,
    potencia,
    raiz_quadrada,
    inverso,
    modulo,
    porcentagem,
    calcular,
    definir_precisao
)

__all__ = [
    "converter_para_decimal",
    "formatar_numero",
    "somar",
    "subtrair",
    "multiplicar",
    "dividir",
    "potencia",
    "raiz_quadrada",
    "inverso",
    "modulo",
    "porcentagem",
    "calcular",
    "definir_precisao"
]
