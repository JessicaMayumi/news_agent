from __future__ import annotations

from .schemas import Digest


def render_digest(d: Digest, date: str) -> str:
    """Render plain text version with clear visual hierarchy."""
    out: list[str] = []

    out.append("=" * 70)
    out.append(f"  🗞️  DIGEST IA — {date}")
    out.append("  últimas 48–72h")
    out.append("=" * 70)
    out.append("")
    out.append("")
    out.append("━━━ TOP NOTÍCIAS ━━━")
    out.append("")

    for i, n in enumerate(d.top_news, 1):
        out.append(f"[{i:02d}]  {n.title}")
        out.append("")
        out.append(f"      {n.summary}")
        out.append("")
        out.append(f"      → {n.source_name} · {n.date}")
        out.append(f"      → {n.url}")
        out.append("")
        out.append("─" * 70)
        out.append("")

    out.append("")
    out.append("━━━ 📄 PAPER DO DIA ━━━")
    out.append("")
    out.append(f"  {d.paper.title}")
    out.append("")
    out.append(f"  Autores:   {', '.join(d.paper.authors)}")
    out.append(f"  Publicado: {d.paper.venue}")
    out.append("")
    out.append(f"  {d.paper.why_read}")
    out.append("")
    out.append(f"  → {d.paper.url}")
    out.append("")
    out.append("─" * 70)
    out.append("")

    out.append("━━━ 💻 REPO EM ALTA ━━━")
    out.append("")
    out.append(f"  {d.repo.full_name}")
    out.append(f"  → {d.repo.url}")
    out.append("")
    out.append(f"  {d.repo.why_matters}")
    out.append("")
    out.append("─" * 70)
    out.append("")

    out.append("━━━ 💡 INSIGHT DO DIA ━━━")
    out.append("")
    out.append(f'  "{d.insight.quote}"')
    out.append("")
    out.append(f"  — {d.insight.author}")
    out.append(f"    {d.insight.context}")
    out.append("")
    out.append("=" * 70)

    return "\n".join(out)


def render_digest_html(d: Digest, date: str) -> str:
    """Render HTML email with card-based layout."""
    css = """
    <style>
      body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
             background: #0d1117; color: #e6edf3; margin: 0; padding: 0; }
      .container { max-width: 680px; margin: 0 auto; padding: 32px 24px; }
      .header { border-bottom: 2px solid #30363d; padding-bottom: 20px; margin-bottom: 32px; }
      .header h1 { margin: 0 0 6px 0; font-size: 26px; color: #f0f6fc; }
      .header .sub { color: #8b949e; font-size: 14px; }
      .section-title { font-size: 13px; font-weight: 600; text-transform: uppercase;
                       letter-spacing: 1.5px; color: #7d8590; margin: 36px 0 18px 0;
                       border-left: 3px solid #58a6ff; padding-left: 10px; }
      .news-item { background: #161b22; border: 1px solid #30363d; border-radius: 8px;
                   padding: 18px 20px; margin-bottom: 14px; }
      .news-num { display: inline-block; background: #1f6feb; color: white;
                  font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 12px;
                  margin-right: 8px; }
      .news-title { font-size: 16px; font-weight: 600; color: #f0f6fc; margin: 0 0 10px 0; }
      .news-summary { color: #c9d1d9; font-size: 14px; line-height: 1.55; margin: 0 0 12px 0; }
      .news-meta { font-size: 12px; color: #8b949e; }
      .news-meta a { color: #58a6ff; text-decoration: none; }
      .news-meta a:hover { text-decoration: underline; }
      .feature-card { background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
                      border: 1px solid #30363d; border-radius: 10px;
                      padding: 22px 24px; margin-bottom: 14px; }
      .feature-title { font-size: 18px; font-weight: 700; color: #f0f6fc; margin: 0 0 10px 0; }
      .feature-meta { font-size: 13px; color: #8b949e; margin: 4px 0; }
      .feature-meta strong { color: #c9d1d9; }
      .feature-body { color: #c9d1d9; font-size: 14px; line-height: 1.6; margin: 14px 0; }
      .feature-link { display: inline-block; margin-top: 8px; color: #58a6ff;
                      text-decoration: none; font-size: 13px; font-weight: 500; }
      .feature-link:hover { text-decoration: underline; }
      .quote { background: #161b22; border-left: 4px solid #d29922; border-radius: 4px;
               padding: 18px 22px; margin: 0; }
      .quote-text { font-size: 16px; font-style: italic; color: #f0f6fc;
                    line-height: 1.55; margin: 0 0 14px 0; }
      .quote-author { font-size: 13px; color: #8b949e; margin: 0; }
      .quote-author strong { color: #c9d1d9; }
      .footer { text-align: center; margin-top: 40px; padding-top: 20px;
                border-top: 1px solid #30363d; font-size: 12px; color: #6e7681; }
    </style>
    """

    parts: list[str] = []
    parts.append(f"<!DOCTYPE html><html><head><meta charset='utf-8'>{css}</head><body>")
    parts.append("<div class='container'>")

    parts.append(
        f"<div class='header'>"
        f"<h1>🗞️ Digest IA</h1>"
        f"<div class='sub'>{date} · últimas 48–72h</div>"
        f"</div>"
    )

    parts.append("<div class='section-title'>Top notícias</div>")
    for i, n in enumerate(d.top_news, 1):
        parts.append(
            f"<div class='news-item'>"
            f"<div class='news-title'><span class='news-num'>{i:02d}</span>{_esc(n.title)}</div>"
            f"<p class='news-summary'>{_esc(n.summary)}</p>"
            f"<div class='news-meta'>"
            f"<strong>{_esc(n.source_name)}</strong> · {_esc(n.date)} · "
            f"<a href='{_esc(n.url)}'>ler →</a>"
            f"</div>"
            f"</div>"
        )

    parts.append("<div class='section-title'>📄 Paper do dia</div>")
    parts.append(
        f"<div class='feature-card'>"
        f"<div class='feature-title'>{_esc(d.paper.title)}</div>"
        f"<div class='feature-meta'><strong>Autores:</strong> {_esc(', '.join(d.paper.authors))}</div>"
        f"<div class='feature-meta'><strong>Publicado em:</strong> {_esc(d.paper.venue)}</div>"
        f"<p class='feature-body'>{_esc(d.paper.why_read)}</p>"
        f"<a class='feature-link' href='{_esc(d.paper.url)}'>abrir paper →</a>"
        f"</div>"
    )

    parts.append("<div class='section-title'>💻 Repositório em alta</div>")
    parts.append(
        f"<div class='feature-card'>"
        f"<div class='feature-title'>{_esc(d.repo.full_name)}</div>"
        f"<p class='feature-body'>{_esc(d.repo.why_matters)}</p>"
        f"<a class='feature-link' href='{_esc(d.repo.url)}'>abrir repo →</a>"
        f"</div>"
    )

    parts.append("<div class='section-title'>💡 Insight do dia</div>")
    parts.append(
        f"<blockquote class='quote'>"
        f"<p class='quote-text'>“{_esc(d.insight.quote)}”</p>"
        f"<p class='quote-author'>— <strong>{_esc(d.insight.author)}</strong><br>"
        f"<span style='color:#6e7681'>{_esc(d.insight.context)}</span></p>"
        f"</blockquote>"
    )

    parts.append(
        "<div class='footer'>"
        f"Gerado automaticamente por <strong>news_agent</strong> · {date}"
        "</div>"
    )

    parts.append("</div></body></html>")
    return "".join(parts)


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
