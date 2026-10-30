# Resumo da análise exploratória

Tech Challenge Fase 1 - Case NPS Preditivo
Autor: Renato Maximiano Ferreira

Este é o resumo dos achados do notebook `notebooks/02_eda.ipynb`, escrito para quem não vai abrir o código. Os gráficos citados estão em `reports/figures/`.

## Situação atual

- NPS da base: -80,0 (IC 95%: -81,9 a -78,0).
- Classificação direto na nota original: abaixo de 7,0 detrator, de 7,0 até abaixo de 9,0 neutro, 9,0 ou mais promotor.
- 84% de detratores (IC 95%: 83% a 86%), 11% de neutros e 4% de promotores (figura 01).
- Os intervalos de confiança são de 95%: Wilson para os percentuais e erro padrão da média para o NPS (cada cliente vale +1, 0 ou -1).
- Não é oscilação: mesmo no melhor cenário do intervalo de confiança o NPS fica abaixo de -78.

## O que mais pesa na nota

Das 14 variáveis operacionais e de perfil, só quatro têm relação relevante com a nota, e todas são coisas que deram errado na jornada: atraso, contatos com o SAC, tempo de resolução e reclamações (figura 02).

### 1. Atraso na entrega (principal fator)

- Cada dia de atraso tira cerca de 1 ponto da nota, mantendo o resto igual (regressão linear múltipla).
- O tempo total de entrega não importa: um pedido que leva 14 dias e chega no prazo tem a mesma nota de um que leva 2 (figura 04). O cliente pune a promessa quebrada, não a espera.
- Ponto de ruptura (figura 06):
  - no prazo: 52% de detratores (IC 95%: 46% a 57%)
  - 1 dia de atraso: 74%
  - 2 dias: 88% (IC 95%: 85% a 90%), aqui a experiência quebra
  - 3 dias: 97%
  - 4 dias ou mais: 99% a 100%, nenhum promotor

### 2. Atendimento

- Cada contato extra com o SAC tira cerca de 0,7 ponto. Sem contato são 71% de detratores (IC 95%: 67% a 74%); com 3 ou mais, 95% (IC 95%: 93% a 97%) (figura 07).
- O tempo de resolução também pesa, mas menos: uma semana a mais de resolução equivale a 1 ponto.

### 3. Atraso e atendimento se somam (figura 08)

- No prazo e sem contato com o SAC: 22% de detratores (contra 84% na base toda).
- Basta um dos dois falhar para o número subir muito (no prazo com 2 contatos: 64%; 2 dias de atraso sem contato: 71%).
- Com atraso e contatos juntos, passa de 90%.

## O que não pesa

- Perfil do cliente: região, idade e tempo de casa não mudam a proporção de detratores (figura 09). Clientes antigos também não são mais tolerantes a atraso.
- Pedido: valor, desconto, parcelas e quantidade de itens não têm relação com a nota. O frete tem um efeito estatisticamente detectável, mas muito pequeno.
- Número de tentativas de entrega: não faz diferença.

Conclusão para o negócio: não é o tipo de cliente que define a nota, é o que acontece com o pedido dele. O problema é operacional e pode ser corrigido.

## Hipóteses

| Hipótese -> Resultado |
H1 - atraso é o principal fator e tem ponto de ruptura -> Confirmada (2 e 4 dias) 
H2 - tentativas de entrega pioram a nota -> Não confirmada 
H3 - contatos e resolução pioram a nota -> Confirmada (contatos pesam mais) 
H4 - frete proporcional pesa, desconto ajuda pouco -> Não confirmada 
H5 - clientes antigos são mais tolerantes -> Não confirmada 
H6 - região influencia a nota -> Não confirmada 

## Recomendações

- Logística: tratar 1 dia de atraso como alerta e agir antes de chegar a 2. Rever os prazos prometidos, já que um prazo maior e cumprido não prejudica a nota.
- Atendimento: focar em resolver no primeiro contato e dar prioridade na fila para clientes com pedido atrasado.
- Ação proativa: avisar o cliente do atraso antes que ele precise procurar o SAC. Validar com um teste A/B antes de levar para toda a base.
- Desconto e frete grátis como forma de compensação não aparecem como solução nos dados.

## Sobre as colunas de satisfação e recompra

`csat_internal_score` e `repeat_purchase_30d` parecem os melhores preditores da base, mas são medidas da mesma satisfação ou consequência dela. A recompra é exatamente nota >= 8 em todos os pedidos. Por isso ficam fora da análise de causas e do modelo (vazamento de dados). `complaints_count` acompanha muito os contatos com o SAC (correlação de 0,74) e tem origem incerta (258 pedidos com 3 ou mais reclamações e nenhum contato), então é tratada como sintoma e não entra como variável principal do modelo.

## Cuidados

- É uma análise de associação. A prova de causa viria de um experimento.

## Próximo passo

Modelo preditivo para classificar pedidos com risco de detrator, usando como entrada principalmente atraso, contatos com o SAC e tempo de resolução.
