# Additional sections for Chapters 02–06 — behind-the-scenes + tool usage + app building
from chapter_content import code, tabs
from chapter_helpers import tool_stack_table

PATCHES_02_06 = {}

PATCHES_02_06["02"] = """
<div class="section">
<h2>Training vs Inference — What the Model Actually "Knows"</h2>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    subgraph Training time past
        TD[Internet + books + code repos] --> W[Model weights frozen]
    end
    subgraph Inference time now
        W --> INF[Your prompt context]
        INF --> OUT[Output]
        RAG[RAG / tools] --> INF
    end
</div></div>
<table>
<tr><th>Source of knowledge</th><th>Freshness</th><th>Your private DB schema?</th><th>Verifiable?</th></tr>
<tr><td>Training weights</td><td>Cutoff date</td><td>❌ No</td><td>❌ No</td></tr>
<tr><td>Prompt / context</td><td>What you inject now</td><td>✅ If you paste/retrieve</td><td>⚠️ Only if you validate</td></tr>
<tr><td>Tool results</td><td>Live query</td><td>✅ Yes</td><td>✅ Yes — ground truth</td></tr>
</table>
<p><strong>Teaching line:</strong> The model does not "look up" your database. It predicts text. Your application must supply facts and verify outputs.</p>
</div>

<div class="section">
<h2>How Developer Tools Use LLMs (Behind the Scenes)</h2>
""" + tool_stack_table() + """
<div class="diagram-container"><div class="mermaid">
flowchart TB
    subgraph ChatGPT / Claude
        U1[User message] --> API1[Remote LLM API]
        API1 --> R1[Text response]
    end
    subgraph Cursor / Copilot
        U2[User + open files] --> IDX[Codebase index]
        IDX --> API2[LLM API]
        API2 --> R2[Edit / completion]
    end
    subgraph Your NL2SQL App
        U3[Natural language] --> PIPE[RAG + validators + LLM]
        PIPE --> R3[Safe SQL]
    end
</div></div>
<div class="info-box"><h4>For juniors</h4>
<p>ChatGPT doesn't see your repo unless you paste or upload. Cursor indexes your project — still not "magic understanding"; it's retrieval + context.</p></div>
<div class="info-box"><h4>For seniors</h4>
<p>Custom apps beat generic chat when you need <strong>ACL, evals, audit logs, and schema binding</strong>. That's why you build NL2SQL as a pipeline, not a ChatGPT prompt.</p></div>
</div>

<div class="section">
<h2>Sampling Parameters Developers Should Know</h2>
<table>
<tr><th>Parameter</th><th>Effect</th><th>NL2SQL / production</th><th>Brainstorming in chat</th></tr>
<tr><td><strong>temperature</strong></td><td>Randomness of token choice</td><td>0–0.2 (deterministic)</td><td>0.7–1.0</td></tr>
<tr><td><strong>top_p</strong></td><td>Nucleus sampling breadth</td><td>Low / default</td><td>Higher for variety</td></tr>
<tr><td><strong>max_tokens</strong></td><td>Output length cap</td><td>Set to fit JSON + SQL</td><td>As needed</td></tr>
<tr><td><strong>stop sequences</strong></td><td>End generation early</td><td>Close JSON reliably</td><td>Rarely needed</td></tr>
</table>
</div>

<div class="section">
<h2>Where LLM Sits in Your NL2SQL Application</h2>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    UI[Chat UI] --> ORCH[Your backend orchestrator]
    ORCH --> RAG[RAG retrieval]
    ORCH --> LLM[LLM: generate SQL only]
    ORCH --> VAL[Validator code]
    ORCH --> DB[(Database read-only)]
    RAG --> LLM
    LLM --> VAL
    VAL --> DB
</div></div>
<p>The LLM is <strong>one component</strong> — not the whole system. Seniors own the boxes around it.</p>
</div>
"""

PATCHES_02_06["03"] = """
<div class="section">
<h2>From Chat Message to API Request (Behind the Scenes)</h2>
<p>When you use ChatGPT, Cursor, or your own app, the same pattern applies: <strong>messages array → API → response</strong>.</p>
""" + code("json", """{
  "model": "gpt-4.1",
  "messages": [
    { "role": "system", "content": "You are a safe SQL assistant..." },
    { "role": "user", "content": "Schema: ...\\n\\nQuestion: Show unpaid invoices" }
  ],
  "temperature": 0.1,
  "response_format": { "type": "json_object" }
}""") + """
<p><strong>Cursor</strong> adds: codebase chunks, open files, rules from <code class="inline-code">.cursor/rules</code>. <strong>Your NL2SQL app</strong> adds: retrieved schema, user ACL, validator after response.</p>
</div>

<div class="section">
<h2>Using Chat Models Properly (Junior + Senior)</h2>
<table>
<tr><th>Do</th><th>Don't</th></tr>
<tr><td>One clear task per message</td><td>"Build entire microservice" in one prompt</td></tr>
<tr><td>Paste relevant schema only</td><td>Dump 500 tables</td></tr>
<tr><td>Ask for JSON / structured output</td><td>Parse free-text with regex in production</td></tr>
<tr><td>Say "use only provided context"</td><td>Assume model knows your stack</td></tr>
<tr><td>Iterate: plan → approve → code</td><td>Accept first output for prod</td></tr>
</table>
</div>

<div class="section">
<h2>Prompt Engineering in Cursor vs Custom API</h2>
<div class="compare-grid">
<div class="compare-col good">
<h4>Cursor (IDE)</h4>
<ul>
<li>System: rules + project context</li>
<li>User: your instruction + @files</li>
<li>Hidden: index retrieval of related files</li>
</ul>
<p>Prompt engineering = <strong>good instructions + right @context</strong></p>
</div>
<div class="compare-col good">
<h4>Custom NL2SQL API</h4>
<ul>
<li>System: safety policy (you own)</li>
<li>Developer: output schema</li>
<li>User: question only — schema from RAG</li>
</ul>
<p>Prompt engineering = <strong>contract + assembly code</strong></p>
</div>
</div>
</div>
"""

PATCHES_02_06["04"] = """
<div class="section">
<h2>Pattern → Tool Mapping (What to Use Where)</h2>
<table>
<tr><th>Pattern</th><th>ChatGPT / Claude</th><th>Cursor</th><th>NL2SQL pipeline</th></tr>
<tr><td>Plan-first</td><td>✅ Before any code ask</td><td>✅ Agent mode step 1</td><td>✅ Before SQL gen in risky domains</td></tr>
<tr><td>Review-first</td><td>✅ Paste PR diff</td><td>✅ Ask mode on @file</td><td>⚠️ Separate validator agent/code</td></tr>
<tr><td>Few-shot</td><td>✅ In prompt</td><td>✅ In rules/examples</td><td>✅ Retrieved example pairs (RAG)</td></tr>
<tr><td>Verification</td><td>✅ Self-check prompt</td><td>✅ + run tests</td><td>✅ Mandatory code validator</td></tr>
<tr><td>ReAct / tools</td><td>✅ Advanced GPT tools</td><td>✅ Agent tools</td><td>✅ search_schema, validate_sql</td></tr>
</table>
</div>

<div class="section">
<h2>Behind the Scenes: Why "Plan First" Changes Model Behavior</h2>
<p>Without plan-first, the model optimizes for <strong>immediate plausible completion</strong> (lowest loss next tokens for "here is code"). With plan-first, you force allocation of context tokens to <strong>structure before syntax</strong> — reducing wrong-file edits and scope creep.</p>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    subgraph Without plan
        Q1[Fix bug] --> G1[Generate code immediately]
        G1 --> R1[Large risky diff]
    end
    subgraph With plan
        Q2[Fix bug] --> P2[Plan + risks + tests]
        P2 --> A2[Human OK]
        A2 --> G2[Minimal targeted code]
    end
</div></div>
</div>

<div class="section">
<h2>Failure → Fix: Advanced Prompting</h2>
<div class="error-box"><h4>❌ Failure</h4>
<p>Developer uses few-shot examples from old schema after migration. Model copies <code class="inline-code">status</code> column that was renamed.</p></div>
<div class="success-box"><h4>✅ Fix</h4>
<ol>
<li>Retrieve few-shot examples dynamically (RAG), don't hardcode in prompt</li>
<li>Validator checks columns against live schema</li>
<li>Eval regression on schema change</li>
</ol></div>
</div>
"""

PATCHES_02_06["05"] = """
<div class="section">
<h2>The Presentation Bridge: Prompt Engineering → Context Engineering</h2>
<div class="diagram-container"><div class="mermaid">
flowchart LR
    PE[Prompt Engineering<br/>Ch 3-4] --> LIMIT[Hits fact ceiling<br/>Ch 5]
    LIMIT --> CE[Context Engineering<br/>Ch 6]
    CE --> BUILD[RAG + Tools + Agents<br/>Ch 7-10]
    BUILD --> APP[NL2SQL / Chat / Code apps]
</div></div>
<p>Your audience should feel: <em>we mastered prompts, we hit a wall, now we engineer context and build systems.</em></p>
</div>

<div class="section">
<h2>Failure Modes When Building Applications</h2>
<table>
<tr><th>App type</th><th>Typical failure</th><th>Looks like prompt problem</th><th>Actual fix</th></tr>
<tr><td>NL2SQL chatbot</td><td>Wrong JOIN</td><td>"Write better SQL prompt"</td><td>RAG schema + relationship metadata</td></tr>
<tr><td>Doc Q&A</td><td>Outdated policy</td><td>"Be more accurate"</td><td>Re-index + version metadata</td></tr>
<tr><td>Cursor refactor</td><td>Breaks unrelated tests</td><td>"Be careful"</td><td>@file scope + plan-first + run tests</td></tr>
<tr><td>Copilot completion</td><td>Wrong import path</td><td>—</td><td>Verify compile; don't tab-accept blindly</td></tr>
<tr><td>Support bot</td><td>Leaks other customer data</td><td>"Don't leak"</td><td>Retriever ACL per user_id</td></tr>
</table>
</div>

<div class="section">
<h2>Junior vs Senior: When Prompting Stops</h2>
<div class="compare-grid">
<div class="compare-col bad">
<h4>Junior mistake</h4>
<p>Keeps adding "be accurate", "double check", "you are expert" to prompt for 2 weeks.</p>
</div>
<div class="compare-col good">
<h4>Senior move</h4>
<p>Builds schema retriever, adds validator, writes 20 eval cases, measures accuracy — prompt becomes stable.</p>
</div>
</div>
</div>
"""

PATCHES_02_06["06"] = """
<div class="section">
<h2>Context Engineering for Each Application Type</h2>
<table>
<tr><th>Application</th><th>Context you must engineer</th><th>Don't rely on model alone</th></tr>
<tr><td><strong>NL2SQL</strong></td><td>Schema RAG, business rules, ACL, SQL validator</td><td>Table/column existence</td></tr>
<tr><td><strong>Doc chatbot</strong></td><td>Chunked wiki, permissions, citations</td><td>Current policy text</td></tr>
<tr><td><strong>Code assistant (Cursor)</strong></td><td>Index, @files, rules, test output</td><td>Project conventions</td></tr>
<tr><td><strong>ChatGPT Q&A</strong></td><td>What you paste/upload per session</td><td>Private data, live schema</td></tr>
<tr><td><strong>Support agent</strong></td><td>Ticket history, product docs, user tier</td><td>Customer B's data for customer A</td></tr>
</table>
</div>

<div class="section">
<h2>End-to-End: Building NL2SQL with Context Engineering</h2>
<div class="diagram-container"><div class="mermaid">
flowchart TB
    subgraph Input layer
        U[User question]
        AUTH[Auth + role]
    end
    subgraph Context engineering core Ch6
        INT[Intent classify]
        RET[RAG: schema + rules + examples]
        ASM[Assemble labeled context bundle]
    end
    subgraph Model Ch2-4
        PR[Prompt templates]
        LLM[LLM generate]
    end
    subgraph Control Ch7-10 preview
        VAL[Validators]
        APP[Human approve]
        EX[Execute read-only]
    end
    U --> AUTH --> INT --> RET --> ASM --> PR --> LLM --> VAL --> APP --> EX
</div></div>
<p>Chapters 7–10 add depth on RAG, tools, and agents — but <strong>Chapter 6 is the architectural center</strong> of your presentation.</p>
</div>

<div class="section">
<h2>Controlling AI in ChatGPT vs Controlling AI in Your App</h2>
<div class="compare-grid">
<div class="compare-col good">
<h4>ChatGPT / Claude (user-controlled)</h4>
<ul>
<li>User chooses what to paste</li>
<li>No enterprise ACL by default</li>
<li>Good for learning and drafts</li>
</ul>
</div>
<div class="compare-col good">
<h4>Your application (developer-controlled)</h4>
<ul>
<li>You enforce retrieval filters</li>
<li>You own validators and logs</li>
<li>You pass evals before deploy</li>
</ul>
</div>
</div>
<div class="quote-block">Build, use, and control AI — "control" only exists when <em>you</em> own the pipeline.</div>
</div>
"""
