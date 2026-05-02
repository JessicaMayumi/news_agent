from .schemas import Digest


def render_digest(d: Digest, date: str) -> str:
    parts: list[str] = []

    parts.append(f"🗞️ TOP 10 NOTÍCIAS DE IA — {date} (últimas 48-72h)")
    parts.append("")

    for i, n in enumerate(d.top_news, 1):
        parts.append(f"{i}. {n.title}")
        parts.append(f"   {n.summary}")
        parts.append(f"   Fonte: {n.source_name} — {n.date} — {n.url}")
        parts.append("")

    parts.append("")
    parts.append("📄 PAPER DO DIA")
    parts.append("")
    parts.append(d.paper.title)
    parts.append(f"Autores: {', '.join(d.paper.authors)}")
    parts.append(f"Publicado em: {d.paper.venue}")
    parts.append(d.paper.why_read)
    parts.append(f"Link: {d.paper.url}")

    parts.append("")
    parts.append("💻 REPOSITÓRIO GITHUB EM ALTA")
    parts.append("")
    parts.append(f"{d.repo.full_name} — {d.repo.url}")
    parts.append(d.repo.why_matters)

    parts.append("")
    parts.append("💡 INSIGHT DO DIA")
    parts.append("")
    parts.append(f'"{d.insight.quote}"')
    parts.append(f"— {d.insight.author}, {d.insight.context}")

    return "\n".join(parts)


def render_digest_html(d: Digest, date: str) -> str:
    rows: list[str] = []
    rows.append(f"<h2>🗞️ TOP 10 NOTÍCIAS DE IA — {date}</h2>")
    rows.append("<p><em>últimas 48-72h</em></p>")
    rows.append("<ol>")
    for n in d.top_news:
        rows.append(
            f'<li><strong>{_esc(n.title)}</strong><br>'
            f"{_esc(n.summary)}<br>"
            f'<small>Fonte: {_esc(n.source_name)} — {n.date} — '
            f'<a href="{_esc(n.url)}">{_esc(n.url)}</a></small></li>'
        )
    rows.append("</ol>")

    rows.append("<h2>📄 Paper do dia</h2>")
    rows.append(f"<p><strong>{_esc(d.paper.title)}</strong><br>")
    rows.append(f"<em>Autores:</em> {_esc(', '.join(d.paper.authors))}<br>")
    rows.append(f"<em>Publicado em:</em> {_esc(d.paper.venue)}</p>")
    rows.append(f"<p>{_esc(d.paper.why_read)}</p>")
    rows.append(f'<p><a href="{_esc(d.paper.url)}">{_esc(d.paper.url)}</a></p>')

    rows.append("<h2>💻 Repositório GitHub em alta</h2>")
    rows.append(
        f'<p><strong>{_esc(d.repo.full_name)}</strong> — '
        f'<a href="{_esc(d.repo.url)}">{_esc(d.repo.url)}</a></p>'
    )
    rows.append(f"<p>{_esc(d.repo.why_matters)}</p>")

    rows.append("<h2>💡 Insight do dia</h2>")
    rows.append(f'<blockquote>"{_esc(d.insight.quote)}"</blockquote>')
    rows.append(f"<p>— {_esc(d.insight.author)}, <em>{_esc(d.insight.context)}</em></p>")

    return "<html><body>" + "\n".join(rows) + "</body></html>"


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
