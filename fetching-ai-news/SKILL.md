---
name: fetching-ai-news
description: Use when the user asks for today's or the latest AI news, an AI daily digest, or says 今日AI新闻 / AI新闻 / AI快讯 / 今天AI圈 / AI日报 / 最新AI资讯 / latest AI newsletters, or asks to fetch or summarize content from The Rundown AI, TLDR AI, Superhuman AI, There's An AI For That, or Mindstream.
---

# fetching-ai-news

## Overview

Fetch the latest content from five major English AI newsletters and compile it into Chinese (标题 / 发布时间 / 原文链接 / 详细内容). Dailies publish Mon–Fri only — on weekends fetch the most recent issue and state its actual date.

## The Five Sources (URLs verified working)

| Site | Fetch entry | Article URL pattern | Publish days |
|---|---|---|---|
| TLDR AI | `https://tldr.tech/api/latest/ai` (redirects to latest issue, date in title) | `https://tldr.tech/ai/YYYY-MM-DD` | Mon–Fri |
| The Rundown AI | `https://www.therundown.ai/` homepage lists latest issues | `/articles/<slug>` (beehiiv mirror: therundownai.beehiiv.com) | Mon–Fri + Tech/Robotics editions |
| Superhuman AI | `https://superhuman.ai/` homepage lists latest issues | `/p/<slug>` | Mon–Fri + weekend specials |
| There's An AI For That | homepage via **playwright only** (see below) | `/ai/<slug>` | directory, updated daily |
| Mindstream | `https://mindstream.news` homepage lists the archive | `/p/<slug>` | ~2 issues/day |

## Workflow

1. Fetch TLDR latest + Rundown homepage + Superhuman homepage + Mindstream homepage in parallel (webfetch, markdown format).
2. From each homepage pick the LATEST issue (check dates — on a Sunday expect Friday's issue; say so explicitly).
3. Fetch each issue's article page for full content (webfetch).
4. Compile in Chinese: per site give 标题、发布时间、原文链接、详细内容（要点式翻译，保留所有数字和链接）, then a cross-site 今日要点总结.
5. Skip sponsor blocks (marked Sponsor / Presented by / TOGETHER WITH) — note the omission once.

## There's An AI For That (TAAFT) — playwright ONLY

webfetch is BLOCKED: `/newsletter/` and `/ai/<slug>/` return 403, homepage exceeds the 5MB fetch limit. Use the playwright skill:

1. `browser_navigate` → `https://theresanaiforthat.com/` (a Cloudflare challenge may show 请稍候… — re-navigate until the real page title loads)
2. `browser_evaluate`: extract `a[href*="/ai/<slug>"]` links plus the nearest date element (`.saved_time, time, [class*=time], [class*=date]`) — the homepage stream shows the newest additions with dates (e.g. "Sep 20, 2026")
3. Tool detail pages: navigate in the SAME browser session (webfetch stays 403), then evaluate `h1` + description selectors
4. TRAP: `/most-recent/` redirects to `/s/most+recent/` = a SEARCH QUERY, not a recency filter (returns news-category tools) — never use it

## Common Mistakes

| Mistake | Reality |
|---|---|
| Fetching on a Sunday and expecting today's issue | Dailies are Mon–Fri; fetch the most recent and state its real date |
| `www.thesuperhuman.ai` | Returns an EMPTY response — use `https://superhuman.ai/` |
| TAAFT via webfetch | 403 (Cloudflare) or >5MB homepage — playwright only |
| TAAFT `/most-recent/` URL | Redirects to a search query, not the recency list |
| Taking the first homepage link as the issue | Rundown's homepage mixes AI/Tech/Robotics editions — pick by category + date |
| Reporting sponsor content as news | Sponsor / Presented-by blocks are ads — skip and note |

## Cross-reference

The user's 163 mailbox holds The Deep View / Unwind AI subscriptions — when the user asks for THOSE, use `reading-mail-via-imap` instead of webfetch.
