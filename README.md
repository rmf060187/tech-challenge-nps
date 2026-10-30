# Tech Challenge Fase 1 - Case NPS Preditivo

Trabalho de conclusão da Fase 1 da pós-graduação em AI Scientist.
Autor: Renato Maximiano Ferreira

## Objetivo

Um e-commerce em crescimento percebeu que o NPS varia muito entre clientes, mesmo quando a operação parece parecida. Hoje a nota só chega depois que a jornada termina, então a empresa não consegue agir antes.

O projeto busca responder duas perguntas:

1. Quais fatores da operação (pedido, entrega e atendimento) mais influenciam a nota de NPS?
2. Dá para identificar, antes da pesquisa, quais pedidos têm mais chance de gerar um detrator?

## Base de dados

Arquivo `data/raw/desafio_nps_fase_1.csv`, fornecido no desafio: 2.500 pedidos (um por cliente) e 19 colunas.

| Grupo -> Colunas |
Cliente -> customer_id, customer_age, customer_region, customer_tenure_months 
Pedido -> order_id, order_value, items_quantity, discount_value, payment_installments, freight_value 
Entrega -> delivery_time_days, delivery_delay_days, delivery_attempts 
Atendimento -> customer_service_contacts, resolution_time_days, complaints_count 
Satisfação e pós-compra -> nps_score (target), csat_internal_score, repeat_purchase_30d 

Classificação do NPS usada no projeto, aplicada direto na nota original (sem arredondar): abaixo de 7,0 detrator, de 7,0 até abaixo de 9,0 neutro, 9,0 ou mais promotor.

Pontos de atenção encontrados na base (detalhes no notebook 01):

- `repeat_purchase_30d` é exatamente igual a nota >= 8 em todos os pedidos, ou seja, foi derivada da target. Junto com `csat_internal_score`, fica fora do modelo por vazamento de dados.
- 121 pedidos têm atraso maior que o tempo total de entrega e 35 têm desconto maior que o valor do pedido. Foram mantidos e marcados com flags, a EDA mostra que retirá-los não muda as conclusões.

## Estrutura do repositório

```
tech-challenge-nps/
├── data/
│   ├── raw/                 # base original, sem alteração
│   └── processed/           # base tratada gerada pelo notebook 01
├── notebooks/
│   ├── 01_tratamento_dados.ipynb
│   ├── 02_eda.ipynb
│   └── 03_modelo.ipynb
├── src/
│   └── nps_utils.py         # funções usadas nos notebooks (classificação, cálculo do NPS)
├── models/
│   ├── modelo_detrator_logistica.joblib   # modelo final
│   └── ficha_modelo.json                  # variáveis, corte e métricas do modelo
├── reports/
│   ├── 01_entendimento_negocio_e_target.md
│   ├── 02_resumo_eda.md
│   └── figures/             # gráficos gerados pela EDA e pelo modelo
├── requirements.txt
└── README.md
```

## Metodologia

O projeto segue as etapas do CRISP-DM:

1. Entendimento do negócio e definição da target (`reports/01_entendimento_negocio_e_target.md`): problema de negócio, importância do NPS, áreas beneficiadas, definição da variável alvo e riscos de uso (vazamento, proxy, desbalanceamento).
2. Entendimento e preparação dos dados (`notebooks/01_tratamento_dados.ipynb`): checagem de qualidade, tratamento das inconsistências, regra de classificação da nota e marcação das colunas com vazamento.
3. Análise exploratória (`notebooks/02_eda.ipynb`): análise com foco em negócio, usando testes de hipótese para validar o que aparece nos gráficos. Como a nota não segue distribuição normal (Shapiro-Wilk), a base da análise são testes não paramétricos (Spearman, Mann-Whitney, Kruskal-Wallis), além de Qui-Quadrado, intervalos de confiança de 95% (Wilson para percentuais e erro padrão para o NPS) e regressão linear múltipla para medir o peso de cada fator.
4. Modelo preditivo (`notebooks/03_modelo.ipynb`): classificação para prever se o pedido vai gerar um detrator, com a previsão feita depois da entrega e antes da pesquisa. Separação treino/teste estratificada (80/20), validação cruzada de 5 partes, comparação entre linha de base, regressão logística, árvore de decisão e random forest, avaliação por AUC, precision, recall e F1 e escolha do ponto de corte pelo negócio. Uma regressão linear para prever a nota (MAE, RMSE e R²) entra como comparação.

## Principais resultados da EDA

- O NPS da base é -80,0 (84% de detratores).
- O atraso na entrega é o fator que mais pesa: cada dia de atraso tira cerca de 1 ponto da nota. O tempo total de entrega, por outro lado, não tem relação com a nota.
- Ponto de ruptura: com 2 dias de atraso 88% dos clientes viram detratores, e com 4 dias praticamente todos.
- O atendimento vem em seguida: cada contato extra com o SAC tira cerca de 0,7 ponto.
- Pedido no prazo e sem contato com o SAC: 22% de detratores, contra 84% na base toda.
- Perfil do cliente (idade, região, tempo de casa), valor do pedido, frete e desconto não mudam a nota de forma relevante.

Resumo completo em `reports/02_resumo_eda.md`.

## Resultado do modelo

- Modelo escolhido: regressão logística, que teve o melhor AUC e é a mais fácil de explicar (AUC de 0,87 na validação cruzada e 0,84 no teste).
- As variáveis que mais pesam no modelo são as mesmas da EDA: atraso, contatos com o SAC e tempo de resolução.
- Com ponto de corte de 0,9, 97% dos pedidos sinalizados realmente viram detratores, e o modelo encontra cerca de 65% dos detratores.
- Uso proposto: separar os pedidos em faixas de risco (baixo, médio e alto) e fazer contato proativo com os de risco alto, validando o efeito com um teste A/B.
- A regressão linear para prever a nota erra em média 1,4 ponto (MAE), então serve mais para explicar do que para decidir.

## Como reproduzir

Requisitos: Python 3.10 ou mais recente.

```bash
# 1. clonar o repositório e entrar na pasta
git clone https://github.com/rmf060187/tech-challenge-nps.git
cd tech-challenge-nps

# 2. criar e ativar um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate

# 3. instalar as dependências
pip install -r requirements.txt

# 4. abrir o Jupyter e rodar os notebooks na ordem
jupyter notebook
```

Se preferir Conda:

```bash
conda create -n nps python=3.11
conda activate nps
pip install -r requirements.txt
```

Ordem de execução:

1. `notebooks/01_tratamento_dados.ipynb` gera `data/processed/nps_tratado.csv`
2. `notebooks/02_eda.ipynb` lê a base tratada e salva os gráficos em `reports/figures/`
3. `notebooks/03_modelo.ipynb` treina e avalia os modelos e salva o modelo final em `models/`

Os notebooks usam caminhos relativos à pasta do projeto, então devem ser abertos a partir da pasta `notebooks/`.
