from typing import List

from pydantic import BaseModel, Field


class NewsItem(BaseModel):
    title: str = Field(..., description="Título original (EN ou PT)")
    summary: str = Field(..., description="Resumo de exatamente 2 frases em pt-BR")
    source_name: str = Field(..., description="Nome da publicação (TechCrunch, Wired, etc)")
    date: str = Field(..., description="Data de publicação no formato YYYY-MM-DD")
    url: str = Field(..., description="URL original na língua da fonte")


class PaperOfDay(BaseModel):
    title: str = Field(..., description="Título do paper")
    authors: List[str] = Field(..., description="Lista de autores principais")
    venue: str = Field(..., description="arXiv ID, conferência ou venue (ex: arXiv:2501.12345)")
    why_read: str = Field(..., description="3 frases em pt-BR: por que vale ler e qual insight técnico traz")
    url: str = Field(..., description="Link direto para o paper")


class RepoOfDay(BaseModel):
    full_name: str = Field(..., description="owner/repo")
    url: str = Field(..., description="URL do GitHub")
    why_matters: str = Field(..., description="2 frases em pt-BR sobre por que importa")


class Insight(BaseModel):
    quote: str = Field(..., description="Citação ou ideia marcante (verbatim)")
    author: str = Field(..., description="Autor / pesquisador / lab")
    context: str = Field(..., description="1 frase em pt-BR de contexto")


class Digest(BaseModel):
    """Estrutura completa do digest diário de IA: 10 notícias, 1 paper, 1 repo, 1 insight."""

    top_news: List[NewsItem] = Field(..., min_length=8, max_length=10)
    paper: PaperOfDay
    repo: RepoOfDay
    insight: Insight
