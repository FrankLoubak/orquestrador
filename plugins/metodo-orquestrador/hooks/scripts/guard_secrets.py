"""
Arquivo: hooks/scripts/guard_secrets.py
O que faz: Antes de cada Write/Edit, bloqueia escrita em arquivos de ambiente reais (.env, .env.local,
  ...) e conteúdo com padrão de segredo (chave privada, tokens de API conhecidos, JWT, atribuição
  literal de senha/segredo).
Para que serve: Aplica de forma determinística a regra do método "segredos nunca no repositório nem no
  chat", sem depender de o modelo lembrar dela.
Relaciona-se com:
  - hooks/hooks.json: registrado em PreToolUse com matcher Write|Edit|MultiEdit
  - hooks/scripts/common.py: usa read_event e blocked
Entradas e saídas: JSON do evento no stdin; código 2 com motivo no stderr quando bloqueia.
Sprint de origem: v0.1.0 | Última revisão: v0.1.0
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import blocked, read_event  # noqa: E402

# Arquivos de ambiente permitidos por conterem só exemplos.
ALLOWED_ENV_FILES = {".env.example", ".env.sample", ".env.template"}

SECRET_PATTERNS = [
    ("chave privada", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----")),
    ("chave de acesso AWS", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("chave da API Anthropic", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}")),
    ("token do GitHub", re.compile(r"\b(?:ghp|gho|ghs|ghu)_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{40,}")),
    ("token do Slack", re.compile(r"\bxox[abprs]-[A-Za-z0-9\-]{10,}")),
    ("JWT (ex.: chave service_role do Supabase)",
     re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
    ("atribuição literal de segredo",
     re.compile(r"(?i)\b(?:password|passwd|senha|secret|api[_-]?key|access[_-]?token|private[_-]?key)\b"
                r"\s*[:=]\s*['\"](?!<|\$\{|your|seu|sua|example|exemplo|changeme|xxx)[^'\"\s]{12,}['\"]")),
]


def written_texts(tool_input: dict) -> list[str]:
    """Texto que a ferramenta vai gravar: content (Write), new_string (Edit) ou edits[] (MultiEdit)."""
    texts = []
    for key in ("content", "new_string"):
        if isinstance(tool_input.get(key), str):
            texts.append(tool_input[key])
    for edit in tool_input.get("edits") or []:
        if isinstance(edit, dict) and isinstance(edit.get("new_string"), str):
            texts.append(edit["new_string"])
    return texts


def main() -> None:
    event = read_event()
    tool_input = event.get("tool_input") or {}
    file_path = str(tool_input.get("file_path") or "")
    name = Path(file_path).name

    if (name == ".env" or name.startswith(".env.")) and name not in ALLOWED_ENV_FILES:
        blocked(f"escrita em '{name}' bloqueada: segredos ficam fora do repositório e do chat. "
                "Use .env.example com valores fictícios e peça ao usuário para gravar o real por conta própria.")

    for text in written_texts(tool_input):
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                blocked(f"conteúdo com aparência de {label} em '{file_path}'. Segredos não são gravados em "
                        "arquivos do projeto. Leia de variável de ambiente. Se for falso positivo, troque o "
                        "valor por um marcador fictício (ex.: <SUA_CHAVE>) e avise o usuário.")
    sys.exit(0)


if __name__ == "__main__":
    main()
