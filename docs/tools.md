# MCP tools catalogue

Every MCP tool function registered under `app/tools`. Each entry lists the function name, its source file, and the first line of its docstring.

## `app/tools/ask.py`

- **ask** — `app/tools/ask.py` — Route natural language to the best Polymarket MCP tool and execute it.

## `app/tools/bridge/core.py`

- **get_bridge_status** — `app/tools/bridge/core.py` — Track bridge deposit or withdrawal progress via the trading API.
- **get_bridge_supported_assets** — `app/tools/bridge/core.py` — Get supported bridge chains and tokens via the trading API.
- **post_bridge_deposit** — `app/tools/bridge/core.py` — Create multi-chain deposit addresses for a Polymarket wallet via the trading API.
- **post_bridge_quote** — `app/tools/bridge/core.py` — Preview bridge fees and estimated output via the trading API.
- **post_bridge_withdraw** — `app/tools/bridge/core.py` — Create withdrawal addresses for bridging pUSD off Polymarket via the trading API.

## `app/tools/clob/account.py`

- **get_clob_api_keys** — `app/tools/clob/account.py` — List CLOB API keys via the trading API.
- **get_clob_builder_api_keys** — `app/tools/clob/account.py` — List CLOB builder API keys via the trading API.
- **get_clob_builder_trades** — `app/tools/clob/account.py` — Get builder-attributed CLOB trades via the trading API.
- **get_clob_closed_only_mode** — `app/tools/clob/account.py` — Get CLOB closed-only ban status via the trading API.
- **get_clob_notifications** — `app/tools/clob/account.py` — Get CLOB notifications via the trading API.
- **get_clob_rewards_markets_current** — `app/tools/clob/account.py` — Get current CLOB reward markets via the trading API.
- **get_clob_rewards_user** — `app/tools/clob/account.py` — Get CLOB user rewards for a day via the trading API.

## `app/tools/clob/history.py`

- **get_clob_batch_prices_history** — `app/tools/clob/history.py` — Get batch CLOB price history via the trading API.
- **get_clob_prices_history** — `app/tools/clob/history.py` — Get CLOB price history via the trading API.

## `app/tools/clob/market_data.py`

- **clob_server_time** — `app/tools/clob/market_data.py` — Get CLOB server time via the trading API.
- **get_clob_fee_rate** — `app/tools/clob/market_data.py` — Get CLOB fee rate via the trading API.
- **get_clob_last_trade_price** — `app/tools/clob/market_data.py` — Get CLOB last trade price via the trading API.
- **get_clob_midpoint** — `app/tools/clob/market_data.py` — Get CLOB midpoint via the trading API.
- **get_clob_neg_risk** — `app/tools/clob/market_data.py` — Get CLOB neg-risk flag via the trading API.
- **get_clob_orderbook** — `app/tools/clob/market_data.py` — Get CLOB orderbook via the trading API.
- **get_clob_price** — `app/tools/clob/market_data.py` — Get CLOB best bid or ask via the trading API.
- **get_clob_spread** — `app/tools/clob/market_data.py` — Get CLOB spread via the trading API.
- **get_clob_tick_size** — `app/tools/clob/market_data.py` — Get CLOB tick size via the trading API.

## `app/tools/clob/markets.py`

- **get_clob_live_activity** — `app/tools/clob/markets.py` — Get CLOB live activity for a market via the trading API.
- **get_clob_market_by_token** — `app/tools/clob/markets.py` — Resolve CLOB market by outcome token ID via the trading API.
- **get_clob_market_info** — `app/tools/clob/markets.py` — Get CLOB market info for a condition ID via the trading API.
- **get_clob_simplified_markets** — `app/tools/clob/markets.py` — List CLOB simplified markets via the trading API.

## `app/tools/clob/trading.py`

- **cancel_all_clob_orders** — `app/tools/clob/trading.py` — Cancel all orders. Pass mode=paper for simulated orders.
- **cancel_clob_order** — `app/tools/clob/trading.py` — Cancel a CLOB order via the trading API.
- **derive_clob_api_key** — `app/tools/clob/trading.py` — Derive CLOB L2 API credentials via the trading API (requires PRIVATE_KEY).
- **get_clob_balance_allowance** — `app/tools/clob/trading.py` — Get CLOB balance and allowance via the trading API.
- **get_clob_open_orders** — `app/tools/clob/trading.py` — Get orders via the trading API. Pass mode=paper or mode=real.
- **get_clob_order** — `app/tools/clob/trading.py` — Get a CLOB order by ID via the trading API.
- **get_clob_positions** — `app/tools/clob/trading.py` — Get positions via the unified CLOB route. Real mode needs user wallet; paper needs paper_account_id.
- **get_clob_trades** — `app/tools/clob/trading.py` — Get authenticated CLOB trades via the trading API.
- **post_clob_heartbeat** — `app/tools/clob/trading.py` — Send CLOB heartbeat via the trading API (keeps resting orders alive).
- **post_clob_limit_order** — `app/tools/clob/trading.py` — Create and post a limit order. Set mode=paper for simulated trading.
- **post_clob_market_order** — `app/tools/clob/trading.py` — Create and post a market order. Set mode=paper for simulated trading.
- **post_clob_order** — `app/tools/clob/trading.py` — Post a pre-signed CLOB order payload (advanced). Prefer post_clob_market_order.

## `app/tools/data/core.py`

- **data_health** — `app/tools/data/core.py` — Check Polymarket Data API health via the trading API.
- **get_data_activity** — `app/tools/data/core.py` — Get on-chain activity for a wallet via the trading API.
- **get_data_closed_positions** — `app/tools/data/core.py` — Get closed positions for a wallet via the trading API.
- **get_data_holders** — `app/tools/data/core.py` — Get top holders for a market condition ID via the trading API.
- **get_data_positions** — `app/tools/data/core.py` — Get open positions for a wallet via the trading API Data service.
- **get_data_traded** — `app/tools/data/core.py` — Get count of markets traded by a wallet via the trading API.
- **get_data_trades** — `app/tools/data/core.py` — Get trade history via the trading API Data service.
- **get_data_value** — `app/tools/data/core.py` — Get total USDC value of a wallet's positions via the trading API.

## `app/tools/data/leaderboards.py`

- **get_data_builder_leaderboard** — `app/tools/data/leaderboards.py` — Get builder leaderboard via the trading API.
- **get_data_builder_volume** — `app/tools/data/leaderboards.py` — Get builder volume time series via the trading API.
- **get_data_leaderboard** — `app/tools/data/leaderboards.py` — Get trader leaderboard via the trading API Data service.

## `app/tools/data/markets.py`

- **get_data_live_volume** — `app/tools/data/markets.py` — Get live event volume via the trading API Data service.
- **get_data_market_positions** — `app/tools/data/markets.py` — Get all positions for a market via the trading API.
- **get_data_open_interest** — `app/tools/data/markets.py` — Get open interest via the trading API Data service.

## `app/tools/gamma/events.py`

- **get_gamma_event** — `app/tools/gamma/events.py` — Fetch a Polymarket event by ID via the trading API.
- **get_gamma_event_by_slug** — `app/tools/gamma/events.py` — Fetch a Polymarket event by slug via the trading API.
- **get_gamma_event_live_volume** — `app/tools/gamma/events.py` — Fetch live volume for an event via the trading API.
- **list_gamma_event_tags** — `app/tools/gamma/events.py` — List Polymarket event tags via the trading API.
- **list_gamma_events** — `app/tools/gamma/events.py` — List Polymarket events via the trading API Gamma service.
- **list_gamma_events_keyset** — `app/tools/gamma/events.py` — List Polymarket events using Gamma keyset pagination via the trading API.

## `app/tools/gamma/history.py`

- **get_gamma_prices_history** — `app/tools/gamma/history.py` — Fetch historical prices from Gamma via the trading API.
- **get_gamma_prices_history_batch** — `app/tools/gamma/history.py` — Fetch batch Gamma price history via the trading API.

## `app/tools/gamma/markets.py`

- **get_gamma_market** — `app/tools/gamma/markets.py` — Fetch a Polymarket market by Gamma market ID via the trading API.
- **get_gamma_market_by_slug** — `app/tools/gamma/markets.py` — Fetch a Polymarket market by URL slug via the trading API.
- **get_gamma_market_by_token** — `app/tools/gamma/markets.py` — Resolve a parent market from an outcome token ID via the trading API.
- **get_gamma_market_tags** — `app/tools/gamma/markets.py` — Fetch tags attached to a market via the trading API.
- **get_gamma_markets_by_condition_ids** — `app/tools/gamma/markets.py` — Fetch Polymarket markets by condition IDs via the trading API.
- **list_gamma_markets** — `app/tools/gamma/markets.py` — List Polymarket markets via the trading API Gamma service.
- **list_gamma_markets_keyset** — `app/tools/gamma/markets.py` — List Polymarket markets using Gamma keyset pagination via the trading API.
- **list_gamma_markets_simplified** — `app/tools/gamma/markets.py` — List simplified Polymarket markets via the trading API.
- **list_gamma_sampling_markets** — `app/tools/gamma/markets.py` — List Polymarket sampling markets via the trading API.
- **list_gamma_sampling_markets_simplified** — `app/tools/gamma/markets.py` — List simplified Polymarket sampling markets via the trading API.

## `app/tools/gamma/profiles.py`

- **get_gamma_comment** — `app/tools/gamma/profiles.py` — Fetch a Polymarket comment by ID via the trading API.
- **get_gamma_profile** — `app/tools/gamma/profiles.py` — Fetch a Polymarket user profile via the trading API.
- **list_gamma_comments** — `app/tools/gamma/profiles.py` — List Polymarket comments via the trading API.
- **list_gamma_comments_by_user** — `app/tools/gamma/profiles.py` — List Polymarket comments for a user address via the trading API.

## `app/tools/gamma/search.py`

- **gamma_search** — `app/tools/gamma/search.py` — Search Polymarket markets, events, or profiles via the trading API.

## `app/tools/gamma/series.py`

- **get_gamma_series** — `app/tools/gamma/series.py` — Fetch a Polymarket series by ID via the trading API.
- **list_gamma_series** — `app/tools/gamma/series.py` — List Polymarket series via the trading API.

## `app/tools/gamma/sports.py`

- **get_gamma_sports_market_types** — `app/tools/gamma/sports.py` — Fetch Polymarket sports market types via the trading API.
- **get_gamma_sports_metadata** — `app/tools/gamma/sports.py` — Fetch Polymarket sports metadata via the trading API.
- **get_gamma_sports_teams** — `app/tools/gamma/sports.py` — Fetch Polymarket sports teams via the trading API.

## `app/tools/gamma/tags.py`

- **get_gamma_related_tags_by_id** — `app/tools/gamma/tags.py` — Fetch related Polymarket tags by tag ID via the trading API.
- **get_gamma_related_tags_by_slug** — `app/tools/gamma/tags.py` — Fetch related Polymarket tags by tag slug via the trading API.
- **get_gamma_tag** — `app/tools/gamma/tags.py` — Fetch a Polymarket tag by ID via the trading API.
- **get_gamma_tag_by_slug** — `app/tools/gamma/tags.py` — Fetch a Polymarket tag by slug via the trading API.
- **list_gamma_tags** — `app/tools/gamma/tags.py` — List Polymarket tags via the trading API.

## `app/tools/health.py`

- **health_check** — `app/tools/health.py` — Check health of the Polymarket trading API.

## `app/tools/paper/accounts.py`

- **create_paper_account** — `app/tools/paper/accounts.py` — Create a simulated paper trading account with virtual USDC.
- **get_paper_account** — `app/tools/paper/accounts.py` — Get a paper trading account summary by account ID.
- **get_paper_balance** — `app/tools/paper/accounts.py` — Get virtual USDC balance for a paper account.
- **get_paper_portfolio** — `app/tools/paper/accounts.py` — Get paper portfolio value (cash + marked positions).
- **get_paper_positions** — `app/tools/paper/accounts.py` — Get open paper positions marked to live midpoints.
- **list_paper_accounts** — `app/tools/paper/accounts.py` — List active paper trading accounts for the current API access token.
- **reset_paper_account** — `app/tools/paper/accounts.py` — Full paper account reset: starting balance, cancel orders, clear positions.
- **reset_paper_balance** — `app/tools/paper/accounts.py` — Reset virtual USDC cash for a paper account. Keeps positions; cancels open orders.

**Total:** 96 tools
