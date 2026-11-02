"""
MÓDULO: styles.py
PROJETO: NEXUS CALC — Sistema de Design Profissional & Hardware Virtual
DESCRICAO:
    Define o sistema de design completo (Design System) da aplicação:
    paleta de cores corporativa, chassis físico de calculadora, display LCD
    com fontes monoespaçadas, teclado com feedback tátil (:active),
    unificação de contraste (WCAG AA) e script de atalhos de teclado.
"""

# ==============================================================================
# CSS PRINCIPAL (DESIGN SYSTEM)
# ==============================================================================
CALCULATOR_CSS = """
<style>
/* 1. IMPORTAÇÃO DE FONTES GOOGLE */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700;800&family=Share+Tech+Mono&display=swap');

/* 2. VARIÁVEIS DE DESIGN SYSTEM (:root) */
:root {
    --bg-main: #0a0f1c;
    --bg-card: #111827;
    --bg-lcd: #070d18;
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-focus: #22d3ee;
    
    --text-primary: #e5e7eb;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    
    --accent-cyan: #22d3ee;
    --accent-indigo: #4f46e5;
    --accent-emerald: #10b981;
    --accent-amber: #f59e0b;
    --accent-rose: #ef4444;

    --btn-num-bg: #1e293b;
    --btn-num-hover: #334155;
    --btn-op-bg: #4338ca;
    --btn-op-hover: #3730a3;
    --btn-fn-bg: #0f172a;
    --btn-clear-bg: #991b1b;
    --btn-clear-hover: #7f1d1d;
}

/* 3. RESET & ESTILOS GLOBAIS COM ALTO CONTRASTE */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

/* Força todo texto básico a ter contraste nítido (WCAG AA) */
p, span, label, div, h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary) !important;
}

/* Labels de Widgets do Streamlit */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span,
[data-testid="stWidgetLabel"] label {
    color: #cbd5e1 !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
}

/* Ocultar elementos padrão do Streamlit */
#MainMenu, footer, header {
    visibility: hidden;
    display: none;
}

/* 4. SIDEBAR PROFISSIONAL UNIFICADA NO TEMA ESCURO */
[data-testid="stSidebar"] {
    background-color: #0c1222 !important;
    border-right: 1px solid var(--border-subtle) !important;
    padding: 24px 18px !important;
}

[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    gap: 14px !important;
}

/* Título e Logo da Sidebar */
.sidebar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 12px;
}
.sidebar-brand-name {
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #ffffff !important;
}
.sidebar-tag {
    font-size: 0.72rem;
    color: var(--accent-cyan) !important;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}

/* Botões da Sidebar (Casos de teste) */
[data-testid="stSidebar"] div.stButton > button {
    background-color: #162033 !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 8px 12px !important;
    text-align: left !important;
    transition: all 0.15s ease !important;
}
[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #1e2c47 !important;
    border-color: var(--accent-cyan) !important;
    color: #ffffff !important;
    transform: translateY(-1px);
}

/* 5. CHASSIS DA CALCULADORA (HARDWARE FÍSICO) */
.calc-chassis {
    background: linear-gradient(165deg, #131c2e 0%, #0d1424 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 24px 22px 28px 22px;
    box-shadow: 
        0 24px 60px -12px rgba(0, 0, 0, 0.85),
        0 0 1px 1px rgba(255, 255, 255, 0.07),
        inset 0 1px 1px rgba(255, 255, 255, 0.12);
    margin: 0 auto 20px auto;
    max-width: 460px;
    position: relative;
}

/* Marca gravada no chassis */
.chassis-brand {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    padding: 0 4px;
}
.chassis-title {
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    color: #64748b !important;
    text-transform: uppercase;
}
.chassis-solar {
    display: flex;
    gap: 3px;
    background: #060911;
    border: 1px solid #1e293b;
    border-radius: 4px;
    padding: 3px 6px;
}
.chassis-solar-cell {
    width: 12px;
    height: 14px;
    background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 100%);
    border-radius: 2px;
    border: 1px solid #312e81;
}

/* 6. DISPLAY LCD PROFISSIONAL */
.lcd-screen {
    background-color: var(--bg-lcd);
    border: 1.5px solid #1e293b;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.8), 0 0 1px rgba(255, 255, 255, 0.05);
    position: relative;
    overflow: hidden;
}

/* Faixa superior de indicadores do LCD */
.lcd-indicators {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
}
.lcd-ind-memory {
    background: rgba(245, 158, 11, 0.15);
    color: #fbbf24 !important;
    border: 1px solid rgba(245, 158, 11, 0.4);
    padding: 1px 6px;
    border-radius: 4px;
}
.lcd-ind-memory.inactive {
    visibility: hidden;
}
.lcd-ind-meta {
    color: #475569 !important;
}

/* Linha de expressão secundária */
.lcd-expression-line {
    font-family: 'Share Tech Mono', 'JetBrains Mono', monospace;
    font-size: 1rem;
    color: #64748b !important;
    text-align: right;
    min-height: 22px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

/* Linha de número principal grande */
.lcd-main-line {
    font-family: 'Share Tech Mono', 'JetBrains Mono', monospace;
    font-size: 2.8rem;
    font-weight: 700;
    color: var(--accent-cyan) !important;
    text-align: right;
    line-height: 1.15;
    letter-spacing: -0.02em;
    text-shadow: 0 0 14px rgba(34, 211, 238, 0.35);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    word-break: break-all;
    margin-top: 4px;
}

.lcd-main-line.error-state {
    color: var(--accent-rose) !important;
    font-size: 1.4rem !important;
    text-shadow: 0 0 10px rgba(239, 68, 68, 0.4);
}

/* 7. TECLADO VISUAL NUMÉRICO (KEYPAD) */
/* Altura uniforme e feedback de clique em botões */
div.stButton > button {
    height: 52px !important;
    border-radius: 10px !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -2px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.12s ease-in-out !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    font-family: 'JetBrains Mono', 'Inter', monospace !important;
}

div.stButton > button:active {
    transform: translateY(2px) !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.4) !important;
}

/* Estilos específicos atribuídos dinamicamente pelo script */
.calc-btn-number, div.stButton > button[kind="secondary"] {
    background-color: var(--btn-num-bg) !important;
    color: #f8fafc !important;
}
.calc-btn-number:hover, div.stButton > button[kind="secondary"]:hover {
    background-color: var(--btn-num-hover) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

.calc-btn-operator {
    background-color: var(--btn-op-bg) !important;
    color: #ffffff !important;
}
.calc-btn-operator:hover {
    background-color: var(--btn-op-hover) !important;
    border-color: #818cf8 !important;
}

.calc-btn-equals, div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #10b981 0%, #06b6d4 100%) !important;
    color: #042f2e !important;
    font-weight: 900 !important;
    font-size: 1.4rem !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35) !important;
}
.calc-btn-equals:hover, div.stButton > button[kind="primary"]:hover {
    filter: brightness(1.1) !important;
    transform: translateY(-1px) !important;
}

.calc-btn-clear {
    background-color: var(--btn-clear-bg) !important;
    color: #ffffff !important;
}
.calc-btn-clear:hover {
    background-color: var(--btn-clear-hover) !important;
}

.calc-btn-memory {
    background-color: #0f172a !important;
    color: #93c5fd !important;
    border-color: rgba(59, 130, 246, 0.3) !important;
    font-size: 0.88rem !important;
    height: 42px !important;
}

.calc-btn-special {
    background-color: #172136 !important;
    color: #38bdf8 !important;
    font-size: 0.95rem !important;
    height: 44px !important;
}

/* 8. ABAS SUPERIORES COM ALTO CONTRASTE */
div[data-baseweb="tab-list"] {
    background-color: #0f172a !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border-subtle) !important;
    gap: 4px !important;
}
div[data-baseweb="tab"] {
    border-radius: 8px !important;
    padding: 8px 16px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: none !important;
}
div[data-baseweb="tab"][aria-selected="true"] {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
}

/* 9. INPUTS DO MODO CAMPOS */
div[data-baseweb="input"] {
    background-color: #0d1424 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.2) !important;
}
input {
    color: #ffffff !important;
    font-size: 1.05rem !important;
}

div[data-baseweb="select"] > div {
    background-color: #0d1424 !important;
    border: 1px solid #334155 !important;
    color: #ffffff !important;
}

/* 10. PAINEL DIDÁTICO ("DISSECAÇÃO DO ALGORITMO") */
.didactic-chassis {
    background: #0f172a;
    border: 1px solid var(--border-subtle);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 8px 24px -6px rgba(0, 0, 0, 0.5);
    margin-bottom: 20px;
}

.didactic-badge {
    background: rgba(34, 211, 238, 0.12);
    border: 1px solid rgba(34, 211, 238, 0.35);
    color: #67e8f9 !important;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 6px;
    letter-spacing: 0.05em;
}

.didactic-box {
    background: #131c2e;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 14px;
    font-size: 0.9rem;
    line-height: 1.5;
    color: #cbd5e1 !important;
}

/* Estilo para blocos de código */
pre, code {
    font-family: 'JetBrains Mono', monospace !important;
    background-color: #070d18 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    color: #38bdf8 !important;
}

/* Histórico em formato de cartão */
.history-entry {
    background: #131d33;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.15s ease;
}
.history-entry:hover {
    border-color: var(--accent-cyan);
    background: #192742;
}

/* Responsividade Mobile */
@media (max-width: 640px) {
    .calc-chassis {
        padding: 16px 12px;
        border-radius: 16px;
    }
    .lcd-main-line {
        font-size: 2.2rem;
    }
    div.stButton > button {
        height: 48px !important;
        font-size: 1rem !important;
    }
}
</style>
"""

# ==============================================================================
# SCRIPT JS: ATRIBUIÇÃO DE CLASSES POR FUNÇÃO & ATALHOS DE TECLADO
# ==============================================================================
KEYPAD_JS = """
<script>
// Função para marcar os botões com classes de estilo específicas
function colorizeButtons() {
    try {
        const doc = window.parent.document;
        const buttons = doc.querySelectorAll('button');
        
        buttons.forEach(btn => {
            const txt = btn.innerText.trim();
            if (['0','1','2','3','4','5','6','7','8','9','.'].includes(txt)) {
                btn.classList.add('calc-btn-number');
            } else if (['+', '-', '×', '÷', '^'].includes(txt)) {
                btn.classList.add('calc-btn-operator');
            } else if (txt === '=') {
                btn.classList.add('calc-btn-equals');
            } else if (['C', '⌫'].includes(txt)) {
                btn.classList.add('calc-btn-clear');
            } else if (['MC', 'MR', 'M+', 'M−'].includes(txt)) {
                btn.classList.add('calc-btn-memory');
            } else if (['xʸ', '√', '1/x', '|x|', '%', '±'].includes(txt)) {
                btn.classList.add('calc-btn-special');
            }
        });
    } catch(e) {}
}

// Executa em loop leve para cobrir re-renderizações do Streamlit
setInterval(colorizeButtons, 150);

// Suporte a Atalhos de Teclado Físico
if (!window.parent._nexusKeypadListenerAttached) {
    window.parent._nexusKeypadListenerAttached = true;
    window.parent.document.addEventListener('keydown', function(event) {
        // Se o usuário estiver digitando em um input de texto, não intercepta
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
            return;
        }

        const key = event.key;
        let targetText = null;

        if (key >= '0' && key <= '9') {
            targetText = key;
        } else if (key === '.' || key === ',') {
            targetText = '.';
        } else if (key === '+') {
            targetText = '+';
        } else if (key === '-') {
            targetText = '-';
        } else if (key === '*') {
            targetText = '×';
        } else if (key === '/') {
            targetText = '÷';
        } else if (key === 'Enter' || key === '=') {
            targetText = '=';
            event.preventDefault();
        } else if (key === 'Escape') {
            targetText = 'C';
        } else if (key === 'Backspace') {
            targetText = '⌫';
        }

        if (targetText) {
            const buttons = window.parent.document.querySelectorAll('button');
            for (let btn of buttons) {
                if (btn.innerText.trim() === targetText) {
                    btn.click();
                    break;
                }
            }
        }
    });
}
</script>
"""
