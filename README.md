# 📟 NEXUS CALC FX-PRO — Calculadora Científica & Educativa em Python

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Engine-Decimal%20Precision-06B6D4?style=for-the-badge" alt="Decimal Engine" />
  <img src="https://img.shields.io/badge/Tests-19%20Passed-10B981?style=for-the-badge" alt="19 Tests Passed" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License" />
</p>

> **"Calcule. Explore. Entenda."**  
> Aplicação interativa de alta precisão que une a estética de uma **calculadora física profissional (hardware virtual)** com um **laboratório didático em tempo real** para dissecação de algoritmos em Python.

---

## 📌 Visão Geral do Projeto

O **NEXUS CALC** foi desenvolvido como solução de destaque para um desafio acadêmico de **Introdução à Inteligência Artificial Aplicada ao Desenvolvimento de Software**. 

O objetivo central é demonstrar, na prática, como conceitos fundamentais da ciência da computação — alocação de variáveis, precisão numérica com `Decimal`, estruturas condicionais de controle de fluxo (`if/elif/else`), modularização em funções puras e tratamento de exceções com `try/except` — articulam-se para construir um produto de software robusto, resiliente e visualmente sofisticado.

### 🎓 Desafios Acadêmicos Integrados

Este repositório foi estruturado para demonstrar a evolução contínua do software através de dois desafios avaliativos:

* **Desafio 1 — Núcleo Aritmético & Modo Didático:**
  - Implementação das 4 operações fundamentais (`+`, `-`, `×`, `÷`) em funções puras sem uso de `eval()`.
  - Tratamento rigoroso de exceções (prevenção contra divisão por zero e sanitização de entradas).
  - Precisão numérica garantida com a biblioteca padrão `decimal.Decimal`.
  - Painel pedagógico ("Dissecação do Algoritmo") com as 5 etapas da mecânica interna do Python.
  - Histórico de sessão via `st.session_state` e testes unitários automatizados (`test_calculadora.py`).

* **Desafio 2 — Evolução Profissional & Cálculo Percentual:**
  - Interface estilo Hardware Virtual com display LCD retroiluminado, contraste WCAG AA e teclado tátil.
  - Implementação da operação de **Porcentagem binária** (`Operando A % de Operando B = C`) via fórmula Decimal: `(a / Decimal('100')) * b`.
  - Inclusão do Seletor Direto de operações, atalho rápido de teste (`15 % de 200 = 30`) e suporte a atalhos do teclado do computador (`Enter`, `Esc`, `Backspace`).
  - Registros completos de memória (`MC`, `MR`, `M+`, `M−`), exportação CSV e expansão da suíte para **19 testes unitários aprovados**.

---

## ✨ Principais Diferenciais

### 1. Hardware Virtual Realista & Display LCD
- **Display LCD Retroiluminado:** Exibição com estética de cristal líquido (`#070d18`), tipografia monoespaçada (*JetBrains Mono* / *Share Tech Mono*), linha secundária de expressão (`15 + 7 =`) e leitura numérica em **Ciano Neon** (`#22d3ee`).
- **Teclado Tátil Color-Coded:** Botões com feedback visual ao pressionar (`:active translateY(2px)`), agrupados por função (números, operadores, limpeza, igual e memória).
- **Atalhos de Teclado Físico:** Suporte nativo ao teclado do computador (`Enter` para calcular, `Esc` para limpar, `Backspace` para apagar, dígitos e operadores).

### 2. Motor Aritmético de Alta Precisão (`engine.py`)
- **Aritmética com `Decimal`:** Previne anomalias clássicas de ponto flutuante binário (como `0.1 + 0.2 = 0.30000000000000004`).
- **Precisão Arbitrária Configurável:** Slider dinâmico que ajusta o contexto do interpretador entre **2 e 28 casas decimais**.
- **Operações Disponíveis:**
  - *Básicas:* Adição (`+`), Subtração (`-`), Multiplicação (`×`), Divisão (`÷`).
  - *Avançadas:* Potência ($x^y$), Raiz Quadrada ($\sqrt{x}$), Inverso ($1/x$), Módulo ($|x|$), Porcentagem ($\%$).
- **Registros de Memória Completos:** `MC` (Limpar), `MR` (Recuperar), `M+` (Somar), `M−` (Subtrair), com indicador `[ M ]` no visor LCD.
- **Formatação Flexível:** Separador de milhar brasileiro (`1.234,56`) e Notação Científica (`1.5E+2`).

### 3. Modo Aprendizado ("Dissecação do Algoritmo")
Para cada cálculo executado, o painel pedagógico disseca a execução em 5 etapas interativas:
1. **Entrada & Armazenamento:** Demonstra como os dados do display foram convertidos e armazenados em memória na classe `Decimal`.
2. **Identificação do Operador:** Como a aplicação normaliza e roteia o símbolo aritmético.
3. **Decisão Condicional:** O ramo exato da cadeia `if/elif/else` que foi satisfeito.
4. **Cálculo Efetivo:** O trecho de código Python real executado pela função aritmética pura.
5. **Retorno & UX:** Como a instrução `return` devolve o valor formatado para a tela.

### 4. Histórico de Sessão & Exportação
- Armazena as últimas **20 operações** com timestamp e status.
- Clique em qualquer item do histórico para recarregá-lo no display LCD.
- Botão para **Exportar Histórico em CSV**.

---

## 🏛️ Arquitetura de Software

O projeto segue padrões modernos de engenharia com arquitetura desacoplada:

```text
nexus_calc/
├── .streamlit/
│   └── config.toml        # Configuração do tema escuro unificado (Dark Theme)
├── app.py                 # Interface do usuário (UI) e orquestração visual
├── engine.py              # Motor matemático puro e geração de metadados didáticos
├── styles.py              # Design System CSS (:root), Display LCD e scripts JS
├── state.py               # Máquina de estados do teclado, memória e histórico
├── calculadora.py         # Módulo de compatibilidade com a suíte de testes
├── test_calculadora.py    # Testes unitários das 4 operações básicas (10 testes)
├── test_engine.py         # Testes unitários das operações científicas e precisão (7 testes)
├── requirements.txt       # Dependências mínimas do projeto
├── LICENSE                # Licença de código aberto MIT
└── README.md              # Documentação completa
```

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
- Ter o **Python 3.11** ou superior instalado ([python.org](https://www.python.org/downloads/)).

### 2. Clonar o Repositório e Navegar
```bash
git clone https://github.com/SEU_USUARIO/nexus_calc.git
cd nexus_calc
```

### 3. (Opcional, mas recomendado) Criar e Ativar Ambiente Virtual
**No Windows:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**No Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 5. Executar os Testes Automatizados
Antes de abrir a tela, você pode verificar a integridade dos cálculos:
```bash
python -m unittest discover -v
```
> Resultado esperado: **17 testes aprovados (`OK`)** em milissegundos.

### 6. Iniciar a Aplicação NEXUS CALC
```bash
streamlit run app.py
```
O Streamlit abrirá automaticamente no seu navegador no endereço:  
👉 **`http://localhost:8501`**

---

## 🧪 Casos de Teste Acadêmicos Incluídos

Na barra lateral da aplicação, você encontra atalhos diretos para validar os principais cenários computacionais:

| Cenário | Entrada | Operação | Resultado | Comportamento Interno |
| :--- | :---: | :---: | :---: | :--- |
| **Inteiros** | `15` e `7` | `+` | `22` | Adição inteira com formatação limpa. |
| **Subtração** | `20` e `8` | `-` | `12` | Subtração básica via função pura `subtrair`. |
| **Multiplicação** | `6` e `9` | `×` | `54` | Multiplicação exata. |
| **Divisão Exata** | `100` e `4` | `÷` | `25` | Quociente inteiro sem casas residuais. |
| **Negativos** | `-5` e `12` | `+` | `7` | Reconhecimento de sinal unário. |
| **Decimais** | `7,5` e `2` | `×` | `15` | Tratamento da vírgula decimal brasileira. |
| **Divisão por Zero** | `10` e `0` | `÷` | ⚠️ *Erro Seguro* | Captura de `ZeroDivisionError` sem quebra de tela. |
| **Potenciação** | `2` e `8` | `^` | `256` | Exponenciação de base inteira. |
| **Raiz Quadrada** | `144` | `√` | `12` | Operação unária sobre o acumulador. |

---

## 👨‍💻 Conceitos de Programação Demonstrados

- **Instruções Sequenciais & Algoritmo:** Fluxo estruturado de leitura de operandos, validação e cálculo.
- **Tipagem com `Decimal`:** Precisão numérica sem artefatos binários.
- **Estruturas Condicionais (`if/elif/else`):** Controle de fluxo determinístico para roteamento de operadores.
- **Funções Puras:** Modularidade, idempotência e ausência de efeitos colaterais.
- **Resiliência & `try/except`:** Prevenção ativa de interrupções críticas (divisão por zero, entradas alfanuméricas inválidas).
- **Gerenciamento de Estado (`st.session_state`):** Persistência de registros em arquitetura reativa web.
- **Interface & Acessibilidade:** Conformidade visual com contraste WCAG AA e microinterações de hardware virtual.

---

## 📄 Licença

Este projeto está licenciado sob a licença **MIT** — consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.

---

<p align="center">
  Desenvolvido com apoio de Inteligência Artificial para o Desafio Acadêmico de Ciência da Computação & Programação.
</p>
