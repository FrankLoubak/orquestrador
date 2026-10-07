# Configuração dos hooks do plugin por projeto

Os hooks do plugin `metodo-orquestrador` leem `.claude/metodo.json` na raiz do projeto. Sem esse
arquivo, só a proteção de segredos fica ativa (ela vale sempre).

```json
{
  "protected_paths": ["src/legacy/*", "supabase/migrations/2024*"],
  "block_push_branches": ["main", "master"],
  "header": {
    "enabled": true,
    "extensions": [".py", ".ts", ".tsx", ".js", ".jsx", ".sql", ".sh"],
    "required_labels": ["O que faz", "Para que serve", "Relaciona-se com"],
    "max_lines": 30,
    "exclude": ["node_modules/*", "dist/*", "tests/fixtures/*"]
  }
}
```

| Campo | Efeito |
|---|---|
| `protected_paths` | Bloqueia Write/Edit nesses padrões glob (zona protegida do S0). |
| `block_push_branches` | Bloqueia `git push` para essas branches, inclusive push implícito a partir delas. Projetos cujo fluxo normal é push direto no `main` devem deixar a lista vazia ou não incluir a branch. |
| `header` | Após cada Write/Edit, avisa o Claude se faltar algum rótulo; para CI: `python3 <plugin>/hooks/scripts/check_header.py --all .` |

Sempre ativos: bloqueio de escrita em `.env*` reais, de conteúdo com padrão de segredo e de `git add`
de arquivo de ambiente.
