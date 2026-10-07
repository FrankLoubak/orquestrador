"""
Arquivo: hooks/scripts/guard_git.py
O que faz: Antes de cada comando Bash, bloqueia (1) `git push` para branches listadas em
  `block_push_branches` do `.claude/metodo.json`, inclusive push sem destino feito a partir dessas
  branches, e (2) `git add` de arquivos de ambiente reais (.env, .env.local, ...).
Para que serve: Garante que o trabalho de uma funcionalidade só chega à branch de produção com
  autorização explícita do usuário, e que arquivos de segredo não entram no índice do git.
Relaciona-se com:
  - hooks/hooks.json: registrado em PreToolUse com matcher Bash
  - hooks/scripts/common.py: usa read_event, project_dir, load_config, blocked
  - templates/metodo.json: define o campo block_push_branches
Entradas e saídas: JSON do evento no stdin; código 2 quando bloqueia.
Sprint de origem: v0.1.0 | Última revisão: v0.1.0
"""
import re
import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import blocked, load_config, project_dir, read_event  # noqa: E402

ENV_FILE = re.compile(r"(^|/)\.env(\.(?!example$|sample$|template$)[\w.-]+)?$")


def current_branch(root: Path) -> str:
    """Branch atual; string vazia se não for possível descobrir."""
    try:
        out = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], cwd=root,
                             capture_output=True, text=True, timeout=5)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def split_commands(command: str) -> list[list[str]]:
    """Separa comandos encadeados (&&, ||, ;, |) e tokeniza cada um."""
    parts = re.split(r"&&|\|\||;|\|", command)
    result = []
    for part in parts:
        try:
            tokens = shlex.split(part)
        except ValueError:
            tokens = part.split()
        if tokens:
            result.append(tokens)
    return result


def git_args(tokens: list[str]) -> list[str] | None:
    """Argumentos após `git` (ignorando opções globais como -C), ou None se não for git."""
    if not tokens or Path(tokens[0]).name != "git":
        return None
    args = tokens[1:]
    while args and args[0].startswith("-"):
        args = args[2:] if args[0] in ("-C", "-c") else args[1:]
    return args


def push_targets(args: list[str]) -> list[str]:
    """Branches de destino de um `git push` (refspecs após o remoto). Lista vazia = push implícito."""
    positional = [a for a in args[1:] if not a.startswith("-")]
    targets = []
    for refspec in positional[1:]:
        dest = refspec.split(":")[-1].lstrip("+")
        targets.append(dest.removeprefix("refs/heads/"))
    return targets


def main() -> None:
    event = read_event()
    command = str((event.get("tool_input") or {}).get("command") or "")
    if "git" not in command:
        sys.exit(0)
    root = project_dir()
    protected = set(load_config(root).get("block_push_branches") or [])

    for tokens in split_commands(command):
        args = git_args(tokens)
        if not args:
            continue
        if args[0] == "add":
            for path in args[1:]:
                if ENV_FILE.search(path):
                    blocked(f"`git add {path}` bloqueado: arquivo de ambiente com segredos não entra no git.")
        if args[0] == "push" and protected:
            if "--all" in args or "--mirror" in args:
                blocked("`git push --all/--mirror` bloqueado: atinge branches protegidas.")
            branch = current_branch(root)
            targets = [branch if t == "HEAD" else t for t in push_targets(args)] or [branch]
            hit = sorted(t for t in targets if t in protected)
            if hit:
                blocked(f"push para branch protegida ({', '.join(hit)}) bloqueado pelo método. "
                        "O merge na branch de produção só acontece no fechamento, com autorização "
                        "explícita do usuário, que executa o push por conta própria.")
    sys.exit(0)


if __name__ == "__main__":
    main()
