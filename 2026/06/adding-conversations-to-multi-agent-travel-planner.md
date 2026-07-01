---
author: "Bimal Gharti Magar"
title: "Adding Multi-Turn Conversations to a Multi-Agent Travel Planner"
description: How to evolve a single-shot multi-agent .NET workflow into a conversational system with routed turns, SQLite persistence, and per-conversation locking.
date: 2026-06-01
tags:
- dotnet
- csharp
- artificial-intelligence
- programming
---

In a [previous post](/blog/2026/03/building-multi-agent-travel-planner-dotnet/), I walked through a multi-agent travel planner built on the [Microsoft Agent Framework (MAF)](https://github.com/microsoft/agents). It worked, but it was single-shot: one prompt produced one plan, and the conversation ended there. If you wanted to swap a city, trim a day, or ask a clarifying question, the only option was to write a new prompt from scratch.

This post is the follow-up. We will turn that one-shot pipeline into a real multi-turn conversation, while keeping the same five agents under the hood. Along the way we will look at how to feed chat history through a MAF workflow, how to avoid re-running the full pipeline on every follow-up, how to persist conversations to SQLite, and how to keep a single conversation from running two turns in parallel.

The source code is on [GitHub](https://github.com/bimalghartimagar/LocalAgentTravelPlanner).

### What we will build

- A multi-turn conversation surface where each follow-up message refines the plan in place
- A small LLM router that decides which subset of agents needs to run for each turn
- SQLite-backed persistence so conversations survive process restarts
- A per-conversation async lock that returns 409 Conflict when two turns race
- A three-pane browser UI: conversation sidebar, chat, and the latest plan pinned on the right

### Why not just re-run the full pipeline?

The simplest design for a follow-up turn is: append the new user message to the conversation, run all five agents again, get a fresh plan. That works, but the cost is steep — every follow-up burns a full Researcher pass that probably does not need to repeat, plus the Planner, Accountant, Auditor, and Aggregator.

A better division: classify the turn first, then run only the agents whose work actually needs to change. A budget tweak does not need new research. A safety question does not need a new plan. A clarification ("what does FLAGGED mean here?") does not need to re-run anything except the Aggregator in chat-answer mode.

That classification is what the rest of this post calls "the router," and it is the single design decision that drives everything else.

![Router decision flow: a user message enters the router, which dispatches to one of six routes — full runs all five agents, replan runs four, rebudget three, reaudit two, clarify only the Aggregator, and offtopic short-circuits with a refusal](/blog/2026/06/adding-conversations-to-multi-agent-travel-planner/router-flow.svg)

### Chat history storage in MAF

Microsoft's own [chat history storage patterns post](https://devblogs.microsoft.com/agent-framework/chat-history-storage-patterns-in-microsoft-agent-framework/) covers two broad approaches: service-managed (the LLM provider tracks the thread by id) and client-managed (the application owns the history). The framework gives you `AgentSession` and built-in `ChatHistoryProvider` types to make either approach trivial — for a single agent.

#### The single-agent path you get out of the box

For one agent, the MAF [multi-turn](https://learn.microsoft.com/en-us/agent-framework/get-started/multi-turn?pivots=programming-language-csharp) and [memory](https://learn.microsoft.com/en-us/agent-framework/get-started/memory?pivots=programming-language-csharp) tutorials show the canonical pattern:

```csharp
AIAgent agent = new AIProjectClient(endpoint, credential)
    .AsAIAgent(model: "gpt-4o-mini", instructions: "You are a friendly assistant.");

AgentSession session = await agent.CreateSessionAsync();

await agent.RunAsync("My name is Alice.", session);
await agent.RunAsync("What's my name?", session);  // remembers
```

`AgentSession` carries the conversation state across calls. The framework picks where to persist history — service-side when the provider supports it, or via an `InMemoryChatHistoryProvider` locally. To take ownership of storage, you pass a custom `ChatHistoryProvider` in `ChatClientAgentOptions` and you're done. Two lines of code for a fully working multi-turn agent with persistent memory.

That works because the unit of state is unambiguous: one agent, one thread, one session.

#### Why a sequenced workflow doesn't fit the same mold

The travel planner is not one agent. It is five agents in sequence, built with `AgentWorkflowBuilder.BuildSequential` and executed via `InProcessExecution.StreamAsync`. The API is "execute the workflow with this input," not "continue this conversation with this agent." There is no single agent to call `CreateSessionAsync()` on.

The natural unit of state is also different. A user thinks of the conversation as a dialogue with *the planner* — they do not care that the Researcher's chat history and the Aggregator's chat history are technically separate threads. The user-visible conversation cuts across all five agents.

So we build the equivalent at the service layer:

| MAF single-agent concept | Travel planner equivalent |
|---|---|
| `AgentSession` (identity + state of an ongoing conversation) | `Conversation` aggregate (`Id`, `History`, `LatestPlan`) |
| `ChatHistoryProvider` (where the history is stored) | `IConversationStore` — `InMemoryConversationStore` for tests, `SqliteConversationStore` for production |
| `agent.RunAsync(message, session)` (continue the conversation) | `service.ContinueConversationAsync(conv, message)` (run a routed workflow turn) |
| Framework decides what to load into context | Service passes the full `List<ChatMessage>` history to the workflow per turn |

Same pattern, applied one layer higher. The `AgentWorkflowBuilder.BuildSequential` workflow accepts a `List<ChatMessage>` as input. On the first turn we pass `[user_message]`. On follow-up turns we pass the full conversation history plus the new user message. Each agent in the workflow sees the same accumulated history when it runs.

If MAF eventually ships a `WorkflowSession` (or any session abstraction at the workflow boundary), the code below becomes a candidate for replacement. Until then, this service-layer pattern is the canonical approach for multi-agent workflows.

### The conversation domain

Three new types under `Services/Conversations/` carry the shape of a conversation:

```csharp
public sealed class Conversation
{
    public required string Id { get; init; }
    public string? Title { get; set; }
    public List<ChatMessage> History { get; init; } = new();
    public string? LatestPlan { get; set; }
    public required DateTime CreatedAt { get; init; }
    public DateTime LastActivity { get; set; }
}

public sealed record ConversationSummary(string Id, string? Title, DateTime LastActivity);

public enum TurnRoute { Full, Replan, Rebudget, Reaudit, Clarify, OffTopic }
```

`History` holds user and assistant turns only, not the per-agent intermediate output. That distinction matters because the per-agent chatter from a five-agent pipeline would balloon the context fast, and most of it is uninteresting to the next turn. The polished Aggregator output, stored as a single assistant message, carries enough context for the downstream agents on the next turn.

The store is hidden behind an interface so the in-memory and SQLite implementations are interchangeable:

```csharp
public interface IConversationStore
{
    Task<Conversation> CreateAsync(CancellationToken ct = default);
    Task<Conversation?> GetAsync(string id, CancellationToken ct = default);
    Task UpdateAsync(Conversation conversation, CancellationToken ct = default);
    Task<bool> DeleteAsync(string id, CancellationToken ct = default);
    Task<IReadOnlyList<ConversationSummary>> ListAsync(CancellationToken ct = default);
}
```

### The router

The router is not a MAF agent. It is a single short LLM call at the start of each turn — same pattern as the intent classifier from the previous post — that returns one of six route tokens:

```csharp
private const string RouterPrompt = """
    You are a router for a travel-planning multi-agent system. Given the conversation history
    and the new user message, decide which subset of agents needs to re-run.

    Routes:
    - full      : new destination/dates/scope, or any request that needs fresh research
    - replan    : itinerary tweaks within the same trip
    - rebudget  : budget/cost adjustments only
    - reaudit   : re-validate the existing plan
    - clarify   : Q&A about the existing plan, no plan change
    - offtopic  : not travel-related

    Respond with exactly one of: full, replan, rebudget, reaudit, clarify, offtopic
    No explanation. No punctuation.
    """;
```

Parsing is deliberately tolerant. The router lowercases and trims the response, matches it against the enum names, and falls back to `Full` on anything unrecognized:

```csharp
return token switch
{
    "full" => TurnRoute.Full,
    "replan" => TurnRoute.Replan,
    "rebudget" => TurnRoute.Rebudget,
    "reaudit" => TurnRoute.Reaudit,
    "clarify" => TurnRoute.Clarify,
    "offtopic" => TurnRoute.OffTopic,
    _ => TurnRoute.Full
};
```

The fallback is intentional. Running too many agents costs latency and tokens; running too few risks shipping a stale plan. The safer mistake is to over-run, so any router failure resolves to the full pipeline.

To keep the router cheap, we compact the conversation history before sending it: take the last eight turns, truncate each to 400 characters, and concatenate them with `Role: text` formatting. That is enough context for the model to tell "tweak" from "new trip," and it bounds the prompt size predictably regardless of how long the conversation gets.

The first turn always skips the router — the only route that makes sense before any plan exists is `Full`.

### Building a workflow from a subset of agents

Once we know the route, the workflow is just the matching subset of the five agents:

```csharp
private List<ChatClientAgent> SelectAgents(TurnRoute route) => route switch
{
    TurnRoute.Full     => new() { _researcher, _planner, _accountant, _auditor, _aggregator },
    TurnRoute.Replan   => new() { _planner, _accountant, _auditor, _aggregator },
    TurnRoute.Rebudget => new() { _accountant, _auditor, _aggregator },
    TurnRoute.Reaudit  => new() { _auditor, _aggregator },
    TurnRoute.Clarify  => new() { _aggregator },
    _ => throw new InvalidOperationException($"No agent subset for route {route}")
};
```

`AgentWorkflowBuilder.BuildSequential` does not care that you only handed it three agents instead of five. It wires them up the same way, and the workflow input — the conversation history — is what gives the subset agents enough context to do their work without the earlier stages.

For `Replan`, `Rebudget`, and `Reaudit`, the prior Aggregator output (which lives in `History` as an assistant message) anchors the downstream agents. The Planner sees the existing itinerary in the transcript and treats the new user request as a diff against it.

### Committing only on success

The streaming variant of the turn looks similar to the original single-shot loop, but with two important differences. First, the workflow input is a `List<ChatMessage>` instead of a string:

```csharp
var workflow = AgentWorkflowBuilder.BuildSequential(SelectAgents(route));
var input = new List<ChatMessage>(conv.History.Count + 1);
input.AddRange(conv.History);
input.Add(new ChatMessage(ChatRole.User, newMessage));

StreamingRun run = await InProcessExecution.StreamAsync(workflow, input);
await run.TrySendMessageAsync(new TurnToken(emitEvents: true));
```

Second, the conversation is only mutated after the workflow reaches `WorkflowOutputEvent`:

```csharp
if (agentError != null) yield break;

conv.History.Add(new ChatMessage(ChatRole.User, newMessage));
conv.History.Add(new ChatMessage(ChatRole.Assistant, finalText));
if (route != TurnRoute.Clarify) conv.LatestPlan = finalText;
```

If a user cancels mid-stream, or any agent fails, the conversation state stays exactly as it was before the turn started. The user can retry the same message cleanly. This is the part of the code where it pays to be paranoid — any mutation before the workflow finishes risks corrupting the conversation if something goes wrong half-way through.

### Teaching the Aggregator about its modes

The Aggregator's existing prompt assumes it always receives output from all four prior agents. When you hand it only its own subset (`Clarify` route), or only an Auditor turn (`Reaudit`), that assumption breaks.

The fix is a short addendum to the prompt that asks the Aggregator to inspect what is actually in its input this turn:

```text
### Multi-Turn Mode

You may be invoked across follow-up turns of a conversation. Detect your mode from
the messages available this turn:

Plan-generation mode — the messages include fresh output from one or more of
Researcher, Planner, Accountant, Auditor. Produce the FULL plan document.

Chat-answer mode — no new Researcher/Planner/Accountant/Auditor output exists
this turn; only the user's latest message and the prior conversation. The user is
asking a question about the existing plan. Respond in 1-3 short paragraphs, do NOT
re-emit the full template, and do NOT invent new facts.
```

This is the only prompt change in the whole project. The five agents and their tools are otherwise unchanged. The router controls which of them run; the Aggregator decides how to respond based on what it sees.

### SSE events for a routed turn

The streaming endpoint gets two new SSE event types on top of the existing `init`/`agent-start`/`content`/`agent-complete`/`error`/`complete` vocabulary:

- `route` — fires once, right after the router decides. Carries the route name and the list of agents that will run. The UI uses it to dim the dots for agents that are being skipped.
- `plan-final` — fires when the Aggregator finishes a plan-changing turn. Carries the full plan markdown.

And one more for chat-answer mode:

- `clarified` — fires when the Aggregator finishes a `Clarify` or `OffTopic` turn. The right pane is not touched; the answer goes into the chat bubble.

The server-side dispatcher is a switch on `ProgressStatus`:

```csharp
case ProgressStatus.Routed when progress.Route is { } route:
    await SendSseEvent("route", new RouteEventData {
        Route = route.ToString().ToLowerInvariant(),
        AgentsToRun = TravelPlannerService.AgentNamesFor(route)
            .Select(n => n.ToLowerInvariant()).ToList()
    });
    break;

case ProgressStatus.PlanFinal:
    await SendSseEvent("plan-final", new PlanFinalEventData {
        Plan = progress.PartialOutput ?? string.Empty
    });
    break;

case ProgressStatus.Clarified:
    await SendSseEvent("clarified", new { reply = progress.PartialOutput ?? string.Empty });
    break;
```

The rest of the SSE flow — agent transitions, content tokens, errors — is identical to the single-shot endpoint. Existing clients of `/api/travel/plan/stream` keep working.

End to end, one turn looks like this:

![One conversation turn as a sequence diagram: the client opens the SSE stream, the controller acquires the per-conversation lock (or returns 409 Conflict if busy), loads the Conversation from the store, calls the router, then streams SSE events for each agent in the chosen subset before committing history and releasing the lock](/blog/2026/06/adding-conversations-to-multi-agent-travel-planner/turn-sequence.svg)

### The frontend: chat on the left, plan on the right

The old UI was a single column: input, pipeline, output. For a conversation it needs three regions arranged side by side. CSS Grid handles that cleanly:

```css
.workspace {
    display: grid;
    grid-template-columns: 240px minmax(0, 1fr) minmax(0, 1.4fr);
}
```

The sidebar (`240px`) lists conversations. The chat (`1fr`) holds the messages and composer. The plan pane (`1.4fr`) holds the latest Aggregator output, kept in view while the user types.

Each assistant turn gets a chat bubble with its own mini pipeline — five small dots, one per agent. When the `route` event arrives, the dots for skipped agents go dim. When `agent-start` fires, the active dot pulses. When `agent-complete` fires, it turns green. The full per-agent output is preserved as a collapsible "Agent details" disclosure inside the bubble, so users can still inspect what each agent contributed on any given turn.

The Aggregator's streamed content is piped into the right pane directly, throttled to a 100 ms render cadence so the browser does not thrash:

```javascript
case 'content': {
    turn.agentContent[data.agent] += data.content;
    if (data.agent === 'aggregator') {
        turn.aggregatorBuffer += data.content;
        schedulePlanRender(turn.aggregatorBuffer, { streaming: true });
    }
    return true;
}

case 'plan-final': {
    if (data.plan) renderPlan(data.plan);
    return true;
}
```

The right pane streams as the Aggregator types and snaps to the canonical final markdown on `plan-final`. A `Clarify` turn never sets a new plan; the right pane stays as the previous successful plan, which is exactly what the user wants when asking "what does this mean?"

### Persistence with SQLite

In-memory storage is fine for a demo but not for a conversation surface — the whole point is being able to come back tomorrow. SQLite is the natural next step: one file, no external server, ACID, and good enough concurrency for a single-instance deployment.

The schema is small:

```sql
CREATE TABLE IF NOT EXISTS Conversations (
    Id           TEXT PRIMARY KEY,
    Title        TEXT NULL,
    LatestPlan   TEXT NULL,
    CreatedAt    TEXT NOT NULL,
    LastActivity TEXT NOT NULL
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS Messages (
    Id              INTEGER PRIMARY KEY AUTOINCREMENT,
    ConversationId  TEXT NOT NULL,
    Role            TEXT NOT NULL,
    Content         TEXT NOT NULL,
    Position        INTEGER NOT NULL,
    CreatedAt       TEXT NOT NULL,
    FOREIGN KEY (ConversationId) REFERENCES Conversations(Id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS IX_Messages_Conv_Position
    ON Messages(ConversationId, Position);
```

`WITHOUT ROWID` on the parent table is appropriate because the primary key is a 32-char hex GUID — a real string key, not an alias for an integer rowid. The `Position` column on `Messages` preserves the conversation order independent of insertion id.

![SQLite entity-relationship diagram showing the Conversations parent table with Id primary key, Title, LatestPlan, CreatedAt, LastActivity, and a one-to-many relationship to the Messages child table which holds Id, ConversationId foreign key, Role, Content, Position, and CreatedAt](/blog/2026/06/adding-conversations-to-multi-agent-travel-planner/sqlite-schema.svg)

Two pragmas worth setting once: `journal_mode=WAL` for reader-during-writer concurrency, and `foreign_keys=ON` per connection (it is off by default in SQLite for backwards compatibility).

The store uses [Dapper](https://github.com/DapperLib/Dapper) for the data access. Raw `SqliteCommand` works fine but is verbose; Dapper trims about 80 lines of boilerplate and parameterizes for you:

```csharp
public async Task<Conversation?> GetAsync(string id, CancellationToken cancellationToken = default)
{
    await using var conn = new SqliteConnection(_connectionString);
    await conn.OpenAsync(cancellationToken);

    var row = await conn.QuerySingleOrDefaultAsync<ConvRow>(new CommandDefinition(
        "SELECT Id, Title, LatestPlan, CreatedAt, LastActivity FROM Conversations WHERE Id = @Id",
        new { Id = id },
        cancellationToken: cancellationToken));
    if (row == null) return null;

    var msgRows = await conn.QueryAsync<MsgRow>(new CommandDefinition(
        "SELECT Role, Content FROM Messages WHERE ConversationId = @Id ORDER BY Position",
        new { Id = id },
        cancellationToken: cancellationToken));

    // ... map to Conversation ...
}
```

`UpdateAsync` runs inside a transaction and uses replace-all semantics for messages — delete the existing rows for the conversation, insert the current `History` in order. With chat-sized histories (dozens of messages, not thousands) this is fine, and it avoids a class of edge-case bugs that come from trying to diff tail-appends.

UTC `DateTime` round-trips are explicit — store as ISO 8601 (`"o"` format), parse back with `DateTimeStyles.RoundtripKind`, and `SpecifyKind(..., Utc)` after parsing. SQLite has no native datetime type and Microsoft.Data.Sqlite returns `Kind=Unspecified` by default, which silently breaks `DateTime.UtcNow` comparisons elsewhere if you do not handle it.

The backend is config-driven, so the in-memory implementation is still available as an opt-out:

```csharp
var backend = builder.Configuration["Conversations:Backend"] ?? "Sqlite";
if (string.Equals(backend, "InMemory", StringComparison.OrdinalIgnoreCase))
{
    builder.Services.AddSingleton<IConversationStore, InMemoryConversationStore>();
}
else
{
    var connectionString = builder.Configuration.GetConnectionString("Conversations")
        ?? "Data Source=conversations.db";
    builder.Services.AddSingleton<IConversationStore>(
        _ => new SqliteConversationStore(connectionString));
}
```

For Docker, the connection string points at a volume-mounted directory so the database survives container rebuilds:

```yaml
environment:
  - ConnectionStrings__Conversations=Data Source=/app/data/conversations.db
volumes:
  - app-data:/app/data
```

### Locking a conversation during a turn

With persistence comes a question the in-memory version could ignore: what if a second client tries to send a message while the first turn is still running? Two parallel turns mutating the same `History` would interleave messages in unpredictable orders and could double-write the `LatestPlan`.

The fix is a per-conversation async lock. A `ConcurrentDictionary<string, SemaphoreSlim>` keyed by conversation id gives each conversation its own mutex, lazily created the first time it is needed:

```csharp
public async Task<IAsyncDisposable> AcquireAsync(string conversationId, CancellationToken ct = default)
{
    var sem = _locks.GetOrAdd(conversationId, _ => new SemaphoreSlim(1, 1));
    var acquired = await sem.WaitAsync(0, ct).ConfigureAwait(false);
    if (!acquired) throw new ConversationBusyException(conversationId);
    return new Releaser(sem);
}
```

`WaitAsync(0)` is the important choice. It returns immediately with `false` if the semaphore is held, instead of queuing. That gives us fail-fast semantics: when the second request loses the race, the controller catches `ConversationBusyException` and returns HTTP 409 Conflict. The first turn keeps streaming undisturbed; the second client sees a clear error and can retry once the first one is done.

The controller integration is short:

```csharp
IAsyncDisposable lockHandle;
try
{
    lockHandle = await _locks.AcquireAsync(id, cancellationToken);
}
catch (ConversationBusyException)
{
    return Conflict(new { error = "Conversation is currently processing another message." });
}

await using (lockHandle)
{
    // ... load, run turn, update store ...
}
```

For the SSE endpoint, the same logic runs before any SSE preamble is written. If the lock cannot be acquired, the response is plain `409 Conflict` with a JSON body — the client's `fetch` sees a normal HTTP error, not a malformed event stream.

The lock service is in-process. If you ever need to scale beyond a single instance, swap the implementation for a Redis-backed distributed lock and keep the interface as is. Multi-instance SQLite is the bigger problem at that point anyway.

### Testing the store

The store tests run against a real SQLite file, not `:memory:`, because the store opens fresh connections per call and `:memory:` is scoped to a single connection. Each test gets a temp file via `IAsyncLifetime`:

```csharp
public Task InitializeAsync()
{
    _dbPath = Path.Combine(Path.GetTempPath(), $"convstore-test-{Guid.NewGuid():n}.db");
    _connectionString = $"Data Source={_dbPath}";
    return Task.CompletedTask;
}

public Task DisposeAsync()
{
    SqliteConnection.ClearAllPools();
    foreach (var ext in new[] { "", "-wal", "-shm" })
    {
        var path = _dbPath + ext;
        if (File.Exists(path)) try { File.Delete(path); } catch { }
    }
    return Task.CompletedTask;
}
```

`SqliteConnection.ClearAllPools()` is the easy-to-miss detail. Microsoft.Data.Sqlite pools connections, and on Windows the pool holds a file handle open even after every `await using` block. Without clearing the pool before the file delete, the cleanup throws an access-denied error and you leak temp files.

The most useful test in the set is the one that verifies persistence across instances — two separate `SqliteConversationStore` objects pointing at the same file, with a conversation created in the first and loaded from the second:

```csharp
[Fact]
public async Task Persistence_survives_store_re_instantiation()
{
    var first = new SqliteConversationStore(_connectionString);
    var conv = await first.CreateAsync();
    conv.Title = "persistent";
    conv.History.Add(new ChatMessage(ChatRole.User, "hello"));
    conv.History.Add(new ChatMessage(ChatRole.Assistant, "world"));
    conv.LatestPlan = "plan body";
    await first.UpdateAsync(conv);

    var second = new SqliteConversationStore(_connectionString);
    var loaded = await second.GetAsync(conv.Id);

    loaded!.Title.Should().Be("persistent");
    loaded.History.Should().HaveCount(2);
    loaded.LatestPlan.Should().Be("plan body");
}
```

That is the test that backs the whole "users can come back tomorrow" claim. If it ever fails, the persistence story is broken regardless of how many other tests pass.

### Key takeaways

The pieces here are not exotic individually. A short LLM classifier, a `List<ChatMessage>` workflow input, an idempotent SQLite schema, a `SemaphoreSlim` keyed by an id — none of it is novel. The interesting part is how they compose to turn a one-shot pipeline into something that feels like a real assistant.

- A router-driven subset workflow is a much better cost story than re-running everything on every follow-up
- Manage conversation history at the service layer when your unit of state is the conversation, not any single agent's thread
- Commit conversation mutations only after the workflow reaches `WorkflowOutputEvent`, so cancellations and errors leave state intact
- One Aggregator that detects its own mode is simpler than two separate agents for "plan" and "chat answer"
- SQLite with WAL mode is the right default for single-instance persistence; the abstraction over `IConversationStore` keeps the migration path open
- Fail fast on concurrent turns with HTTP 409 — queuing invisibly is worse for users than rejecting cleanly
- `SqliteConnection.ClearAllPools()` before deleting test database files on Windows, or you will leak temp files

What did not change matters too: the five agents, their tools, the provider abstraction, the SSE event names. Adding conversation did not require redesigning the pipeline — it required wrapping it in the right state machine and giving the right layer ownership of the history.

The source code is on [GitHub](https://github.com/bimalghartimagar/LocalAgentTravelPlanner).
