# From Prompt Engineering to Context Engineering

**How Developers Should Build, Use, and Control AI in 2026**

Interactive HTML learning guide for developer presentations — sequel to [llm-learning-guide](https://github.com/rafiq-sgc/llm-learning-guide).

## Topics Covered

- Prompt engineering fundamentals & advanced patterns
- Why AI fails (hallucination, missing context, believable wrong code)
- Context engineering (RAG, tools, agents, guardrails)
- NL-to-SQL production case study
- Vibe coding risks, evals, security, governance
- Presentation flow & checklist

## Quick Start

Open `index.html` in any browser — no build step required.

```bash
# Optional: serve locally
cd prompt-to-context
python3 -m http.server 8080
# Visit http://localhost:8080
```

## Structure

| File | Description |
|------|-------------|
| `index.html` | Home page with learning path & chapter index |
| `chapter01.html` … `chapter20.html` | One chapter per page |
| `styles.css` | Responsive design |
| `js/app.js` | Tabs, mobile menu, copy buttons, progress bar |
| `generate_site.py` | Regenerates HTML from `chapter_content.py` |

## Learning Path

1. **Pass 1 (Ch 1–6):** Foundations — prompts, failures, context engineering
2. **Pass 2 (Ch 7–15):** Implementation — RAG, agents, NL-to-SQL, vibe coding
3. **Pass 3 (Ch 16–20):** Production — evals, security, governance, presentation

### Core presentation arcs

**Ch 2–10 (Build):** Presentation banner, journey map, LLM mechanics, failure→fix examples, ChatGPT / Cursor / Claude / NL2SQL guidance. Chapter 10 ends with the Ch2–10 application blueprint.

**Ch 11–20 (Use · Control · Deliver):** Production journey map, SDLC integration, daily workflow, tool comparison, vibe coding, flagship NL2SQL demo script, evals, security, governance, future skills, and full presentation delivery guide (timing, demos, slide mapping).

**Ch 21–25 (Advanced & Reference):** Prompt vs context; productivity paradox; supervisory engineering; context debt; complete LLM models guide.

**25 chapters total.**

## Regenerating

After editing chapter content files (`chapter_content_02_06.py`, `chapter_content_07_10.py`, etc.):

```bash
python3 generate_site.py
```

## Prepared For

Sakib Hasan · Office AI Presentation · June 2026
