# Etapa 1 e 2: Entendimento do negócio e definição da target

Tech Challenge - Fase 1 (Case NPS Preditivo)
Autor: Renato Maximiano Ferreira

Este documento cobre as duas primeiras entregas do desafio. Primeiramente, tentar entender a dor e a decisão que o negócio precisa tomar, depois traduzir isso em perguntas analíticas e, por fim, definir a variável alvo. Ainda não é uma análise exploratória completa, mas em alguns pontos eu já olhei a base para checar se as hipóteses faziam sentido.

---

## 1. Entendimento do negócio

### 1.1 Contexto

A empresa é um e-commerce nacional que cresceu rápido. Mais pedidos, mais entregas e mais contatos com o atendimento. O crescimento trouxe escala, mas a área de Experiência do Cliente começou a ver um NPS muito instável entre perfis de clientes, inclusive entre clientes que, olhando só os indicadores operacionais, tiveram experiências parecidas.

Hoje o NPS só é coletado depois que a jornada de compra termina. Ou seja, quando a empresa descobre que o cliente ficou insatisfeito, o problema já aconteceu e normalmente não dá mais tempo de fazer nada por aquele pedido.

### 1.2 Qual problema de negócio está sendo resolvido?

O pedido que chega para a área de dados poderia ser resumido como: queremos prever o NPS. Mas o gestor costuma trazer o pedido em formato de solução. A dor por trás dele é outra:

A empresa não sabe quais fatores da operação (pedido, entrega e atendimento) realmente fazem um cliente virar detrator, e por isso só consegue reagir depois que a nota ruim já foi dada.

Daí saem duas perguntas que guiam o trabalho:

1. Pergunta da análise (descritiva): quais fatores operacionais mais influenciam a nota de NPS e em que ponto a experiência do cliente quebra?
2. Pergunta do modelo (preditiva): com as informações disponíveis antes da pesquisa, conseguimos identificar quais pedidos têm alta chance de gerar um detrator?

Pensando nas três categorias de problema de dados vistas no curso, o caso passa pelas três. A EDA é a parte descritiva (o que está acontecendo e por quê). O modelo é a parte preditiva (quem provavelmente vai dar nota baixa). E as recomendações para as áreas são o começo de uma parte prescritiva (o que fazer com esse cliente ou com esse processo). O trabalho foca nas duas primeiras e deixa a terceira como proposta.

Metas de negócio x metas analíticas

Separei as metas para não cair na armadilha de otimizar uma métrica técnica que não muda nada no negócio:

| Meta de negócio -> Meta analítica relacionada |
Reduzir a proporção de detratores e subir o NPS -> Identificar, com evidência estatística, os fatores mais associados a notas baixas
Agir antes da pesquisa nos pedidos com problema -> Modelo que encontre a maior parte dos futuros detratores (recall alto na classe detrator) sem gerar alerta demais
Priorizar onde investir -> Medir o tamanho do efeito de cada fator, não só se ele é significativo

Hipóteses iniciais

Antes de abrir a base com calma, anotei o que eu esperaria encontrar, para depois confirmar ou não na EDA:

- H1: atraso na entrega é o fator que mais derruba a nota, e deve existir um número de dias de atraso a partir do qual quase todo mundo vira detrator.
- H2: mais tentativas de entrega pioram a nota, mesmo quando o pedido chega sem atraso.
- H3: quanto mais o cliente precisa falar com o atendimento e quanto mais demora a resolução, menor a nota.
- H4: frete alto em relação ao valor do pedido pesa negativamente; desconto ajuda pouco.
- H5: clientes com mais tempo de casa são mais tolerantes a um problema pontual.
- H6: a região influencia a nota, provavelmente por causa de prazo e custo de entrega, e não pela região em si.

### 1.3 Por que o NPS é importante para um e-commerce?

No e-commerce o cliente não tem contato com loja nem vendedor. A experiência dele é basicamente o site, a entrega e, se algo der errado, o atendimento. Isso faz o NPS ser um termômetro bem direto da operação.

Alguns motivos que eu considero mais importantes:

- É uma métrica simples e comparável. Uma pergunta só ("de 0 a 10, quanto você recomendaria?") que dá para acompanhar ao longo do tempo e comparar com o mercado.
- Está ligado a comportamento futuro. A ideia do NPS é justamente que a intenção de recomendar antecipa recompra e indicação, que são as coisas que dão lucro.
- A troca de loja custa quase nada. No online o concorrente está a um clique. Um cliente insatisfeito não precisa nem reclamar, ele só não volta.
- Reputação pública. Detrator de e-commerce costuma deixar avaliação ruim, postar em rede social ou registrar queixa em sites como Reclame Aqui, e isso afeta quem ainda nem comprou.

O ponto fraco é que o NPS chega tarde e não explica o motivo da nota. Por isso faz sentido cruzar a nota com os dados operacionais, que é o que este trabalho propõe.

### 1.4 Quais áreas se beneficiam desses insights?

- Logística: é provavelmente a área mais afetada. Saber quanto o atraso e as tentativas de entrega pesam ajuda a priorizar transportadoras, rotas e regiões, e a decidir se vale pagar mais caro por um prazo menor.
- Atendimento (SAC): entender a partir de quantos contatos ou de quantos dias de resolução o cliente desiste da marca. Pode virar regra de prioridade na fila (por exemplo, cliente com pedido atrasado e segundo contato vai para o topo).
- Comercial: avaliar se frete, desconto e parcelamento mudam a percepção do cliente ou se o peso real está na entrega.
- Marketing e CRM: não mandar campanha de recompra para quem acabou de ter uma experiência ruim, e trabalhar indicação com quem tem perfil de promotor.
- Diretoria e estratégia: ter uma visão de quais alavancas operacionais mexem no NPS e quanto investir em cada uma.

### 1.5 Reflexão: como o NPS impacta recompra, boca a boca e market share

Recompra. Cliente satisfeito tende a voltar. Um detrator dificilmente compra de novo. Na base do desafio isso aparece de forma muito forte: nenhum detrator recomprou em 30 dias, enquanto todos os promotores recompraram.

Boca a boca. O promotor faz propaganda de graça e o detrator faz propaganda contra. No online esse efeito é amplificado, porque a opinião fica registrada em avaliações e redes sociais e é lida por muita gente. Em geral um cliente insatisfeito fala do problema com mais intensidade do que um satisfeito elogia, então reduzir detratores costuma ter mais impacto do que só aumentar promotores.

Market share. No e-commerce o mercado é muito disputado e o cliente compara preço, prazo e frete em segundos. Se a empresa perde clientes por experiência ruim, precisa gastar mais com mídia para repor a base, enquanto um concorrente com NPS melhor cresce com indicação e recompra, que são canais mais baratos. É uma relação de longo prazo e com muitos outros fatores no meio, então eu não trataria o NPS como causa única.

### 1.6 Indicadores de mercado que poderiam complementar a análise

A base só tem dados internos e de uma única empresa. Para interpretar melhor os resultados, eu buscaria:

- Benchmark de NPS do setor: NPS médio de e-commerce e varejo online no Brasil, para saber se o nosso número é ruim em termos absolutos ou só em relação ao passado.
- Reputação pública: nota e índice de solução no Reclame Aqui e no consumidor.gov.br, comparando com os principais concorrentes.
- SLA logístico: percentual de entregas no prazo, prazo prometido versus prazo realizado, comparado com o prazo médio que os concorrentes prometem para a mesma região.
- Indicadores de atendimento: taxa de contato por pedido, resolução no primeiro contato e tempo médio de resposta.
- Concorrência: frete grátis, preço e prazo dos concorrentes para os mesmos produtos e regiões.
- Outras métricas de cliente: CSAT por etapa da jornada, taxa de recompra em 90 dias e churn.
- Contexto de calendário: datas como Black Friday e Natal, quando prazo e atendimento costumam piorar e a tolerância do cliente muda.

---

## 2. Definição da target

### 2.1 Qual variável representa a satisfação do cliente?

A variável alvo é a `nps_score`, a nota de 0 a 10 que o cliente dá na pesquisa aplicada depois da experiência de compra.

A partir dela crio a classificação padrão de NPS:

| Nota -> Categoria |
| 0 até menos de 7,0 -> Detrator |
| 7,0 até menos de 9,0 -> Neutro |
| 9,0 a 10 -> Promotor |

E o NPS da empresa é calculado como % de promotores menos % de detratores.

Um detalhe da base: cerca de 83% das notas vêm com casas decimais (ex.: 6,4 ou 8,7), o que não acontece numa pesquisa real de NPS, onde a escala é inteira. Para classificar, não arredondo a nota. Usei os pontos de corte da escala: o cliente só passa a neutro quando atinge 7,0 e só passa a promotor quando atinge 9,0. Uma nota 6,5 ou 6,9, por exemplo, ainda não chegou ao 7 e continua sendo de detrator. Essa decisão importa porque 258 notas estão entre 6 e 7 e 91 estão entre 8 e 9. De eu arredondasse, boa parte delas mudaria de grupo e o NPS da base ficaria mais otimista do que realmente é.

Usando essa regra, a base fica assim: 84,4% de detratores, 11,2% de neutros e 4,4% de promotores, ou seja, um NPS de -80,0. É um resultado muito negativo, o que reforça a urgência do problema.

O alvo do modelo fica:

A probabilidade de que um pedido gere uma avaliação de detrator (nota abaixo de 7,0) na pesquisa de NPS aplicada após o fim da jornada daquele pedido.

- Unidade: o pedido. Na base cada cliente aparece uma única vez, então pedido e cliente se confundem, mas a ação da empresa (avisar, priorizar, compensar) é sobre um pedido específico.
- Ação: dar nota de detrator.
- Período: a pesquisa pós-compra daquele pedido.

Também deixo registrada a versão contínua (prever a nota de 0 a 10, como regressão). A escolha entre regressão e classificação é feita na etapa do modelo, mas para uso no dia a dia acho a versão "detrator ou não" mais útil, porque vira uma regra de ação simples.

### 2.2 Por que ela foi escolhida?

- É exatamente o indicador que a área de Experiência do Cliente acompanha e quer melhorar. Se o alvo fosse outro, o modelo responderia uma pergunta que ninguém fez.
- É a única medida da percepção do próprio cliente sobre a jornada inteira (compra, entrega e atendimento juntos).
- As outras candidatas não servem tão bem como alvo:
  - `csat_internal_score` é um score interno, sem definição clara de como e quando é calculado. Parece mais uma medida paralela da mesma satisfação do que a dor do negócio.
  - `repeat_purchase_30d` é uma consequência da satisfação, e não a satisfação em si. Poderia ser alvo de outro projeto (prever recompra), mas não deste.

### 2.3 Em que momento da jornada essa informação é coletada?

A nota é coletada depois do encerramento da jornada de compra, ou seja, depois da entrega e de eventuais contatos com o atendimento. Montei a linha do tempo de um pedido para deixar claro o que se sabe em cada momento:

1. Compra: idade, região, tempo de casa, valor do pedido, quantidade de itens, desconto, parcelas, frete.
2. Entrega: tempo de entrega, dias de atraso, tentativas de entrega.
3. Pós-entrega / atendimento: contatos com o SAC, reclamações, tempo de resolução.
4. Pesquisa: nota de NPS (e, provavelmente, o CSAT interno).
5. Depois da pesquisa: recompra em até 30 dias.

Para o modelo ser útil, a previsão precisa acontecer antes do passo 4. O momento mais natural é logo após a entrega (ou após o fechamento do atendimento, quando houver), que é quando a empresa ainda tem tempo de entrar em contato, compensar ou resolver antes de o cliente responder a pesquisa.

### 2.4 Existe algum risco de usar essa variável de forma inadequada?

Sim, vários. Os principais:

a) Vazamento de dados (data leakage). É o risco mais sério neste caso. Algumas colunas só existem depois ou ao mesmo tempo que a nota, e se entrarem no modelo ele vai parecer ótimo no teste e não vai funcionar na prática.

- `repeat_purchase_30d`: acontece depois da pesquisa, é informação do futuro. Além disso, conferindo a base, descobri que ela é idêntica a uma regra sobre a própria nota: todos os 218 pedidos com recompra têm `nps_score` maior ou igual a 8,0, e nenhum pedido com nota abaixo de 8,0 recomprou. Ou seja, a coluna foi derivada da target. Qualquer modelo que a use "acerta" sem aprender nada. Fica fora das variáveis de entrada.
- `csat_internal_score`: é outra medida de satisfação, coletada no mesmo momento ou depois. A correlação com o NPS é alta (cerca de 0,56) e a média sobe de 2,5 entre detratores para 6,0 entre promotores. Também fica fora do modelo. Na EDA ela pode aparecer só como comparação.
- `complaints_count`: precisa de cuidado. A média é de 4 reclamações por pedido, o que é alto para uma única compra, e não está claro se a contagem é do pedido ou do histórico do cliente, nem se inclui reclamações feitas depois da pesquisa. Vou investigar na EDA antes de decidir se entra.
- `customer_service_contacts` e `resolution_time_days`: em princípio são conhecidas antes da pesquisa, mas o tempo de resolução só existe quando o atendimento fecha. Na prática o modelo teria que rodar depois desse fechamento ou usar o tempo "até agora".

A regra que vou seguir é: respeitar a linha do tempo e usar só o que estaria disponível no momento da decisão.

b) Proxy imperfeito. O NPS mede intenção de recomendar, não exatamente satisfação. Um cliente pode estar satisfeito e mesmo assim não ter o hábito de recomendar lojas, e isso puxa a nota para baixo. Também há diferenças culturais e regionais na forma de dar nota. O próprio material do curso usa o NPS como exemplo de proxy que pode ser um sinal fraco. Por isso os resultados devem ser lidos como tendência, não como verdade sobre cada cliente.

c) Viés de quem responde. Só uma parte dos clientes responde pesquisa, normalmente quem está muito satisfeito ou muito irritado. A base não informa a taxa de resposta, então não dá para saber se esses 2.500 pedidos representam todos os clientes.

---

## Resumo das decisões

- Target: `nps_score`, classificado sem arredondamento em detrator (abaixo de 7,0), neutro (de 7,0 até abaixo de 9,0) e promotor (9,0 ou mais).
- Alvo principal do modelo: pedido vai ou não gerar um detrator, com a previsão feita depois da entrega e antes da pesquisa.
- Fora das variáveis de entrada: `repeat_purchase_30d` (derivada da nota) e `csat_internal_score` (medida paralela da satisfação). `complaints_count` em avaliação.
- Os resultados devem ser usados para corrigir a operação e priorizar contatos, não para metas individuais nem para tratar perfis de clientes de forma diferente.

## Referências

- Material da disciplina "Metodologia CRISP-DM para projetos de ciência de dados" (Fase 1), capítulos 1 a 4.
