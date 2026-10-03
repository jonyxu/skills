---
name: fetching-ai-news
description: Use when the user asks for today's or the latest AI news, an AI daily digest, or says 今日AI新闻 / AI新闻 / AI快讯 / 今天AI圈 / AI日报 / 最新AI资讯 / latest AI newsletters, or asks to fetch or summarize content from The Rundown AI, TLDR AI, Superhuman AI, Mindstream, TechCrunch AI, or Product Hunt.
---

# fetching-ai-news

## Overview

Fetch the latest AI news and new AI-tool launches from six English sources and compile into Chinese (标题 / 发布时间 / 原文链接 / 详细内容). Four are curated newsletters — Mon–Fri only, so on weekends fetch the most recent issue and state its actual date. TechCrunch AI and Product Hunt update daily (incl. weekends), so they always have fresh items. All six are plain `webfetch` — no browser/GUI needed.

## The Six Sources (URLs verified working)

| Site | Fetch entry | Article URL pattern | Publish days |
|---|---|---|---|
| TLDR AI | `https://tldr.tech/api/latest/ai` (redirects to latest issue, date in title) | `https://tldr.tech/ai/YYYY-MM-DD` | Mon–Fri |
| The Rundown AI | `https://www.therundown.ai/` homepage lists latest issues | `/articles/<slug>` (beehiiv mirror: therundownai.beehiiv.com) | Mon–Fri + Tech/Robotics editions |
| Superhuman AI | `https://superhuman.ai/` homepage lists latest issues | `/p/<slug>` | Mon–Fri + weekend specials |
| Mindstream | `https://mindstream.news` homepage lists the archive | `/p/<slug>` | ~2 issues/day |
| TechCrunch AI | `https://techcrunch.com/category/artificial-intelligence/` category page = latest AI articles (relative time + author) | `https://techcrunch.com/YYYY/MM/DD/<slug>/` | Daily, incl. weekends |
| Product Hunt | `https://www.producthunt.com/` homepage "Top Products Launching Today" (+ yesterday/week/month) | `/products/<slug>` | Daily, 24/7 launches |

## Workflow

1. Fetch in parallel (webfetch, markdown format): TLDR latest + Rundown homepage + Superhuman homepage + Mindstream homepage + TechCrunch AI category page + Product Hunt homepage.
2. Pick the LATEST from each (check dates — on a Sunday the newsletters show Friday's issue, say so explicitly; TechCrunch / Product Hunt are daily, so always fresh).
3. Fetch each issue's article page for full content (webfetch). For Product Hunt, open the top AI-tagged launches of the day (`/products/<slug>`) for their descriptions.
4. Compile in Chinese: per site give 标题、发布时间、原文链接、详细内容（要点式翻译，保留所有数字和链接）, then a cross-site 今日要点总结. Product Hunt fills the "new AI tools" slot: list the day's top AI launches (名称、一句话简介、社区热度/投票数、链接).
5. Skip sponsor blocks (Sponsor / Presented by / TOGETHER WITH) and Product Hunt "Promoted" items — note the omission once.

## Common Mistakes

| Mistake | Reality |
|---|---|
| Fetching on a Sunday expecting today's issue | The four newsletters are Mon–Fri — fetch the most recent and state its real date (TechCrunch / Product Hunt are daily, always fresh) |
| `www.thesuperhuman.ai` | Returns an EMPTY response — use `https://superhuman.ai/` |
| Taking the first homepage link as the issue | Rundown's homepage mixes AI/Tech/Robotics editions — pick by category + date |
| Reporting sponsor content as news | Sponsor / Presented-by / Promoted blocks are ads — skip and note |
| Treating Product Hunt upvotes as a quality verdict | They're community votes, not endorsements — present as 社区热度 with the raw count |

## Cross-reference

The user's 163 mailbox holds The Deep View / Unwind AI subscriptions — when the user asks for THOSE, use `reading-mail-via-imap` instead of webfetch.
