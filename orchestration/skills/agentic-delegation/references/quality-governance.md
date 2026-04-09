# Quality Governance

This document covers quality control patterns for agent-delegated work: detecting bad output, handling contradictions, and verification strategies.

## Detecting Bad Output

You receive completion summaries, not full reports. Scan summaries for:

| Signal | Likely Problem | Action |
|--------|---------------|--------|
| Extraordinary claims (huge numbers, superlatives) | Hallucination | Launch verification agent |
| Two agents contradict each other | At least one is wrong | Launch resolution agent |
| Agent says "I couldn't find" or "not available" | Agent couldn't use tools effectively | Re-launch with clearer tool instructions |
| Report is suspiciously short | Agent gave up early or misunderstood | Re-launch with more specific prompt |
| Agent made recommendations when told not to | Prompt wasn't clear enough | Discard recommendations, use findings only |

## The Re-Launch Principle

**Never debug a failed agent in orchestrator context.** Don't read its full output, don't trace its reasoning, don't figure out where it went wrong. Instead:

1. Note the failure signal from the completion summary
2. Re-launch the task with either:
   - A more specific prompt (if the issue was vague instructions)
   - A better model (if the issue was reasoning capability)
   - Decomposed sub-tasks (if the issue was task complexity)

Debugging an agent burns YOUR context. Re-launching costs nearly nothing.

### Why Re-Launch Instead of Debug

| Debugging in orchestrator context | Re-launching with better prompt |
|----------------------------------|--------------------------------|
| Consumes orchestrator context with failed output | Zero context cost — new agent gets fresh window |
| Takes time to trace reasoning | Takes seconds to write clearer prompt |
| May not find the root cause | Addresses root cause directly (vague prompt, wrong tier) |
| Teaches you about failure | Produces the result you needed |

**Example:**

Agent returns: "I found 3 components but couldn't verify compatibility."

**Wrong response:**
Read the agent's full report, examine its search process, figure out what went wrong, manually verify compatibility yourself.

**Correct response:**
Launch new agent: "Search the registry for compatible components. For each, fetch the metadata and check version requirements. Verify compatibility with v4.x. Use WebFetch for metadata."

## Contradiction Resolution

When two agents disagree:

1. Do NOT decide which is right by reading both reports
2. Launch a new agent tasked ONLY with checking primary sources
3. Give it both file paths and the specific contradiction
4. It reports back which claim is supported by evidence

### The Resolution Agent Pattern

```
Agent A reports: "Library X supports version 4"
Agent B reports: "Library X requires version 3"
```

**Wrong response:**
Read both reports, compare their reasoning, decide which sounds more credible.

**Correct response:**
Launch resolution agent:

> "Two agents disagree about library X's version compatibility. Agent A's report: `/path/to/report-a.md`. Agent B's report: `/path/to/report-b.md`. Fetch library X's official documentation and metadata. Check the actual version requirements and compatibility statements. Report which claim is supported by primary sources."

### Why This Works

- **No context contamination:** You don't read either flawed report
- **Independent verification:** Resolution agent checks sources, not opinions
- **Definitive answer:** Evidence-based resolution, not credibility judgment
- **Cheap:** One haiku agent resolves what would have consumed orchestrator context

## Spot-Checking

For any research/audit with more than 10 agents, spot-check 1-2 reports by launching a verification agent that re-does a specific agent's task independently. If the spot-check matches, trust the batch. If it doesn't, re-run the suspect agent (or the whole tier) at higher fidelity.

### When to Spot-Check

- Large parallel batches (10+ agents)
- High-stakes audits (security, compatibility, compliance)
- When agent outputs will inform major decisions
- After upgrading from haiku to sonnet (verify the upgrade was necessary)

### The Spot-Check Agent Pattern

```
Batch of 15 haiku agents complete → orchestrator reads summaries
   ↓
Pick 1-2 reports at random or based on criticality
   ↓
Launch verification agent: "Re-do the task from Agent 7. Do not read Agent 7's report. Produce an independent report."
   ↓
Compare completion summaries (not full reports)
   ↓
If match: trust the batch
If mismatch: investigate (launch resolution agent or re-run the tier)
```

### Spot-Check Sampling Strategy

**Random sampling:** For general confidence in batch quality
- Pick 1-2 agents at random from the batch
- Verify their findings independently
- If both match, statistical confidence in the batch

**Critical sampling:** For high-stakes verification
- Pick agents whose findings are most consequential
- Example: "Agent 12 found a security vulnerability" → verify that claim
- Example: "Agent 5 says library X is incompatible" → verify before discarding library X

**Outlier sampling:** For anomaly detection
- Pick agents whose summaries seem extraordinary or suspicious
- Example: "Agent 9 found 47 issues while others found 2-5" → verify Agent 9
- Example: "Agent 3 says library Y doesn't exist" → verify that claim

## Concurrent File Write Prevention

Never dispatch two parallel agents that write to the same file. The later agent's version wins silently — the earlier agent's work is lost with no error, no warning, no conflict marker.

**Before parallel dispatch:**
1. List which files each agent will modify
2. If any file appears in two agents' write sets, make those agents sequential
3. Include isolation context in each agent's brief: which files it owns and which files other agents own

**If concurrent writes happen despite precautions:**
1. Identify which agent's output matches the spec
2. Keep that output
3. Re-dispatch the other agent with updated context

## Independent Verification

Agent self-reports ("DONE, all tests pass") are unreliable. After every agent completes, verify independently:

- Run the test suite or type checker yourself
- Check that output files actually exist and contain expected content
- Verify that the agent's claimed changes appear in git diff

**Why agents lie (unintentionally):**
- Agent ran tests on a stale version
- Agent's test command had a filter that excluded failing tests
- Agent reported based on partial output (truncated by context limits)
- Agent confused "no errors printed" with "tests pass"

This is not about distrusting agents. It's about recognizing that an agent's view of system state may diverge from actual system state, especially after long implementation sessions with multiple file modifications.
