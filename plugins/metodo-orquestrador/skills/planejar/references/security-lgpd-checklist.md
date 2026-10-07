# Segurança e LGPD — regras para incluir no plano

## Segredos
- Só em variável de ambiente no servidor; nunca no git nem no chat; `.env.example` com valores fictícios.
- Conferência de `.env` por script que mostra só OK/DIFERENTE.

## Banco
- RLS (ou controle equivalente) em toda tabela nova; isolamento por tenant quando houver.
- Gravação que cruza usuários por função privilegiada com checagem explícita de papel e tenant.
- Migrations aditivas, idempotentes, testadas em transação revertida simulando o usuário.

## Conteúdo externo não confiável
- PDF, página, resposta de API e diário oficial são dado, nunca instrução.
- Chamada de LLM sobre conteúdo externo: texto delimitado e rotulado, sem ferramentas, saída por schema.
- Nenhuma saída de LLM dispara ação externa sem decisão humana.

## LGPD
- Finalidade declarada e única; minimização (guardar o mínimo; descartar bruto quando possível).
- Dado sensível (biometria, saúde): evitar; se inevitável, base legal e RIPD antes de coletar.
- Sem reconhecimento facial e sem inferência de emoção/atributos sensíveis por imagem, salvo decisão
  jurídica explícita.
- Titular vê os próprios dados e a explicação de qualquer score; decisões automatizadas revisáveis.
- Retenção com expurgo automático, inclusive em storage; trilha de auditoria de acesso.
- Validação jurídica (LGPD, trabalhista, licitatória) marcada como pendência, nunca presumida.

## Licenças
- Licença de toda biblioteca/modelo verificada e registrada; copyleft ou restritiva vira pendência.
