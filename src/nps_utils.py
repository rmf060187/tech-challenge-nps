"""
Funcoes auxiliares usadas nos notebooks do Tech Challenge (case NPS).

Deixei aqui o que se repete entre o tratamento, a EDA e o modelo, para
nao ter a mesma regra escrita de jeitos diferentes em cada notebook.
"""

import numpy as np
import pandas as pd

# Faixas do NPS (definidas na etapa de target), aplicadas direto na nota original.
# Nao arredondo: 6.5 ainda nao chegou em 7, entao continua sendo detrator.
LIMITE_NEUTRO = 7.0     # abaixo disso e detrator
LIMITE_PROMOTOR = 9.0   # a partir disso e promotor

ORDEM_CATEGORIAS = ["Detrator", "Neutro", "Promotor"]


def classificar_nps(notas):
    """Recebe a nota original (0 a 10, com decimais) e devolve a categoria do NPS.

    nota < 7.0         -> Detrator
    7.0 <= nota < 9.0  -> Neutro
    nota >= 9.0        -> Promotor
    """
    notas = pd.Series(notas, dtype="float64")
    categoria = np.select(
        [notas < LIMITE_NEUTRO, notas < LIMITE_PROMOTOR],
        ["Detrator", "Neutro"],
        default="Promotor",
    )
    return pd.Categorical(categoria, categories=ORDEM_CATEGORIAS, ordered=True)


def calcular_nps(categorias):
    """NPS = % promotores - % detratores (resultado entre -100 e 100)."""
    categorias = pd.Series(categorias)
    pct_promotores = (categorias == "Promotor").mean() * 100
    pct_detratores = (categorias == "Detrator").mean() * 100
    return pct_promotores - pct_detratores


def resumo_por_grupo(df, coluna_grupo, coluna_categoria="categoria_nps", coluna_nota="nps_score"):
    """Tabela com quantidade de pedidos, nota media, % detratores, % promotores e NPS por grupo."""
    resumo = df.groupby(coluna_grupo, observed=True).agg(
        pedidos=(coluna_nota, "size"),
        nota_media=(coluna_nota, "mean"),
        pct_detratores=(coluna_categoria, lambda s: (s == "Detrator").mean() * 100),
        pct_promotores=(coluna_categoria, lambda s: (s == "Promotor").mean() * 100),
    )
    resumo["nps"] = resumo["pct_promotores"] - resumo["pct_detratores"]
    return resumo.round(2)


def ic_nps(categorias, z=1.96):
    """NPS com intervalo de confianca de 95%.

    Cada cliente vira +1 (promotor), 0 (neutro) ou -1 (detrator). A media dessa
    variavel vezes 100 e o proprio NPS, entao da para usar o IC de uma media:
    media +- z * erro padrao. Com 2.500 pedidos a amostra e grande o bastante
    para usar z = 1.96 (teorema central do limite).
    """
    pontos = pd.Series(categorias).astype(str).map({"Promotor": 1, "Neutro": 0, "Detrator": -1})
    media = pontos.mean()
    erro_padrao = pontos.std(ddof=1) / np.sqrt(len(pontos))
    return media * 100, (media - z * erro_padrao) * 100, (media + z * erro_padrao) * 100


def ic_detratores(df, coluna_grupo, coluna_alvo="flag_detrator", alfa=0.05):
    """% de detratores por grupo com intervalo de confianca de Wilson (recomendado para proporcoes)."""
    from statsmodels.stats.proportion import proportion_confint

    tabela = df.groupby(coluna_grupo, observed=True)[coluna_alvo].agg(pedidos="size", detratores="sum")
    inferior, superior = proportion_confint(tabela["detratores"], tabela["pedidos"], alpha=alfa, method="wilson")
    tabela["pct_detratores"] = tabela["detratores"] / tabela["pedidos"] * 100
    tabela["ic_inferior"] = inferior * 100
    tabela["ic_superior"] = superior * 100
    return tabela.round(1)
