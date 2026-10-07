# Prompt do Orquestrador — <Projeto>
# <Funcionalidade ou app>

> **Como usar:** cole como instrução inicial do Claude Code na VPS, no repositório <repo>. Execute a
> seção 0 e o Sprint 0. Nenhum sprint seguinte começa sem `PASS` do tests-agent, aprovação do
> reviewer-agent e ausência de pendências bloqueantes daquele sprint.
> **Fonte de verdade:** `CLAUDE.md` do repositório. Divergência = pergunta ao usuário.

## 0. Setup
1. Branch própria (app existente) ou estrutura inicial (app novo).
2. `.claude/agents/`, `.claude/skills/`, `.claude/sprints/<feature>/`, log de decisões.
3. `.claude/metodo.json` (zona protegida, branches protegidas, cabeçalho).
4. Feature flag (app existente).

## 1. Regras permanentes
<sem suposições; zona protegida; migrations; RLS; segredos; API externa só com documentação;
padrão de código; cabeçalho; licenças; contexto enxuto; regras de domínio e LGPD aplicáveis>

## 2. Decisões já tomadas
| ID | Decisão |
|----|---------|

## 3. Arquitetura alvo
<diagrama em texto; interfaces de desacoplamento; sincronia de relógio/consistência se aplicável>

## 4. Modelo de dados proposto (a validar no S0/S2)

## 5. Domínio (fluxos, estados, regras, métricas)

## 6. Agentes
| Agente | Responsabilidade | Modelo | Effort | Restrição de ferramentas |
|--------|------------------|--------|--------|--------------------------|
### 6.1 Pacote de contexto por delegação
```
[CONTEXTO PARA <agente> — Sprint <n>]
Objetivo do sprint:
Decisões vigentes relevantes:
Arquivos que PODE modificar:
Arquivos que NÃO PODE tocar:
Entregas anteriores aprovadas (até 10 linhas):
Critério de aceite desta tarefa:
Formato de retorno: resumo de até 40 linhas + caminhos alterados
```

## 7. Skills do projeto

## 8. Sprints
| Sprint | Entregas | Aceite |
|--------|----------|--------|
| S0 | Inventário só leitura / setup | Usuário valida zona protegida |
| S1 | Gate de decisões | Aprovação do usuário (bloqueante) |
| ... | ... | ... |
| Sn-2 | Navegação e operação contínuas | Sem falha bloqueante |
| Sn-1 | Red team | Sem falha crítica/alta |
| Sn | Fechamento | Aprovação do usuário |

## 9. Testes (ver checklists)

## 10. Critérios de aceite da funcionalidade

## 11. Pendências
| ID | Pendência | Antes do |
|----|-----------|----------|

## 12. Fechamento
Lint, testes, build; README/MANUAL/CLAUDE.md/schema atualizados; relatórios anexados; merge só com
autorização explícita do usuário.
