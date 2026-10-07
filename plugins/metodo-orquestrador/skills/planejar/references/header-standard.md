# Cabeçalho obrigatório de script

Todo arquivo de código começa com: **o que faz, para que serve, com quais arquivos se relaciona**.
O hook `check_header.py` verifica os rótulos configurados em `.claude/metodo.json`.

## Python
```python
"""
Arquivo: app/modulo/arquivo.py
O que faz: <comportamento objetivo>
Para que serve: <papel no fluxo / problema de negócio>
Relaciona-se com:
  - <caminho>: <chama | é chamado por | grava em | lê de | implementa interface de>
Entradas e saídas: <resumo>
Sprint de origem: S<n> | Última revisão: S<n>
"""
```

## TypeScript / JavaScript
```ts
/**
 * Arquivo: src/modulo/arquivo.ts
 * O que faz: ...
 * Para que serve: ...
 * Relaciona-se com:
 *   - <caminho>: <relação>
 * Sprint de origem: S<n> | Última revisão: S<n>
 */
```

## SQL / shell / YAML
Mesmo conteúdo em comentários de linha (`--` ou `#`) no topo. Em shell, depois do shebang.

## Regras
- Alterou o arquivo: atualize "Relaciona-se com" e "Última revisão".
- Nova dependência criada no sprint aparece nos dois lados (quem chama e quem é chamado).
- JSON não aceita comentário: documente arquivos JSON no README ou num `.md` vizinho.
- Projetos com padrão próprio (ex.: rótulos em maiúsculas) configuram `required_labels` de acordo.
