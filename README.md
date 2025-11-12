Here you go, Everett — clean, sharp, and ready to drop straight into GitHub.
Badges up top, Markdown perfect, no frills, no clutter.
Copy → paste → done.

---

# **VIRTUS**

### *Backbone of the Christman Fusion Architecture*

[![Status](https://img.shields.io/badge/Status-Core%20Protocol-blue)]()
[![Version](https://img.shields.io/badge/Version-v1.0-black)]()
[![Security](https://img.shields.io/badge/Security-Ed25519%20JWT-green)]()
[![Architecture](https://img.shields.io/badge/Layer-Fusion%20Backbone-orange)]()
[![Compliance](https://img.shields.io/badge/Policy-Least%20Privilege-important)]()

---

# **Overview**

Virtus is the neutral backbone of the Christman Fusion Architecture.
No personality. No identity. No ego.
Just law, structure, and the clean orchestration that keeps the entire constellation stable.

Virtus governs:

* identity and authentication
* cross-agent communication
* provider selection
* memory mesh access
* safety, rate limits, and kill-switches
* audit trails and consistency rules

Everything that moves through this system touches Virtus first.

---

# **1. Purpose**

Virtus exists to:

* Authenticate each agent with short-lived, scope-limited tokens
* Route all cross-agent traffic through a single safe bus
* Control provider routing and fallback logic
* Regulate the Memory Mesh (tags, ownership, visibility)
* Guard the system with rate limits, safety checks, and breakers
* Log every meaningful action with immutable audit entries

Virtus is the conductor. The children are the orchestra.

---

# **2. System Architecture**

Virtus consists of five pillars:

### **1. Auth Layer**

Short-TTL Ed25519 JWT signing.
Strict scope enforcement.
Per-agent, per-task audience targeting.

### **2. Fusion Bus**

The only legal way for agents to talk to each other.
Caller → Virtus → Target.
No direct agent-to-agent traffic.

### **3. Provider Router**

Unified abstraction over OpenAI, Anthropic, Ollama, Bedrock.
Picks the right model at the right moment.
Logs all routing decisions.

### **4. Memory Mesh Router**

Defines laws for tagging, visibility, ownership, retention.
Does **not** store memory.
Keeps identities separate.

### **5. Guardian Layer**

Rate limits, kill switches, deny lists, allowlists.
Circuit breakers.
Action safety and environment isolation.

---

# **3. Token Model**

Virtus signs tokens with **Ed25519**, rotated daily.

### **Mandatory Claims**

```json
{
  "iss": "virtus.auth",
  "sub": "<agent_id>",
  "aud": "<service_name>",
  "exp": 1234567890,
  "iat": 1234560000,
  "jti": "<uuid>",
  "scp": ["chat.send", "mem.read"],
  "ctx": {
    "user_id": "<uuid>",
    "session_id": "<uuid>",
    "trace_id": "<uuid>"
  }
}
```

### **Available Scopes**

* `chat.send`
* `mem.read` / `mem.write`
* `fusion.call`
* `audio.tts` / `audio.stt`
* `vision.read`
* `actions.exec:<capability>`

**Rule:** no agent gets more scope than it needs *this minute*.

---

# **4. Fusion Protocol**

This governs Brockston → Derek, Wolf → Vox, Inferno → Brockston, etc.

### **Call Flow**

1. Caller requests JWT from Virtus.auth
2. Caller sends Fusion Call to Virtus.bus
3. Bus validates + issues new audience-scoped token for target
4. Target executes
5. Bus relays results
6. Everything gets audited

### **Request Example**

```json
{
  "trace_id":"<uuid>",
  "caller":"brockston",
  "target":"derek.chat",
  "intent":"reasoning.delegate",
  "payload":{
    "messages":[
      {"role":"system","content":"Derek: act as gateway."},
      {"role":"user","content":"<input>"}
    ],
    "constraints":{"max_tokens":1200,"deadline_ms":4000}
  }
}
```

### **Hard Laws**

* No agent may call another directly
* Fusion Bus must issue the new token each hop
* Intent must be explicit
* Allowlist controls who can target whom

---

# **5. Provider Router**

All providers read the same neutral envelope.

### **Example**

```json
{
  "trace_id":"<uuid>",
  "agent":"brockston",
  "task":"user.chat",
  "input":{
    "messages":[...],
    "system":"...",
    "tools":[],
    "hints":{"latency_ms_max":2500}
  },
  "policy":{
    "provider_preferences":["openai:gpt-5"],
    "tokens_cap":8000,
    "cost_cap_usd":0.02
  },
  "telemetry":{
    "deadline_ms":5000,
    "retry":{"max":1,"backoff_ms":200}
  }
}
```

### **Routing Rules**

1. Deadline
2. Cost
3. Capability
4. Fallback

Every decision gets recorded.

---

# **6. Memory Mesh Router**

Virtus enforces memory *law*, not memory *storage*.

### **Write Example**

```json
{
  "owner":"alphawolf",
  "visibility":"private",
  "tags":["medication","evening"],
  "content":{"type":"note","text":"Took 5mg at 8:05pm"},
  "retention":{"ttl_days":365}
}
```

### **Read Example**

```json
{
  "owner":"alphawolf",
  "query":{"tags":["medication"]},
  "limit":50
}
```

### **Visibility**

* `private` — owner only
* `shared:<group>` — controlled and redacted
* No cross-agent reads into private shards

---

# **7. Module Loader**

All modules require a manifest:

```json
{
  "name":"audio_tts",
  "version":"1.2.3",
  "scopes_required":["audio.tts"],
  "entrypoint":"audio_tts:Module",
  "capabilities":["synthesize"],
  "limits":{"qps":5},
  "policy":{"allowed_agents":["alphavox","brockston"]}
}
```

### **Lifecycle**

* load
* capabilities
* call
* shutdown

Modules cannot elevate privilege after load.

---

# **8. Guardian Layer**

Virtus enforces:

### **Rate Limits**

* 60 requests/min per agent
* 30 fusion calls/min per user
* Per-module QPS limits

### **Circuit Breakers**

Trip after 3 failures/30s.

### **Safety**

* Action allowlists
* Outbound network controls
* No filesystem access outside approved paths
* Unsafe content returns `blocked:true`

---

# **9. Telemetry & Audit**

Every hop logs:

* trace_id
* span_id
* caller/target
* provider
* latency
* token counts
* cost
* routing decisions

Append-only audit.
30-day hot.
1-year cold.

---

# **10. Versioning**

Virtus uses strict semantic versioning.

* `v1` — current
* breaking changes require dual-stack deployment
* clients send `Accept-Proto: v1`
* mismatches fail closed

---

# **11. Rollout Checklist**

1. Generate Ed25519 keypairs
2. Deploy Auth with mTLS
3. Deploy Fusion Bus with allowlist
4. Implement Router with fallback logic
5. Bring up Memory Router with tag index
6. Enable Guardian layer
7. wire OpenTelemetry
8. Run Game Day (failure injection)
9. Approve production deployment

---

# **12. Non-Negotiables**

* No long-lived tokens
* No direct agent-to-agent calls
* No identity bleed
* Least privilege everywhere
* Logs or it didn’t happen

---

