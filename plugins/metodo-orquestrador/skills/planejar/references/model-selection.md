# Seleção de modelo por agente

Confirme na documentação atual do Claude Code os aliases aceitos no campo `model` do frontmatter de
subagentes e o campo `effort`. Confirme com `/model` o que o plano do usuário oferece (o Fable pode exigir
compra de créditos).

## Agentes de desenvolvimento

| Perfil da tarefa | Modelo | Effort |
|---|---|---|
| Orquestração, gates, perguntas ao usuário (sessão principal) | opus | high |
| Arquitetura e desenho de ML/score: alto impacto, baixo volume | opus (fable opcional, se o usuário autorizar créditos para aquela entrega) | high |
| Domínio jurídico/regulatório, privacidade, segurança | opus | high |
| Revisão de cada entrega | opus | high |
| Red team | opus (o Fable tem salvaguardas adicionais em cibersegurança que podem limitar testes ofensivos) | high |
| Implementação com especificação clara | sonnet | medium |
| Testes por sprint, navegação contínua | sonnet | medium |
| Inventário só leitura, triagem de logs, documentação, tarefas mecânicas | haiku | low |

Regra: agente recorrente (implementação, testes, revisão) nunca usa modelo pago por crédito avulso.

## LLM em tempo de execução (dentro do app)

| Tarefa | Modelo | Motivo |
|---|---|---|
| Classificação/triagem de alto volume | Haiku | custo e latência |
| Extração estruturada de documentos longos | Sonnet | precisão |
| Parecer consolidado sob demanda | Opus | raciocínio |

Sempre: saída validada por schema, custo registrado por chamada, teto diário/mensal com degradação
para regras, IDs e preços conferidos na documentação atual. Visão computacional embarcada e tarefas
de baixa latência usam modelos próprios, não LLM.
