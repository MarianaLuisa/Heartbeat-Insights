Aqui está o `README.md` completo e finalizado para o seu repositório do Pipeline de Processamento de Dados (Python).

-----

# 🔬 Heartbeat Insights - Pipeline de Processamento de Dados (Python)

[](https://www.python.org/downloads/)
[](https://scikit-learn.org/stable/)
[](https://opensource.org/licenses/MIT)

## Visão Geral e Papel na Arquitetura

Este repositório contém o **Motor de Processamento de Dados** do projeto Heartbeat Insights. O seu objetivo é transformar dados cardiovasculares brutos em **insights acionáveis e clinicamente relevantes**, que são então enviados via API REST (POST) para o servidor Node.js/MongoDB.

**Papel na Arquitetura Híbrida:**

`Dados Brutos (.csv) → [PROCESSAMENTO PYTHON/ML] → Insights JSON → API Node.js → Frontend React`

O processamento é feito usando **Pipelines de ML** (Scikit-learn) para garantir que as análises complexas não sobrecarreguem o servidor web.

-----

## Stack Tecnológica

  * **Linguagem:** Python
  * **Manipulação de Dados:** Pandas
  * **Machine Learning:** Scikit-learn (Pipelines, ColumnTransformer, Regressão Logística)
  * **Comunicação API:** Requests
  * **Gerenciamento de Configurações:** python-dotenv

-----

## Estrutura do Projeto

A lógica de análise é dividida em módulos para garantir a modularidade e a manutenibilidade:

```
heartbeat-insights/
├── src/
│   ├── data_loader.py            # Carregamento, renomeamento e mapeamento de códigos para strings descritivas.
│   ├── ml_processor.py           # Implementa o Pipeline de ML completo (StandardScaler, OneHotEncoder, Regressão Logística).
│   ├── insight_generator.py      # Funções dedicadas à criação de insights 'dashboard', 'distributions' e 'correlations'.
│   └── __init__.py
├── run_sender.py                 # Script orquestrador principal: chama as análises, junta os insights e envia via API.
├── Heart_Disease_Prediction.csv  # Dataset de exemplo utilizado para treinamento.
├── .env                          # Arquivo de configuração (Ignorado pelo Git por questões de segurança).
└── README.md
```

-----

## Instalação e Configuração

### 1\. Pré-requisitos

1.  Python 3.8+
2.  Servidor Node.js/MongoDB do Heartbeat Insights rodando (para receber o POST).

### 2\. Instalação de Dependências

Crie um ambiente virtual e instale todas as bibliotecas necessárias:

```bash
# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/Scripts/activate 

# Instale todas as dependências do pipeline
pip install pandas scikit-learn numpy requests python-dotenv
```

### 3\. Configuração de Variáveis de Ambiente

Crie um arquivo chamado **`.env`** na **raiz** do projeto e insira as configurações de conexão da API. O script `run_sender.py` usará estas variáveis.

```
# .env (ESTE ARQUIVO DEVE SER IGNORADO PELO .gitignore)

# Variáveis para a API de Envio
ADMIN_TOKEN=seu_token_jwt_de_admin_real_aqui
API_INSIGHTS_URL=http://localhost:5000/api/analytics/insights 
```

-----

## Execução

O script `run_sender.py` é o ponto de entrada. Ele executa toda a pipeline em série.

1.  Verifique se o servidor Node.js está ativo.
2.  Execute o script no seu terminal:

<!-- end list -->

```bash
python run_sender.py
```

O console exibirá logs de progresso e, idealmente, uma lista de mensagens `Sucesso` para cada insight enviado ao banco de dados.

-----

## Insights Gerados (Valor Clínico)

O pipeline gera insights para todas as categorias da API:

| Categoria | Insight Clínico | Foco |
| :--- | :--- | :--- |
| `predictions` | **Fatores Preditivos de Risco** | Extrai os coeficientes da Regressão Logística (peso positivo/negativo de cada fator) para determinar o que mais aumenta ou diminui o risco de doença. |
| `distributions` | **Perfil de Pacientes de Risco** | Distribuição de casos confirmados por Tipo de Dor no Peito, destacando que o tipo **Assintomático** (`ChestPainType_4`) é o maior preditor de risco. |
| `correlations` | **Relação Idade vs. Capacidade Cardíaca (MaxHR)** | Gráfico de dispersão que permite ao médico avaliar se a frequência cardíaca máxima do paciente está dentro ou abaixo da curva esperada para sua idade. |
| `dashboard` | **KPIs e Prevalência** | Taxa geral de prevalência da doença e o risco associado a fatores metabólicos chave (como glicemia alta em jejum - FBS). |
| `trends` | **(Placeholder)** | Estrutura para futura análise temporal (requer dados com carimbo de tempo). |
