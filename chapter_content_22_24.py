# Chapters 22–24 — Advanced topics: Productivity Paradox, Supervisory Engineering, Context Debt
from chapter_content import obj, code, tabs
from chapter_helpers import presentation_thread, journey_map_advanced

CHAPTER_BODIES_22_24 = {}

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 22 — The AI Productivity Paradox
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_22_24["22"] = presentation_thread(22, "Advanced — The AI Productivity Paradox",
    "AI can make individual tasks faster — but teams and companies are not automatically more productive. This chapter explains why seniors need to hear this.") + journey_map_advanced(22) + obj([
    "Explain the AI productivity paradox with research-backed evidence",
    "Distinguish individual task speed from team and organizational productivity",
    "List where AI-hidden work appears: review, debugging, debt, security",
    "Compare bad vs better AI usage with the payment module example",
    "Apply the lesson: productivity comes from workflows, not blind generation"
]) + """
<div class="section">
<h2>The Paradox in One Sentence</h2>
<div class="quote-block">AI can make individual tasks faster, but it does <strong>not</strong> automatically make the whole team or company more productive.</div>
<p>A developer may finish a function in 20 minutes instead of 2 hours and still feel productive — while the <em>organization</em> loses time across review, debugging, corrections, and debt. That gap is the <strong>AI Productivity Paradox</strong>.</p>
</div>

<div class="section">
<h2>What Developers Feel vs What Teams Experience</h2>
<div class="compare-grid">
<div class="compare-col good">
<h4>👤 Individual developer feels</h4>
<ul>
<li>"AI helped me write this function faster"</li>
<li>"I shipped the PR the same day"</li>
<li>"I didn't need to look up syntax"</li>
<li>"The demo works"</li>
</ul>
</div>
<div class="compare-col bad">
<h4>👥 Team / company may still lose</h4>
<ul>
<li>More review effort on larger AI diffs</li>
<li>More debugging of subtle wrong assumptions</li>
<li>More technical debt from unreviewed code</li>
<li>More security checks and incidents</li>
<li>More context correction ("that's not how we do it")</li>
<li>More dependency on AI without understanding</li>
</ul>
</div>
</div>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    subgraph Visible gain
        A[Task completed faster]
    end
    subgraph Hidden cost
        B[Review time]
        C[Debug time]
        D[Rework]
        E[Security fix]
        F[Debt paydown later]
    end
    A --> NET{Net productivity?}
    B --> NET
    C --> NET
    D --> NET
    E --> NET
    F --> NET
</div></div>
</div>

<div class="section">
<h2>What Research Shows (2025–2026)</h2>
<div class="info-box"><h4>2026 longitudinal developer study</h4>
<p><strong>82%</strong> of developers reported spending <em>less time writing code</em> — but work shifted toward <strong>supervisory engineering</strong>: directing, evaluating, and correcting AI output. Coding time went down; oversight time went up.</p></div>
<div class="warning-box"><h4>2025 randomized trial (experienced OSS developers)</h4>
<p>On <strong>mature open-source projects</strong>, AI tools <em>slowed</em> experienced developers by <strong>19%</strong> — even though those developers <em>expected</em> AI to make them faster. Familiar codebases + AI review overhead can invert the benefit.</p></div>
<table>
<tr><th>Finding</th><th>Implication for your team</th></tr>
<tr><td>Less typing, more supervising</td><td>Plan for review capacity, not just generation speed</td></tr>
<tr><td>Experts can slow down on mature code</td><td>AI is not free speed on every task</td></tr>
<tr><td>Expectations ≠ measured outcomes</td><td>Measure workflow end-to-end, not "lines per hour"</td></tr>
</table>
<div class="presentation-tip"><strong>🎤 For seniors:</strong> This is the slide that earns credibility. You are not anti-AI — you are pro-<em>realistic</em> AI. Quote the paradox before showing solutions.</div>
</div>

<div class="section">
<h2>AI Does Not Remove Work — It Changes the Type of Work</h2>
<div class="diagram-container"><div class="mermaid">
flowchart TB
    subgraph Before AI
        B1[Understand requirement]
        B2[Write code]
        B3[Test]
        B4[Review]
        B5[Deploy]
    end
    subgraph With AI undisciplined
        A1[Short prompt]
        A2[AI generates large diff]
        A3[Review huge PR]
        A4[Debug wrong assumptions]
        A5[Security fix]
        A6[Rework architecture]
    end
    subgraph With AI disciplined
        D1[Explain + plan with AI]
        D2[Small AI-generated change]
        D3[Review + test]
        D4[Ship confidently]
    end
</div></div>
<table>
<tr><th>Before AI</th><th>With AI (typical shift)</th></tr>
<tr><td>Developer writes code</td><td>Developer explains task</td></tr>
<tr><td>—</td><td>AI generates code</td></tr>
<tr><td>Developer reviews own code</td><td>Developer reviews <em>AI</em> code (harder — didn't write it)</td></tr>
<tr><td>Developer fixes bugs</td><td>Developer fixes wrong <em>assumptions</em> in plausible code</td></tr>
<tr><td>Developer tests edge cases</td><td>Developer must <em>design</em> tests AI didn't imagine</td></tr>
<tr><td>Developer owns security</td><td>Developer audits AI security patterns</td></tr>
<tr><td>—</td><td>Developer maintains <strong>ownership</strong> (still accountable)</td></tr>
</table>
</div>

<div class="section">
<h2>Where Hidden Time Goes</h2>
<table>
<tr><th>Hidden cost</th><th>What happens</th><th>Example</th></tr>
<tr><td><strong>Review inflation</strong></td><td>400-line AI PR vs 40-line human PR</td><td>Reviewer skips deep read → bug ships</td></tr>
<tr><td><strong>Assumption debugging</strong></td><td>Code runs but wrong business rule</td><td>Revenue uses billed not paid amount</td></tr>
<tr><td><strong>Context correction</strong></td><td>AI used wrong pattern for your stack</td><td>Added library you don't use</td></tr>
<tr><td><strong>Security rework</strong></td><td>SQL injection in "working" code</td><td>Emergency patch week later</td></tr>
<tr><td><strong>Tech debt</strong></td><td>Duplicate utilities, inconsistent style</td><td>6-month refactor project</td></tr>
<tr><td><strong>Eval / pipeline work</strong></td><td>Building guardrails for NL2SQL</td><td>Upfront cost — pays later</td></tr>
</table>
</div>

<div class="section">
<h2>Example: Payment Module — Bad vs Better</h2>
""" + tabs("payment-module",
"❌ Bad use (feels fast)",
code("", """Generate the full payment module with Stripe integration,
webhooks, refunds, and admin dashboard."""),
"✅ Better use (actually productive)",
code("", """First analyze the payment workflow.
List:
1. Business rules (when is payment captured vs authorized?)
2. Failure cases (webhook retry, duplicate events, idempotency)
3. Security risks (signature verify, replay, PCI scope)
4. Test scenarios (happy path, declined card, partial refund)
Do not write code yet.""")
) + """
<div class="success-box"><h4>Why "better" wins on net productivity</h4>
<ul>
<li>Smaller, reviewable implementation scope</li>
<li>Security and idempotency designed upfront</li>
<li>Tests defined before code exists</li>
<li>Less rework in production incidents</li>
</ul></div>
</div>

<div class="section">
<h2>Measuring Real Productivity</h2>
<p>Don't measure: <em>lines generated per hour</em>. Measure:</p>
<ul class="checklist">
<li>Time from ticket to <strong>merged, tested</strong> PR</li>
<li>Defect rate in AI-touched code vs baseline</li>
<li>Review time per PR (watch for inflation)</li>
<li>Incident count on AI-generated features</li>
<li>Rework rate within 30 days of merge</li>
<li>NL2SQL: eval accuracy + unsafe query rate</li>
</ul>
</div>

<div class="section">
<h2>Main Lesson</h2>
<div class="quote-block">AI productivity comes from <strong>better workflows</strong>, not blind code generation.</div>
<p>Connect to this guide: Ch 12 (daily workflow), Ch 14 (vibe coding trap), Ch 16 (evals), Ch 21 (prompt + context discipline).</p>
</div>

<div class="takeaway"><h3>Key Takeaway</h3>
<p>Feel faster ≠ team faster. Seniors should design workflows that account for review, verification, and ownership — then AI becomes a real multiplier.</p></div>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 23 — Supervisory Engineering
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_22_24["23"] = presentation_thread(23, "Advanced — Supervisory Engineering",
    "Developers are becoming supervisors of AI-generated work. This is the defining skill of the AI-native developer in 2026.") + journey_map_advanced(23) + obj([
    "Define supervisory engineering and the 2026 role shift",
    "List the seven supervisor skills every developer needs",
    "Apply junior vs senior supervisory mindsets",
    "Use the junior-then-senior-reviewer prompt pattern",
    "Connect supervision to NL2SQL, Cursor, and production ownership"
]) + """
<div class="section">
<h2>The New Developer Skill</h2>
<div class="quote-block">The future developer is not only a coder. The future developer is an <strong>AI supervisor</strong>.</div>
<p>Research on the 2026 developer workforce describes a shift to <strong>supervisory engineering work</strong>: less time typing implementations, more time directing, evaluating, and correcting AI output. This is not a downgrade — it is a <em>higher-leverage</em> role when done well.</p>
<div class="diagram-container"><div class="mermaid">
pie title Developer effort shift (AI-native teams)
    "Directing and planning" : 25
    "Reviewing and correcting AI" : 30
    "Testing and verification" : 20
    "Writing code (often with AI)" : 25
</div></div>
</div>

<div class="section">
<h2>What Is Supervisory Engineering?</h2>
<p><strong>Supervisory engineering</strong> means treating the LLM as a capable but unreliable team member: you assign work clearly, inspect output critically, reject bad work, and remain accountable for what ships.</p>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    DEV[Developer supervisor] -->|clear direction| AI[LLM worker]
    AI -->|draft output| DEV
    DEV -->|review| Q{Accept?}
    Q -->|No| FIX[Correct / re-prompt / fix]
    Q -->|Yes| TEST[Test and ship]
    FIX --> AI
</div></div>
</div>

<div class="section">
<h2>The Seven Supervisor Skills</h2>
<table>
<tr><th>#</th><th>Skill</th><th>What it means</th><th>Failure if missing</th></tr>
<tr><td>1</td><td><strong>Give clear direction</strong></td><td>Role, task, constraints, output format</td><td>AI guesses scope</td></tr>
<tr><td>2</td><td><strong>Review AI output</strong></td><td>Read every line before merge</td><td>Believable bugs ship</td></tr>
<tr><td>3</td><td><strong>Detect hallucinations</strong></td><td>Verify APIs, schema, facts</td><td>Invented tables in SQL</td></tr>
<tr><td>4</td><td><strong>Correct mistakes</strong></td><td>Fix or re-prompt with specifics</td><td>Wrong patterns spread</td></tr>
<tr><td>5</td><td><strong>Verify with tests</strong></td><td>Automated + edge cases</td><td>Demo-only correctness</td></tr>
<tr><td>6</td><td><strong>Protect architecture</strong></td><td>Reject scope creep refactors</td><td>Inconsistent system design</td></tr>
<tr><td>7</td><td><strong>Control scope</strong></td><td>One step at a time, plan-first</td><td>500-line agent diffs</td></tr>
</table>
</div>

<div class="section">
<h2>Junior Developer Lesson</h2>
<div class="compare-grid">
<div class="compare-col bad">
<h4>❌ Wrong mindset</h4>
<p><em>"AI will do everything for me."</em></p>
<ul>
<li>Merge without reading</li>
<li>Can't debug at 2am</li>
<li>Skills stagnate</li>
</ul>
</div>
<div class="compare-col good">
<h4>✅ Right mindset</h4>
<p><em>"AI helps me learn faster — I must understand what it generates."</em></p>
<ul>
<li>Ask AI to explain its code</li>
<li>Run tests yourself</li>
<li>Use AI as tutor + draft assistant</li>
</ul>
</div>
</div>
<p><strong>Junior supervisory habit:</strong> After every AI generation, write one sentence: "This code works because ___." If you can't, don't merge.</p>
</div>

<div class="section">
<h2>Senior Developer Lesson</h2>
<div class="compare-grid">
<div class="compare-col bad">
<h4>❌ Wrong mindset</h4>
<p><em>"AI is only for junior boilerplate."</em></p>
</div>
<div class="compare-col good">
<h4>✅ Right mindset</h4>
<p><em>"AI helps with architecture comparison, review, test strategy, migration planning, and documentation — I supervise quality."</em></p>
</div>
</div>
<table>
<tr><th>Senior use case</th><th>Supervisory prompt pattern</th></tr>
<tr><td>Architecture decision</td><td>3 options + trade-offs + recommendation — you decide</td></tr>
<tr><td>Code review</td><td>AI lists risks; senior approves merge</td></tr>
<tr><td>Migration planning</td><td>AI drafts steps; senior validates rollback</td></tr>
<tr><td>NL2SQL system</td><td>AI drafts pipeline; senior owns evals + ACL</td></tr>
<tr><td>Security audit</td><td>AI finds candidates; senior confirms exploitability</td></tr>
</table>
</div>

<div class="section">
<h2>Power Prompt: Junior Proposes, Senior Reviews</h2>
""" + code("", """Act in two phases.

PHASE 1 — Junior developer:
Propose a solution for: [describe task]
Include: approach, files to change, risks, test ideas.

PHASE 2 — Senior reviewer:
Critique the Phase 1 proposal for:
- correctness
- security
- maintainability
- scope creep
- missing edge cases

PHASE 3 — Safest implementation plan:
Give a minimal, safest plan based on the critique.
Do not write full code yet.""") + """
<p>This single prompt trains <strong>supervisory thinking</strong>: generate → critique → refine. Use in ChatGPT, Claude, or Cursor Ask mode.</p>
</div>

<div class="section">
<h2>Supervisory Engineering in Different Tools</h2>
<table>
<tr><th>Tool</th><th>You supervise</th><th>How</th></tr>
<tr><td>ChatGPT / Claude</td><td>Text and code drafts</td><td>Review-first; reject vague output</td></tr>
<tr><td>Cursor Agent</td><td>Multi-file diffs</td><td>Plan approve → scope @files → review diff</td></tr>
<tr><td>Copilot</td><td>Inline completions</td><td>Don't tab-accept without reading</td></tr>
<tr><td>NL2SQL app</td><td>Generated SQL</td><td>Validator + human approval gate</td></tr>
</table>
</div>

<div class="section">
<h2>Supervision vs Micromanagement</h2>
<div class="diagram-container"><div class="mermaid">
flowchart TD
    S[Good supervision] --> S1[Clear goals]
    S --> S2[Review outcomes]
    S --> S3[Trust but verify]
    M[Bad micromanagement] --> M1[Rewrite every line yourself]
    M --> M2[Reject AI entirely]
    M --> M3[Accept AI blindly]
</div></div>
<p>Supervisory engineering is the <strong>middle path</strong>: use AI fully, verify rigorously, own the result.</p>
</div>

<div class="section">
<h2>Ownership Remains Human</h2>
<div class="error-box"><h4>Incident scenario</h4>
<p>AI-generated NL2SQL exposes student emails to unauthorized role. Who is responsible?</p>
<p><strong>Answer:</strong> The developer and organization — not the model vendor. Supervisors own output.</p></div>
</div>

<div class="takeaway"><h3>Key Takeaway</h3>
<p>Supervisory engineering is the professional response to the productivity paradox: direct AI well, evaluate critically, verify always, own completely.</p></div>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 24 — Context Debt
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_22_24["24"] = presentation_thread(24, "Advanced — Context Debt",
    "Bad documentation becomes bad AI output. Context debt is the hidden reason AI systems fail even with good prompts.") + journey_map_advanced(24) + obj([
    "Define context debt and how it differs from technical debt",
    "Identify sources: stale docs, missing schema, tribal knowledge",
    "Connect context debt to NL2SQL and RAG failures",
    "Apply engineering culture fixes seniors care about",
    "Build a context debt reduction checklist for teams"
]) + """
<div class="section">
<h2>Everyone Knows Technical Debt — Meet Context Debt</h2>
<div class="compare-grid">
<div class="compare-col good">
<h4>Technical debt</h4>
<p>Shortcuts in <strong>code</strong> that slow future development.</p>
<p><em>Example:</em> Skipped tests, tangled modules.</p>
</div>
<div class="compare-col bad">
<h4>Context debt</h4>
<p>Shortcuts in <strong>knowledge</strong> that slow or break AI systems.</p>
<p><em>Example:</em> Outdated wiki, missing schema descriptions.</p>
</div>
</div>
<div class="quote-block">Bad documentation becomes bad AI output.</div>
<p><strong>Context debt</strong> means the AI system operates with incomplete, outdated, noisy, or poorly structured context — so even perfect prompts produce wrong or unreliable answers.</p>
</div>

<div class="section">
<h2>What Context Debt Looks Like</h2>
<div class="diagram-container"><div class="mermaid">
mindmap
  root((Context Debt))
    Documentation
      Outdated wiki pages
      Missing API docs
      Conflicting requirements
    Schema and data
      No column descriptions
      Undocumented joins
      Renamed tables not indexed
    Business rules
      Tribal knowledge only
      Multiple definitions
      No glossary
    AI artifacts
      Stale few-shot examples
      Wrong sample prompts in repo
      Old RAG index
    Organization
      Duplicated knowledge
      Siloed Confluence spaces
      No single source of truth
</div></div>
</div>

<div class="section">
<h2>Sources of Context Debt</h2>
<table>
<tr><th>Source</th><th>Symptom in AI output</th><th>Who suffers</th></tr>
<tr><td>Old documentation</td><td>AI cites deprecated API</td><td>Developers using Cursor/RAG</td></tr>
<tr><td>Missing schema descriptions</td><td>Hallucinated column names</td><td>NL2SQL users</td></tr>
<tr><td>Unclear business rules</td><td>Wrong revenue / retention metrics</td><td>Business users</td></tr>
<tr><td>Outdated API examples</td><td>Broken integration code</td><td>Juniors copying AI output</td></tr>
<tr><td>Duplicated knowledge</td><td>Model picks wrong version</td><td>Everyone</td></tr>
<tr><td>Conflicting requirements</td><td>Inconsistent answers</td><td>Product + engineering</td></tr>
<tr><td>Hidden tribal knowledge</td><td>AI can't retrieve what was never written</td><td>Whole company</td></tr>
<tr><td>Stale RAG index</td><td>Correct last month, wrong today</td><td>Production AI apps</td></tr>
</table>
</div>

<div class="section">
<h2>Flagship Example: Revenue by Department</h2>
<p><strong>User asks:</strong> Show revenue by department.</p>
<div class="error-box"><h4>Context in RAG index (outdated)</h4>
""" + code("", """Revenue = sum(invoice.amount)  -- wiki page last updated 2023""") + """
</div>
<div class="success-box"><h4>Actual business rule (never updated in wiki)</h4>
""" + code("", """Revenue = sum(paid_invoice.amount) - sum(refunds.amount)
-- Only finance team knows this; lives in Slack, not docs""") + """
</div>
""" + code("sql", """-- ❌ AI generates SQL from stale context
SELECT department, SUM(amount) AS revenue
FROM invoices
GROUP BY department;

-- Missing: paid filter, refund adjustment, correct table joins""") + """
<div class="warning-box"><h4>Root cause</h4>
<p>The model did not fail alone. <strong>The context failed.</strong> No prompt wording fixes missing business rules.</p></div>
</div>

<div class="section">
<h2>Context Debt in NL2SQL Projects</h2>
<div class="diagram-container"><div class="mermaid">
flowchart TD
    CD[Context debt] --> CD1[Schema registry outdated]
    CD --> CD2[No FK documentation]
    CD --> CD3[Business glossary missing]
    CD --> CD4[Example queries from old schema]
    CD1 --> FAIL[Wrong SQL]
    CD2 --> FAIL
    CD3 --> FAIL
    CD4 --> FAIL
    FAIL --> SYM[Users trust wrong numbers]
</div></div>
<table>
<tr><th>NL2SQL symptom</th><th>Likely context debt</th><th>Fix</th></tr>
<tr><td>Wrong table names</td><td>RAG index not updated after migration</td><td>CI re-index on schema change</td></tr>
<tr><td>Missing JOIN</td><td>Relationships not in entity metadata</td><td>Document FK graph per entity</td></tr>
<tr><td>Wrong metric</td><td>Stale business definition</td><td>Versioned glossary with owner</td></tr>
<tr><td>Inconsistent answers</td><td>Two docs, same term, different meanings</td><td>Single authoritative source</td></tr>
</table>
</div>

<div class="section">
<h2>Why Seniors Care: Engineering Culture Connection</h2>
<div class="quote-block">If our docs are messy, our AI assistant will be messy.<br>
If our schema is unclear, our NL-to-SQL will be unreliable.<br>
If our business rules live only in people's heads, AI cannot use them.</div>
<p>Context engineering (Ch 6–7) is not only a model problem — it is an <strong>organizational knowledge problem</strong>. Seniors who own architecture also own context quality.</p>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    CULT[Engineering culture] --> DOC[Documentation quality]
    CULT --> SCH[Schema hygiene]
    CULT --> GOV[Business rule ownership]
    DOC --> CTX[Good AI context]
    SCH --> CTX
    GOV --> CTX
    CTX --> AI[Reliable AI systems]
</div></div>
</div>

<div class="section">
<h2>Context Debt vs Prompt Failure — How to Tell</h2>
<table>
<tr><th>Signal</th><th>Probably prompt issue</th><th>Probably context debt</th></tr>
<tr><td>Wrong output format</td><td>✅ Fix template</td><td>—</td></tr>
<tr><td>Scope creep refactor</td><td>✅ Plan-first</td><td>—</td></tr>
<tr><td>Wrong metric definition</td><td>—</td><td>✅ Fix glossary / RAG</td></tr>
<tr><td>Renamed column in SQL</td><td>—</td><td>✅ Re-index schema</td></tr>
<tr><td>Conflicting answers same week</td><td>—</td><td>✅ Duplicate/conflicting docs</td></tr>
<tr><td>Worked before migration</td><td>—</td><td>✅ Stale few-shots + RAG</td></tr>
</table>
</div>

<div class="section">
<h2>Reducing Context Debt — Team Checklist</h2>
<ul class="checklist">
<li>Schema registry is source of truth — wiki links to it, not vice versa</li>
<li>Business glossary with version, owner, and review date</li>
<li>RAG re-index triggered on migration merge</li>
<li>Entity metadata includes relationships and example queries</li>
<li>Deprecate — don't duplicate — conflicting documentation</li>
<li>Few-shot examples loaded dynamically, not hardcoded stale SQL</li>
<li>Quarterly "context audit" for top 10 AI user questions</li>
<li>Tribal knowledge → written rule before NL2SQL launch</li>
</ul>
</div>

<div class="section">
<h2>Failure → Fix: Context Debt Paydown</h2>
<div class="error-box"><h4>❌ Failure</h4>
<p>NL2SQL launched with strong prompts. Accuracy 95% in demo. After org renamed <code class="inline-code">invoices</code> → <code class="inline-code">billing_invoices</code>, accuracy drops to 60%. Team blames "the model."</p></div>
<div class="success-box"><h4>✅ Fix (context debt paydown)</h4>
<ol>
<li>Schema registry auto-feeds RAG index</li>
<li>CI eval fails if golden cases break on schema PR</li>
<li>Glossary entry for every metric in finance NL2SQL</li>
<li>Ownership: data team maintains entity metadata</li>
</ol></div>
</div>

<div class="section">
<h2>Link to Anthropic's Framing</h2>
<p>Anthropic describes context engineering as curating what enters the model's limited window from many sources: tools, external data, MCP, message history. <strong>Context debt is what happens when those sources are neglected.</strong></p>
<p>Prompt engineering optimizes the question. Context engineering optimizes the knowledge. Context debt is the accumulated mess in the knowledge layer.</p>
</div>

<div class="presentation-tip"><strong>🎤 Senior audience line:</strong> "We spent $X on AI tooling but zero on schema documentation — that's context debt, and the model can't pay it down for us."</div>

<div class="takeaway"><h3>Key Takeaway</h3>
<p>Context debt is technical debt for the AI age. Pay it down with documentation, schema hygiene, versioned business rules, and fresh retrieval — or accept unreliable AI no matter how good your prompts are.</p></div>
"""
