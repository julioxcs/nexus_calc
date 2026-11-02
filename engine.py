"""
MÓDULO: engine.py
PROJETO: NEXUS CALC — Motor Aritmético de Alta Precisão
DESCRICAO:
    Implementa a lógica matemática do sistema utilizando a biblioteca Decimal
    para precisão arbitrária. Suporta operações básicas (+, -, ×, ÷),
    operações científicas/financeiras (potência, raiz quadrada, inverso, módulo, porcentagem),
    configuração dinâmica de precisão e geração de metadados didáticos.
"""

from decimal import Decimal, InvalidOperation, getcontext
from typing import Dict, Any, Optional


def definir_precisao(casas: int) -> None:
    """Configura o número de dígitos significativos para o contexto global do Decimal."""
    casas_validas = max(2, min(int(casas), 50))
    getcontext().prec = casas_validas


def converter_para_decimal(valor: Any) -> Decimal:
    """
    Converte uma entrada (string, int ou float) para Decimal com segurança.
    Substitui vírgula por ponto para suportar o formato brasileiro.
    Lança ValueError se a conversão for impossível.
    """
    if valor is None:
        raise ValueError("O valor informado não pode ser nulo.")

    texto = str(valor).strip()
    if not texto:
        raise ValueError("O campo numérico não pode estar vazio.")

    # Suporte a vírgula brasileira
    texto = texto.replace(",", ".")

    try:
        return Decimal(texto)
    except InvalidOperation as exc:
        raise ValueError(f"'{valor}' não é um número válido.") from exc


def formatar_numero(
    valor: Decimal,
    separador_milhar: bool = False,
    notacao_cientifica: bool = False
) -> str:
    """
    Formata um Decimal para exibição:
    - Suporta notação científica se solicitado.
    - Suporta separador de milhar no padrão brasileiro (1.234,56).
    - Remove zeros decimais irrelevantes em números inteiros.
    """
    if notacao_cientifica:
        return f"{valor:E}"

    # Caso seja número inteiro exato
    if valor == valor.to_integral():
        val_int = valor.quantize(Decimal(1))
        if separador_milhar:
            return f"{int(val_int):,}".replace(",", ".")
        return str(val_int)

    # Caso tenha parte fracionária
    normalizado = valor.normalize()
    texto_raw = f"{normalizado:f}"

    if separador_milhar:
        if "." in texto_raw:
            partes = texto_raw.split(".")
            parte_inteira = f"{int(partes[0]):,}".replace(",", ".")
            return f"{parte_inteira},{partes[1]}"
        return f"{int(texto_raw):,}".replace(",", ".")

    return texto_raw


# ==============================================================================
# FUNÇÕES ARITMÉTICAS PURAS
# ==============================================================================

def somar(a: Decimal, b: Decimal) -> Decimal:
    """Soma aritmética: a + b."""
    return a + b


def subtrair(a: Decimal, b: Decimal) -> Decimal:
    """Subtração aritmética: a - b."""
    return a - b


def multiplicar(a: Decimal, b: Decimal) -> Decimal:
    """Multiplicação aritmética: a × b."""
    return a * b


def dividir(a: Decimal, b: Decimal) -> Decimal:
    """
    Divisão aritmética: a ÷ b.
    Lança ZeroDivisionError se b for zero.
    """
    if b == Decimal(0):
        raise ZeroDivisionError("Divisão por zero não é permitida na matemática.")
    return a / b


def potencia(a: Decimal, b: Decimal) -> Decimal:
    """Potenciação: a ^ b."""
    try:
        return a ** b
    except (InvalidOperation, ZeroDivisionError) as exc:
        raise ValueError("Operação de potência inválida para os operandos fornecidos.") from exc


def raiz_quadrada(a: Decimal) -> Decimal:
    """Raiz quadrada: √a. Lança ValueError se a < 0."""
    if a < Decimal(0):
        raise ValueError("Raiz quadrada de número negativo não pertence aos reais.")
    return a.sqrt()


def inverso(a: Decimal) -> Decimal:
    """Inverso multiplicativo: 1 / a. Lança ZeroDivisionError se a == 0."""
    if a == Decimal(0):
        raise ZeroDivisionError("Não é possível calcular o inverso de zero (1/0).")
    return Decimal(1) / a


def modulo(a: Decimal) -> Decimal:
    """Valor absoluto: |a|."""
    return abs(a)


def porcentagem(a: Decimal, b: Optional[Decimal] = None) -> Decimal:
    """
    Cálculo de porcentagem:
    - Se apenas 'a' for fornecido: converte a em fração (a / Decimal('100')).
    - Se 'a' e 'b' forem fornecidos: calcula a% de b: (a / Decimal('100')) * b.
    """
    if b is None:
        return a / Decimal('100')
    return (a / Decimal('100')) * b


# ==============================================================================
# MOTOR PRINCIPAL DE PROCESSAMENTO & METADADOS DIDÁTICOS
# ==============================================================================

def calcular(
    num1_raw: Any,
    num2_raw: Any,
    operacao: str,
    precisao: int = 10,
    separador_milhar: bool = False,
    notacao_cientifica: bool = False
) -> Dict[str, Any]:
    """
    Executa a operação matemática solicitada, aplicando tratamento de erros rigoroso
    e gerando a dissecação didática passo a passo para o estudante.
    """
    definir_precisao(precisao)

    resposta: Dict[str, Any] = {
        "sucesso": False,
        "resultado": None,
        "resultado_formatado": "",
        "erro": None,
        "num1_formatado": "",
        "num2_formatado": "",
        "operacao": operacao,
        "nome_operacao": "",
        "expressao": "",
        "explicacao_passos": {}
    }

    # Validação dos dados de entrada
    try:
        a = converter_para_decimal(num1_raw)
    except ValueError as e:
        resposta["erro"] = f"Operando A inválido: {str(e)}"
        return resposta

    str_a = formatar_numero(a, separador_milhar, notacao_cientifica)
    resposta["num1_formatado"] = str_a

    # Operações unárias (que usam apenas um número)
    op_clean = operacao.strip()
    is_unaria = (op_clean in ("√", "sqrt", "1/x", "inv", "|x|", "abs")) or (
        op_clean in ("%", "porcento", "Porcentagem", "% Porcentagem", "% (Porcentagem)")
        and (num2_raw is None or str(num2_raw).strip() == "")
    )

    b: Optional[Decimal] = None
    str_b = ""
    if not is_unaria:
        try:
            b = converter_para_decimal(num2_raw)
            str_b = formatar_numero(b, separador_milhar, notacao_cientifica)
            resposta["num2_formatado"] = str_b
        except ValueError as e:
            resposta["erro"] = f"Operando B inválido: {str(e)}"
            return resposta

    # Identificação do operador e mapeamento
    mapa_ops = {
        "+": ("+", "Adição"),
        "somar": ("+", "Adição"),
        "-": ("-", "Subtração"),
        "subtrair": ("-", "Subtração"),
        "×": ("×", "Multiplicação"),
        "*": ("×", "Multiplicação"),
        "multiplicar": ("×", "Multiplicação"),
        "÷": ("÷", "Divisão"),
        "/": ("÷", "Divisão"),
        "dividir": ("÷", "Divisão"),
        "^": ("^", "Potenciação"),
        "xʸ": ("^", "Potenciação"),
        "√": ("√", "Raiz Quadrada"),
        "sqrt": ("√", "Raiz Quadrada"),
        "1/x": ("1/x", "Inverso"),
        "|x|": ("|x|", "Módulo"),
        "%": ("%", "Porcentagem"),
        "Porcentagem": ("%", "Porcentagem"),
        "porcentagem": ("%", "Porcentagem"),
        "% Porcentagem": ("%", "Porcentagem"),
        "% (Porcentagem)": ("%", "Porcentagem")
    }

    if op_clean not in mapa_ops:
        resposta["erro"] = f"Operador não reconhecido: '{operacao}'."
        return resposta

    simbolo, nome = mapa_ops[op_clean]
    resposta["operacao"] = simbolo
    resposta["nome_operacao"] = nome

    # Execução condicional
    try:
        if simbolo == "+":
            res = somar(a, b)
            expressao = f"{str_a} + {str_b}"
            trecho = f"def somar(a, b):\n    return a + b\n\nresultado = somar({str_a}, {str_b})"
        elif simbolo == "-":
            res = subtrair(a, b)
            expressao = f"{str_a} - {str_b}"
            trecho = f"def subtrair(a, b):\n    return a - b\n\nresultado = subtrair({str_a}, {str_b})"
        elif simbolo == "×":
            res = multiplicar(a, b)
            expressao = f"{str_a} × {str_b}"
            trecho = f"def multiplicar(a, b):\n    return a * b\n\nresultado = multiplicar({str_a}, {str_b})"
        elif simbolo == "÷":
            res = dividir(a, b)
            expressao = f"{str_a} ÷ {str_b}"
            trecho = (
                f"def dividir(a, b):\n"
                f"    if b == 0:\n"
                f"        raise ZeroDivisionError('Divisão por zero!')\n"
                f"    return a / b\n\n"
                f"resultado = dividir({str_a}, {str_b})"
            )
        elif simbolo == "^":
            res = potencia(a, b)
            expressao = f"{str_a} ^ {str_b}"
            trecho = f"def potencia(a, b):\n    return a ** b\n\nresultado = potencia({str_a}, {str_b})"
        elif simbolo == "√":
            res = raiz_quadrada(a)
            expressao = f"√({str_a})"
            trecho = f"def raiz_quadrada(a):\n    return a.sqrt()\n\nresultado = raiz_quadrada({str_a})"
        elif simbolo == "1/x":
            res = inverso(a)
            expressao = f"1 / ({str_a})"
            trecho = f"def inverso(a):\n    return Decimal(1) / a\n\nresultado = inverso({str_a})"
        elif simbolo == "|x|":
            res = modulo(a)
            expressao = f"|{str_a}|"
            trecho = f"def modulo(a):\n    return abs(a)\n\nresultado = modulo({str_a})"
        elif simbolo == "%":
            if b is not None:
                res = porcentagem(a, b)
                expressao = f"{str_a}% de {str_b}"
                trecho = (
                    "def porcentagem(a: Decimal, b: Decimal) -> Decimal:\n"
                    "    return (a / Decimal('100')) * b\n\n"
                    f"resultado = porcentagem(Decimal('{str_a}'), Decimal('{str_b}'))"
                )
            else:
                res = porcentagem(a)
                expressao = f"{str_a}%"
                trecho = (
                    "def porcentagem(a: Decimal) -> Decimal:\n"
                    "    return a / Decimal('100')\n\n"
                    f"resultado = porcentagem(Decimal('{str_a}'))"
                )
        else:
            resposta["erro"] = "Operação não implementada."
            return resposta

        str_res = formatar_numero(res, separador_milhar, notacao_cientifica)
        resposta["sucesso"] = True
        resposta["resultado"] = res
        resposta["resultado_formatado"] = str_res
        resposta["expressao"] = f"{expressao} = {str_res}"

        # Descrições dinâmicas para o painel didático
        if simbolo == "%":
            desc_etapa3 = (
                f"A aplicação identificou a operação de Porcentagem ('%').\n"
                f"Ramo executado: `elif operacao == '%':`"
            )
            desc_etapa4 = (
                f"A função executou o cálculo percentual utilizando Decimal:\n"
                f"Fórmula: `(a / Decimal('100')) * b` com os valores ({str_a} / 100) * {str_b} = {str_res}."
                if b is not None else
                f"Fórmula: `a / Decimal('100')` com o valor {str_a} / 100 = {str_res}."
            )
        else:
            desc_etapa3 = f"A instrução condicional correspondente `if operacao == '{simbolo}':` foi atendida com sucesso."
            desc_etapa4 = "A função aritmética pura foi acionada com os valores reais da sessão."

        # Metadados Didáticos
        resposta["explicacao_passos"] = {
            "etapa1": {
                "titulo": "Etapa 1 — Entrada & Armazenamento",
                "conceito": "Variáveis e Tipagem Decimal",
                "descricao": (
                    f"Os dados fornecidos foram convertidos para a classe `Decimal` com precisão de {precisao} casas.\n"
                    f"• Operando A: `Decimal('{str_a}')`" +
                    (f"\n• Operando B: `Decimal('{str_b}')`" if b is not None else "")
                ),
                "codigo": f"a = Decimal('{str_a}')" + (f"\nb = Decimal('{str_b}')" if b is not None else "")
            },
            "etapa2": {
                "titulo": "Etapa 2 — Identificação do Operador",
                "conceito": "Controle de Entrada",
                "descricao": f"O sistema identificou o operador '{simbolo}' mapeado para a operação de {nome}.",
                "codigo": f"operacao = '{simbolo}'  # {nome}"
            },
            "etapa3": {
                "titulo": "Etapa 3 — Estrutura de Decisão",
                "conceito": "Controle de Fluxo (if / elif)",
                "descricao": desc_etapa3,
                "codigo": f"if operacao == '{simbolo}':\n    # Ramo executado com sucesso\n    resultado = {nome.lower()}(...)"
            },
            "etapa4": {
                "titulo": "Etapa 4 — Cálculo em Python",
                "conceito": "Funções Puras & Operadores",
                "descricao": desc_etapa4,
                "codigo": trecho
            },
            "etapa5": {
                "titulo": "Etapa 5 — Retorno e Exibição",
                "conceito": "Retorno de Função & Formatação",
                "descricao": f"O valor retornado foi {str_res}, formatado para o display LCD da calculadora.",
                "codigo": f"return res  # Valor retornado: {str_res}\n# Atualização do Display LCD\nst.session_state.display = '{str_res}'"
            }
        }

    except ZeroDivisionError as zde:
        resposta["erro"] = str(zde)
        resposta["explicacao_passos"] = {
            "etapa1": {
                "titulo": "Etapa 1 — Entrada & Tipagem",
                "conceito": "Variáveis",
                "descricao": f"Valores recebidos: A = {str_a}, B = {str_b}.",
                "codigo": f"a = Decimal('{str_a}')\nb = Decimal('{str_b}')"
            },
            "etapa2": {
                "titulo": "Etapa 2 — Operação de Divisão",
                "conceito": "Operação",
                "descricao": "Operação de divisão (÷) solicitada com divisor zero.",
                "codigo": "operacao = '÷'"
            },
            "etapa3": {
                "titulo": "Etapa 3 — Validação de Segurança",
                "conceito": "Prevenção de Falhas",
                "descricao": "O divisor b é igual a 0. Uma divisão matemática por zero é indefinida.",
                "codigo": "if b == 0:\n    raise ZeroDivisionError('Divisão por zero!')"
            },
            "etapa4": {
                "titulo": "Etapa 4 — Captura da Exceção",
                "conceito": "Tratamento de Erros (try/except)",
                "descricao": "O bloco `try...except ZeroDivisionError` interceptou o erro e protegeu a interface contra falhas.",
                "codigo": "try:\n    res = dividir(a, b)\nexcept ZeroDivisionError as err:\n    exibir_no_lcd('Erro: divisão por zero')"
            }
        }
    except ValueError as ve:
        resposta["erro"] = str(ve)

    return resposta
