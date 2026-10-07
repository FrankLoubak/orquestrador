# Banco de perguntas de lacuna

Use só as que se aplicam e que mudam o desenho. Numere. Ofereça opções quando ajudar a responder.

## Enquadramento
1. App novo ou funcionalidade num app existente? Qual repositório?
2. Quem usa (perfis) e qual o objetivo de negócio?
3. Uso interno, produto vendido a terceiros, ou disputa de licitação?
4. Escopo do MVP: as 3 a 5 funcionalidades sem as quais não faz sentido.
5. O que fica explicitamente fora da primeira versão?

## Técnico
6. Stack: seguir a existente ou há preferência/restrição?
7. Onde roda (VPS, nuvem, dispositivo embarcado) e onde roda o Claude Code?
8. Integrações externas e se há documentação oficial de cada uma.
9. Volume esperado (usuários, registros, eventos por dia) e requisitos de tempo real.
10. Conectividade e limites de banda (para apps de campo/embarcados).

## Dados, segurança e LGPD
11. Há dados pessoais? Sensíveis (saúde, biometria, etc.)? De quem?
12. Multi-tenant? Quem pode ver o quê?
13. Finalidade do tratamento e se gera decisão sobre pessoas (impacta LGPD art. 20).
14. Prazos de retenção e expurgo.

## Custo e operação
15. Teto de custo (infraestrutura, hardware, API de LLM) ou critério para defini-lo.
16. Modelos disponíveis no plano do Claude Code (Fable exige créditos?).
17. Piloto: tamanho, duração e critério de sucesso.

## Aceite
18. Critérios objetivos de pronto (cobertura, métricas, cenários de ataque).
19. Frequências operacionais (varreduras, sincronizações) e disparos manuais.
