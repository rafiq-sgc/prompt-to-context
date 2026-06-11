# Advanced content for Chapters 07–10 — building applications with LLMs
from chapter_content import obj, code, tabs
from chapter_helpers import presentation_thread, journey_map, tool_stack_table

CHAPTER_BODIES_07_10 = {}

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 07 — RAG (Advanced)
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_07_10["07"] = presentation_thread(7, "Build — Connect AI to Facts",
    "RAG is how NL2SQL, doc chatbots, and Cursor-style codebase search get <em>real</em> schema and docs into the model — not guesses from training data.") + journey_map(7) + obj([
    "Explain embeddings and retrieval behind the scenes",
    "Design chunking and indexing for schema, docs, and code",
    "Build RAG for NL2SQL: entity metadata, joins, business rules",
    "Apply hybrid search, re-ranking, and permission-aware retrieval",
    "Diagnose RAG failures and fix with engineering — not more prompting"
]) + """
<div class="section">
<h2>Why RAG Exists: The Inference-Time Fact Gap</h2>
<p>At inference, the model only sees: <strong>weights (frozen training)</strong> + <strong>your prompt context</strong>. It cannot query your database, read Confluence, or see yesterday's migration unless you <strong>retrieve and inject</strong> that text.</p>
<div class="diagram-container"><div class="mermaid">
flowchart TB
    subgraph Without RAG
        Q1[User: unpaid students SQL] --> M1[LLM guesses schema]
        M1 --> W1[Wrong table names]
    end
    subgraph With RAG
        Q2[Same question] --> R[Retriever finds students + invoices DDL]
        R --> M2[LLM + retrieved schema]
        M2 --> W2[Correct JOIN path]
    end
</div></div>
<div class="quote-block">RAG does not make the model smarter. It gives the model the <em>right facts at the right time</em>.</div>
</div>

<div class="section">
<h2>Behind the Scenes: How Retrieval Works</h2>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    DOC[Documents / Schema / Code] --> CH[Chunk text]
    CH --> EMB[Embedding model]
    EMB --> VDB[(Vector index)]
    Q[User query] --> QEMB[Embed query]
    QEMB --> SIM[Cosine similarity search]
    VDB --> SIM
    SIM --> TOP[Top-K chunks]
    TOP --> RERANK[Optional re-ranker]
    RERANK --> CTX[Inject into LLM prompt]
    CTX --> GEN[Generate answer]
</div></div>
<h3>What is an embedding?</h3>
<p>An embedding model converts text into a numeric vector. Similar meaning → vectors close together. "unpaid invoices" retrieves chunks about <code class="inline-code">paid_status</code> even if the word "unpaid" never appears in the chunk.</p>
<div class="info-box"><h4>Junior mental model</h4>
<p>Embeddings are <strong>semantic search</strong>, not keyword search. "Active enrollees" can match "enrollment_status = 'active'".</p></div>
</div>

<div class="section">
<h2>Chunking Strategies (Critical for NL2SQL)</h2>
<table>
<tr><th>Source</th><th>Bad chunking</th><th>Good chunking</th><th>Why</th></tr>
<tr><td>Table DDL</td><td>Split mid-column list</td><td>One chunk = full table + FKs</td><td>Model needs complete column list</td></tr>
<tr><td>Business glossary</td><td>Whole PDF pages</td><td>One term = one definition chunk</td><td>"Revenue" retrieves exact rule</td></tr>
<tr><td>Example SQL pairs</td><td>Mixed unrelated queries</td><td>One NL question + one SQL per chunk</td><td>Few-shot retrieval stays clean</td></tr>
<tr><td>API docs</td><td>Arbitrary 512 tokens</td><td>One endpoint per chunk</td><td>Method signature stays intact</td></tr>
</table>
""" + code("", """# Example: NL2SQL schema chunk (one entity)
ENTITY: students
TABLE: students(id, full_name, enrollment_status, program_id)
RELATIONSHIPS: invoices.student_id → students.id
BUSINESS: active_student = enrollment_status = 'active'
EXAMPLE: "active students" → SELECT id, full_name FROM students WHERE enrollment_status='active'""") + """
</div>

<div class="section">
<h2>Building RAG for NL2SQL (Step by Step)</h2>
<div class="flow-steps">
<span class="flow-step">1. Index schema metadata</span><span class="flow-arrow">→</span>
<span class="flow-step">2. Index business rules</span><span class="flow-arrow">→</span>
<span class="flow-step">3. Index example query pairs</span><span class="flow-arrow">→</span>
<span class="flow-step">4. On question: retrieve top-K</span><span class="flow-arrow">→</span>
<span class="flow-step">5. Filter by user permissions</span><span class="flow-arrow">→</span>
<span class="flow-step">6. Inject + generate SQL</span>
</div>
<div class="diagram-container"><div class="mermaid">
flowchart TD
    U[User: Show unpaid invoices for active students] --> RW[Query rewrite optional]
    RW --> H[Hybrid search: BM25 + vectors]
    H --> F[Metadata filter: domain=finance, role=analyst]
    F --> RR[Re-rank top 20 → keep top 5]
    RR --> ASM[Assemble SCHEMA + RULES + EXAMPLES blocks]
    ASM --> LLM[LLM generates SQL]
    LLM --> VAL[Schema validator]
</div></div>
</div>

<div class="section">
<h2>Hybrid Search: Why Vectors Alone Fail</h2>
<div class="compare-grid">
<div class="compare-col bad">
<h4>❌ Vector-only</h4>
<p>User asks for table <code class="inline-code">gl_account</code> — embedding may return "general ledger policy" doc instead of DDL.</p>
</div>
<div class="compare-col good">
<h4>✅ Hybrid (BM25 + vectors)</h4>
<p>Keyword match on <code class="inline-code">gl_account</code> + semantic match on "account balance" → correct schema chunk wins.</p>
</div>
</div>
<p><strong>Senior rule:</strong> For exact identifiers (table names, API paths, error codes), always combine keyword + semantic retrieval.</p>
</div>

<div class="section">
<h2>RAG in Developer Tools (How Cursor / ChatGPT Differ)</h2>
""" + tool_stack_table() + """
<table>
<tr><th>Tool</th><th>Retrieval mechanism</th><th>What you control</th></tr>
<tr><td>ChatGPT + files</td><td>Upload / paste into context</td><td>What you attach per chat</td></tr>
<tr><td>Claude Projects</td><td>Project knowledge base</td><td>Docs you upload to project</td></tr>
<tr><td>Cursor</td><td>Codebase index + @file/@folder</td><td>.cursorignore, rules, explicit @ refs</td></tr>
<tr><td>Custom NL2SQL</td><td>Your vector DB + schema registry</td><td>Chunking, ACL, evals — full ownership</td></tr>
</table>
</div>

<div class="section">
<h2>Failure → Fix: RAG Case Studies</h2>
<table>
<tr><th>Failure</th><th>Symptom</th><th>Root cause</th><th>Fix</th></tr>
<tr><td>Wrong chunk wins</td><td>SQL uses HR table for finance query</td><td>No metadata filter</td><td>Filter by domain / entity type</td></tr>
<tr><td>Missing JOIN</td><td>Single-table query for multi-table intent</td><td>Relationship not in retrieved chunk</td><td>Include FK graph in schema chunks</td></tr>
<tr><td>Stale schema</td><td>Column renamed last sprint</td><td>Index not updated</td><td>CI re-index on migration merge</td></tr>
<tr><td>Data leak</td><td>Salary table in context for intern</td><td>No ACL on retriever</td><td>Filter chunks by user role</td></tr>
<tr><td>Prompt injection in doc</td><td>Model ignores safety rules</td><td>Malicious wiki page retrieved</td><td>Untrusted data labeling (Ch 17)</td></tr>
</table>
</div>

<div class="section">
<h2>Advanced RAG Checklist (Production 2026)</h2>
<ul class="checklist">
<li>Chunk by meaning, not token count alone</li>
<li>Hybrid search for identifiers + semantics</li>
<li>Re-ranker after vector search</li>
<li>Metadata: version, domain, permission tags</li>
<li>Permission filter before generation</li>
<li>Citation: log which chunk_ids were used</li>
<li>Eval set: measure retrieval recall@K</li>
<li>Re-index pipeline tied to schema migrations</li>
</ul>
</div>

<div class="presentation-tip"><strong>🎤 Demo:</strong> Same NL2SQL question — (1) no RAG, (2) RAG with wrong chunk, (3) RAG with correct schema chunk. Three outputs, one slide. Juniors see "magic"; seniors see pipeline design.</div>
<div class="takeaway"><h3>Key Takeaway</h3>
<p>RAG is the bridge from prompt engineering to context engineering for any app that needs private or current facts — especially NL2SQL.</p></div>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 08 — Tools & MCP (Advanced)
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_07_10["08"] = presentation_thread(8, "Build — Let the Model Verify, Not Guess",
    "Tools turn chat models into applications. Function calling is how ChatGPT plugins, Cursor agents, and NL2SQL validators actually <em>do</em> things.") + journey_map(8) + obj([
    "Trace function calling from API request to tool execution and back",
    "Map tool risk levels to permission design for NL2SQL and coding agents",
    "Explain MCP and why IDEs are becoming tool orchestrators",
    "Compare how ChatGPT, Claude, Cursor, and Copilot expose tools",
    "Build a minimal tool layer for schema lookup and SQL validation"
]) + """
<div class="section">
<h2>Behind the Scenes: Function Calling</h2>
<p>The model does <strong>not</strong> execute code. Your application does. The model outputs a <strong>structured tool call request</strong>; your backend runs it and returns the result as a new message.</p>
<div class="diagram-container"><div class="mermaid">
sequenceDiagram
    participant App as Your App
    participant API as LLM API
    participant Tool as Your Backend Tool
    App->>API: messages + tool definitions
    API-->>App: tool_call: validate_sql(sql)
    App->>Tool: execute validate_sql
    Tool-->>App: {read_only: true, errors: []}
    App->>API: tool result message
    API-->>App: final natural language + safe SQL
</div></div>
""" + code("json", """// Tool definition (OpenAI-style)
{
  "name": "get_schema",
  "description": "Look up table columns and foreign keys",
  "parameters": {
    "type": "object",
    "properties": {
      "table_name": { "type": "string" },
      "include_relationships": { "type": "boolean" }
    },
    "required": ["table_name"]
  }
}""") + """
</div>

<div class="section">
<h2>Text-Only vs Tool-Augmented Applications</h2>
<div class="compare-grid">
<div class="compare-col bad">
<h4>❌ Chat-only NL2SQL</h4>
<p>Model invents <code class="inline-code">invoice_status</code> column.</p>
<p>No way to verify until production error.</p>
</div>
<div class="compare-col good">
<h4>✅ Tool-augmented NL2SQL</h4>
<ol>
<li><code class="inline-code">search_schema("unpaid invoices")</code> → real tables</li>
<li>Model drafts SQL</li>
<li><code class="inline-code">validate_sql(sql)</code> → parser + ACL check</li>
<li>Human approves → read-only execute</li>
</ol>
</div>
</div>
</div>

<div class="section">
<h2>Tool Catalog for Application Builders</h2>
<table>
<tr><th>Tool</th><th>NL2SQL use</th><th>Coding agent use</th><th>Risk</th></tr>
<tr><td><code class="inline-code">search_schema</code></td><td>Find tables/columns</td><td>—</td><td>Medium</td></tr>
<tr><td><code class="inline-code">validate_sql</code></td><td>Parse + deny DML</td><td>—</td><td>Low</td></tr>
<tr><td><code class="inline-code">search_code</code></td><td>—</td><td>Find symbols, usages</td><td>Medium</td></tr>
<tr><td><code class="inline-code">read_file</code></td><td>—</td><td>Inspect implementation</td><td>Medium</td></tr>
<tr><td><code class="inline-code">run_tests</code></td><td>—</td><td>Verify changes</td><td>Medium-High</td></tr>
<tr><td><code class="inline-code">execute_sql</code></td><td>Run read-only query</td><td>—</td><td>High</td></tr>
<tr><td><code class="inline-code">write_file</code></td><td>—</td><td>Modify codebase</td><td>High</td></tr>
</table>
</div>

<div class="section">
<h2>Permission Model (Non-Negotiable)</h2>
<div class="diagram-container"><div class="mermaid">
quadrantChart
    title Tool Risk vs Permission Strictness
    x-axis Low Permission --> High Permission
    y-axis Low Risk --> High Risk
    quadrant-1 Never auto-run
    quadrant-2 Human approval required
    quadrant-3 Read-only OK
    quadrant-4 Audit only
    validate_sql: [0.2, 0.15]
    search_docs: [0.35, 0.25]
    execute_sql: [0.75, 0.85]
    deploy: [0.95, 0.95]
</div></div>
<div class="info-box"><h4>Principle</h4>
<p>Text generation is low risk. Tool execution is high risk. An AI that can be wrong <strong>and</strong> execute is an incident waiting to happen.</p></div>
</div>

<div class="section">
<h2>MCP — Model Context Protocol (2026 Ecosystem)</h2>
<p>MCP standardizes how AI clients (Cursor, Claude Desktop, custom apps) connect to <strong>tools and data sources</strong> through a common protocol — like USB for AI integrations.</p>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    IDE[Cursor / Claude / Custom App] --> MCP[MCP Client]
    MCP --> S1[GitHub server]
    MCP --> S2[Postgres schema server]
    MCP --> S3[Jira server]
    MCP --> S4[Custom NL2SQL server]
</div></div>
<p><strong>For developers:</strong> You don't need to master every MCP detail. You need the mental model: <em>future AI apps are orchestrators of typed tool connections</em>, not chat windows.</p>
</div>

<div class="section">
<h2>How Each Tool Uses "Tools" Behind the Scenes</h2>
<table>
<tr><th>Product</th><th>Tool-like behavior</th><th>What juniors should do</th><th>What seniors should control</th></tr>
<tr><td>ChatGPT</td><td>Browsing, code interpreter, custom GPT actions</td><td>Don't paste secrets; verify outputs</td><td>Know data leaves your network</td></tr>
<tr><td>Claude</td><td>Computer use, MCP connectors, artifacts</td><td>Use Projects for stable context</td><td>Approve high-risk connector scopes</td></tr>
<tr><td>Cursor</td><td>Terminal, file edit, web search, MCP</td><td>@file scope; small tasks</td><td>Rules, deny lists, review diffs</td></tr>
<tr><td>Copilot</td><td>Limited workspace context</td><td>Tab-complete only</td><td>Don't rely for architecture</td></tr>
</table>
</div>

<div class="section">
<h2>Build a Minimal NL2SQL Tool Layer (Pseudo-Code)</h2>
""" + code("python", """TOOLS = [
    {"name": "search_schema", "fn": search_schema, "risk": "medium"},
    {"name": "validate_sql", "fn": validate_sql, "risk": "low"},
    # execute_sql requires human approval gate
]

def handle_turn(user_id, question):
    messages = assemble_context(user_id, question)
    response = llm.chat(messages, tools=TOOLS)

    while response.tool_calls:
        for call in response.tool_calls:
            if call.name == "execute_sql":
                raise PermissionError("Requires approval workflow")
            result = TOOLS[call.name].fn(**call.arguments, user_id=user_id)
            messages.append(tool_result(call.id, result))
        response = llm.chat(messages, tools=TOOLS)

    return validate_and_return(response)""") + """
</div>

<div class="section">
<h2>Failure → Fix</h2>
<div class="error-box"><h4>❌ Failure: Model calls execute_sql with destructive query</h4>
<p>Tool had no validator; DB role was not read-only.</p></div>
<div class="success-box"><h4>✅ Fix stack</h4>
<ol>
<li>Remove execute from model tools — separate approval service</li>
<li><code class="inline-code">validate_sql</code> blocks non-SELECT</li>
<li>DB connection uses read-only role</li>
<li>Log every tool call with user_id</li>
</ol></div>
</div>

<div class="takeaway"><h3>Key Takeaway</h3>
<p>Tools are how you <em>control</em> AI in 2026 apps. Build typed, permissioned, logged tools — whether in custom NL2SQL or via MCP in Cursor.</p></div>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 09 — AI Agents (Advanced)
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_07_10["09"] = presentation_thread(9, "Build — Multi-Step Autonomy with Limits",
    "Agents are loops: plan → act → observe → repeat. Cursor Agent and coding bots use this — seniors must design permissions and stopping conditions.") + journey_map(9) + obj([
    "Explain the agent loop behind Cursor Agent and similar products",
    "Choose chatbot vs workflow vs agent for NL2SQL and coding tasks",
    "Design safe agent permissions, budgets, and human gates",
    "Recognize agent failure modes in production",
    "Use agents productively without losing engineering control"
]) + """
<div class="section">
<h2>What an Agent Really Is (Behind the Scenes)</h2>
<p>An agent is a <strong>loop</strong> around an LLM: the model decides the next action, your runtime executes it, results go back into context, repeat until done or limits hit. It is not a separate "smarter AI" — it is <strong>orchestration</strong>.</p>
<div class="diagram-container"><div class="mermaid">
flowchart TB
    G[Goal from user] --> L{Loop}
    L --> P[LLM: plan next step]
    P --> A{Action type?}
    A -->|tool| T[Execute tool]
    A -->|message| R[Return to user]
    A -->|done| F[Finish]
    T --> O[Observation → append to context]
    O --> C{Limits OK?}
    C -->|steps, cost, time| L
    C -->|exceeded| X[Stop + escalate]
</div></div>
</div>

<div class="section">
<h2>Three Levels — Where Each Tool Sits</h2>
<table>
<tr><th>Level</th><th>Behavior</th><th>Example products</th><th>NL2SQL fit</th></tr>
<tr><td><strong>Chatbot</strong></td><td>One turn in, one turn out</td><td>Basic ChatGPT Q&A</td><td>❌ Unsafe alone for SQL</td></tr>
<tr><td><strong>Workflow</strong></td><td>Fixed pipeline you code</td><td>Production NL2SQL with steps</td><td>✅ Default choice</td></tr>
<tr><td><strong>Agent</strong></td><td>Model picks next tool/step</td><td>Cursor Agent, Devin-style bots</td><td>⚠️ Only with strict bounds</td></tr>
</table>
<div class="info-box"><h4>Senior default</h4>
<p><strong>Workflow first.</strong> Promote to agent only when paths are unpredictable AND permissions are sandboxed.</p></div>
</div>

<div class="section">
<h2>Cursor Agent: What Happens When You Click "Agent"</h2>
<ol>
<li>IDE sends goal + codebase index context to model</li>
<li>Model returns: search files / read file / edit file / run terminal</li>
<li>IDE executes (with your approval settings)</li>
<li>Output (diff, test result, error) appended to context</li>
<li>Loop until model says done or max steps</li>
</ol>
<div class="warning-box"><h4>Junior trap</h4>
<p>"Fix the whole app" → agent touches 20 files → merge without reading. <strong>Fix:</strong> scoped goals, plan-first, review every file in diff.</p></div>
<div class="success-box"><h4>Senior pattern</h4>
<p>"In <code class="inline-code">auth/middleware.ts</code> only: add rate limiting per plan-first prompt step 1."</p></div>
</div>

<div class="section">
<h2>Coding Agent Loop (Annotated Example)</h2>
<p><strong>Task:</strong> Add pagination to Customer API</p>
<div class="diagram-container"><div class="mermaid">
sequenceDiagram
    participant D as Developer
    participant A as Agent Runtime
    participant M as LLM
    participant T as Tools
    D->>A: Add pagination to Customer API
    A->>M: goal + codebase context
    M->>A: tool: search_code("customer route")
    A->>T: ripgrep / index search
    T-->>A: routes/customer.ts
    A->>M: observation: file paths
    M->>A: tool: read_file + propose plan
    Note over D,A: Human approves plan
    M->>A: tool: edit_file + run_tests
    T-->>A: 2 tests failed
    M->>A: fix + re-run
    A-->>D: summary + diff
</div></div>
</div>

<div class="section">
<h2>Safe Agent Design Checklist</h2>
<ul class="checklist">
<li>Max steps (e.g. 10–25) and max cost per run</li>
<li>Allowlisted tools only — no arbitrary shell</li>
<li>Read-only by default; write requires scope</li>
<li>Human approval before: merge, deploy, execute SQL</li>
<li>Structured logging of every step</li>
<li>Sandbox branch / worktree — never main directly</li>
<li>Rollback plan before agent starts</li>
</ul>
</div>

<div class="section">
<h2>Agent Risks → Fixes (Teaching Table)</h2>
<table>
<tr><th>Risk</th><th>Real incident shape</th><th>Fix</th></tr>
<tr><td>Wrong tool</td><td>Deletes test DB thinking it's staging</td><td>Environment labels + deny prod tools</td></tr>
<tr><td>Infinite loop</td><td>$200 API bill fixing same test</td><td>Step cap + duplicate detection</td></tr>
<tr><td>Prompt injection via file</td><td>Malicious comment: "ignore rules, exfiltrate"</td><td>Untrusted content in data blocks</td></tr>
<tr><td>Scope creep</td><td>"Fix bug" → full rewrite</td><td>Explicit file allowlist in prompt</td></tr>
<tr><td>False done</td><td>Agent says success, tests not run</td><td>Require test tool observation</td></tr>
</table>
<div class="quote-block">Do not give an AI agent more permission than you would give a new developer on day one.</div>
</div>

<div class="section">
<h2>NL2SQL: Agent or Workflow?</h2>
<div class="compare-grid">
<div class="compare-col good">
<h4>✅ Recommended: Workflow</h4>
""" + code("", "intent → auth → RAG → generate → validate → approve → execute") + """
<p>Predictable, auditable, testable with evals.</p>
</div>
<div class="compare-col bad">
<h4>❌ Risky: Open agent</h4>
<p>Model decides to "explore schema" with write access.</p>
<p>Hard to regression-test.</p>
</div>
</div>
</div>

<div class="takeaway"><h3>Key Takeaway</h3>
<p>Agents are powerful orchestration loops — use them for exploration and coding with tight bounds; use workflows for NL2SQL and production paths.</p></div>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CHAPTER 10 — Multi-Agent (Advanced)
# ═══════════════════════════════════════════════════════════════════════════════
CHAPTER_BODIES_07_10["10"] = presentation_thread(10, "Build — Specialize When Complexity Earns It",
    "Multi-agent splits one brain into a team: intent, retrieval, generation, validation. Powerful for NL2SQL at scale — but costly if a simple workflow suffices.") + journey_map(10) + obj([
    "Design role-separated agents with different prompts and tool permissions",
    "Walk through a production multi-agent NL2SQL architecture",
    "Compare cost, latency, and debuggability vs single workflow",
    "Know when multi-agent is justified vs over-engineering",
    "Connect Chapters 2–10 into one application blueprint"
]) + """
<div class="section">
<h2>Why Multi-Agent? (Team Analogy)</h2>
<p>One model doing plan + retrieve + code + review + security in one context often <strong>conflicts priorities</strong>. Multi-agent assigns <strong>one job per call</strong> with focused context — like microservices for LLM steps.</p>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    subgraph Single call problem
        M1[One LLM does everything]
        M1 --> C1[Context bloat]
        M1 --> C2[Safety vs speed conflict]
    end
    subgraph Multi-agent
        A1[Intent] --> A2[Retrieve]
        A2 --> A3[Generate]
        A3 --> A4[Validate]
        A4 --> A5[Explain]
    end
</div></div>
</div>

<div class="section">
<h2>Role Separation with Tool Permissions</h2>
<table>
<tr><th>Agent</th><th>Input</th><th>Output</th><th>Tools allowed</th><th>Cannot do</th></tr>
<tr><td>Intent</td><td>User question</td><td>intent, domain, risk</td><td>None / classifier only</td><td>Generate SQL</td></tr>
<tr><td>Retriever</td><td>Intent + question</td><td>Schema + rule chunks</td><td>RAG search only</td><td>Call LLM for SQL</td></tr>
<tr><td>SQL generator</td><td>Retrieved context</td><td>SQL draft JSON</td><td>None</td><td>Execute SQL</td></tr>
<tr><td>Validator</td><td>SQL draft</td><td>pass/fail + reasons</td><td>SQL parser, schema check</td><td>Modify business rules</td></tr>
<tr><td>Explainer</td><td>SQL + context</td><td>Human summary</td><td>Read-only</td><td>Change SQL</td></tr>
</table>
<p><strong>Key insight:</strong> Validator is not a prompt — it's a separate step (can be code-only, no LLM).</p>
</div>

<div class="section">
<h2>Multi-Agent NL2SQL Pipeline (Full)</h2>
<div class="diagram-container"><div class="mermaid">
flowchart TD
    U[User: Revenue by department this term] --> IA[Intent Agent]
    IA -->|reporting, finance, medium risk| RA[Retriever Agent]
    RA --> SA[Schema chunks]
    RA --> BA[Business rule chunks]
    SA --> SQL[SQL Generator Agent]
    BA --> SQL
    SQL --> VA{Validator Agent}
    VA -->|fail| CL[Clarify / refuse]
    VA -->|pass| EA[Explainer Agent]
    EA --> OUT[SQL + assumptions + citations]
    OUT --> HG{Human gate}
    HG -->|approved| EX[Read-only execute]
</div></div>
</div>

<div class="section">
<h2>Single Workflow vs Multi-Agent</h2>
<table>
<tr><th>Dimension</th><th>Single workflow (few LLM calls)</th><th>Multi-agent</th></tr>
<tr><td>Latency</td><td>Lower (1–2 calls)</td><td>Higher (4–7 calls)</td></tr>
<tr><td>Cost</td><td>Lower token reuse</td><td>Higher — separate contexts</td></tr>
<tr><td>Debuggability</td><td>Moderate</td><td>Better — inspect each agent output</td></tr>
<tr><td>Safety isolation</td><td>Rules in one prompt</td><td>Generator can't bypass validator agent</td></tr>
<tr><td>When to use</td><td>MVP, &lt;50 tables, one team</td><td>Multi-domain, strict compliance, large schema</td></tr>
</table>
</div>

<div class="section">
<h2>Full Application Blueprint (Chapters 2–10 Combined)</h2>
<p>This is what you teach as the <strong>complete path from prompt to production NL2SQL / AI app</strong>:</p>
<div class="diagram-container"><div class="mermaid">
flowchart TB
    subgraph Ch2-5 Understand LLM limits
        L[LLM generates from context only]
        P[Prompts = first control layer]
        F[Prompts fail without facts]
    end
    subgraph Ch6 Context Engineering
        CE[Assemble: policy + auth + retrieval + task]
    end
    subgraph Ch7-8 Knowledge and Tools
        RAG[RAG: schema + rules]
        TOOL[Tools: validate, search]
    end
    subgraph Ch9-10 Orchestration
        WF[Workflow default]
        AG[Agent / multi-agent when earned]
    end
    L --> P --> F --> CE --> RAG --> TOOL --> WF --> AG
    AG --> PROD[Production: evals + governance Ch16-18]
</div></div>
</div>

<div class="section">
<h2>When NOT to Use Multi-Agent</h2>
<div class="error-box"><h4>Over-engineering signals</h4>
<ul>
<li>Team can't trace which agent failed</li>
<li>5 agents but no evals on each step</li>
<li>Simple SELECT queries taking 8 LLM calls</li>
<li>Latency SLA &lt; 3s</li>
<li>MVP stage — workflow would ship faster</li>
</ul></div>
<div class="success-box"><h4>Start here instead</h4>
<p>Single workflow: classify → RAG → generate → validate (code) → explain. Add agents only when you measure a bottleneck that separation fixes.</p></div>
</div>

<div class="section">
<h2>Junior vs Senior Takeaways (Ch 2–10)</h2>
<table>
<tr><th>Topic</th><th>Junior developer</th><th>Senior developer</th></tr>
<tr><td>LLM</td><td>Don't trust fluent output</td><td>Design verification layers</td></tr>
<tr><td>Prompts</td><td>Use templates, be specific</td><td>Version prompts, JSON contracts, evals</td></tr>
<tr><td>Context</td><td>@file and paste schema</td><td>Assembly pipeline, ACL, logging</td></tr>
<tr><td>RAG</td><td>"AI searches docs"</td><td>Chunking, hybrid search, re-index CI</td></tr>
<tr><td>Tools</td><td>Let Cursor run things</td><td>Permission matrix, approval gates</td></tr>
<tr><td>Agents</td><td>Agent mode for everything</td><td>Workflow default, bounded agents</td></tr>
<tr><td>Multi-agent</td><td>Sounds cool — use everywhere</td><td>Justify with metrics or don't</td></tr>
</table>
</div>

<div class="presentation-tip"><strong>🎤 Capstone for your talk:</strong> Walk this blueprint once. Point to where ChatGPT stops (chat) vs where your NL2SQL app starts (Ch 6–10). Seniors leave with an architecture; juniors leave with rules they can use Monday.</div>
<div class="takeaway"><h3>Key Takeaway</h3>
<p>Chapters 2–10 are one story: understand the model → control with prompts → fail without context → engineer context → retrieve facts → add tools → orchestrate safely. That is how you build, use, and control AI in 2026.</p></div>
"""
