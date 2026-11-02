"""
ARQUIVO: app.py
PROJETO: NEXUS CALC — Calculadora Científica & Profissional
DESCRICAO:
    Interface gráfica moderna estilo Hardware Virtual com display LCD,
    teclado numérico visual interativo, suporte a atalhos de teclado,
    registros de memória, precisão configurável, casos de teste acadêmicos
    e dissecação pedagógica de código ("Modo Aprendizado").

EXECUTAR:
    streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components
from decimal import Decimal

# Importações dos módulos arquiteturais do projeto
from engine import calcular, formatar_numero
from styles import CALCULATOR_CSS, KEYPAD_JS
from state import (
    inicializar_estado,
    pressionar_digito,
    pressionar_ponto,
    pressionar_backspace,
    pressionar_limpar,
    pressionar_mais_menos,
    pressionar_operador,
    pressionar_igual,
    pressionar_unaria,
    memoria_clear,
    memoria_recall,
    memoria_add,
    memoria_sub,
    carregar_do_historico,
    exportar_historico_csv
)

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA & INJEÇÃO DE DESIGN SYSTEM
# ==============================================================================
st.set_page_config(
    page_title="NEXUS CALC — Calculadora Profissional",
    page_icon="📟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção do CSS mestre e do listener JS para atalhos de teclado
st.markdown(CALCULATOR_CSS, unsafe_allow_html=True)
components.html(KEYPAD_JS, height=0)

# Inicialização do estado de sessão
inicializar_estado()


# ==============================================================================
# 2. BARRA LATERAL (SIDEBAR) — CONFIGURAÇÕES, CASOS DE TESTE & HISTÓRICO
# ==============================================================================
with st.sidebar:
    # Cabeçalho da Sidebar (Alto Contraste)
    st.markdown("""
        <div class="sidebar-brand">
            <span style="font-size: 1.8rem;">📟</span>
            <div>
                <div class="sidebar-brand-name">NEXUS CALC</div>
                <div class="sidebar-tag">FX-PRO • SCIENTIFIC EDITION</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Painel de Configurações da Calculadora
    st.markdown("#### ⚙️ Parâmetros do Motor")
    
    nova_precisao = st.slider(
        "Precisão Decimal (Casas)",
        min_value=2,
        max_value=28,
        value=st.session_state.precisao,
        help="Ajusta o contexto de precisão decimal global (decimal.getcontext().prec)."
    )
    st.session_state.precisao = nova_precisao

    c_milhar, c_sci = st.columns(2)
    with c_milhar:
        st.session_state.separador_milhar = st.checkbox(
            "Milhar (1.234)",
            value=st.session_state.separador_milhar,
            help="Ativa o separador de milhar no padrão brasileiro."
        )
    with c_sci:
        st.session_state.notacao_cientifica = st.checkbox(
            "Científica (1E+2)",
            value=st.session_state.notacao_cientifica,
            help="Exibe os resultados em notação científica exponencial."
        )

    st.markdown("---")

    # Casos de Teste Acadêmicos Pré-configurados
    st.markdown("#### 🎯 Casos de Teste")
    st.caption("Clique para carregar e calcular imediatamente no display LCD:")

    casos_predefinidos = [
        ("15 + 7", "15", "7", "+", "Adição de números inteiros"),
        ("20 - 8", "20", "8", "-", "Subtração clássica"),
        ("6 × 9", "6", "9", "×", "Multiplicação inteira"),
        ("100 ÷ 4", "100", "4", "÷", "Divisão exata"),
        ("-5 + 12", "-5", "12", "+", "Operação com número negativo"),
        ("7,5 × 2", "7.5", "2", "×", "Operação com número decimal"),
        ("15 % de 200", "15", "200", "%", "Cálculo de porcentagem: 15% de 200 = 30"),
        ("10 ÷ 0", "10", "0", "÷", "Divisão por zero (Tratamento seguro) ⚠️"),
        ("2 ^ 8", "2", "8", "^", "Potenciação (2 elevado a 8)"),
        ("√144", "144", None, "√", "Raiz quadrada de 144")
    ]

    for label, op1, op2, op, desc in casos_predefinidos:
        if st.button(f"{label}", help=desc, use_container_width=True, key=f"side_case_{label}"):
            res = calcular(
                op1,
                op2,
                op,
                precisao=st.session_state.precisao,
                separador_milhar=st.session_state.separador_milhar,
                notacao_cientifica=st.session_state.notacao_cientifica
            )
            st.session_state.ultimo_calculo = res
            if res["sucesso"]:
                st.session_state.display_val = res["resultado_formatado"]
                st.session_state.expression_str = res["expressao"].split("=")[0] + "="
            else:
                st.session_state.display_val = f"Erro: {res['erro']}"
                st.session_state.expression_str = f"{label} ="
            st.session_state.awaiting_second_operand = True
            st.rerun()

    st.markdown("---")

    # Histórico de Cálculos (Últimos 20 registros)
    st.markdown(f"#### 🕒 Histórico ({len(st.session_state.historico)})")
    if st.session_state.historico:
        for idx, item in enumerate(st.session_state.historico[:12]):
            cor_tag = "#10b981" if item["sucesso"] else "#ef4444"
            if st.button(
                f"{item['expressao']}",
                key=f"hist_btn_{idx}_{item['hora']}",
                help="Clique para recarregar esta operação no LCD",
                use_container_width=True
            ):
                carregar_do_historico(item)
                st.rerun()

        # Botões de Ação do Histórico
        col_exp, col_cls = st.columns(2)
        with col_exp:
            csv_dados = exportar_historico_csv()
            st.download_button(
                label="📥 Exportar CSV",
                data=csv_dados,
                file_name="nexus_calc_historico.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_cls:
            if st.button("🗑️ Limpar", use_container_width=True):
                st.session_state.historico = []
                st.rerun()
    else:
        st.info("Nenhuma operação registrada ainda.")


# ==============================================================================
# 3. WORKSPACE PRINCIPAL — CHASSIS DA CALCULADORA & MODO APRENDIZADO
# ==============================================================================

# Barra Superior com Status e Badges
tem_memoria = st.session_state.memory_val != Decimal(0)
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 10px;">
        <div>
            <h2 style="margin: 0; font-size: 1.6rem; font-weight: 800; color: #ffffff;">NEXUS CALC PRO</h2>
            <div style="color: #94a3b8; font-size: 0.85rem;">Sistema Aritmético de Alta Precisão & Engenharia Didática</div>
        </div>
        <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
            <span class="didactic-badge" style="border-color: rgba(16, 185, 129, 0.4); color: #34d399 !important;">✓ MOTOR DECIMAL ATIVO</span>
            <span class="didactic-badge">PRECISÃO: {st.session_state.precisao} CASAS</span>
            <span class="didactic-badge" style="border-color: rgba(245, 158, 11, 0.4); color: #fbbf24 !important;">
                {'MEMÓRIA: ' + formatar_numero(st.session_state.memory_val) if tem_memoria else 'MEMÓRIA: VAZIA'}
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Layout Principal em Duas Colunas
col_chassis, col_didatica = st.columns([1.15, 1.35], gap="large")

# ------------------------------------------------------------------------------
# COLUNA ESQUERDA: O CHASSIS DA CALCULADORA (HARDWARE VIRTUAL)
# ------------------------------------------------------------------------------
with col_chassis:
    # Seletor de Modo: Teclado Numérico Visual vs Entrada por Campos
    modo_selecionado = st.radio(
        "Modo de Operação",
        ["⌨️ Teclado Visual", "📝 Entrada por Campos"],
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown('<div class="calc-chassis">', unsafe_allow_html=True)

    # Marca do chassis e célula solar decorativa
    st.markdown("""
        <div class="chassis-brand">
            <span class="chassis-title">NEXUS FX-990 PRO • DECIMAL ENGINE</span>
            <div class="chassis-solar">
                <div class="chassis-solar-cell"></div>
                <div class="chassis-solar-cell"></div>
                <div class="chassis-solar-cell"></div>
                <div class="chassis-solar-cell"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # DISPLAY LCD
    eh_erro = str(st.session_state.display_val).startswith("Erro")
    classe_erro = "error-state" if eh_erro else ""
    memoria_visivel = "" if tem_memoria else "inactive"

    st.markdown(f"""
        <div class="lcd-screen">
            <div class="lcd-indicators">
                <span class="lcd-ind-memory {memoria_visivel}">[ M ]</span>
                <span class="lcd-ind-meta">DEG • PREC:{st.session_state.precisao}</span>
            </div>
            <div class="lcd-expression-line">{st.session_state.expression_str}</div>
            <div class="lcd-main-line {classe_erro}">{st.session_state.display_val}</div>
        </div>
    """, unsafe_allow_html=True)

    # Botões de Memória (Linha Superior)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        if st.button("MC", help="Memory Clear: Limpa o valor da memória", use_container_width=True):
            memoria_clear()
            st.rerun()
    with m2:
        if st.button("MR", help="Memory Recall: Recupera o valor da memória para a tela", use_container_width=True):
            memoria_recall()
            st.rerun()
    with m3:
        if st.button("M+", help="Memory Add: Soma o valor do display à memória", use_container_width=True):
            memoria_add()
            st.rerun()
    with m4:
        if st.button("M−", help="Memory Subtract: Subtrai o valor do display da memória", use_container_width=True):
            memoria_sub()
            st.rerun()

    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

    # MODO 1: TECLADO VISUAL NUMÉRICO
    if modo_selecionado == "⌨️ Teclado Visual":
        # Linha Científica Especial (5 Colunas)
        s1, s2, s3, s4, s5 = st.columns(5)
        with s1:
            if st.button("xʸ", help="Potenciação: x elevado a y", use_container_width=True):
                pressionar_operador("^")
                st.rerun()
        with s2:
            if st.button("√", help="Raiz quadrada de x", use_container_width=True):
                pressionar_unaria("√")
                st.rerun()
        with s3:
            if st.button("1/x", help="Inverso multiplicativo: 1 dividido por x", use_container_width=True):
                pressionar_unaria("1/x")
                st.rerun()
        with s4:
            if st.button("|x|", help="Módulo: Valor absoluto de x", use_container_width=True):
                pressionar_unaria("|x|")
                st.rerun()
        with s5:
            if st.button("%", help="Porcentagem: Operando A % de Operando B", use_container_width=True):
                pressionar_operador("%")
                st.rerun()

        st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)

        # Grade Principal do Teclado (4 Colunas)
        # Linha 1: Limpeza & Divisão
        r1_1, r1_2, r1_3, r1_4 = st.columns(4)
        with r1_1:
            if st.button("C", help="Limpar tudo (Esc)", use_container_width=True):
                pressionar_limpar()
                st.rerun()
        with r1_2:
            if st.button("⌫", help="Apagar último caractere (Backspace)", use_container_width=True):
                pressionar_backspace()
                st.rerun()
        with r1_3:
            if st.button("±", help="Inverter sinal positivo/negativo", use_container_width=True):
                pressionar_mais_menos()
                st.rerun()
        with r1_4:
            if st.button("÷", help="Operação de Divisão (/)", use_container_width=True):
                pressionar_operador("÷")
                st.rerun()

        # Linha 2: 7, 8, 9, ×
        r2_1, r2_2, r2_3, r2_4 = st.columns(4)
        with r2_1:
            if st.button("7", use_container_width=True):
                pressionar_digito("7")
                st.rerun()
        with r2_2:
            if st.button("8", use_container_width=True):
                pressionar_digito("8")
                st.rerun()
        with r2_3:
            if st.button("9", use_container_width=True):
                pressionar_digito("9")
                st.rerun()
        with r2_4:
            if st.button("×", help="Operação de Multiplicação (*)", use_container_width=True):
                pressionar_operador("×")
                st.rerun()

        # Linha 3: 4, 5, 6, -
        r3_1, r3_2, r3_3, r3_4 = st.columns(4)
        with r3_1:
            if st.button("4", use_container_width=True):
                pressionar_digito("4")
                st.rerun()
        with r3_2:
            if st.button("5", use_container_width=True):
                pressionar_digito("5")
                st.rerun()
        with r3_3:
            if st.button("6", use_container_width=True):
                pressionar_digito("6")
                st.rerun()
        with r3_4:
            if st.button("-", help="Operação de Subtração (-)", use_container_width=True):
                pressionar_operador("-")
                st.rerun()

        # Linha 4: 1, 2, 3, +
        r4_1, r4_2, r4_3, r4_4 = st.columns(4)
        with r4_1:
            if st.button("1", use_container_width=True):
                pressionar_digito("1")
                st.rerun()
        with r4_2:
            if st.button("2", use_container_width=True):
                pressionar_digito("2")
                st.rerun()
        with r4_3:
            if st.button("3", use_container_width=True):
                pressionar_digito("3")
                st.rerun()
        with r4_4:
            if st.button("+", help="Operação de Adição (+)", use_container_width=True):
                pressionar_operador("+")
                st.rerun()

        # Linha 5: 0, ., 00, =
        r5_1, r5_2, r5_3, r5_4 = st.columns(4)
        with r5_1:
            if st.button("0", use_container_width=True):
                pressionar_digito("0")
                st.rerun()
        with r5_2:
            if st.button(".", help="Ponto decimal", use_container_width=True):
                pressionar_ponto()
                st.rerun()
        with r5_3:
            if st.button("00", use_container_width=True):
                pressionar_digito("0")
                pressionar_digito("0")
                st.rerun()
        with r5_4:
            if st.button("=", help="Calcular resultado (Enter)", type="primary", use_container_width=True):
                pressionar_igual()
                st.rerun()

    # MODO 2: ENTRADA POR CAMPOS ESTRUTURADOS
    else:
        st.markdown("<div style='font-size: 0.85rem; color: #94a3b8; margin-bottom: 12px;'>Informe os operandos e selecione o operador:</div>", unsafe_allow_html=True)
        
        c_a, c_op, c_b = st.columns([2, 1.4, 2])
        with c_a:
            v_a = st.text_input("Operando A", value=st.session_state.campo_num1, key="fld_a")
        with c_op:
            ops_disponiveis = ["+", "-", "×", "÷", "%", "^"]
            idx_op = ops_disponiveis.index(st.session_state.campo_op) if st.session_state.campo_op in ops_disponiveis else 0
            v_op = st.selectbox(
                "Operador",
                ops_disponiveis,
                index=idx_op,
                format_func=lambda x: {
                    "+": "+ (Adição)",
                    "-": "- (Subtração)",
                    "×": "× (Multiplicação)",
                    "÷": "÷ (Divisão)",
                    "%": "% (Porcentagem)",
                    "^": "^ (Potência)"
                }.get(x, x),
                key="fld_op"
            )
        with c_b:
            v_b = st.text_input("Operando B", value=st.session_state.campo_num2, key="fld_b")

        # Seletor Direto de Operações Rápidas
        st.markdown("<div style='font-size: 0.75rem; color: #94a3b8; margin: 8px 0 4px 0; font-weight: 600;'>SELETOR DIRETO:</div>", unsafe_allow_html=True)
        q1, q2, q3, q4, q5 = st.columns(5)
        with q1:
            if st.button("+ Adição", use_container_width=True, key="fld_btn_add"):
                st.session_state.campo_op = "+"
                st.rerun()
        with q2:
            if st.button("- Subtração", use_container_width=True, key="fld_btn_sub"):
                st.session_state.campo_op = "-"
                st.rerun()
        with q3:
            if st.button("× Multiplicação", use_container_width=True, key="fld_btn_mul"):
                st.session_state.campo_op = "×"
                st.rerun()
        with q4:
            if st.button("÷ Divisão", use_container_width=True, key="fld_btn_div"):
                st.session_state.campo_op = "÷"
                st.rerun()
        with q5:
            if st.button("% Porcentagem", use_container_width=True, key="fld_btn_pct"):
                st.session_state.campo_op = "%"
                st.rerun()

        b_exec, b_clr = st.columns([2, 1])
        with b_exec:
            if st.button("Calcular Operação", type="primary", use_container_width=True, key="fld_btn_calc"):
                st.session_state.campo_num1 = v_a
                st.session_state.campo_num2 = v_b
                st.session_state.campo_op = v_op
                res = calcular(
                    v_a,
                    v_b,
                    v_op,
                    precisao=st.session_state.precisao,
                    separador_milhar=st.session_state.separador_milhar,
                    notacao_cientifica=st.session_state.notacao_cientifica
                )
                st.session_state.ultimo_calculo = res
                if res["sucesso"]:
                    st.session_state.display_val = res["resultado_formatado"]
                    st.session_state.expression_str = f"{res['num1_formatado']} {v_op} {res['num2_formatado']} ="
                    st.session_state.historico.insert(0, {
                        "hora": res.get("hora", "Agora"),
                        "expressao": res["expressao"],
                        "resultado": res["resultado_formatado"],
                        "sucesso": True,
                        "detalhes": res
                    })
                else:
                    st.session_state.display_val = f"Erro: {res['erro']}"
                    st.session_state.expression_str = f"{v_a} {v_op} {v_b} ="
                st.rerun()

        with b_clr:
            if st.button("Limpar", use_container_width=True, key="fld_btn_clr"):
                st.session_state.campo_num1 = ""
                st.session_state.campo_num2 = ""
                pressionar_limpar()
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# COLUNA DIREITA: PAINEL DIDÁTICO ("DISSECAÇÃO DO ALGORITMO")
# ------------------------------------------------------------------------------
with col_didatica:
    st.markdown('<div class="didactic-chassis">', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <h3 style="margin: 0; font-size: 1.25rem; color: #ffffff;">🧠 Dissecação do Algoritmo</h3>
            <span class="didactic-badge">Modo Aprendizado</span>
        </div>
        <p style="color: #94a3b8; font-size: 0.88rem; margin-bottom: 18px;">
            Acompanhe exatamente como o interpretador Python processou os dados da operação atual:
        </p>
    """, unsafe_allow_html=True)

    calc_atual = st.session_state.ultimo_calculo

    if calc_atual and calc_atual.get("explicacao_passos"):
        passos = calc_atual["explicacao_passos"]

        nomes_abas = [
            "1. Entrada",
            "2. Operação",
            "3. Decisão (if)",
            "4. Cálculo",
            "5. Retorno & LCD"
        ] if calc_atual.get("sucesso") else [
            "1. Entrada",
            "2. Operação",
            "3. Validação",
            "4. Proteção de Erro"
        ]

        abas = st.tabs(nomes_abas)

        # Aba 1: Entrada de Dados e Tipagem
        with abas[0]:
            p1 = passos.get("etapa1", {})
            st.markdown(f"**Conceito Computacional:** `{p1.get('conceito', 'Variáveis e Tipagem')}`")
            st.write(p1.get("descricao", ""))
            st.code(p1.get("codigo", ""), language="python")
            st.markdown("""
                <div class="didactic-box">
                    📌 <strong>Fundamento de Engenharia:</strong> Números em computação de ponto flutuante padrão (float) possuem erros de precisão binária (ex: 0.1 + 0.2 ≠ 0.3). O módulo <code>decimal.Decimal</code> resolve esse problema garantindo aritmética decimal exata para sistemas financeiros e científicos.
                </div>
            """, unsafe_allow_html=True)

        # Aba 2: Identificação do Operador
        with abas[1]:
            p2 = passos.get("etapa2", {})
            st.markdown(f"**Conceito Computacional:** `{p2.get('conceito', 'Mapeamento e Roteamento')}`")
            st.write(p2.get("descricao", ""))
            st.code(p2.get("codigo", ""), language="python")
            st.markdown("""
                <div class="didactic-box">
                    📌 <strong>Fundamento de Engenharia:</strong> O operador selecionado funciona como um seletor de rotas. O código normaliza caracteres matemáticos (como '×' e '*') para símbolos internos padronizados antes da tomada de decisão.
                </div>
            """, unsafe_allow_html=True)

        # Aba 3: Controle de Fluxo Condicional (if / elif)
        with abas[2]:
            p3 = passos.get("etapa3", {})
            st.markdown(f"**Conceito Computacional:** `{p3.get('conceito', 'Controle de Fluxo')}`")
            st.write(p3.get("descricao", ""))
            st.code(p3.get("codigo", ""), language="python")
            st.markdown("""
                <div class="didactic-box">
                    📌 <strong>Fundamento de Engenharia:</strong> Estruturas <code>if / elif / else</code> garantem que apenas a função matemática correta seja executada. Uma vez que uma condição é atendida como verdadeira (True), as demais são ignoradas, otimizando o processamento.
                </div>
            """, unsafe_allow_html=True)

        # Aba 4: Cálculo Efetivo da Função
        with abas[3]:
            p4 = passos.get("etapa4", {})
            st.markdown(f"**Conceito Computacional:** `{p4.get('conceito', 'Funções Puras & Operadores')}`")
            st.write(p4.get("descricao", ""))
            st.code(p4.get("codigo", ""), language="python")
            st.markdown("""
                <div class="didactic-box">
                    📌 <strong>Fundamento de Engenharia:</strong> Funções puras têm comportamento determinístico: dados os mesmos parâmetros de entrada, sempre devolvem exatamente a mesma saída, sem produzir efeitos colaterais indesejados.
                </div>
            """, unsafe_allow_html=True)

        # Aba 5: Retorno e Exibição Visual (quando houver sucesso)
        if calc_atual.get("sucesso") and len(abas) > 4:
            with abas[4]:
                p5 = passos.get("etapa5", {})
                st.markdown(f"**Conceito Computacional:** `{p5.get('conceito', 'Retorno de Função e UX')}`")
                st.write(p5.get("descricao", ""))
                st.code(p5.get("codigo", ""), language="python")
                st.markdown("""
                    <div class="didactic-box">
                        📌 <strong>Fundamento de Engenharia:</strong> O comando <code>return</code> devolve o objeto Decimal calculado para o motor de apresentação. A interface então remove resíduos decimais e atualiza o display LCD virtual.
                    </div>
                """, unsafe_allow_html=True)

    else:
        st.info("Execute qualquer cálculo no teclado para visualizar a dissecação do algoritmo.")

    st.markdown("---")

    # Fluxograma Algorítmico Mermaid
    st.markdown("#### 📐 Fluxograma Algorítmico do Sistema")
    st.caption("Diagrama formal de decisão percorrido pelo algoritmo:")

    st.markdown("""
```mermaid
graph TD
    A([Início: Usuário Dispara Ação]) --> B[Receber Operandos no Buffer]
    B --> C{Entrada Válida?}
    C -- Não --> D[Exibir Erro no LCD]
    C -- Sim --> E[Converter em Decimal com Precisão]
    E --> F{Identificar Operador}
    F -- '+' --> G[somar: a + b]
    F -- '-' --> H[subtrair: a - b]
    F -- '×' --> I[multiplicar: a * b]
    F -- '÷' --> J{Divisor == 0?}
    F -- '^' --> K[potencia: a ^ b]
    F -- '√' --> L[raiz_quadrada: √a]
    J -- Sim --> M[Lançar ZeroDivisionError]
    J -- Não --> N[dividir: a / b]
    G --> O[Formatar para o LCD]
    H --> O
    I --> O
    K --> O
    L --> O
    N --> O
    O --> P([Exibir no Display LCD em Ciano])
    M --> Q([Exibir Alerta Amigável em Vermelho])
```
    """)

    st.markdown('</div>', unsafe_allow_html=True)
