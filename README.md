# From Prompt Engineering to Context Engineering

**How Developers Should Build, Use, and Control AI in 2026**

Interactive HTML learning guide for developer presentations — sequel to [llm-learning-guide](https://github.com/rafiq-sgc/llm-learning-guide).

## Topics Covered

- **AI failures: WHY, WHEN, HOW → solutions → success** (Ch 31 — presentation core)
- Prompt engineering fundamentals & advanced patterns
- Why AI fails (hallucination, missing context, believable wrong code)
- Context engineering (RAG, tools, agents, guardrails)
- **CampusCom NL2SQL production audit** (Ch 26–30) — real `message.py` pipeline
- Best way to use AI in daily life (ChatGPT, Cursor, Claude)
- Vibe coding risks, evals, security, governance
- 45-minute presentation master script

## Quick Start

Open `index.html` in any browser — no build step required.

```bash
cd prompt-to-context
python3 -m http.server 8080
# Visit http://localhost:8080
```

## Failure-Focused Presentation (Recommended)

| Order | Chapter | Why |
|-------|---------|-----|
| **1** | **Ch 31** | **Why/When/How AI fails + fixes + daily success** |
| — | **[Cheat sheet](cheat-sheet.html)** | **One-page printable speaker notes** |
| 2 | Ch 5 | Failure taxonomy (deep dive) |
| 3 | Ch 26–28 | Real NL2SQL failure examples |
| 4 | Ch 12 | Best daily AI habits |
| 5 | Ch 30 | Timing + IDE setup |

**31 chapters total.**

## Learning Paths

1. **Pass 1 (Ch 1–6):** Foundations
2. **Pass 2 (Ch 7–15):** Implementation
3. **Pass 3 (Ch 11–20):** Production & delivery
4. **Pass 4 (Ch 21–25):** Advanced reference
5. **Pass 5 (Ch 26–30):** CampusCom NL2SQL deep dive
6. **Pass 6 (Ch 31):** ⭐ Failure → Success (presentation core)

## Regenerating

```bash
python3 generate_site.py
```

## Prepared For

Sakib Hasan · Office AI Presentation · June 2026
