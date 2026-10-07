# metodo-orquestrador

Marketplace pessoal com o plugin **metodo-orquestrador**: o método de desenvolvimento orientado a
agentes usado no Rota33, no TruckHelm e no Painel de Monitoramento.

## O que o plugin traz

| Componente | Conteúdo |
|---|---|
| Skill `planejar` | Fluxo F1–F8: enquadramento, contexto real, pesquisa, perguntas de lacuna, trade-offs, plano, entregáveis, iteração. Referências: banco de perguntas, modelo de ORCHESTRATOR/README/MANUAL, seleção de modelo, cabeçalho, checklists de testes e de segurança/LGPD. |
| Agentes | `revisor` (opus), `testador` (sonnet), `navegacao` (sonnet), `red-team` (opus), `triagem-logs` (haiku), `documentador` (haiku). |
| Hooks | Bloqueio de segredos e de `.env` reais (sempre); zona protegida, push em branch protegida e verificação de cabeçalho (configuráveis por projeto em `.claude/metodo.json`). |

O que é específico de cada projeto (stack, VPS, regras de banco) continua no `CLAUDE.md` do projeto.
O plugin só traz o que é genérico.

## Instalação

Teste local, sem marketplace:
```bash
claude --plugin-dir ./plugins/metodo-orquestrador
```

Validação e instalação pelo marketplace local:
```bash
claude plugin validate .
claude plugin marketplace add .
claude plugin install metodo-orquestrador@frankloubak-metodo
```

Depois de publicar este diretório como repositório no GitHub, adicione o marketplace pelo repositório
(conferir a sintaxe na documentação de marketplaces do Claude Code) e instale em escopo de usuário para
valer em todos os projetos.

## Uso

- Planejar: `/metodo-orquestrador:planejar` (a skill também é acionada quando você pede um plano).
- Em cada projeto, copie `plugins/metodo-orquestrador/templates/metodo.json` para `.claude/metodo.json`
  e ajuste. Projetos cujo fluxo normal é push direto no `main` devem tirar `main` de
  `block_push_branches`.
- Verificação de cabeçalho na CI:
  `python3 <caminho-do-plugin>/hooks/scripts/check_header.py --all .`

## Requisitos

- Python 3.10+ (os hooks usam só a biblioteca padrão).
- git (para os bloqueios de push).

## Arquivos sem cabeçalho

`plugin.json`, `marketplace.json`, `hooks.json` e `templates/metodo.json` são JSON e não aceitam
comentários. Eles estão documentados neste README e em `skills/planejar/references/hooks-config.md`.

## Uso no claude.ai

A skill `planejar` também é distribuída como arquivo `.skill` para instalar no claude.ai, onde
acontece a fase de perguntas e montagem do plano. Agentes e hooks só funcionam no Claude Code.

## Versionamento

Toda melhoria do método vira nova versão em `plugins/metodo-orquestrador/.claude-plugin/plugin.json`
(`0.1.0` → `0.2.0` ...), com nota em `CHANGELOG.md`.
