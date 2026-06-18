# Chapters 26–30 — CampusCom NL2SQL deep dive (audit + presentation capstone)
from chapter_content import obj, code, tabs
from chapter_helpers import presentation_thread, journey_map_nl2sql_capstone

CHAPTER_BODIES_26_30 = {}

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 26 — Message Endpoint End-to-End
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_26_30["26"] = presentation_thread(26, "NL2SQL Deep Dive — Pipeline",
    "Your real production path: <code>app/routers/message.py</code> from user question to streamed SQL response. This is the architecture you demo to seniors.") + journey_map_nl2sql_capstone(26) + obj([
    "Trace the full NL2SQL request path from HTTP to database",
    "Identify which steps use an LLM vs deterministic code",
    "Explain where context is assembled before each model call",
    "Map each stage to prompt engineering vs context engineering",
    "Use this flow as your live presentation backbone"
]) + """
<div class="section">
<h2>Why Start Here</h2>
<p>Chapters 1–25 teach patterns with generic examples. <strong>Chapter 26 onward uses your actual CampusCom NL2SQL application</strong> — the system you build every day. Seniors want to see a real pipeline, not a toy diagram.</p>
<div class="quote-block">The message endpoint is not "an LLM call." It is an orchestration layer that decides <em>when</em> to call models, <em>what context</em> to inject, and <em>what code</em> must never be delegated to AI.</div>
</div>

<div class="section">
<h2>End-to-End Flow (Your Code)</h2>
<div class="diagram-container"><div class="mermaid">
flowchart TD
    POST["POST /messages/"] --> CONV[Get or create Conversation]
    CONV --> UM[Save user Message]
    UM --> KP{key_phrase_id set?}
    KP -->|yes| SKIP_INT[Skip intent — force SQL]
    KP -->|no| INT["determine_intent() — LLM #1"]
    INT --> ROUTE{datasource?}
    ROUTE -->|sql| PERM{user.query permission?}
    ROUTE -->|docs| DOCS[ask_question_proxy — external RAG]
    ROUTE -->|other| REJECT[Static refusal message]
    PERM -->|no| DENY1[Permission message]
    PERM -->|yes| DIS{Disambiguation needed?}
    DIS -->|matched terms| DISAM["SemanticPhraseMatcherTool — LLM #2"]
    DISAM --> CLARIFY[Stream clarification UI]
    DIS -->|no| HS[hybrid_search — embeddings, not LLM]
    HS --> POL[get_user_permissions + evaluate_nl_governed_access]
    POL -->|blocked| DENY2[Governed access message]
    POL -->|ok| AGENT["run_db_agent() — LLM #3 ReAct agent"]
    AGENT --> VAL[validate_and_rewrite_sql — deterministic]
    VAL -->|BLOCK| BLOCK[User-facing block message]
    VAL -->|PASS/REWRITE| EXEC[Execute SQL on Databricks]
    EXEC --> STREAM[Stream data + ai_response + usage]
</div></div>
<p><strong>File map:</strong> orchestration in <code class="inline-code">app/routers/message.py</code> · intent in <code class="inline-code">llm/intent.py</code> · disambiguation in <code class="inline-code">llm/tools.py</code> · retrieval in <code class="inline-code">embedding/utils.py</code> · agent in <code class="inline-code">llm/sql_agent.py</code> · validator in <code class="inline-code">llm/sql_validator.py</code>.</p>
</div>

<div class="section">
<h2>Step-by-Step: What Happens on Each Request</h2>
<table>
<tr><th>Step</th><th>Component</th><th>LLM?</th><th>Context injected</th></tr>
<tr><td>1</td><td>Conversation + user message saved</td><td>❌</td><td>Stores <code>chat_data.message</code> for audit</td></tr>
<tr><td>2</td><td>Intent routing</td><td>✅</td><td>System rules + 26 few-shot pairs + user question</td></tr>
<tr><td>3</td><td>Permission gate (<code>current_user.query</code>)</td><td>❌</td><td>User role flags — before any SQL LLM</td></tr>
<tr><td>4</td><td>Key-phrase disambiguation</td><td>✅</td><td>Canonical terms list + user query</td></tr>
<tr><td>5</td><td>Hybrid search</td><td>❌ (embeddings)</td><td>Top tables, entities, metadata text</td></tr>
<tr><td>6</td><td>Security policy compile</td><td>❌</td><td>Entities, tables, governed rules per user</td></tr>
<tr><td>7</td><td>NL governed access check</td><td>❌</td><td>NL query + policy — blocks before agent</td></tr>
<tr><td>8</td><td>SQL ReAct agent</td><td>✅</td><td>System prefix + schema tools + metadata + ACL block</td></tr>
<tr><td>9</td><td>SQL validator + rewrite</td><td>❌</td><td>Policy, runtime columns, identity placeholders</td></tr>
<tr><td>10</td><td>Execute + stream</td><td>❌</td><td>Validated SQL only — never raw LLM output</td></tr>
</table>
<div class="info-box"><h4>Key design principle already in your app</h4>
<p><strong>Security is deterministic.</strong> The LLM drafts SQL; <code class="inline-code">validate_and_rewrite_sql</code> has final authority. This is correct context engineering — the model proposes, code disposes.</p></div>
</div>

<div class="section">
<h2>Two Paths: SQL vs Docs</h2>
<div class="compare-grid">
<div class="compare-col">
<h4>🗄️ SQL path (your core product)</h4>
<ul>
<li>Full context pipeline: retrieval → policy → agent → validator</li>
<li>Three LLM touchpoints (intent, disambiguation, SQL agent)</li>
<li>Streaming loaders: ambiguity check, SQL construction, query execution</li>
</ul>
</div>
<div class="compare-col good">
<h4>📚 Docs path</h4>
<ul>
<li><code>ask_question_proxy</code> — external help/training RAG</li>
<li>Separate permission: <code>current_user.ask_question_api</code></li>
<li>Teaches audience: one app, multiple AI backends by intent</li>
</ul>
</div>
</div>
</div>

<div class="section">
<h2>Disambiguation: Context Across Turns</h2>
<p>When ambiguous key phrases match, the API streams clarification chunks and saves <code>conversation.disambiguation</code>. On follow-up, the client sends <code>key_phrase_id</code> and optionally <code>original_prompt</code>:</p>
""" + code("python", """# message.py — recombining context after user clarifies
if chat_data.original_prompt:
    msg = chat_data.original_prompt + " " + chat_data.message
else:
    msg = chat_data.message

# hybrid_search + run_db_agent use the recombined msg""") + """
<p><strong>Presentation point:</strong> This is context engineering for multi-turn NL2SQL — not chat history in the LLM, but <em>structured state</em> the orchestrator controls.</p>
</div>

<div class="section">
<h2>Streaming Protocol (Demo-Friendly)</h2>
<p>Your endpoint streams XML-tagged chunks — great for UI and for explaining layers in a talk:</p>
<table>
<tr><th>Tag</th><th>Meaning</th><th>When to show in demo</th></tr>
<tr><td><code>&lt;loader&gt;</code></td><td>Progress step</td><td>"Watch the pipeline think"</td></tr>
<tr><td><code>&lt;sql_query&gt;</code></td><td>Drafted SQL</td><td>"Model proposed this"</td></tr>
<tr><td><code>&lt;data&gt;</code></td><td>Result JSON</td><td>"Only after validator passed"</td></tr>
<tr><td><code>&lt;message&gt;</code></td><td>User-facing status</td><td>Blocks, permissions, errors</td></tr>
<tr><td><code>&lt;ai_response&gt;</code></td><td>Reasoning summary</td><td>"Human must still read this"</td></tr>
</table>
</div>

<div class="presentation-tip"><strong>🎤 Live demo script (2 min):</strong> Ask a reporting question → point at intent loader → show hybrid search narrowing tables in logs → show SQL draft → explain validator rewrite → show data. Say: "Three LLM calls, four deterministic guardrails."</div>
<div class="takeaway"><h3>Key Takeaway</h3>
<p>Your message endpoint is a <strong>context orchestrator</strong>. Prompt engineering lives inside each LLM step; context engineering is the full path including retrieval, policy, and validation.</p></div>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 27 — Every LLM Call Audited
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_26_30["27"] = presentation_thread(27, "NL2SQL Deep Dive — Prompt Inventory",
    "Every prompt in the CampusCom codebase: what it does, what context it receives, which model runs it, and what can go wrong.") + journey_map_nl2sql_capstone(27) + obj([
    "List every LLM invocation in the NL2SQL application",
    "Classify each prompt by role: router, extractor, generator, assistant",
    "Understand task-specific model routing via config",
    "Spot anti-patterns and strengths in current prompts",
    "Compare prompt-only steps vs context-heavy steps"
]) + """
<div class="section">
<h2>LLM Inventory (Production Path)</h2>
<table>
<tr><th>#</th><th>Location</th><th>Task key</th><th>Output</th><th>Primary context</th></tr>
<tr><td>1</td><td><code>llm/intent.py</code></td><td><code>intent_routing</code></td><td>JSON: sql / docs / other</td><td>26 few-shot examples + rules</td></tr>
<tr><td>2</td><td><code>llm/tools.py</code></td><td><code>semantic_disambiguation</code></td><td>SemanticMatchOutput</td><td>terms_list + user_query</td></tr>
<tr><td>3</td><td><code>llm/sql_agent.py</code></td><td><code>sql_generation</code></td><td>ReAct + structured JSON</td><td>construct_system_prefix bundle</td></tr>
<tr><td>4</td><td><code>llm/sql_agent.py</code></td><td><code>sql_generation</code></td><td>Fallback SQL text</td><td>Question + tables + metadata (recovery)</td></tr>
</table>
<p><strong>Admin / permissions subsystem</strong> (separate from message endpoint):</p>
<table>
<tr><th>Location</th><th>Purpose</th><th>Context</th></tr>
<tr><td><code>llm/permissions/prompts.py</code></td><td>Suggest entities for new role</td><td>Role description + entity docs + preview tables</td></tr>
<tr><td><code>llm/permissions/prompts.py</code></td><td>Role conversation agent</td><td>Dynamic system prompt + rules docs + DB tool results</td></tr>
<tr><td><code>llm/permissions/prompts.py</code></td><td>State sync (structured)</td><td>Conversation history → UI state JSON</td></tr>
<tr><td><code>llm/policy_compiler.py</code></td><td>Compile governed policy draft</td><td>Role rows + metadata semantics</td></tr>
</table>
</div>

<div class="section">
<h2>Model Routing (Smart Cost Control)</h2>
<p><code>llm/utils.py → get_llm(task)</code> maps tasks to config models:</p>
""" + code("python", """# config.py settings (task-specific overrides)
chat_model              # default
chat_model_low_cost     # cheaper fallback
chat_model_intent       # intent_routing
chat_model_disambiguation
chat_model_sql_generation
chat_model_policy_compiler""") + """
<div class="info-box"><h4>Why this matters for your presentation</h4>
<p>Context engineering includes <strong>which model sees which context</strong>. Routing cheap models to intent/disambiguation and a stronger model to SQL generation is a 2026 best practice — you already do it.</p></div>
</div>

<div class="section">
<h2>Prompt Deep Dive #1 — Intent Router</h2>
<p><strong>File:</strong> <code class="inline-code">llm/intent.py</code></p>
""" + tabs("intent", "❌ Weak pattern", """<p>Single line: "Classify this question as sql or docs."</p>
<p>No examples → model confuses "how many students" (sql) vs "how do I count students" (docs).</p>""",
"✅ Your pattern", """<ul>
<li>Clear decision rules: data retrieval = sql, how/where/what is = docs</li>
<li><strong>26 few-shot pairs</strong> covering edge cases (definitions, jokes, weather)</li>
<li>Structured output via Pydantic <code>RouteQuery</code> — no free-text parsing</li>
<li>Confidence score for future thresholding</li>
</ul>""") + """
<div class="warning-box"><h4>Gap to mention honestly</h4>
<p>Intent receives <strong>only the current question</strong> — no conversation history. Follow-ups like "same but for last year" may misroute. Improvement: pass last user turn as optional context (Ch 29).</p></div>
</div>

<div class="section">
<h2>Prompt Deep Dive #2 — Semantic Disambiguation</h2>
<p><strong>File:</strong> <code class="inline-code">llm/tools.py → SemanticPhraseMatcherTool</code></p>
<p>Matches user phrases against canonical key phrases (e.g. business terms with multiple meanings). Strong prompt features:</p>
<ul>
<li>Match priority ladder: exact → partial → semantic → contextual</li>
<li>Structured schema prevents invented terms</li>
<li>Separate <code>clarification_message</code> — conversational, does not list terms (UI handles options)</li>
<li>Silent fallback to empty matches on error (safe degrade)</li>
</ul>
""" + tabs("disambig", "Failure mode", """<p>User says "active students" but key phrase list has both "active enrollment" and "active holds" — model must not merge unrelated concepts.</p>""",
"Your guardrail", """<p>Rules forbid semantic opposites, require exact <code>terms_list</code> membership, and longest-span wins for duplicates.</p>""") + """
</div>

<div class="section">
<h2>Prompt Deep Dive #3 — SQL Agent System Prefix</h2>
<p><strong>File:</strong> <code class="inline-code">llm/utils.py → construct_system_prefix()</code></p>
<p>This is your <strong>largest context bundle</strong> — injected as <code>SystemMessage</code> into a LangGraph ReAct agent:</p>
<table>
<tr><th>Section in prefix</th><th>Source</th><th>Type</th></tr>
<tr><td>Role + mandatory SQL rules (15+ rules)</td><td>Static template</td><td>Prompt engineering</td></tr>
<tr><td>User identity placeholders</td><td><code>current_user</code></td><td>Context</td></tr>
<tr><td>Allowed tables list</td><td><code>hybrid_search</code> + policy</td><td>Context (RAG)</td></tr>
<tr><td>Entity documentation</td><td><code>entity_metadata_desc</code></td><td>Context (RAG)</td></tr>
<tr><td>Table/column metadata</td><td><code>metadata</code> string</td><td>Context (RAG)</td></tr>
<tr><td>Role constraints block</td><td><code>SecurityPolicy</code></td><td>Context (governance)</td></tr>
<tr><td>Tool workflow (mandatory sequence)</td><td>Static</td><td>Prompt + tool design</td></tr>
<tr><td>Structured response schema</td><td><code>structured_response_format</code></td><td>Output contract</td></tr>
</table>
<p>Agent tools: <code>sql_db_list_tables</code>, <code>sql_db_schema</code>, <code>sql_db_query_checker</code>, <code>sql_db_query</code> — the prompt <em>forces</em> tool use; markdown SQL alone is not executed.</p>
</div>

<div class="section">
<h2>What Is NOT an LLM (But Is Context Engineering)</h2>
<table>
<tr><th>Component</th><th>Role</th></tr>
<tr><td><code>hybrid_search()</code></td><td>PGVector similarity + entity scoring heuristics → context strings</td></tr>
<tr><td><code>get_user_permissions()</code></td><td>Compiles ACL from roles + query entities</td></tr>
<tr><td><code>evaluate_nl_governed_access()</code></td><td>Blocks NL queries before agent if policy violated</td></tr>
<tr><td><code>validate_and_rewrite_sql()</code></td><td>Deterministic SQL firewall — PASS / REWRITE / BLOCK</td></tr>
<tr><td><code>usage_tracker</code></td><td>Token/cost observability per request</td></tr>
</table>
<div class="quote-block">The best context engineering decision in your app: <strong>never let the LLM be the security boundary.</strong></div>
</div>

<div class="section">
<h2>Legacy / Caution Items (Be Honest in Q&A)</h2>
<ul>
<li><code>system_prompt_with_permissions()</code> in <code>llm/utils.py</code> — hardcoded batch example; production uses deterministic validator instead ✅</li>
<li><code>SecureSQLQueryTool</code> — LLM YES/NO permission check with <strong>fail-open</strong> on error; main path uses code validator ✅</li>
<li>Fallback SQL prompts in <code>_fallback_generate_sql</code> — recovery path if agent produces no tool call</li>
</ul>
</div>

<div class="takeaway"><h3>Key Takeaway</h3>
<p>You have <strong>four production LLM calls</strong> on the hot path, each with a distinct prompt contract. Presentation gold: show the inventory table and ask "which of these should be deterministic?" (Answer: security always.)</p></div>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 28 — Nine Context Layers Applied
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_26_30["28"] = presentation_thread(28, "NL2SQL Deep Dive — Context Layers",
    "The nine-layer context stack — mapped layer by layer to what CampusCom NL2SQL ships today and what best practice looks like in 2026.") + journey_map_nl2sql_capstone(28) + obj([
    "Define the nine context layers for LLM applications",
    "Map each layer to your NL2SQL codebase",
    "Rate current maturity: ✅ strong, ⚠️ partial, ❌ missing",
    "Explain why layers beat 'one big prompt'",
    "Use the layer diagram as a senior-architect slide"
]) + """
<div class="section">
<h2>The Nine Context Layers (2026 Model)</h2>
<div class="diagram-container"><div class="mermaid">
flowchart TB
    L1[Layer 1: System identity & rules]
    L2[Layer 2: Task / user message]
    L3[Layer 3: Retrieved knowledge — RAG]
    L4[Layer 4: Permissions & policy]
    L5[Layer 5: Session & conversation state]
    L6[Layer 6: Tool definitions & results]
    L7[Layer 7: Output schema / format]
    L8[Layer 8: Post-generation validators]
    L9[Layer 9: Observability & evals]
    L1 --> L2 --> L3 --> L4 --> L5 --> L6 --> L7 --> L8 --> L9
</div></div>
<p>Prompt engineering mostly affects <strong>Layers 1–2</strong>. Context engineering owns <strong>Layers 3–9</strong>. Production quality requires all nine.</p>
</div>

<div class="section">
<h2>Layer Map — Your NL2SQL App</h2>
<table>
<tr><th>Layer</th><th>What it is</th><th>Your implementation</th><th>Status</th></tr>
<tr><td><strong>1 — System rules</strong></td><td>Role, constraints, tool workflow</td><td><code>construct_system_prefix()</code>, intent system prompt</td><td>✅ Strong</td></tr>
<tr><td><strong>2 — Task message</strong></td><td>User NL question</td><td><code>HumanMessage(content=question)</code></td><td>✅ Strong</td></tr>
<tr><td><strong>3 — Retrieved knowledge</strong></td><td>Schema, entities, synonyms</td><td><code>hybrid_search()</code> → metadata strings in prefix</td><td>✅ Strong</td></tr>
<tr><td><strong>4 — Permissions</strong></td><td>ACL, governed values, identity</td><td><code>SecurityPolicy</code> + pre-agent NL block + SQL validator</td><td>✅ Strong</td></tr>
<tr><td><strong>5 — Session state</strong></td><td>Multi-turn context</td><td><code>disambiguation</code>, <code>original_prompt</code> recombination</td><td>⚠️ Partial</td></tr>
<tr><td><strong>6 — Tools</strong></td><td>Schema lookup, query, checker</td><td>LangChain SQL toolkit in ReAct loop</td><td>✅ Strong</td></tr>
<tr><td><strong>7 — Output schema</strong></td><td>Structured response contract</td><td><code>structured_response_format</code> + stream XML tags</td><td>✅ Strong</td></tr>
<tr><td><strong>8 — Validators</strong></td><td>Code-enforced safety</td><td><code>validate_and_rewrite_sql()</code></td><td>✅ Strong</td></tr>
<tr><td><strong>9 — Observability</strong></td><td>Usage, tracing, evals</td><td><code>usage_tracker</code>; evals not in CI yet</td><td>⚠️ Partial</td></tr>
</table>
</div>

<div class="section">
<h2>Layer 3 Deep Dive — hybrid_search as RAG</h2>
<p>Not every retrieval system calls an LLM. Yours uses <strong>embeddings + heuristics</strong>:</p>
<ol>
<li>PGVector <code>similarity_search</code> on table metadata chunks</li>
<li>Top 5 tables → related table expansion</li>
<li>Entity scoring by table overlap (e.g. student_entity heuristics)</li>
<li>Outputs: <code>entities</code>, <code>tables</code>, <code>metadata</code>, <code>entity_metadata_desc</code></li>
</ol>
<p><code>message.py</code> precomputes hybrid search once and passes results to <code>run_db_agent</code> — avoids duplicate retrieval. <strong>Good context engineering.</strong></p>
<div class="warning-box"><h4>Context debt signal</h4>
<p>Special-case logic for <code>std_*</code> tables and <code>student_entity</code> in retrieval means behavior depends on tribal knowledge in code — document in metadata instead (see Ch 24, Ch 29).</p></div>
</div>

<div class="section">
<h2>Layer 5 Gap — Conversation History</h2>
<p>Today the SQL agent receives a <strong>single-turn</strong> question. Disambiguation handles one multi-turn pattern; general follow-ups ("now filter by department") do not automatically include prior SQL or answers.</p>
<div class="compare-grid">
<div class="compare-col bad">
<h4>❌ Dump full chat into prompt</h4>
<ul>
<li>Token bloat, lost-in-the-middle</li>
<li>Old wrong SQL pollutes context</li>
</ul>
</div>
<div class="compare-col good">
<h4>✅ Structured session context</h4>
<ul>
<li>Last validated SQL + last entities used</li>
<li>Summary of disambiguation choices</li>
<li>Explicit "this is a follow-up" flag from client</li>
</ul>
</div>
</div>
</div>

<div class="section">
<h2>Why Layers Beat One Big Prompt</h2>
""" + tabs("layers", "❌ Monolith prompt", """<p>Stuff schema + ACL + examples + user question + history into one 50k-token message.</p>
<ul>
<li>Model ignores middle sections</li>
<li>Cannot update retrieval without redeploying prompt</li>
<li>Security mixed with generation — audit nightmare</li>
</ul>""",
"✅ Your layered approach", """<ul>
<li>Retrieval updates independently (re-embed metadata)</li>
<li>Policy updates independently (roles DB)</li>
<li>Validator unchanged when prompt wording shifts</li>
<li>Intent uses small context + few-shots — fast/cheap</li>
</ul>""") + """
</div>

<div class="presentation-tip"><strong>🎤 Senior slide:</strong> Draw the 9 layers. Color Layers 3–4–8 green (your strengths). Color Layer 5 amber. Say: "We built a production system; here's the roadmap to best-in-class."</div>
<div class="takeaway"><h3>Key Takeaway</h3>
<p>CampusCom NL2SQL scores <strong>7/9 layers strong</strong>. The presentation story is not "we need prompts" — it's "we engineered context; here's what's next."</p></div>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 29 — Improvements Roadmap
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_26_30["29"] = presentation_thread(29, "NL2SQL Deep Dive — Improvements",
    "Honest gap analysis and prioritized improvements — what to fix before the next release and what to say when seniors ask hard questions.") + journey_map_nl2sql_capstone(29) + obj([
    "Prioritize NL2SQL improvements by impact and effort",
    "Separate quick wins from architectural investments",
    "Connect each gap to a chapter in this guide",
    "Prepare answers for senior developer Q&A",
    "Turn weaknesses into a credible engineering roadmap"
]) + """
<div class="section">
<h2>Current State Summary</h2>
<div class="overview-cards">
<div class="card"><h3>✅ Strengths</h3>
<ul>
<li>Task-specific model routing</li>
<li>Hybrid search before generation</li>
<li>Deterministic SQL validator (not LLM security)</li>
<li>Pre-agent permission + governed NL checks</li>
<li>Structured outputs (intent, disambiguation, response JSON)</li>
<li>Streaming UX with pipeline visibility</li>
<li>Usage tracking per request</li>
</ul></div>
<div class="card"><h3>⚠️ Gaps</h3>
<ul>
<li>Limited multi-turn context for SQL agent</li>
<li>No eval CI gate on prompt/RAG changes</li>
<li>Retrieval heuristics vs pure semantic ranking</li>
<li>Intent router lacks conversation context</li>
<li>Legacy LLM permission tool (fail-open) unused in main path</li>
</ul></div>
</div>
</div>

<div class="section">
<h2>Prioritized Roadmap</h2>
<table>
<tr><th>Priority</th><th>Improvement</th><th>Impact</th><th>Effort</th><th>Guide ref</th></tr>
<tr><td>P0</td><td>Golden eval suite in CI (intent, retrieval, SQL safety)</td><td>🔴 High</td><td>Medium</td><td>Ch 16</td></tr>
<tr><td>P0</td><td>Retrieval eval: correct tables in top-K for 100 benchmark questions</td><td>🔴 High</td><td>Medium</td><td>Ch 7, 16</td></tr>
<tr><td>P1</td><td>Structured follow-up context (last SQL + entities, not full chat)</td><td>🟠 High</td><td>Medium</td><td>Ch 6, 28 L5</td></tr>
<tr><td>P1</td><td>Intent router: optional previous turn + last datasource</td><td>🟠 Medium</td><td>Low</td><td>Ch 4, 27</td></tr>
<tr><td>P2</td><td>Replace retrieval heuristics with metadata-driven entity linking</td><td>🟠 Medium</td><td>High</td><td>Ch 24</td></tr>
<tr><td>P2</td><td>Prompt version registry + A/B metrics in usage_tracker</td><td>🟡 Medium</td><td>Low</td><td>Ch 16, 18</td></tr>
<tr><td>P3</td><td>Remove or harden legacy SecureSQLQueryTool fail-open path</td><td>🟡 Low</td><td>Low</td><td>Ch 17</td></tr>
<tr><td>P3</td><td>Re-ranker on hybrid_search top-20 → top-5</td><td>🟡 Medium</td><td>Medium</td><td>Ch 7</td></tr>
</table>
</div>

<div class="section">
<h2>Improvement #1 — Eval CI (P0)</h2>
<p><strong>Problem:</strong> Prompt or embedding changes can silently break production SQL quality.</p>
<p><strong>Fix:</strong> Minimum eval categories:</p>
<ul>
<li><strong>Intent:</strong> 50 labeled sql/docs/other questions (from your few-shots + production logs)</li>
<li><strong>Retrieval:</strong> expected tables for each benchmark question</li>
<li><strong>SQL safety:</strong> no DML, tables ⊆ allowed, validator never PASS on shielded columns</li>
<li><strong>Regression:</strong> golden NL→SQL pairs after validator</li>
</ul>
""" + code("yaml", """# Example CI step (conceptual)
- name: NL2SQL evals
  run: pytest tests/evals/ --min-pass-rate 0.92
  # Block deploy if intent accuracy or retrieval recall drops""") + """
</div>

<div class="section">
<h2>Improvement #2 — Follow-Up Context (P1)</h2>
<p><strong>Problem:</strong> User asks "show unpaid invoices by student" then "same for faculty" — agent lacks structured prior context.</p>
<p><strong>Fix pattern:</strong></p>
""" + code("python", """# Orchestrator-owned session bundle (not raw chat dump)
session_context = {
    "last_sql": previous_message.sql_query,
    "last_entities": ["invoice", "student"],
    "disambiguation_resolved": conversation.disambiguation,
}
# Inject summary into system prefix or prefixed HumanMessage""") + """
</div>

<div class="section">
<h2>Improvement #3 — Context Debt in Retrieval (P2)</h2>
<p>Move special cases from Python heuristics into indexed metadata:</p>
<table>
<tr><th>Today (code)</th><th>Tomorrow (metadata)</th></tr>
<tr><td><code>table.startswith("std_")</code> boosts student entity</td><td>Entity tag on every table chunk in vector index</td></tr>
<tr><td>Manual entity score thresholds</td><td>Graph edges: entity → tables in embedding metadata</td></tr>
<tr><td>Synonyms only in entity row</td><td>Glossary chunks: "active student" → enrollment rule</td></tr>
</table>
</div>

<div class="section">
<h2>Senior Q&A — Prepared Answers</h2>
<table>
<tr><th>Question</th><th>Answer</th></tr>
<tr><td>"Why not one GPT call?"</td><td>Security, retrieval, and cost require layers — one call can't enforce ACL in code.</td></tr>
<tr><td>"Is the LLM our security boundary?"</td><td>No. <code>validate_and_rewrite_sql</code> is. LLM proposes only.</td></tr>
<tr><td>"ChatGPT with schema paste?"</td><td>No audit, no ACL, no evals — fine for dev, not for campus data.</td></tr>
<tr><td>"How do you measure quality?"</td><td>usage_tracker today; eval CI is P0 on roadmap (Ch 16).</td></tr>
<tr><td>"Biggest risk?"</td><td>Believable wrong SQL that passes casual review — mitigated by validator + human reasoning UI.</td></tr>
</table>
</div>

<div class="takeaway"><h3>Key Takeaway</h3>
<p>Showing a roadmap makes you credible. Winners don't claim perfection — they show <strong>layered engineering with a measured next step.</strong></p></div>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 30 — Presentation Master Script + IDE Setup
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_26_30["30"] = presentation_thread(30, "Deliver — Master Presentation Script",
    "45-minute winning talk: timing, demos, IDE setup for daily work, and the two-scenario framework juniors and seniors both need.") + journey_map_nl2sql_capstone(30) + obj([
    "Deliver a 45-minute presentation with clear acts and timing",
    "Run two live demos: daily AI workflow + NL2SQL pipeline",
    "Configure Cursor (and alternatives) for better daily results",
    "Apply the two-scenario framework: chat tools vs LLM apps",
    "Handle Q&A from juniors and senior architects confidently"
]) + """
<div class="section">
<h2>Two Scenarios Framework (Open With This)</h2>
<div class="info-box" style="border-color:#dc2626;background:#fef2f2">
<h4>⭐ Failure-focused presentation?</h4>
<p>Use <a href="chapter31.html"><strong>Chapter 31</strong></a> as your primary script — Why/When/How failures, real NL2SQL examples, daily-life success checklist. This chapter (30) covers timing and IDE setup.</p>
</div>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    subgraph Scenario A["Scenario A — Daily work"]
        A1[ChatGPT / Claude / Cursor chat]
        A2[You are the orchestrator]
        A3[Prompt + paste context + review output]
    end
    subgraph Scenario B["Scenario B — LLM applications"]
        B1[Your NL2SQL product]
        B2[Code is the orchestrator]
        B3[9 context layers + validators + evals]
    end
    A1 --> LESSON[Same principles — different responsibility]
    B1 --> LESSON
</div></div>
<table>
<tr><th></th><th>Scenario A: Daily development</th><th>Scenario B: NL2SQL / production app</th></tr>
<tr><td>Who builds context?</td><td>You, manually</td><td>Pipeline code</td></tr>
<tr><td>Who validates?</td><td>You, before merge</td><td>Code + optional human</td></tr>
<tr><td>Prompt role</td><td>Primary lever</td><td>One layer among nine</td></tr>
<tr><td>Failure cost</td><td>Bad commit, leaked paste</td><td>Wrong data to thousands of users</td></tr>
<tr><td>Best tool</td><td>Cursor with rules</td><td>Custom pipeline + evals</td></tr>
</table>
</div>

<div class="section">
<h2>45-Minute Presentation Script</h2>
<table>
<tr><th>Act</th><th>Min</th><th>Content</th><th>Chapters</th></tr>
<tr><td><strong>1 — Hook</strong></td><td>0–5</td><td>Believable wrong SQL; "AI fails predictably"</td><td><strong>31</strong>, 5</td></tr>
<tr><td><strong>2 — WHY + WHEN</strong></td><td>5–12</td><td>Five root causes; trigger moments table</td><td><strong>31</strong>, 2</td></tr>
<tr><td><strong>3 — HOW + FIX</strong></td><td>12–22</td><td>6 real failures → NL2SQL fixes</td><td><strong>31</strong>, 26–28</td></tr>
<tr><td><strong>4 — Live demos</strong></td><td>22–35</td><td>Naive SQL fail · App pipeline success · Cursor plan-first</td><td>31, 26, 12</td></tr>
<tr><td><strong>5 — Daily success</strong></td><td>35–40</td><td>Best way to use AI in life; checklist</td><td><strong>31</strong>, 12, 13</td></tr>
<tr><td><strong>6 — Close + Q&A</strong></td><td>40–45</td><td>Failure → eval loop; roadmap</td><td>29, 23</td></tr>
</table>
</div>

<div class="section">
<h2>Demo A — Daily Work in Cursor (5 min)</h2>
<ol>
<li><strong>Show bad:</strong> "Fix this bug" with no @file — agent guesses wrong module</li>
<li><strong>Show good:</strong> Plan mode → @file <code>message.py</code> → @codebase "trace LLM calls" → small scoped edit</li>
<li><strong>Say:</strong> "In Scenario A, <em>you</em> are the context engineer."</li>
</ol>
<div class="presentation-tip"><strong>Prep:</strong> Open nl2sql repo in Cursor before the talk. Have <code>.cursor/rules</code> visible if you use them.</div>
</div>

<div class="section">
<h2>Demo B — NL2SQL Pipeline (8 min)</h2>
<table>
<tr><th>Min</th><th>Action</th><th>Say this</th></tr>
<tr><td>0–1</td><td>Ask reporting question in your app UI</td><td>"Watch the loaders — each is a pipeline stage."</td></tr>
<tr><td>1–2</td><td>Point at intent (or logs)</td><td>"Cheap model routes — sql vs docs."</td></tr>
<tr><td>2–4</td><td>If disambiguation triggers, show it</td><td>"Context engineering for ambiguous business terms."</td></tr>
<tr><td>4–6</td><td>Show SQL draft in stream</td><td>"Model proposed — not yet trusted."</td></tr>
<tr><td>6–7</td><td>Show validator rewrite or policy message</td><td>"Code has final say — Layer 8."</td></tr>
<tr><td>7–8</td><td>Show data or block message</td><td>"This is Scenario B — the app orchestrates."</td></tr>
</table>
<p><strong>Backup:</strong> Screenshots from Ch 26 diagram + pre-recorded 30s screen capture.</p>
</div>

<div class="section">
<h2>IDE Setup — Cursor (Recommended)</h2>
<h3>1. Project rules (<code>.cursor/rules</code>)</h3>
""" + code("markdown", """# Example: nl2sql-dev.mdc
---
description: NL2SQL Python conventions
globs: app/**/*.py, llm/**/*.py
---
- FastAPI routers stay thin; LLM logic in llm/
- Never use LLM for security decisions — use validators
- Match existing logging patterns with extra={}
- Task-specific models via get_llm(task=...)""") + """
<h3>2. User rules (Cursor Settings → Rules)</h3>
<ul>
<li>Ask for plan before multi-file changes</li>
<li>Prefer minimal diff; no drive-by refactors</li>
<li>Cite file paths when suggesting edits</li>
</ul>
<h3>3. Context commands — when to use what</h3>
<table>
<tr><th>Command</th><th>Use when</th><th>Avoid when</th></tr>
<tr><td><code>@file</code></td><td>Editing one known file</td><td>Whole feature design</td></tr>
<tr><td><code>@folder</code></td><td>Module-wide refactor</td><td>Unrelated directories</td></tr>
<tr><td><code>@codebase</code></td><td>"Where is X?" discovery</td><td>Simple typo fix</td></tr>
<tr><td><code>@docs</code></td><td>Library API questions</td><td>Internal business rules</td></tr>
<tr><td>Agent mode</td><td>Multi-step with verification</td><td>Production hotfix without review</td></tr>
</table>
</div>

<div class="section">
<h2>IDE Setup — Other Tools</h2>
<table>
<tr><th>Tool</th><th>Setup for better results</th></tr>
<tr><td><strong>ChatGPT</strong></td><td>Custom GPT with pasted architecture doc; never prod credentials; use for learning and drafts</td></tr>
<tr><td><strong>Claude</strong></td><td>Projects with nl2sql README + schema samples; long-context doc review</td></tr>
<tr><td><strong>GitHub Copilot</strong></td><td>Open relevant file first; copilot-instructions.md for repo conventions</td></tr>
<tr><td><strong>VS Code + Continue</strong></td><td>config.yaml context providers: file, codebase; local model for privacy-sensitive snippets</td></tr>
</table>
</div>

<div class="section">
<h2>Daily Work Prompt Template (Scenario A)</h2>
""" + code("", """ROLE: Senior Python reviewer for FastAPI + LangChain codebase.

CONTEXT:
- File: app/routers/message.py (or @attach)
- Task: [one sentence goal]
- Constraints: minimal diff, match existing patterns, no new deps

TASK:
1. Explain current flow in 3 bullets
2. Propose smallest change
3. List what could break

Do not write code until I approve the plan.""") + """
</div>

<div class="section">
<h2>Winning Lines (Memorize These)</h2>
<div class="quote-block">Prompting is how we talk to AI. Context engineering is how we make AI useful.</div>
<div class="quote-block">In chat, you are the pipeline. In production, the code is the pipeline.</div>
<div class="quote-block">Our NL2SQL app does not trust the model with security — it trusts the validator.</div>
<div class="quote-block">Seven layers strong today. Eval CI is how we stay strong tomorrow.</div>
</div>

<div class="section">
<h2>Pre-Presentation Checklist (Final)</h2>
<ul class="checklist">
<li>Read Ch 26–28 (know your pipeline cold)</li>
<li>Read Ch 29 (roadmap for hard questions)</li>
<li>Practice Demo B three times with real app</li>
<li>Prepare Cursor window with message.py + llm/intent.py open</li>
<li>Export Ch 26 mermaid diagram as slide image (backup)</li>
<li>Share prompt-to-context guide link with audience</li>
<li>Time Act 4 — cut Demo A if running long, never cut Demo B</li>
</ul>
</div>

<div class="quick-start" style="margin-top:2rem">
<h2>You Are Ready to Win</h2>
<p>You have theory (Ch 1–25), your real system (Ch 26–29), and the delivery script (Ch 30). Teach juniors the two scenarios. Show seniors the nine layers. Demo the pipeline. Own the roadmap.</p>
<div class="button-group">
<a href="chapter26.html" class="btn btn-primary">Start NL2SQL Deep Dive →</a>
<a href="chapter20.html" class="btn btn-secondary">Original Presentation Guide</a>
</div>
</div>

<div class="takeaway"><h3>Key Takeaway</h3>
<p>The prize goes to the speaker who connects <strong>daily AI habits</strong> to <strong>production architecture</strong> with honesty and a live demo of their own system.</p></div>
"""
