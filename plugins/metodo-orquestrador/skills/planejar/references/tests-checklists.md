# Checklists de testes

## Por sprint
- Lint, tipagem, testes unitários e de integração do que o sprint entregou; build.
- Pisos de cobertura não caem.
- Integrações externas testadas contra fixtures reais coletadas no S0, sem rede (suíte "live" só manual).

## Regressão (app existente)
- Linha de base registrada no S0 roda em todo sprint, com a feature flag desligada e ligada.

## Navegação de uso contínuo (UI)
- Sessão longa simulando um turno, navegação repetida entre telas novas e antigas.
- Expiração e renovação de sessão no meio do uso.
- Perda e retorno de conexão durante carregamento.
- Voltar, recarregar, link direto (válido, inexistente, vencido).
- Várias abas com o mesmo usuário; mudança concorrente do mesmo registro em duas abas.
- Filtros e paginação com grande volume gerado por simulador.
- Troca de usuário no mesmo navegador sem vazamento de dados em cache.
- Upload/download repetidos.
- Crescimento de memória, se a ferramenta expuser a métrica; senão, registrar a limitação.
- Fuso horário fixado (ex.: TZ=America/Sao_Paulo) quando houver datas.

## Operação contínua (workers e integrações)
- Dias seguidos simulados: falhas intermitentes, respostas vazias, paginação irregular, duplicatas,
  reinício no meio da janela, execução agendada que não rodou, disparo manual concorrente.
- Resultado esperado: nada perdido, nada duplicado, nunca duas execuções simultâneas.

## Red team (só ambiente de teste e dados com prefixo "QA")
- IDOR e acesso entre tenants/usuários; escalada de papel; burla de RLS via RPC privilegiada.
- URLs assinadas: adivinhação, reutilização, uso após expiração.
- Webhook falsificado, assinatura ausente/errada, replay.
- Payload malformado, gigante, mídia/PDF corrompido; processamento isolado.
- Injeção (SQL, comando, prompt injection em conteúdo externo lido por LLM).
- Vazamento de dado pessoal ou segredo em log, erro e resposta.
- Expurgo: nada sobra no banco nem no storage.
- Limites de taxa; rajadas para contornar travas; estouro de teto de custo.
- Veredito: nenhuma falha crítica ou alta aberta; médias e baixas viram pendências aceitas pelo usuário.
