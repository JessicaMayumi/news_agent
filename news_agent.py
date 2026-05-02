"""Entry point: roda o curador Agno e envia o digest por email."""
from __future__ import annotations

import os
import sys
import traceback
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

from agent.curator import build_curator
from agent.emailer import send_email
from agent.render import render_digest, render_digest_html
from agent.schemas import Digest


def main() -> int:
    if not (os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")):
        print("ERROR: defina ANTHROPIC_API_KEY ou OPENAI_API_KEY no .env", file=sys.stderr)
        return 1

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{today}] Construindo curador Agno...", flush=True)

    agent = build_curator()

    prompt = (
        f"Gere o digest de IA de hoje. Data atual: {today}. "
        "Cubra notícias publicadas nas últimas 48-72 horas. "
        "Use TODAS as ferramentas (duckduckgo_search, fetch_arxiv_recent, "
        "fetch_github_trending, fetch_url_content) antes de escrever o resultado final. "
        "Faça pelo menos 8 buscas web variadas em inglês e português."
    )

    print("Executando agente (isso pode levar 1-3 minutos)...", flush=True)
    try:
        response = agent.run(prompt)
    except Exception as e:
        print(f"ERROR durante execução do agente: {e}", file=sys.stderr)
        traceback.print_exc()
        return 2

    digest = response.content
    if not isinstance(digest, Digest):
        print(f"ERROR: output não é Digest (got {type(digest).__name__})", file=sys.stderr)
        print(f"raw content: {digest!r}", file=sys.stderr)
        return 3

    plain = render_digest(digest, today)
    html = render_digest_html(digest, today)

    if os.getenv("DRY_RUN"):
        print("\n" + "=" * 60)
        print(plain)
        print("=" * 60)
        return 0

    subject = f"Digest IA — {today}"
    try:
        send_email(subject, plain, html_body=html)
    except Exception as e:
        print(f"ERROR enviando email: {e}", file=sys.stderr)
        traceback.print_exc()
        print("\n--- DIGEST GERADO (não enviado) ---\n", file=sys.stderr)
        print(plain)
        return 4

    print(f"Enviado para {os.environ['EMAIL_TO']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
