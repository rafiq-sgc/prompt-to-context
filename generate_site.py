#!/usr/bin/env python3
"""Generate the Context Engineering Learning Guide HTML site."""

from pathlib import Path

OUTPUT = Path(__file__).parent
TOTAL = 25

CHAPTERS = [
    ("01", "🚀", "Introduction", "From AI User to AI-Native Developer",
     "Understand the shift from casual AI usage to professional AI-assisted development."),
    ("02", "🧠", "LLM Recap", "Quick Recap of LLMs for Developers",
     "Advanced: autoregressive generation, failure taxonomy, lost-in-the-middle, ICL vs RAG."),
    ("03", "✍️", "Prompt Basics", "Prompt Engineering Fundamentals",
     "Advanced: prompts as API contracts, message roles, structured JSON output, token budgets."),
    ("04", "🎯", "Advanced Prompts", "Advanced Prompting Techniques",
     "Advanced: workflow state machine, ReAct, rubrics, pattern matrix, IDE patterns."),
    ("05", "⚠️", "Why Prompts Fail", "Why Prompting Alone Fails",
     "Advanced: failure taxonomy, 3 case studies, context rot, decision tree, metrics."),
    ("06", "🏗️", "Context Engineering", "Context Engineering",
     "Advanced: 7-layer stack, context assembly, guardrails, NL-to-SQL bundle, observability."),
    ("07", "📚", "RAG", "Retrieval-Augmented Generation",
     "Embeddings, chunking, hybrid search, NL2SQL indexing, RAG failures and fixes."),
    ("08", "🔧", "Tools & MCP", "Tool Use, Function Calling, and MCP",
     "Function calling flow, MCP, tool permissions, ChatGPT/Cursor/Claude tool models."),
    ("09", "🤖", "AI Agents", "AI Agents",
     "Agent loop behind Cursor Agent, workflow vs agent, safe permissions for coding & SQL."),
    ("10", "👥", "Multi-Agent", "Multi-Agent Systems",
     "Role-separated agents, NL2SQL pipeline, Ch2–10 blueprint, when not to use."),
    ("11", "🔄", "AI SDLC", "AI-Augmented SDLC",
     "AI per SDLC phase, human checkpoints, NL2SQL through lifecycle, failure→fix."),
    ("12", "⚡", "Productivity", "Developer Productivity Workflow",
     "6-stage daily workflow, tool-specific prompts, junior vs senior habits."),
    ("13", "🛠️", "AI Tools", "ChatGPT, Claude, Cursor, Copilot & AI IDEs",
     "Behind the scenes per tool, decision tree, deep comparison, durable skills."),
    ("14", "🎨", "Vibe Coding", "Vibe Coding — Benefits and Dark Side",
     "Prototype vs production mode, auth case study, responsible checklist."),
    ("15", "🗄️", "NL-to-SQL", "NL-to-SQL Production Case Study",
     "Flagship 3-stage live demo script, enterprise entities, Ch2–10 applied."),
    ("16", "📊", "Evals", "Evals and AI Quality Measurement",
     "Golden datasets, CI pipeline, retrieval + generation metrics, eval categories."),
    ("17", "🔒", "Security", "AI Security and Prompt Injection",
     "Threat model, injection demo, OWASP-style defenses, NL2SQL security checklist."),
    ("18", "🏢", "Governance", "AI Governance for Companies",
     "Shadow AI, developer policy, controls stack, organizational questions."),
    ("19", "🔮", "Future", "Productivity, Pros/Cons & Future of Coding",
     "Honest productivity table, junior/senior paths, durable skills 2026."),
    ("20", "🎤", "Present", "Presentation Flow & Checklist",
     "Full 5-act arc, timing, demos, speaker scripts, slide mapping, checklist."),
    ("21", "⚖️", "Prompt vs Context", "Prompt vs Context Engineering — Deep Dive",
     "Definitive guide: definitions, differences, when/how to use, daily life + NL2SQL examples."),
    ("22", "⚡", "Productivity Paradox", "The AI Productivity Paradox",
     "Why faster tasks ≠ faster teams — research, hidden costs, workflow lesson."),
    ("23", "👁️", "Supervisory Eng.", "Supervisory Engineering",
     "The new developer skill: direct, review, verify, own — junior and senior lessons."),
    ("24", "📉", "Context Debt", "Context Debt",
     "Bad docs → bad AI — sources, NL2SQL examples, team checklist, culture link."),
    ("25", "🔬", "How LLMs Work", "How LLM Models Work — Complete Guide",
     "Architecture, training, inference, parameters, model families, best output playbook."),
]


def nav_html(active: str = "index") -> str:
    items = ['<li><a href="index.html"' + (' class="active"' if active == "index" else "") + '>🏠 Home</a></li>']
    for num, icon, short, title, _ in CHAPTERS:
        href = f"chapter{num}.html"
        cls = ' class="active"' if active == num else ""
        items.append(f'<li><a href="{href}"{cls}>{icon} Ch{int(num)}: {short}</a></li>')
    return "\n                ".join(items)


def page_shell(active, title, subtitle, body, prev_link, next_link, ch_num=None):
    ch_label = f"Chapter {int(ch_num)} of {TOTAL}" if ch_num else "Home"
    prev_a = f'<a href="{prev_link}">← Previous</a>' if prev_link else "<span></span>"
    next_a = f'<a href="{next_link}">Next Chapter →</a>' if next_link else "<span></span>"
    nav = nav_html(active)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="reading-progress"></div>
    <button class="mobile-menu-toggle" onclick="toggleMobileMenu()" aria-label="Toggle menu">☰</button>
    <div class="container">
        <header class="header">
            <h1>{title}</h1>
            <p class="subtitle">{subtitle}</p>
        </header>
        <nav class="nav-sidebar" id="nav-sidebar">
            <div class="nav-brand">CONTEXT ENGINEERING 2026</div>
            <ul>
                {nav}
            </ul>
        </nav>
        <main class="main-content">
            {body}
        </main>
        <footer class="footer">
            <p>From Prompt Engineering to Context Engineering — Developer Learning Guide</p>
            <p>{ch_label} · Prepared for Sakib Hasan · June 2026</p>
        </footer>
    </div>
    <script src="js/app.js"></script>
</body>
</html>"""


def chapter_nav(num: str) -> tuple:
    idx = next(i for i, c in enumerate(CHAPTERS) if c[0] == num)
    prev_link = "index.html" if idx == 0 else f"chapter{CHAPTERS[idx-1][0]}.html"
    next_link = None if idx == len(CHAPTERS) - 1 else f"chapter{CHAPTERS[idx+1][0]}.html"
    return prev_link, next_link


def ch_header(num, icon, title, desc):
    return f"""
            <div class="chapter-header">
                <h1>{icon} Chapter {int(num)}: {title}</h1>
                <p class="chapter-meta">{desc}</p>
            </div>"""


def ch_nav_block(prev, next_):
    prev_a = f'<a href="{prev}">← Previous</a>' if prev else "<span></span>"
    next_a = f'<a href="{next_}">Next Chapter →</a>' if next_ else "<span></span>"
    return f'<div class="chapter-nav">{prev_a}<a href="index.html">🏠 Home</a>{next_a}</div>'


# Import chapter bodies
from chapter_content import CHAPTER_BODIES  # noqa: E402


def generate_chapters():
    for num, icon, short, title, desc in CHAPTERS:
        prev, nxt = chapter_nav(num)
        body = ch_header(num, icon, title, desc)
        body += ch_nav_block(prev, nxt)
        body += CHAPTER_BODIES[num]
        body += ch_nav_block(prev, nxt)
        html = page_shell(num, f"Chapter {int(num)}: {title}", desc, body, prev, nxt, num)
        (OUTPUT / f"chapter{num}.html").write_text(html, encoding="utf-8")
        print(f"  chapter{num}.html")


def generate_index():
    toc = ""
    for num, icon, short, title, desc in CHAPTERS:
        toc += f"""
                        <a href="chapter{num}.html" class="toc-item">
                            <span class="toc-number">{num}</span>
                            <div class="toc-content">
                                <h4>{icon} {title}</h4>
                                <p>{desc}</p>
                            </div>
                        </a>"""

    body = f"""
            <div class="hero">
                <h2>From Prompt Engineering to Context Engineering</h2>
                <p class="lead">How Developers Should Build, Use, and Control AI in 2026 — a complete study guide focusing on AI failures, fixes, and productive professional usage.</p>
            </div>

            <div class="tagline-banner">
                Prompting is how we talk to AI. Context engineering is how we make AI useful.
                Evals make it reliable. Guardrails make it safe. Human judgment makes it valuable.
            </div>

            <div class="overview-cards">
                <div class="card">
                    <div class="card-icon">⚠️</div>
                    <h3>Failure-First Learning</h3>
                    <p>Every chapter shows how AI fails in real projects — hallucinated SQL, prompt injection, vibe coding debt — then how to fix it.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🏗️</div>
                    <h3>Production Patterns</h3>
                    <p>RAG pipelines, tool permissions, agent loops, evals, and NL-to-SQL workflows you can demo to senior and junior developers.</p>
                </div>
                <div class="card">
                    <div class="card-icon">📊</div>
                    <h3>Visual & Interactive</h3>
                    <p>Mermaid diagrams, weak-vs-strong prompt comparisons, code examples, and presentation tips in every chapter.</p>
                </div>
                <div class="card">
                    <div class="card-icon">🎤</div>
                    <h3>Presentation Ready</h3>
                    <p>Sequel to "Behind the Scenes of LLMs" — structured for learning first, then converting sections into slides and live demos.</p>
                </div>
            </div>

            <div class="section">
                <h2>📍 Three-Pass Learning Path</h2>
                <div class="learning-path">
                    <div class="path-phase">
                        <h3>Pass 1 — Foundations (Chapters 1–6)</h3>
                        <p>AI-native developer mindset, LLM recap, prompt engineering, why prompts fail, and context engineering fundamentals.</p>
                    </div>
                    <div class="path-phase phase-2">
                        <h3>Pass 2 — Implementation (Chapters 7–15)</h3>
                        <p>RAG, tools, MCP, agents, multi-agent systems, SDLC, productivity workflows, AI tools, vibe coding, and NL-to-SQL.</p>
                    </div>
                    <div class="path-phase phase-3">
                        <h3>Pass 3 — Production & Delivery (Chapters 11–20)</h3>
                        <p>SDLC, productivity, tools, vibe coding, NL2SQL demo, evals, security, governance, future skills, and presentation delivery.</p>
                    </div>
                    <div class="path-phase" style="border-left-color:#7c3aed">
                        <h3>Pass 4 — Advanced & Reference (Chapters 21–25)</h3>
                        <p>Prompt vs context, productivity paradox, supervisory engineering, context debt, and the complete LLM models reference.</p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>📑 All Chapters</h2>
                <div class="toc-grid">{toc}
                </div>
            </div>

            <div class="quick-start">
                <h2>🚀 Start Learning</h2>
                <p>Read sequentially, or jump to <strong>Ch 25</strong> (how LLMs work), <strong>Ch 21</strong> (prompt vs context), Ch 15 (NL2SQL), or Ch 5 (why AI fails).</p>
                <div class="button-group">
                    <a href="chapter01.html" class="btn btn-primary">Chapter 1 →</a>
                    <a href="chapter25.html" class="btn btn-secondary">How LLMs Work</a>
                    <a href="chapter21.html" class="btn btn-secondary">Prompt vs Context</a>
                </div>
            </div>

            <div class="section">
                <h2>🔗 Related Resource</h2>
                <p>Previous presentation companion: <a href="https://github.com/rafiq-sgc/llm-learning-guide" target="_blank" rel="noopener">Behind the Scenes of LLMs — Learning Guide</a> (tokens, transformers, how LLMs work).</p>
                <p>This guide is the advanced sequel: from <em>how LLMs work</em> to <em>how developers build, use, and control AI systems</em>.</p>
            </div>"""

    html = page_shell("index", "Context Engineering Guide 2026",
                      "Prompting · RAG · Agents · Evals · Security · Productive AI Development", body, None, "chapter01.html")
    (OUTPUT / "index.html").write_text(html, encoding="utf-8")
    print("  index.html")


if __name__ == "__main__":
    print("Generating site...")
    generate_index()
    generate_chapters()
    print("Done.")
