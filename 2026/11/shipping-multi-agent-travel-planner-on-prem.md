---
author: "Bimal Gharti Magar"
title: "Shipping a Multi-Agent Travel Planner On-Prem"
description: Packaging a five-agent .NET workflow as a Docker Compose stack an ops team can run on their own hardware — multi-stage image, nginx in front, SQLite with a Litestream backup sidecar, OpenTelemetry traces, Prometheus metrics with a starter Grafana dashboard, two health endpoints, SSE keep-alive with resumable turns, a plan-diff view, and a structured error taxonomy.
featured:
  image_url: /blog/2026/11/shipping-multi-agent-travel-planner-on-prem/cover.webp
date: 2026-11-26
github_issue_number:
tags:
- dotnet
- csharp
- docker
- devops
- artificial-intelligence
- programming
---

The [previous post](/blog/2026/10/human-in-the-loop-multi-agent-travel-planner/) wired a human-in-the-loop approval gate into the multi-agent travel planner and talked about the weak-model hardening that made it safe to run on cheap providers. What was still missing was the piece between "works on my laptop" and "an operator can install this on their own hardware without asking me questions."

This post is that piece. The target is an on-prem Docker Compose stack — the kind of thing you hand to an internal ops team along with a one-page README. Nothing cloud-vendor-specific, no Kubernetes, no managed Postgres. SQLite on a volume, nginx in front, Litestream for backup, OpenTelemetry traces and Prometheus metrics, two health endpoints, structured errors with stable codes.

Two more things landed alongside the deploy work because they matter at the same "handing it off to someone else" boundary: turns that survive a tab reload, and a plan-diff view so follow-up edits read as deltas instead of regenerated prose.

The source code is on [GitHub](https://github.com/bimalghartimagar/LocalAgentTravelPlanner).

### What we will cover

- A multi-stage `Dockerfile` with a non-root runtime user and a writable `/app/data` directory for the SQLite file
- A `docker-compose.yml` wiring the app, nginx, and an optional Litestream sidecar, plus the nginx config that turns SSE buffering off
- `/health/live` and `/health/ready` — a cheap heartbeat for Docker and a deeper probe for load balancers
- OpenTelemetry traces so one slow turn is a timeline, not a mystery
- Prometheus metrics on `/metrics` plus a starter Grafana dashboard so the oncall has rate / p95 / cost graphs, not just traces
- SSE keep-alive frames so a 40-second Auditor pass does not get torn down by nginx or a corporate proxy
- Resumable turns so a tab reload or a dropped Wi-Fi reattaches to the same running pipeline with a `turnId` + `lastEventId` resume
- A line + inline-word plan diff so follow-up turns show the delta, not the whole regenerated plan
- A structured error taxonomy with stable codes that lets the frontend branch on intent
- A GitHub Actions pipeline that builds, tests, and (on tags) pushes an image to GHCR
- The "what's in the box vs what's the operator's" boundary — what the repo ships and what every site answers for itself

### The container image: small, non-root, writable where it needs to be

The runtime image is a plain multi-stage `aspnet` build. Nothing clever — the clever part is making sure the non-root user owns the directories the app writes to:

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0-preview AS build
WORKDIR /src
COPY LocalAgentTravelPlanner.sln .
COPY LocalAgentTravelPlanner.csproj .
COPY Api/LocalAgentTravelPlanner.Api.csproj Api/
COPY Tests/LocalAgentTravelPlanner.Tests.csproj Tests/
RUN dotnet restore LocalAgentTravelPlanner.sln
COPY . .
RUN dotnet publish Api/LocalAgentTravelPlanner.Api.csproj \
    -c Release -o /app --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:10.0-preview AS runtime
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser
RUN mkdir -p /app/logs /app/data && chown -R appuser:appuser /app/logs /app/data
COPY --from=build --chown=appuser:appuser /app .
USER appuser
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
ENTRYPOINT ["dotnet", "LocalAgentTravelPlanner.Api.dll"]
```

Two details that bit me the first time around. SQLite needs to open the DB file *and* create a WAL + shared-memory file next to it, which means the whole directory has to be writable, not just the DB file. If you only chown the file, the first write fails with a cryptic `SQLITE_CANTOPEN`. Make the directory itself owned by `appuser`.

The `apt-get install curl` step is the other one. The `aspnet:10.0-preview` base image does not ship `curl`, and the compose health check below shells out to it. Without this line the container boots fine but never reports healthy, and nginx's `depends_on: service_healthy` holds the whole stack behind a container stuck at `starting`. It costs about 2 MB. The alternative is a container-native probe operators would have to learn; curl is the one they already know.

The `.csproj` files are copied before the rest of the source so `dotnet restore` lives on its own cached layer. On a cold build that saves nothing, but on every subsequent iteration the restore layer stays warm as long as package references do not change.

### Compose: app, nginx, and an opt-in backup sidecar

The compose file is where the deployment shape becomes explicit — one app, one reverse proxy, named volumes for logs and the SQLite data, and a Litestream sidecar guarded by a profile so it only runs when the operator opts in:

![Compose topology — nginx in front of the app on the default profile, Litestream sidecar on an opt-in backup profile replicating the SQLite volume](/blog/2026/11/shipping-multi-agent-travel-planner-on-prem/compose-topology.svg)


```yaml
services:
  app:
    build: .
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ApiKey=${API_KEY:?Set API_KEY in .env or environment}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
      - OPEN_ROUTER_AI_KEY=${OPEN_ROUTER_AI_KEY:-}
      - OTEL_EXPORTER_OTLP_ENDPOINT=${OTEL_EXPORTER_OTLP_ENDPOINT:-}
      - ConnectionStrings__Conversations=Data Source=/app/data/conversations.db
    volumes:
      - app-logs:/app/logs
      - app-data:/app/data
    expose: ["8080"]
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health/live"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

  litestream:
    image: litestream/litestream:0.3
    profiles: ["backup"]
    depends_on: [app]
    environment:
      - LITESTREAM_REPLICA_URL=${LITESTREAM_REPLICA_URL:-}
      - LITESTREAM_ACCESS_KEY_ID=${LITESTREAM_ACCESS_KEY_ID:-}
      - LITESTREAM_SECRET_ACCESS_KEY=${LITESTREAM_SECRET_ACCESS_KEY:-}
    volumes:
      - app-data:/data
      - ./litestream.yml:/etc/litestream.yml:ro
    command: replicate
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports: ["80:80"]
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      app:
        condition: service_healthy

volumes:
  app-logs:
  app-data:
```

The `${API_KEY:?...}` syntax turns a missing value into a boot-time error with a readable message. Operators who forget to copy `.env.example` to `.env` get a clear complaint instead of a running app with blank authentication, which is the only failure mode worth optimizing for.

`depends_on.condition: service_healthy` means nginx will not start accepting traffic until the app's `/health/live` has gone green. On a cold boot that is a few seconds of difference, but the few seconds matter — otherwise nginx returns 502 to anyone who refreshes during startup.

The backup profile is important for a reason that is not obvious. If an operator does not want remote backups (air-gapped install, offline demo, local dev), they should not have to run and silence a sidecar that is trying and failing to reach `s3://`. `profiles: ["backup"]` means `docker compose up` runs app + nginx only; `docker compose --profile backup up` adds Litestream. Default is the safe case.

One subtlety: `LITESTREAM_REPLICA_URL` uses the `:-` empty-default form, not the `:?` required-or-fail form I reached for first. Compose interpolates every service's environment at parse time, *before* it filters by profile — so `:?` on a profile-only service aborts plain `docker compose up` with "required variable ... is missing" even though Litestream was never going to start. With `:-`, the default profile ignores the variable entirely, and Litestream itself refuses to start with an empty URL once the `backup` profile is on. Same guard, right place.

### nginx: SSE buffering off is the whole trick

The nginx config is otherwise unremarkable — security headers, a rate limit zone, upstream pointing at `app:8080`. The one block that matters for a streaming API is this:

```nginx
location = /api/travel/plan/stream {
    limit_req zone=api burst=5 nodelay;
    proxy_pass http://app;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    # SSE: disable buffering, long timeouts
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 300s;
    proxy_send_timeout 300s;
    chunked_transfer_encoding off;
}
```

With default `proxy_buffering on`, nginx holds bytes until it has a full buffer or the backend closes the connection. Fine for a REST API. For SSE, it means tokens that the server flushed one at a time arrive at the browser in a single chunk after the stream ends — the live-typing effect disappears. `proxy_buffering off` is a per-location setting on purpose: you want it off on the streaming routes, on for everything else where buffering actually helps.

The 300-second read/send timeouts work alongside the SSE keep-alive the app sends on the conversation streams (covered below). Either one by itself prevents a tear-down by nginx; together they also survive a corporate proxy with a stricter idle policy. The one-shot `/api/travel/plan/stream` route above predates the keep-alive pump, so it relies on the timeout alone — fine behind this nginx, fragile behind anything stricter.

The two conversation SSE routes get the same treatment with regex `location` blocks: `/api/conversations/{id}/messages/stream` for a normal turn and `/api/conversations/{id}/decision/stream` for the HITL approve/reject phase. All three streaming routes get the same `limit_req` burst because the realistic concurrency per IP on this app is "one browser tab," not "load test."

### SQLite on a volume, Litestream for anything bigger than that

SQLite is the backend because the data shape — small, write-light, single-tenant per conversation — does not justify Postgres. One file, journal_mode=WAL, foreign keys on, no DBA required. The whole state is a few MB until a site has thousands of conversations.

But a single file is a single point of failure if nobody is backing it up. The compose file ships a `litestream` sidecar on the `backup` profile, with a minimal `litestream.yml`:

```yaml
dbs:
  - path: /data/conversations.db
    replicas:
      - url: ${LITESTREAM_REPLICA_URL}
        snapshot-interval: 6h
        retention: 72h
        sync-interval: 10s
```

Three numbers that are worth tuning per site. `sync-interval: 10s` sets the recovery point objective — if the host loses power right now, up to 10 seconds of writes are gone. On an S3 target that is a PUT request every 10 seconds; on a self-hosted MinIO or an SFTP destination that is free. Tighten to 1s if the workload justifies it, loosen if hosting bandwidth is expensive.

`snapshot-interval: 6h` controls how much WAL has to be replayed on restore — six hours of chatty writes replay in seconds; a week's worth replays in minutes. `retention: 72h` is a weekend-outage buffer: three days of snapshots is enough that a human can notice the alert, log in, and restore without rushing.

Recovery is one command, run through the sidecar so the restored DB lands on the shared `app-data` volume at the path the sidecar sees (`/data`), which the app sees at `/app/data`:

```bash
docker compose run --rm litestream restore \
    -o /data/conversations.db "$LITESTREAM_REPLICA_URL"
```

Point it at the same `LITESTREAM_REPLICA_URL` the sidecar is pushing to, and it rebuilds the DB file from the most recent snapshot + WAL. On an air-gapped site, the same mechanism works against `file:///mnt/backup/travel-planner` — Litestream treats a mounted filesystem the same as S3.

### API key: env var in dev, mounted secret in prod

The API key middleware reads from `IConfiguration`, which means it will accept the key from any provider ASP.NET Core knows about — appsettings, env vars, Azure Key Vault, Docker secrets. In Compose, the convenient path is a mounted file:

```yaml
services:
  app:
    environment:
      - ApiKeyFile=/run/secrets/api-key
    secrets:
      - api-key

secrets:
  api-key:
    file: ./secrets/api-key.txt
```

And on the app side, `ApiKeyMiddleware` resolves the key in order — `IConfiguration["ApiKey"]` first (which already covers appsettings, env vars, and user secrets), then `IConfiguration["ApiKeyFile"]` as the Docker-secrets path. The point is operational: an env var shows up in `docker inspect`, process-table listings, and anywhere the environment leaks. A file secret can be mode `0400` and bind-mounted read-only. The key is loaded once at middleware construction and cached, so rotating a mounted secret still needs a container restart — swap the secret, restart the service, no code change.

For a single-tenant on-prem deploy the difference is small. For a shared ops host where multiple apps run under docker, where somebody might run `docker inspect` as a diagnostic step and paste the output into a ticket, env-var secrets are a quietly bad default. Shipping both options and documenting the trade-off is the simplest way to let operators make the right call.

### Two health endpoints, not one

The existing `/api/travel/health` is a per-provider diagnostic report, not a liveness signal, and it sits under `/api/*` where the API key middleware has to whitelist it. Rather than retrofit it and break anyone already scraping it, I added two dedicated endpoints at the root:

```csharp
app.MapGet("/health/live", () => Results.Ok(new
{
    status = "live",
    timestamp = DateTime.UtcNow
}));

app.MapGet("/health/ready", async (IConversationStore store, CancellationToken ct) =>
{
    var checks = new Dictionary<string, object>();
    var allOk = true;

    try
    {
        var probe = await store.CreateAsync(ct);
        await store.DeleteAsync(probe.Id, ct);
        checks["db"] = "ok";
    }
    catch (Exception ex)
    {
        checks["db"] = new { status = "failing", error = ex.Message };
        allOk = false;
    }

    // ...same pattern for "at least one LLM provider configured"

    var payload = new { status = allOk ? "ready" : "degraded", checks };
    return allOk ? Results.Ok(payload) : Results.Json(payload, statusCode: 503);
});
```

`/health/live` is a heartbeat — the process is up, that is all. Docker's HEALTHCHECK hits it every 30 seconds without touching the database. `/health/ready` is the real probe — it creates and deletes a throwaway conversation to verify the SQLite file is writable, checks that at least one LLM provider credential is configured, and returns 503 if either check fails. That is what a load balancer should use to decide whether this instance should receive traffic.

Both new endpoints live at the root, so `ApiKeyMiddleware` (which only intercepts `/api/*`) skips them naturally. `/api/travel/health` stays as the per-provider diagnostic view.

### OpenTelemetry so you can see what happened

Serilog with a rolling daily file was already logging the important structured fields (`ConversationId`, `Route`, `DurationMs`, token counts). What was missing was traces — the ability to look at one specific turn and see the timing waterfall across router, per-agent LLM calls, tool invocations, and the final Aggregator commit.

That is what OpenTelemetry gives you, and the wiring is short:

```csharp
public static class Diagnostics
{
    public const string ActivitySourceName = "LocalAgentTravelPlanner";
    public static readonly ActivitySource ActivitySource = new(ActivitySourceName, "1.0.0");
}

// Program.cs
builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService(serviceName, serviceVersion: "1.0.0"))
    .WithTracing(t =>
    {
        t.AddSource(Diagnostics.ActivitySourceName)
         .AddAspNetCoreInstrumentation(opts =>
         {
             opts.Filter = ctx =>
                 !ctx.Request.Path.StartsWithSegments("/health") &&
                 !ctx.Request.Path.StartsWithSegments("/api/travel/health") &&
                 !ctx.Request.Path.StartsWithSegments("/metrics");
         })
         .AddHttpClientInstrumentation();

        if (!string.IsNullOrWhiteSpace(otlpEndpoint))
            t.AddOtlpExporter(opt => opt.Endpoint = new Uri(otlpEndpoint));
    });
```

`ContinueConversationStreamingAsync` and `RunAggregatorPhaseAsync` each open an activity with tags for the conversation id, route, provider, model, and — for the aggregator phase — upstream duration. The AspNetCore instrumentation adds a span per HTTP request, and HttpClient instrumentation covers outbound calls to LLM providers and the tool APIs.

The filter matters more than it looks. Docker's health check fires every 30 seconds and Prometheus scrapes `/metrics` every 15; without the filter, one real turn is buried under a hundred uptime pings in the trace view.

OTLP export is opt-in via `OTEL_EXPORTER_OTLP_ENDPOINT`. When it is unset (dev mode), spans stay in-process and cost nothing. When it is set, the app ships spans to whichever OTLP receiver the operator points at — a Grafana Tempo container next to the app, a Jaeger all-in-one image, an OpenTelemetry Collector fanning out to multiple backends. Nothing app-side changes when the receiver does.

### Prometheus metrics: graphs the oncall actually looks at

Traces answer *why was this one turn slow*. Metrics answer *is anything getting slower, and is the error rate drifting up*. Different question, different tool. Operators want both.

The wiring is `prometheus-net.AspNetCore` and a thin `IMetricsRecorder` abstraction so the core project does not take a direct dependency on the Prometheus client library:

```csharp
public interface IMetricsRecorder
{
    void TurnCompleted(string route, string provider, string outcome,
                       double durationSeconds, long? inputTokens, long? outputTokens);
}
```

The core ships a `NoOpMetricsRecorder` so unit tests and the console app stay zero-overhead. The Api project binds the interface to `PrometheusMetricsRecorder`, which maintains three series:

- `conversation_turns_total{route,provider,outcome}` — counter. Rate panels, error-rate alert.
- `conversation_turn_duration_seconds{route,provider}` — histogram. p50/p95/p99 panels, slow-turn alert. Buckets are tuned to the observed distribution (Clarify ~2-5s, Replan ~15-25s, Full ~30-60s) instead of the Prometheus defaults, which bottom out at 10s and smear everything together.
- `conversation_tokens_total{provider,kind}` — counter. Cost-per-turn and burn-rate panels. `kind` is `input` or `output` so dashboards can apply per-direction price multipliers.

`TravelPlannerService.LogTurnCompleted` was already the single emit point for completed turns; the recorder call piggybacks on it so there is no second place to keep in sync. Router tokens roll into the per-turn total since operators want cost-per-turn, not router-vs-agent split.

Scraping is `/metrics` at the root (not under `/api/*`, so the API-key middleware ignores it) with the standard `app.MapMetrics("/metrics")`. nginx passes it through without rate limiting. `app.UseHttpMetrics(opts => opts.ReduceStatusCodeCardinality())` layers the free HTTP series (`http_requests_received_total`, `http_request_duration_seconds`, `http_requests_in_progress`) on top.

The repo ships a starter Grafana dashboard at `ops/grafana-dashboard.json` — turns-per-second by route, error rate, duration quantiles, tokens-per-minute by provider, HTTP p95 by action. Starting point, not a final answer: operators should layer in alerts and tune panels for their own SLOs. The dashboard references a datasource variable `${DS_PROMETHEUS}` so a drop-in Prometheus (whatever port the operator picked) works without editing the JSON.

### SSE keep-alive so nginx does not tear down long streams

A full pipeline turn on a slower model can spend 40 seconds in Auditor without producing a single output event. That is uncomfortably close to nginx's default `proxy_read_timeout` of 60s, and any corporate proxy with a stricter idle policy will cut the connection sooner.

The SSE spec has a built-in solution: comment frames. A line starting with `:` is ignored by every client, but it counts as bytes on the wire, and that is enough to keep TCP intermediaries happy. So on the conversation stream routes (normal turns, HITL decisions, and resume), a background pump writes `: keep-alive\n\n` every 15 seconds while the main event loop is quiet:

```csharp
private async Task KeepAlivePumpAsync(CancellationToken ct)
{
    try
    {
        using var timer = new PeriodicTimer(KeepAliveInterval);
        while (await timer.WaitForNextTickAsync(ct))
        {
            await _writeLock.WaitAsync(ct);
            try
            {
                // Comment frame per SSE spec: lines starting with `:` are ignored by clients.
                await Response.WriteAsync(": keep-alive\n\n", ct);
                await Response.Body.FlushAsync(ct);
            }
            catch (ObjectDisposedException) { break; }
            catch (InvalidOperationException) { break; }
            finally { _writeLock.Release(); }
        }
    }
    catch (OperationCanceledException) { /* normal shutdown */ }
}
```

Two things I nearly got wrong. `HttpResponse.Body` is not thread-safe, so the pump and the main stream have to share a `SemaphoreSlim` — writing SSE frames from two tasks without serializing produces garbled output. And the pump has to be linked to the request cancellation token (via `CancellationTokenSource.CreateLinkedTokenSource` in the wrapping `RunWithKeepAliveAsync`) so it dies cleanly when the client disconnects. The inner `catch (ObjectDisposedException)` / `catch (InvalidOperationException)` handle the race where the main stream has already closed `Response.Body` by the time the pump tries its next flush; the outer `catch (OperationCanceledException)` is normal cancellation.

### Resumable turns: pipelines that survive a reload

Keep-alive handles the proxy. The other failure mode is the human — a user reloads the tab 30 seconds into a 60-second Auditor pass, or Wi-Fi flickers, or they close the laptop. With the pipeline tied to the HTTP request, that cancels the whole turn mid-flight and the next page load shows an empty right pane.

![Resume sequence — a client disconnect leaves the broker-owned pipeline running, a reconnect with ?turnId and lastEventId replays buffered events then yields live frames](/blog/2026/11/shipping-multi-agent-travel-planner-on-prem/resume-sequence.svg)


The fix is a `TurnBroker` that owns pipeline lifetime instead of the controller. Each turn gets a bounded ring buffer of events with a monotonic id, kept for 90 seconds past completion. The controller asks the broker to start a turn (handing over the `IConversationLock` so the lock belongs to the pipeline, not the request), then becomes a subscriber. The runner writes events into the buffer; subscribers fan them out to their own `Response.Body`. Dropping a subscriber unwinds only the HTTP write — the pipeline keeps going.

Resume is the same endpoint with two extra query params:

```
GET /api/conversations/{id}/messages/stream?turnId=<id>&lastEventId=<n>
```

The server looks the turn up in the broker (active or still inside the retention window), replays every buffered event with `Id > lastEventId`, then yields live events until the pipeline completes. The `init` event carries the server-assigned `turnId`; the client stashes it with `lastEventId` in `sessionStorage`, and on page load pairs them into the resume URL and reattaches without re-dispatching anything.

Three design calls worth naming:

- **Monotonic ids per turn, not global.** Each `(conversationId, turnId)` has its own id space, so ids stay small integers and gap detection on the client is one comparison: `got > prev + 1` means the buffer evicted frames the client never saw, and the UI should reload rather than guess.
- **Lock stays with the pipeline, not the request.** A new POST or stream request on the same conversation sees the broker's active entry and 409s. That is the correct answer: the committed conversation state is still being written.
- **Explicit cancel endpoint.** `DELETE /api/conversations/{id}/active-turn` signals the broker's per-turn CTS. The Cancel button in the UI fires that first, *then* aborts the fetch. The old behavior (abort alone) silently left the pipeline running under the broker.

A 410 Gone with `conversation.turn_not_resumable` is the client's cue that it has fallen past the retention window — reload to see the committed state.

### Plan diff view: delta over regenerated prose

Resumable turns fix what happens *during* a turn. The plan diff fixes what the user sees *after* one. Subset routes (`Replan`, `Rebudget`, `Reaudit`) regenerate the whole plan markdown even when the actual change is one line, and re-rendering the full plan every turn hides that edit under a wall of unchanged text.

`PlanDiffService` runs `DiffPlex` line-level over the plan at turn start vs the plan at Aggregator finish, then a second word-level pass inside any line pair that looks like a rewrite (same markdown prefix like `- ` or `### `, or >30% token overlap). The result ships inside the `plan-final` SSE event so the client gets both the current plan and the delta in one frame — no follow-up round-trip. Three result kinds steer the UI: `no_previous_plan` for the first plan-changing turn, `no_change` for a Reaudit that approved as-is, `changed` for everything else.

The right pane got a `Full | Diff` toggle. It auto-switches to Diff on `Replan`/`Rebudget`/`Reaudit` since the delta is the point of those turns, and to Full on `Full` and first-plan turns. A separate endpoint — `GET /api/conversations/{id}/turns/{turnIndex}/diff` — rebuilds a historical diff by walking turns forward and tracking plan state, treating `Clarify` and `OffTopic` turns as no-ops on the plan.

### Structured errors with stable codes

Every controller was returning free-form `{ error: "..." }` bodies. Fine for a demo, painful once you want a client to branch on intent. The compromise was to keep the `error` string for backwards compatibility but add a stable `code` field and an optional `extras` bag:

```csharp
public sealed class ApiError
{
    public required string Error { get; init; }
    public required string Code { get; init; }
    public IReadOnlyDictionary<string, object?>? Extras { get; init; }
}

public static class ErrorCodes
{
    public const string ConversationBusy       = "conversation.busy";
    public const string PendingDecisionOpen    = "conversation.pending_decision_open";
    public const string ProviderNotConfigured  = "provider.not_configured";
    public const string RateLimited            = "rate.limited";
    // ...15 codes total
}
```

The frontend gained a `handleApiErrorResponse` that dispatches on `code` instead of HTTP status. When the server returns `conversation.pending_decision_open`, the client pulls the pending decision out of `extras` and hydrates the approval UI without a follow-up round-trip. It is the same code path that runs on page refresh.

One place to check when doing this: middleware that short-circuits before MVC. `ApiKeyMiddleware`'s 401 was still writing a free-form body, so the frontend's `auth.api_key_missing` branch (the one that prompts for a key) never fired on a real 401. Serializing the same `ApiError` shape with `JsonSerializerDefaults.Web` there closed the loop.

Deliberately not RFC 7807 ProblemDetails. The shape overlaps enough that a migration later is trivial (`type`, `title`, `status` as aliases), and shipping ProblemDetails mid-cycle would have broken every frontend fetch handler that reads `data.error`.

### CI: build, test, and (on tag) push an image

The GitHub Actions pipeline runs on every push to `main` and every PR. The build-test job is the usual restore/build/test triplet with the evaluation category skipped (those tests need a live LLM provider and would make PR builds flaky and expensive):

```yaml
- name: Test (skip Evaluation category — requires live LLM)
  run: >
    dotnet test Tests/LocalAgentTravelPlanner.Tests.csproj
    --configuration Release --no-build --verbosity normal
    --filter "Category!=Evaluation"
```

The image job is gated on `github.event_name == 'push' && (github.ref_type == 'tag' || github.ref == 'refs/heads/main')`. PRs get build + test only — no image. `main` pushes get an image tagged `main` + a `sha-` tag. Semver tags (`v1.2.3`) get `1.2.3`, `1.2`, and `sha-` tags via `docker/metadata-action`. That is enough for an operator to pin to a specific release, pin to a minor, or chase `main` for development.

The registry is GHCR because it is free, works out of the box with `GITHUB_TOKEN`, and is a trivial repoint for an operator who wants Harbor or a self-hosted GitLab registry instead — change the `images:` line in the metadata step and the `registry:` in the login step. For an air-gapped install, strip the image job entirely and distribute a `docker save` tarball out of band.

Build cache is `type=gha` — on a reasonably warm cache, the image job completes in under 90 seconds. Cold builds take about three minutes, dominated by `dotnet restore`.

### What's in the box, what's the operator's

The last thing worth being explicit about is the deployment boundary. The repo ships:

- A multi-stage `Dockerfile` (SDK → aspnet runtime, non-root user, port 8080)
- A `docker-compose.yml` with the app, nginx, named volumes for logs and the SQLite data file, health check pointing at `/health/live`, and an opt-in Litestream sidecar
- `nginx/nginx.conf` with security headers, SSE buffering off on the streaming routes, per-IP rate limiting
- `litestream.yml` with sync/retention tuned for a low-write, sub-MB database
- `.env.example` listing every environment variable the app reads
- `ops/grafana-dashboard.json` as a drop-in starting point for the metrics UI
- A CI workflow that builds, tests, and (on tag) pushes to GHCR

An operator gets from cloned repo to running instance with:

```bash
cp .env.example .env      # fill in API_KEY plus at least one provider key
docker compose build
docker compose up -d      # add --profile backup once LITESTREAM_REPLICA_URL is set
```

Everything else is intentionally left to the operator. TLS termination — nginx is configured as a plain HTTP upstream; put Let's Encrypt, an internal CA cert, or an upstream corporate load balancer in front. Image registry — the CI pushes to GHCR but repointing at Harbor or GitLab is a two-line change. Backup target — Litestream speaks S3, GCS, Azure Blob, SFTP, and plain filesystem; the choice is a URL in `.env`. Secrets — `.env` for dev, `ApiKeyFile` + Docker secrets or a secrets manager for anything shared.

The point of the split is that the app should not have opinions about things the operator already has opinions about. Different sites have different backup targets, different TLS chains, different registries. The app's job is to be a good citizen inside whichever answer they picked.

Looking back across the four posts, the five agents are recognizably the same ones from [Part 1](/blog/2026/05/building-multi-agent-travel-planner-dotnet/). What changed was everything around them: [conversations](/blog/2026/07/adding-conversations-to-multi-agent-travel-planner/) that persist and route, a [human approval gate](/blog/2026/10/human-in-the-loop-multi-agent-travel-planner/) before the plan is finalized, and now a stack someone else can boot, back up, watch, and recover without me in the room.

Shipping turned out to be less about one big production feature and more about removing the places where an operator would have to guess. Where does state live? What happens when the browser disappears mid-turn? Which endpoint should Docker hit? Once those questions have boring answers, the multi-agent part stops feeling like a demo and starts feeling like software someone else can own.

### Key takeaways

- Non-root containers with a writable data directory are not glamorous but they are the thing a security review will fail you on. The chown has to cover the directory, not just the file, or SQLite's WAL will not open.
- `profiles` in Compose turn optional sidecars (backup, metrics, observability) into opt-in services instead of silently failing dependencies. Default is the safe case.
- `/health/live` and `/health/ready` do different jobs. Point Docker at the first, point load balancers and smoke tests at the second.
- Long-lived SSE needs two things to survive proxies: `proxy_buffering off` on the route and keep-alive comment frames from the app. Either alone is fragile; both together are solid.
- A pipeline that owns its own lifetime, detached from the HTTP request, is what turns "survives a flaky proxy" into "survives a tab reload." Monotonic event ids, a bounded ring buffer, and `Last-Event-Id`-style resume give you reconnection with zero re-dispatch. The lock follows the pipeline, not the request.
- OpenTelemetry costs almost nothing when `OTEL_EXPORTER_OTLP_ENDPOINT` is unset and gives you a per-turn timeline the moment an operator points it at Tempo or Jaeger. Ship the wiring, let the operator decide whether to light it up.
- Traces answer "why was this slow", metrics answer "is it getting slower." Ship both, plus a starter dashboard — the first thing an operator asks after `/metrics` lights up is "what should I graph?"
- The deployment boundary is a design decision, not a documentation task. Pick the things the app owns (image, config shape, health endpoints) and the things the operator owns (TLS, backups, registry, secrets) and make the handoff explicit in the config file.

The source code is on [GitHub](https://github.com/bimalghartimagar/LocalAgentTravelPlanner).
