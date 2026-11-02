"""
MÓDULO: state.py
PROJETO: NEXUS CALC
DESCRICAO:
    Gerenciamento de estado da calculadora, máquina de estados do teclado visual,
    registros de memória (MC, MR, M+, M-), histórico de até 20 cálculos
    e exportação de dados em CSV.
"""

import csv
import io
import streamlit as st
from decimal import Decimal
from datetime import datetime
from typing import Dict, Any, List
from engine import calcular, formatar_numero, converter_para_decimal


def inicializar_estado() -> None:
    """Inicializa as variáveis de sessão no Streamlit de forma limpa e consistente."""
    if "display_val" not in st.session_state:
        st.session_state.display_val = "22"

    if "expression_str" not in st.session_state:
        st.session_state.expression_str = "15 + 7 ="

    if "memory_val" not in st.session_state:
        st.session_state.memory_val = Decimal(0)

    if "pending_first_operand" not in st.session_state:
        st.session_state.pending_first_operand = None

    if "pending_op" not in st.session_state:
        st.session_state.pending_op = None

    if "awaiting_second_operand" not in st.session_state:
        st.session_state.awaiting_second_operand = True

    if "precisao" not in st.session_state:
        st.session_state.precisao = 8

    if "separador_milhar" not in st.session_state:
        st.session_state.separador_milhar = False

    if "notacao_cientifica" not in st.session_state:
        st.session_state.notacao_cientifica = False

    if "historico" not in st.session_state:
        st.session_state.historico = []

    if "ultimo_calculo" not in st.session_state:
        # Pré-computa o cálculo inicial (15 + 7 = 22) para que as abas didáticas já comecem preenchidas
        res_padrao = calcular("15", "7", "+", st.session_state.precisao)
        st.session_state.ultimo_calculo = res_padrao
        st.session_state.historico.append({
            "hora": datetime.now().strftime("%H:%M:%S"),
            "expressao": "15 + 7 = 22",
            "resultado": "22",
            "sucesso": True,
            "detalhes": res_padrao
        })

    # Campos do modo alternativo "Campos"
    if "campo_num1" not in st.session_state:
        st.session_state.campo_num1 = "15"
    if "campo_num2" not in st.session_state:
        st.session_state.campo_num2 = "7"
    if "campo_op" not in st.session_state:
        st.session_state.campo_op = "+"


# ==============================================================================
# AÇÕES DO TECLADO NUMÉRICO (MÁQUINA DE ESTADOS)
# ==============================================================================

def pressionar_digito(digito: str) -> None:
    """Insere um dígito numérico (0 a 9) no buffer do display LCD."""
    disp = str(st.session_state.display_val)

    if st.session_state.awaiting_second_operand or disp == "0" or disp.startswith("Erro"):
        st.session_state.display_val = digito
        st.session_state.awaiting_second_operand = False
    else:
        # Limita o comprimento do display para manter a estética do LCD
        if len(disp) < 18:
            st.session_state.display_val = disp + digito


def pressionar_ponto() -> None:
    """Insere o ponto decimal no display se já não houver um."""
    disp = str(st.session_state.display_val)

    if st.session_state.awaiting_second_operand or disp.startswith("Erro"):
        st.session_state.display_val = "0."
        st.session_state.awaiting_second_operand = False
    elif "." not in disp and "," not in disp:
        st.session_state.display_val = disp + "."


def pressionar_backspace() -> None:
    """Apaga o último caractere digitado (botão ⌫)."""
    disp = str(st.session_state.display_val)
    if disp.startswith("Erro") or len(disp) <= 1:
        st.session_state.display_val = "0"
    else:
        st.session_state.display_val = disp[:-1]


def pressionar_limpar() -> None:
    """Limpa o display e a operação pendente (botão C)."""
    st.session_state.display_val = "0"
    st.session_state.expression_str = ""
    st.session_state.pending_first_operand = None
    st.session_state.pending_op = None
    st.session_state.awaiting_second_operand = False


def pressionar_mais_menos() -> None:
    """Inverte o sinal do número atualmente em tela (botão ±)."""
    disp = str(st.session_state.display_val)
    if disp == "0" or disp.startswith("Erro"):
        return
    if disp.startswith("-"):
        st.session_state.display_val = disp[1:]
    else:
        st.session_state.display_val = "-" + disp


def pressionar_operador(op: str) -> None:
    """Registra o operador binário (+, -, ×, ÷, ^) e prepara a tela para o segundo operando."""
    disp = str(st.session_state.display_val)
    if disp.startswith("Erro"):
        return

    # Se já havia uma operação pendente e o usuário digitou um novo número, resolve a anterior primeiro
    if st.session_state.pending_op and not st.session_state.awaiting_second_operand:
        pressionar_igual()

    st.session_state.pending_first_operand = st.session_state.display_val
    st.session_state.pending_op = op
    st.session_state.expression_str = f"{st.session_state.display_val} {op}"
    st.session_state.awaiting_second_operand = True


def pressionar_igual() -> None:
    """Executa a operação binária pendente (=)."""
    if not st.session_state.pending_op or st.session_state.pending_first_operand is None:
        return

    op1 = st.session_state.pending_first_operand
    op2 = st.session_state.display_val
    operador = st.session_state.pending_op

    res = calcular(
        op1,
        op2,
        operador,
        precisao=st.session_state.precisao,
        separador_milhar=st.session_state.separador_milhar,
        notacao_cientifica=st.session_state.notacao_cientifica
    )

    st.session_state.ultimo_calculo = res
    if res["sucesso"]:
        st.session_state.display_val = res["resultado_formatado"]
        st.session_state.expression_str = f"{res['num1_formatado']} {operador} {res['num2_formatado']} ="
        adicionar_ao_historico(res["expressao"], res["resultado_formatado"], True, res)
    else:
        st.session_state.display_val = f"Erro: {res['erro']}"
        st.session_state.expression_str = f"{op1} {operador} {op2} ="
        adicionar_ao_historico(f"{op1} {operador} {op2} → Erro", "Erro", False, res)

    st.session_state.pending_first_operand = None
    st.session_state.pending_op = None
    st.session_state.awaiting_second_operand = True


def pressionar_unaria(op_unaria: str) -> None:
    """Executa operações de um único operando (√, 1/x, |x|, %)."""
    disp = str(st.session_state.display_val)
    if disp.startswith("Erro"):
        return

    res = calcular(
        disp,
        None,
        op_unaria,
        precisao=st.session_state.precisao,
        separador_milhar=st.session_state.separador_milhar,
        notacao_cientifica=st.session_state.notacao_cientifica
    )

    st.session_state.ultimo_calculo = res
    if res["sucesso"]:
        st.session_state.display_val = res["resultado_formatado"]
        st.session_state.expression_str = res["expressao"].split("=")[0] + "="
        adicionar_ao_historico(res["expressao"], res["resultado_formatado"], True, res)
    else:
        st.session_state.display_val = f"Erro: {res['erro']}"
        st.session_state.expression_str = f"{op_unaria}({disp}) ="
        adicionar_ao_historico(f"{op_unaria}({disp}) → Erro", "Erro", False, res)

    st.session_state.awaiting_second_operand = True


# ==============================================================================
# FUNÇÕES DE MEMÓRIA (MC, MR, M+, M-)
# ==============================================================================

def memoria_clear() -> None:
    """Zera o registrador de memória (MC)."""
    st.session_state.memory_val = Decimal(0)


def memoria_recall() -> None:
    """Recupera o valor salvo na memória para o display LCD (MR)."""
    mem_fmt = formatar_numero(
        st.session_state.memory_val,
        st.session_state.separador_milhar,
        st.session_state.notacao_cientifica
    )
    st.session_state.display_val = mem_fmt
    st.session_state.awaiting_second_operand = True


def memoria_add() -> None:
    """Soma o valor do display atual à memória (M+)."""
    try:
        val = converter_para_decimal(st.session_state.display_val)
        st.session_state.memory_val += val
        st.session_state.awaiting_second_operand = True
    except Exception:
        pass


def memoria_sub() -> None:
    """Subtrai o valor do display atual da memória (M-)."""
    try:
        val = converter_para_decimal(st.session_state.display_val)
        st.session_state.memory_val -= val
        st.session_state.awaiting_second_operand = True
    except Exception:
        pass


# ==============================================================================
# HISTÓRICO & EXPORTAÇÃO
# ==============================================================================

def adicionar_ao_historico(expressao: str, resultado: str, sucesso: bool, detalhes: Dict[str, Any]) -> None:
    """Registra uma operação no histórico (mantém até os últimos 20 registros)."""
    item = {
        "hora": datetime.now().strftime("%H:%M:%S"),
        "expressao": expressao,
        "resultado": resultado,
        "sucesso": sucesso,
        "detalhes": detalhes
    }
    st.session_state.historico.insert(0, item)
    if len(st.session_state.historico) > 20:
        st.session_state.historico = st.session_state.historico[:20]


def carregar_do_historico(item: Dict[str, Any]) -> None:
    """Recarrega um item histórico diretamente no display e na dissecação de código."""
    if item.get("sucesso"):
        st.session_state.display_val = item["resultado"]
        st.session_state.expression_str = item["expressao"].split("=")[0] + "="
    else:
        st.session_state.display_val = "Erro"
        st.session_state.expression_str = item["expressao"]
    st.session_state.ultimo_calculo = item.get("detalhes")
    st.session_state.awaiting_second_operand = True


def exportar_historico_csv() -> str:
    """Gera uma string no formato CSV com todos os cálculos realizados na sessão."""
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow(["Hora", "Expressão", "Resultado", "Status"])
    for h in st.session_state.historico:
        writer.writerow([
            h["hora"],
            h["expressao"],
            h["resultado"],
            "Sucesso" if h["sucesso"] else "Falha/Erro"
        ])
    return output.getvalue()
