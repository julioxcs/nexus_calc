"""
MÓDULO: test_engine.py
PROJETO: NEXUS CALC
DESCRICAO:
    Testes unitários automatizados para as novas funcionalidades matemáticas
    da engine científica (potência, raiz quadrada, inverso, porcentagem, módulo).
"""

import unittest
from decimal import Decimal
from engine import (
    potencia,
    raiz_quadrada,
    inverso,
    modulo,
    porcentagem,
    formatar_numero,
    definir_precisao,
    calcular
)


class TestEngine(unittest.TestCase):
    """Testes para as operações científicas do motor matemático."""

    def test_potencia(self):
        self.assertEqual(potencia(Decimal("2"), Decimal("3")), Decimal("8"))
        self.assertEqual(potencia(Decimal("5"), Decimal("2")), Decimal("25"))

    def test_raiz_quadrada(self):
        self.assertEqual(raiz_quadrada(Decimal("16")), Decimal("4"))
        self.assertEqual(raiz_quadrada(Decimal("0")), Decimal("0"))
        with self.assertRaises(ValueError):
            raiz_quadrada(Decimal("-9"))

    def test_inverso(self):
        self.assertEqual(inverso(Decimal("2")), Decimal("0.5"))
        self.assertEqual(inverso(Decimal("4")), Decimal("0.25"))
        with self.assertRaises(ZeroDivisionError):
            inverso(Decimal("0"))

    def test_modulo(self):
        self.assertEqual(modulo(Decimal("-15.5")), Decimal("15.5"))
        self.assertEqual(modulo(Decimal("10")), Decimal("10"))

    def test_porcentagem(self):
        # 15% simples
        self.assertEqual(porcentagem(Decimal("15")), Decimal("0.15"))
        # 20% de 50 = 10
        self.assertEqual(porcentagem(Decimal("20"), Decimal("50")), Decimal("10"))

    def test_formatacao_milhar(self):
        self.assertEqual(formatar_numero(Decimal("1234567"), separador_milhar=True), "1.234.567")
        self.assertEqual(formatar_numero(Decimal("1234.56"), separador_milhar=True), "1.234,56")

    def test_calcular_unaria(self):
        res = calcular("25", None, "√")
        self.assertTrue(res["sucesso"])
        self.assertEqual(res["resultado_formatado"], "5")


if __name__ == "__main__":
    unittest.main()
