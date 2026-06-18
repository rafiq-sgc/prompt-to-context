# Shared helpers for chapter content — presentation theme alignment

PRESENTATION_TITLE = "From Prompt Engineering to Context Engineering"
PRESENTATION_SUB = "How Developers Should Build, Use, and Control AI in 2026"


def presentation_thread(ch_num: int, phase: str, bridge: str) -> str:
    """Consistent banner linking each chapter to the presentation arc."""
    return f"""
<div class="tagline-banner" style="text-align:left;margin-bottom:1.5rem">
<strong>{PRESENTATION_TITLE}</strong><br>
<span style="font-size:.95rem;color:#4338ca">{PRESENTATION_SUB}</span>
<div style="margin-top:.75rem;font-size:.9rem;color:#334155">
📍 <strong>Chapter {ch_num}</strong> · Phase: <strong>{phase}</strong><br>
{bridge}
</div>
</div>"""


def journey_map(highlight: int) -> str:
    """Visual map of chapters 2–10 in the presentation arc."""
    steps = [
        (2, "LLM Recap", "Know what the model actually does"),
        (3, "Prompts", "First layer of control"),
        (4, "Advanced Prompts", "Control workflow, not wording"),
        (5, "Why Prompts Fail", "Failure → need context"),
        (6, "Context Engineering", "Core topic — design the environment"),
        (7, "RAG", "Connect to trusted knowledge"),
        (8, "Tools & MCP", "Let model verify, not guess"),
        (9, "Agents", "Multi-step with permissions"),
        (10, "Multi-Agent", "Specialize when justified"),
    ]
    items = []
    for num, label, desc in steps:
        style = "font-weight:700;color:#4f46e5" if num == highlight else "color:#64748b"
        items.append(f'<span style="{style}">Ch{num} {label}</span>')
    flow = " → ".join(items)
    return f"""
<div class="diagram-section">
<h3>Your Presentation Journey (Chapters 2–10)</h3>
<div style="overflow-x:auto;padding:.5rem 0;font-size:.82rem;line-height:2">{flow}</div>
<p style="font-size:.88rem;color:#64748b;margin-top:.5rem">Prompting is how we talk to AI. Context engineering is how we make AI useful. Chapters 7–10 show how to <em>build</em> applications (NL2SQL, chatbots, coding assistants) on top.</p>
</div>"""


def journey_map_production(highlight: int) -> str:
    """Visual map of chapters 11–20 — production, productivity, delivery."""
    steps = [
        (11, "SDLC", "AI across the lifecycle"),
        (12, "Workflow", "Daily productivity"),
        (13, "Tools", "ChatGPT, Cursor, Claude"),
        (14, "Vibe Coding", "Speed vs discipline"),
        (15, "NL-to-SQL", "Flagship case study"),
        (16, "Evals", "Make AI reliable"),
        (17, "Security", "Make AI safe"),
        (18, "Governance", "Make AI organizational"),
        (19, "Future", "Skills & productivity"),
        (20, "Present", "Deliver the talk"),
    ]
    items = []
    for num, label, _ in steps:
        style = "font-weight:700;color:#4f46e5" if num == highlight else "color:#64748b"
        items.append(f'<span style="{style}">Ch{num} {label}</span>')
    flow = " → ".join(items)
    return f"""
<div class="diagram-section">
<h3>Production & Delivery Journey (Chapters 11–20)</h3>
<div style="overflow-x:auto;padding:.5rem 0;font-size:.82rem;line-height:2">{flow}</div>
<p style="font-size:.88rem;color:#64748b;margin-top:.5rem">Chapters 2–10 taught you to <em>build</em> AI systems. Chapters 11–20 teach you to <em>use, measure, secure, govern</em>, and <em>present</em> them professionally.</p>
</div>"""


def journey_map_llm(highlight: int = 25) -> str:
    """Reference map linking Ch 2 recap to Ch 25 deep dive and downstream chapters."""
    steps = [
        (2, "LLM Recap", "Production mental model"),
        (25, "LLM Deep Dive", "Architecture & best output"),
        (3, "Prompts", "Control the ask"),
        (6, "Context", "Control the environment"),
        (7, "RAG", "Ground truth"),
    ]
    items = []
    for num, label, _ in steps:
        style = "font-weight:700;color:#4f46e5" if num == highlight else "color:#64748b"
        items.append(f'<span style="{style}">Ch{num} {label}</span>')
    flow = " → ".join(items)
    return f"""
<div class="diagram-section">
<h3>LLM Knowledge Path</h3>
<div style="overflow-x:auto;padding:.5rem 0;font-size:.82rem;line-height:2">{flow}</div>
<p style="font-size:.88rem;color:#64748b;margin-top:.5rem"><a href="chapter02.html">Chapter 2</a> = fast recap for seniors. <strong>Chapter 25</strong> = full reference. Then apply via prompts, context, and evals.</p>
</div>"""


def journey_map_advanced(highlight: int) -> str:
    """Visual map of chapters 22–24 — advanced topics."""
    steps = [
        (22, "Productivity Paradox", "Feel faster ≠ team faster"),
        (23, "Supervisory Engineering", "Direct, review, own"),
        (24, "Context Debt", "Bad docs → bad AI"),
    ]
    items = []
    for num, label, _ in steps:
        style = "font-weight:700;color:#4f46e5" if num == highlight else "color:#64748b"
        items.append(f'<span style="{style}">Ch{num} {label}</span>')
    flow = " → ".join(items)
    return f"""
<div class="diagram-section">
<h3>Advanced Topics (Chapters 22–24)</h3>
<div style="overflow-x:auto;padding:.5rem 0;font-size:.82rem;line-height:2">{flow}</div>
<p style="font-size:.88rem;color:#64748b;margin-top:.5rem">These chapters answer the hard questions seniors ask: <em>Why doesn't AI always speed us up? What is my new role? Why does our AI know nothing about our business?</em></p>
</div>"""


def journey_map_failures(highlight: int = 31) -> str:
    """Visual map for failure-focused presentation arc."""
    steps = [
        (5, "Why Prompts Fail", "Failure taxonomy"),
        (31, "Why/When/How", "Presentation core"),
        (6, "Context Fix", "Engineering solutions"),
        (26, "NL2SQL Real", "Your app examples"),
        (12, "Daily Success", "Best habits"),
    ]
    items = []
    for num, label, _ in steps:
        style = "font-weight:700;color:#dc2626" if num == highlight else "color:#64748b"
        items.append(f'<span style="{style}">Ch{num} {label}</span>')
    flow = " → ".join(items)
    return f"""
<div class="diagram-section">
<h3>Failure → Solution → Success Path</h3>
<div style="overflow-x:auto;padding:.5rem 0;font-size:.82rem;line-height:2">{flow}</div>
<p style="font-size:.88rem;color:#64748b;margin-top:.5rem"><strong>Chapter 31</strong> is the presentation centerpiece: why AI fails, when it fails, how to fix it, and how to use AI successfully in daily life and production.</p>
</div>"""


def journey_map_nl2sql_capstone(highlight: int) -> str:
    """Visual map of chapters 26–30 — CampusCom NL2SQL deep dive."""
    steps = [
        (26, "Pipeline E2E", "message.py orchestration"),
        (27, "Prompt Audit", "Every LLM call inventoried"),
        (28, "9 Layers", "Mapped to your codebase"),
        (29, "Roadmap", "Gaps & improvements"),
        (30, "Master Script", "45-min talk + IDE setup"),
    ]
    items = []
    for num, label, _ in steps:
        style = "font-weight:700;color:#4f46e5" if num == highlight else "color:#64748b"
        items.append(f'<span style="{style}">Ch{num} {label}</span>')
    flow = " → ".join(items)
    return f"""
<div class="diagram-section">
<h3>NL2SQL Deep Dive (Chapters 26–30)</h3>
<div style="overflow-x:auto;padding:.5rem 0;font-size:.82rem;line-height:2">{flow}</div>
<p style="font-size:.88rem;color:#64748b;margin-top:.5rem">Chapters 1–25 teach patterns. <strong>Chapters 26–30</strong> apply every concept to the <em>CampusCom NL2SQL</em> codebase you ship in production.</p>
</div>"""


def tool_stack_table() -> str:
    return """
<table>
<tr><th>Tool</th><th>What it really is</th><th>Best for juniors</th><th>Best for seniors</th><th>Failure mode</th></tr>
<tr><td><strong>ChatGPT</strong></td><td>Chat UI over a remote LLM API</td><td>Learning, quick questions</td><td>Architecture drafts, eval design</td><td>Treating chat as source of truth</td></tr>
<tr><td><strong>Claude</strong></td><td>Chat + API + long-context models</td><td>Explaining code, writing docs</td><td>Long doc analysis, review</td><td>Pasting prod secrets into chat</td></tr>
<tr><td><strong>Cursor</strong></td><td>IDE + codebase index + agent loop</td><td>Small edits with @file</td><td>Plan-first multi-file with rules</td><td>Agent refactors without review</td></tr>
<tr><td><strong>GitHub Copilot</strong></td><td>Inline completion on current file context</td><td>Boilerplate, tests</td><td>Fast typing aid only</td><td>Accepting wrong completions blindly</td></tr>
<tr><td><strong>Your NL2SQL app</strong></td><td>Custom pipeline: RAG + LLM + validators</td><td>—</td><td>Full control, evals, governance</td><td>Prompt-only without schema RAG</td></tr>
</table>"""
