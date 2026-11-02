"""
MÓDULO: test_calculadora.py
PROJETO: NEXUS CALC
DESCRICAO:
    Testes unitários automatizados para validar a lógica matemática,
    a precisão da biblioteca Decimal e o tratamento de erros e exceções.
"""

import unittest
from decimal import Decimal
from calculadora import (
    somar,
    subtrair,
    multiplicar,
    dividir,
    converter_para_decimal,
    formatar_numero,
    calcular
)


class TestNexusCalc(unittest.TestCase):
    """Conjunto de testes unitários para a calculadora NEXUS CALC."""

    def test_somar(self):
        # Números inteiros
        self.assertEqual(somar(Decimal("15"), Decimal("7")), Decimal("22"))
        # Número negativo + positivo
        self.assertEqual(somar(Decimal("-5"), Decimal("12")), Decimal("7"))
        # Decimais (com precisão exata)
        self.assertEqual(somar(Decimal("0.1"), Decimal("0.2")), Decimal("0.3"))

    def test_subtrair(self):
        # Inteiros positivos
        self.assertEqual(subtrair(Decimal("20"), Decimal("8")), Decimal("12"))
        # Subtração resultando em negativo
        self.assertEqual(subtrair(Decimal("5"), Decimal("12")), Decimal("-7"))
        # Decimais
        self.assertEqual(subtrair(Decimal("10.5"), Decimal("0.5")), Decimal("10.0"))

    def test_multiplicar(self):
        # Inteiros
        self.assertEqual(multiplicar(Decimal("6"), Decimal("9")), Decimal("54"))
        # Decimal com inteiro
        self.assertEqual(multiplicar(Decimal("7.5"), Decimal("2")), Decimal("15.0"))
        # Negativo com positivo
        self.assertEqual(multiplicar(Decimal("-4"), Decimal("3")), Decimal("-12"))

    def test_dividir(self):
        # Divisão exata
        self.assertEqual(dividir(Decimal("100"), Decimal("4")), Decimal("25"))
        # Divisão com resultado decimal
        self.assertEqual(dividir(Decimal("10"), Decimal("4")), Decimal("2.5"))
        # Divisão com números negativos
        self.assertEqual(dividir(Decimal("-20"), Decimal("5")), Decimal("-4"))

    def test_divisao_por_zero(self):
        # Validação do tratamento da divisão por zero
        with self.assertRaises(ZeroDivisionError):
            dividir(Decimal("10"), Decimal("0"))

    def test_converter_para_decimal_com_virgula(self):
        # Suporte a vírgula brasileira
        d = converter_para_decimal("7,5")
        self.assertEqual(d, Decimal("7.5"))

    def test_converter_para_decimal_invalido(self):
        # Entrada com texto ou caracteres inválidos
        with self.assertRaises(ValueError):
            converter_para_decimal("texto_invalido")

    def test_formatar_numero(self):
        # Remoção de zeros desnecessários
        self.assertEqual(formatar_numero(Decimal("15.00")), "15")
        self.assertEqual(formatar_numero(Decimal("7.500")), "7.5")
        self.assertEqual(formatar_numero(Decimal("0.0")), "0")

    def test_calcular_orquestracao_sucesso(self):
        # Teste do fluxo completo via função calcular
        res = calcular("15", "7", "+")
        self.assertTrue(res["sucesso"])
        self.assertEqual(res["resultado_formatado"], "22")
        self.assertEqual(res["expressao"], "15 + 7 = 22")
        self.assertIn("etapa1", res["explicacao_passos"])

    def test_calcular_divisao_por_zero_segura(self):
        # Teste do fluxo seguro ao tentar dividir por zero
        res = calcular("10", "0", "÷")
        self.assertFalse(res["sucesso"])
        self.assertIn("zero", res["erro"].lower())


if __name__ == "__main__":
    unittest.main()
