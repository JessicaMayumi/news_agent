import json
import os
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

from agno.tools import tool


@tool(show_result=False)
def web_search(query: str, max_results: int = 5) -> str:
    """Busca web genérica para notícias recentes. Tenta múltiplas vezes e tolera falhas.

    Use para encontrar notícias gerais de IA. Faça queries variadas em inglês e português.

    Args:
        query: termo de busca (ex: 'OpenAI release May 2026', 'agente IA novo modelo')
        max_results: número máximo de resultados (default 5)

    Returns:
        JSON com lista de {title, body, url}, ou {error, results: []} se tudo falhar.
    """
    try:
        from ddgs import DDGS
    except ImportError:
        return json.dumps({"error": "ddgs not installed", "results": []})

    last_err = None
    for attempt in range(3):
        try:
            results = list(DDGS().text(query, max_results=max_results, region="wt-wt"))
            if results:
                return json.dumps(
                    [
                        {
                            "title": r.get("title"),
                            "body": r.get("body"),
                            "url": r.get("href"),
                        }
                        for r in results
                    ],
                    ensure_ascii=False,
                )
        except Exception as e:
            last_err = str(e)
        time.sleep(1.5 * (attempt + 1))

    return json.dumps({"error": last_err or "no results", "results": []})


@tool(show_result=False)
def fetch_arxiv_recent(query: str, max_results: int = 15) -> str:
    """Busca papers recentes em arXiv (cs.AI / cs.LG / cs.CL), ordenados por data de submissão.

    Args:
        query: termo de busca em inglês (ex: 'agent reasoning', 'mixture of experts')
        max_results: quantos papers retornar (default 15, max 30)

    Returns:
        XML do Atom feed do arXiv com títulos, autores, abstracts e URLs.
    """
    max_results = min(max(1, max_results), 30)
    base = "http://export.arxiv.org/api/query"
    search = f"all:{query} AND (cat:cs.AI OR cat:cs.LG OR cat:cs.CL)"
    params = urllib.parse.urlencode({
        "search_query": search,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    })
    req = urllib.request.Request(
        f"{base}?{params}",
        headers={"User-Agent": "news-agent/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8")[:50000]
    except Exception as e:
        return f"ERROR fetching arxiv: {e}"


@tool(show_result=False)
def fetch_github_trending(topic: str = "llm", days: int = 7) -> str:
    """Busca repos do GitHub mais populares em um tópico de IA, atualizados nos últimos N dias.

    Args:
        topic: tópico do GitHub (ex: 'llm', 'agent', 'rag', 'diffusion', 'mlops', 'ai')
        days: janela em dias (default 7)

    Returns:
        JSON com nome, descrição, stars, linguagem e URL dos top 15 repos.
    """
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    q = f"topic:{topic} pushed:>{since}"
    url = (
        "https://api.github.com/search/repositories?"
        f"q={urllib.parse.quote(q)}&sort=stars&order=desc&per_page=15"
    )
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "news-agent/1.0",
    }
    if token := os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
    except Exception as e:
        return json.dumps({"error": str(e)})
    items = [
        {
            "full_name": it["full_name"],
            "description": it.get("description"),
            "stars": it["stargazers_count"],
            "language": it.get("language"),
            "url": it["html_url"],
            "updated_at": it["updated_at"],
        }
        for it in data.get("items", [])[:15]
    ]
    return json.dumps(items, ensure_ascii=False)


@tool(show_result=False)
def fetch_url_content(url: str) -> str:
    """Lê o conteúdo textual de uma URL (HTML strip). Use quando o snippet de busca não for suficiente.

    Args:
        url: URL completa (http/https)

    Returns:
        Texto extraído (até 20k chars).
    """
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 news-agent/1.0"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            content = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return f"ERROR fetching {url}: {e}"

    text = re.sub(r"<script[^>]*>.*?</script>", "", content, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:20000]
