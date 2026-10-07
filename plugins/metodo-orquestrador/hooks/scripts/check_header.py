"""
Arquivo: hooks/scripts/check_header.py
O que faz: Verifica se um arquivo de código tem, nas primeiras linhas, o cabeçalho obrigatório do método
  (rótulos configurados em `header.required_labels` do `.claude/metodo.json`). Funciona de dois modos:
  como hook PostToolUse (verifica o arquivo recém-gravado) e como comando de linha para a CI
  (`--all [raiz]` verifica todos os arquivos versionados).
Para que serve: Torna verificável a regra "todo script diz o que faz, para que serve e com o que se
  relaciona", tanto durante o trabalho do agente quanto no pipeline.
Relaciona-se com:
  - hooks/hooks.json: registrado em PostToolUse com matcher Write|Edit|MultiEdit
  - hooks/scripts/common.py: usa project_dir, load_config, rel_path, blocked
  - skills/planejar/references/header-standard.md: define o padrão verificado aqui
  - templates/metodo.json: define extensions, required_labels, max_lines, exclude
Entradas e saídas: modo hook: JSON no stdin, código 2 com rótulos ausentes no stderr (o Claude recebe a
  mensagem e corrige); modo CLI: lista de arquivos reprovados e código 1 se houver algum.
Sprint de origem: v0.1.0 | Última revisão: v0.1.0
"""
import fnmatch
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import blocked, load_config, project_dir, rel_path  # noqa: E402


def header_config(root: Path) -> dict | None:
    """Configuração do cabeçalho; None se a verificação não estiver ligada no projeto."""
    cfg = load_config(root).get("header") or {}
    return cfg if cfg.get("enabled") else None


def applies(rel: str, cfg: dict) -> bool:
    """O arquivo é de uma extensão verificada e não está excluído."""
    if not any(rel.endswith(ext) for ext in cfg.get("extensions") or []):
        return False
    return not any(fnmatch.fnmatch(rel, pat) for pat in cfg.get("exclude") or [])


def missing_labels(path: Path, cfg: dict) -> list[str]:
    """Rótulos obrigatórios ausentes nas primeiras `max_lines` linhas (comparação sem caixa)."""
    try:
        with path.open(encoding="utf-8", errors="replace") as fh:
            head = "".join(line for _, line in zip(range(int(cfg.get("max_lines", 30))), fh)).lower()
    except OSError:
        return []
    return [lbl for lbl in cfg.get("required_labels") or [] if lbl.lower() not in head]


def hook_mode() -> None:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)
    file_path = str((event.get("tool_input") or {}).get("file_path") or "")
    root = project_dir()
    cfg = header_config(root)
    if not file_path or cfg is None:
        sys.exit(0)
    rel = rel_path(file_path, root)
    if not applies(rel, cfg):
        sys.exit(0)
    absent = missing_labels(root / rel, cfg)
    if absent:
        blocked(f"'{rel}' está sem o cabeçalho obrigatório (faltam: {', '.join(absent)}). "
                "Adicione no topo do arquivo o cabeçalho do padrão do método (ver referência "
                "header-standard da skill planejar) antes de continuar.")
    sys.exit(0)


def cli_mode(root: Path) -> None:
    cfg = header_config(root)
    if cfg is None:
        print("Verificação de cabeçalho desligada ou .claude/metodo.json ausente.")
        sys.exit(0)
    try:
        files = subprocess.run(["git", "ls-files"], cwd=root, capture_output=True,
                               text=True, check=True).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        files = [p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()]
    failures = []
    for rel in files:
        if applies(rel, cfg):
            absent = missing_labels(root / rel, cfg)
            if absent:
                failures.append(f"{rel}: faltam {', '.join(absent)}")
    for line in failures:
        print(line)
    print(f"{len(failures)} arquivo(s) sem cabeçalho válido.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        cli_mode(Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path.cwd())
    else:
        hook_mode()
