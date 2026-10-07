"""
Arquivo: hooks/scripts/guard_protected_paths.py
O que faz: Antes de cada Write/Edit, bloqueia alterações em caminhos listados em `protected_paths`
  do `.claude/metodo.json` do projeto (padrões glob relativos à raiz).
Para que serve: Implementa a "zona protegida" do método: o que já funciona e foi validado pelo usuário
  no Sprint 0 não é alterado sem autorização explícita.
Relaciona-se com:
  - hooks/hooks.json: registrado em PreToolUse com matcher Write|Edit|MultiEdit
  - hooks/scripts/common.py: usa read_event, project_dir, load_config, rel_path, blocked
  - templates/metodo.json: define o campo protected_paths
Entradas e saídas: JSON do evento no stdin; código 2 quando o caminho é protegido.
Sprint de origem: v0.1.0 | Última revisão: v0.1.0
"""
import fnmatch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import blocked, load_config, project_dir, read_event, rel_path  # noqa: E402


def main() -> None:
    event = read_event()
    file_path = str((event.get("tool_input") or {}).get("file_path") or "")
    if not file_path:
        sys.exit(0)
    root = project_dir()
    patterns = load_config(root).get("protected_paths") or []
    rel = rel_path(file_path, root)
    for pattern in patterns:
        if fnmatch.fnmatch(rel, pattern):
            blocked(f"'{rel}' está na zona protegida (padrão '{pattern}' em .claude/metodo.json). "
                    "Não altere. Registre a necessidade como pendência e pergunte ao usuário.")
    sys.exit(0)


if __name__ == "__main__":
    main()
