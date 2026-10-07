"""
Arquivo: hooks/scripts/common.py
O que faz: Lê o evento do hook (JSON no stdin), localiza o diretório do projeto e carrega a
  configuração opcional `.claude/metodo.json` do projeto.
Para que serve: Evita duplicar a mesma leitura de entrada e de configuração em todos os hooks.
Relaciona-se com:
  - hooks/scripts/guard_secrets.py: importa read_event e blocked
  - hooks/scripts/guard_protected_paths.py: importa read_event, project_dir, load_config, rel_path, blocked
  - hooks/scripts/guard_git.py: importa read_event, project_dir, load_config, blocked
  - hooks/scripts/check_header.py: importa project_dir, load_config, rel_path, blocked
  - templates/metodo.json: formato da configuração lida por load_config
Entradas e saídas: stdin com JSON do Claude Code; saída por código de saída (2 bloqueia) e stderr.
Sprint de origem: v0.1.0 | Última revisão: v0.1.0
"""
import json
import os
import sys
from pathlib import Path


def read_event() -> dict:
    """Lê o JSON do evento. Entrada ilegível resulta em dicionário vazio (o hook não bloqueia)."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return {}


def project_dir() -> Path:
    """Diretório do projeto informado pelo Claude Code; na ausência, o diretório atual."""
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()


def load_config(root: Path) -> dict:
    """Carrega `.claude/metodo.json`. Arquivo ausente ou inválido equivale a configuração vazia."""
    cfg = root / ".claude" / "metodo.json"
    if not cfg.is_file():
        return {}
    try:
        return json.loads(cfg.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        sys.stderr.write(f"[metodo] aviso: {cfg} inválido; proteções configuráveis desligadas.\n")
        return {}


def rel_path(file_path: str, root: Path) -> str:
    """Caminho relativo ao projeto, com barras normais, para comparar com padrões glob."""
    p = Path(file_path)
    if not p.is_absolute():
        p = root / p
    try:
        return p.resolve().relative_to(root).as_posix()
    except ValueError:
        return p.as_posix()


def blocked(message: str) -> None:
    """Encerra com código 2: o Claude Code bloqueia a ação (PreToolUse) e mostra a mensagem ao Claude."""
    sys.stderr.write(f"[metodo] {message}\n")
    sys.exit(2)
