import os

from agno.agent import Agent
from agno.db.sqlite import SqliteDb

from .schemas import Digest
from .tools import (
    fetch_arxiv_recent,
    fetch_github_trending,
    fetch_url_content,
    web_search,
)


def _build_model():
    """Escolhe o modelo de acordo com MODEL_PROVIDER (ou auto-detecta pela API key disponível)."""
    provider = os.getenv("MODEL_PROVIDER", "").lower().strip()

    if not provider:
        if os.getenv("ANTHROPIC_API_KEY"):
            provider = "anthropic"
        elif os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        else:
            raise RuntimeError(
                "Nenhuma API key configurada. Defina ANTHROPIC_API_KEY ou OPENAI_API_KEY no .env"
            )

    if provider == "anthropic":
        from agno.models.anthropic import Claude
        return Claude(id=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"))

    if provider == "openai":
        from agno.models.openai import OpenAIChat
        return OpenAIChat(id=os.getenv("OPENAI_MODEL", "gpt-4o"))

    raise ValueError(f"MODEL_PROVIDER inválido: {provider!r} (use 'anthropic' ou 'openai')")


CURATOR_INSTRUCTIONS = """Você é um curador especialista em IA. Sua tarefa: produzir um digest diário das últimas 48-72h em pt-BR.

WORKFLOW (siga nesta ordem, pensando passo a passo):

1. PLAN — Liste mentalmente os ângulos a cobrir:
   - Modelos frontier (OpenAI, Anthropic, Google DeepMind, Meta, Mistral, xAI, DeepSeek, Qwen)
   - Agents e capabilities novas
   - Papers com insight técnico
   - Open-source / lançamentos
   - Regulação, mercado, M&A
   - Pesquisadores em destaque (X / LinkedIn)

2. GATHER — Use TODAS as tools agressivamente:
   - web_search → faça 8-12 buscas variadas em INGLÊS e PORTUGUÊS (tolere falhas — algumas queries podem retornar vazio)
   - fetch_arxiv_recent → busque papers em cs.AI / cs.LG / cs.CL
   - fetch_github_trending → busque repos por tópicos (llm, agent, rag, diffusion)
   - fetch_url_content → quando o snippet de busca for raso, leia o artigo completo

3. CRITIQUE — Filtre rigorosamente:
   - Descarte rumores sem fonte primária
   - Descarte fofoca, posts patrocinados, opinião sem dados
   - Priorize: surpreendente, impactante, tecnicamente significativo
   - Verifique as datas: deve ser das últimas 48-72h

4. WRITE — Preencha o schema Digest:
   - top_news: 10 itens (ou 8-9 se não houver 10 notícias verdadeiramente relevantes)
   - paper: 1 paper do arXiv com explicação técnica em 3 frases
   - repo: 1 repo open-source com 2 frases sobre relevância
   - insight: 1 citação verbatim de pesquisador/lab com contexto

REGRAS RÍGIDAS:
- Resumos das notícias: EXATAMENTE 2 frases em pt-BR
- Datas no formato YYYY-MM-DD
- URLs sempre originais (sem redirect/encurtador)
- NUNCA invente URLs, autores, citações, ou datas
- Se não houver fonte primária verificável, descarte o item
- Língua dos títulos: original (pode ser EN); resumos sempre em pt-BR"""


def build_curator() -> Agent:
    db_path = os.getenv("AGENT_DB", "tmp/news_agent.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    return Agent(
        name="AI News Curator",
        model=_build_model(),
        tools=[
            web_search,
            fetch_arxiv_recent,
            fetch_github_trending,
            fetch_url_content,
        ],
        instructions=CURATOR_INSTRUCTIONS,
        output_schema=Digest,
        db=SqliteDb(db_file=db_path),
        add_datetime_to_context=True,
        add_history_to_context=False,
        markdown=False,
        debug_mode=bool(os.getenv("DEBUG")),
        retries=2,
    )
