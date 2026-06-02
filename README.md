# Polymarket MCP Server

[MCP](https://modelcontextprotocol.io/) server that exposes Polymarket tools to AI clients (Cursor, Claude Desktop, custom apps). Proxies all operations to the **Polymarket API** over HTTP.

Runs **independently** of the API — point it at any reachable API instance.

---

## Stack

| Component | Version |
|-----------|---------|
| Python | ≥ 3.14 |
| FastMCP | ≥ 3.3.1 |
| httpx | API client |
| uvicorn | HTTP transport |
| OpenAI API | optional `ask` router |

---

## Features

- **60+ tools** — Gamma, CLOB, Data, Bridge, paper trading
- **Structured responses** — every tool returns `{ok, data, error}`
- **HTTP transport** — Streamable HTTP for remote clients
- **Natural-language routing** — `ask` tool with OpenAI
- **Paper trading** — `mode=paper` on order tools
- **API token auth** — sends `Authorization: Bearer` to the API
- **Dynamic credentials** — optional per-tool Polymarket key overrides

---

## Architecture

```
AI Client  →  MCP (this repo)  →  Polymarket API  →  Polymarket / SQLite
   stdio/HTTP       FastMCP            FastAPI
```

---

## Quick start (local)

### 1. Start the API first

See [../api/README.md](../api/README.md). The API must be running and reachable.

### 2. Configure MCP

```bash
cd mcp
python3.14 -m venv .venv
source .venv/bin/activate
pip install -e .

cp .env.example .env
```

Required `.env` values:

```bash
POLYMARKET_API_URL=http://127.0.0.1:8005
POLYMARKET_API_ACCESS_TOKEN=<same as API API_ACCESS_TOKEN>
```

Optional for `ask` tool:

```bash
OPENAI_API_KEY=sk-...
```

### 3. Run MCP

**stdio (Cursor / Claude Desktop):**

```bash
python -m app.main
```

**HTTP (remote clients):**

```bash
uvicorn app.http_app:app --host 127.0.0.1 --port 8001
```

Or:

```bash
polymarket-mcp-http
```

Health:

```bash
curl http://127.0.0.1:8001/health
```

---

## Docker

```bash
cd mcp
cp .env.example .env
# Set POLYMARKET_API_URL, POLYMARKET_API_ACCESS_TOKEN, OPENAI_API_KEY

docker compose up -d --build
```

When the API runs on the host and MCP in Docker:

```bash
DOCKER_POLYMARKET_API_URL=http://host.docker.internal:8005
```

When both run in Docker, use a shared network or `host.docker.internal`.

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `POLYMARKET_API_URL` | `http://127.0.0.1:8005` | Upstream API base URL |
| `POLYMARKET_API_ACCESS_TOKEN` | — | Bearer token sent on **every** API request |
| `MCP_HOST` | `127.0.0.1` | HTTP bind address (`0.0.0.0` in Docker) |
| `MCP_PORT` | `8001` | HTTP port |
| `MCP_URL` | `http://127.0.0.1:8001` | Public URL for clients |
| `MCP_AUTH_TOKEN` | — | Optional Bearer auth **for MCP clients** |
| `MCP_STATELESS_HTTP` | `true` | Stateless HTTP mode |
| `OPENAI_API_KEY` | — | Required for `ask` tool |
| `OPENAI_MODEL` | `gpt-4o-mini` | Ask router model |

---

## API authentication

Every request to the Polymarket API includes:

```http
Authorization: Bearer <POLYMARKET_API_ACCESS_TOKEN>
```

This must match `API_ACCESS_TOKEN` on the API service. Mismatched tokens receive HTTP 401.

---

## Dynamic Polymarket credentials

By default, live trading uses credentials configured in the **API's** `.env`.

Override per tool call by passing optional parameters (sent as `X-Poly-*` headers):

| Tool parameter | Header sent to API |
|----------------|-------------------|
| `private_key` | `X-Poly-Private-Key` |
| `deposit_wallet_address` | `X-Poly-Deposit-Wallet-Address` |
| `poly_api_key` | `X-Poly-Api-Key` |
| `poly_api_secret` | `X-Poly-Api-Secret` |
| `poly_passphrase` | `X-Poly-Api-Passphrase` |
| `poly_builder_code` | `X-Poly-Builder-Code` |
| `clob_signature_type` | `X-Poly-Signature-Type` |

Supported on: `post_clob_market_order`, `post_clob_limit_order`, `post_clob_order`, `get_clob_balance_allowance`, `derive_clob_api_key`.

Example — trade with a different wallet for one call:

```
post_clob_market_order(
  token_id="...",
  amount=10,
  mode="real",
  private_key="0x...",
  deposit_wallet_address="0x...",
  poly_api_key="...",
  poly_api_secret="...",
  poly_passphrase="..."
)
```

---

## Paper trading via MCP

### 1. Create a paper account

```
create_paper_account(name="demo", starting_balance_usdc=10000)
```

Save the returned `id`.

### 2. Place a paper order

```
post_clob_market_order(
  token_id="...",
  amount=10,
  mode="paper",
  paper_account_id="<account-id>"
)
```

### 3. Check balance / portfolio

```
get_paper_balance(account_id="<account-id>")
get_paper_portfolio(account_id="<account-id>")
```

### 4. Reset

```
reset_paper_balance(account_id="<account-id>")          # cash only
reset_paper_account(account_id="<account-id>")          # full reset
```

Paper accounts are **scoped to your API access token**. Different tokens = isolated account namespaces. Account UUIDs are portable — use the same token + account ID to access them later.

---

## Ask tool (natural language)

```
ask(query="paper buy $10 on token ...", session_id=null)
```

The router understands paper vs live intent and routes to the correct tools. Destructive actions (orders, resets) require confirmation via `session_id` follow-up.

Requires `OPENAI_API_KEY`.

---

## Cursor configuration

`.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "polymarket": {
      "command": "/path/to/mcp/.venv/bin/python",
      "args": ["-m", "app.main"],
      "env": {
        "POLYMARKET_API_URL": "http://127.0.0.1:8005",
        "POLYMARKET_API_ACCESS_TOKEN": "your-token"
      }
    }
  }
}
```

For HTTP MCP instead of stdio, configure your client to connect to `MCP_URL`.

---

## Tool response format

All tools return:

```json
{
  "ok": true,
  "data": { ... },
  "error": null
}
```

On failure:

```json
{
  "ok": false,
  "data": null,
  "error": {
    "code": "http_error",
    "message": "...",
    "status_code": 400
  }
}
```

---

## Production checklist

- [ ] Set `POLYMARKET_API_ACCESS_TOKEN` matching the API
- [ ] Set `MCP_AUTH_TOKEN` to protect the MCP HTTP endpoint
- [ ] Use HTTPS for both MCP and API in production
- [ ] Keep `OPENAI_API_KEY` server-side only
- [ ] Never pass raw private keys through untrusted MCP clients unless intentional
- [ ] Run API and MCP as separate services with network policies

---

## Deploy independently

| Service | Port | Depends on |
|---------|------|------------|
| API | 8005 | Polymarket upstream, SQLite volume |
| MCP | 8001 | API reachable at `POLYMARKET_API_URL` |

Neither service requires the other to be on the same machine — only network connectivity and matching access tokens.
