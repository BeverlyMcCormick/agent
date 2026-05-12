# 📟 Standup Bot Agent

### SJ Group Project Planner Agent — Agentic AI for Task Progress & Team Visibility

> Built for **Code Without Barriers Hackathon**
>
> *"Old-school communication. Next-gen intelligence."*

---

## 🚀 Overview

The **Standup Bot Agent** transforms your Telegram team chat into an intelligent project coordination workspace.

Built for distributed engineering and project teams at **SJ Group**, this AI-powered Telegram bot listens to daily standup updates, understands natural language, detects blockers, and generates leadership-ready progress summaries — all without forcing teams into rigid workflows.

No dashboards.  
No form fatigue.  
No context switching.

Just seamless collaboration where your team already works.

---

## ❗ Problem Statement

In modern distributed teams, daily standups often become messy and inefficient.

Common challenges:

- Important updates get buried in long chat threads
- Managers lack real-time visibility into blockers
- Team members skip structured reporting
- Dependencies surface too late
- Traditional standup tools feel rigid and disruptive

Teams need a solution that fits naturally into existing workflows.

---

## 🤖 Meet the Agent

The **Standup Bot Agent** lives directly inside your Telegram group.

A team member can simply post:

```text
Finished API integration yesterday.
Today I’m fixing authentication bugs.
Blocked because QA credentials are still pending.
```

The agent automatically understands the message and extracts:

- Yesterday's work
- Today's planned tasks
- Current blockers
- Priority signals
- Task domain tags
- Sentiment indicators

---

## ✨ Features

### 📱 Native Telegram Experience

Works directly inside existing Telegram groups.

No extra apps. No onboarding friction.

---

### 🧠 AI-Powered Standup Parsing

Converts free-form standup messages into structured project intelligence.

Extracts:

- Yesterday
- Today
- Blockers
- Tags
- Sentiment
- Urgency

---

### 🚨 Intelligent Blocker Detection

Automatically identifies blockers such as:

- Missing credentials
- Waiting for approvals
- Environment failures
- Dependency bottlenecks
- Infrastructure issues

Critical blockers can trigger escalations.

---

### 📊 Team Digest Generation

Run:

```bash
/digest
```

Get a leadership-ready summary containing:

- Team progress overview
- Delivery confidence
- Key blockers
- Workstream breakdown
- Risk indicators
- People requiring assistance
- Suggested actions

---

### 🏷 Smart Auto-Tagging

Automatically categorizes updates:

- frontend
- backend
- infra
- QA
- design
- DevOps
- product

---

### 🤝 Agent-to-Agent Collaboration

Serious blockers can be handed off to a **Task Progress Agent** using Microsoft Agent Framework.

This makes the system truly **agentic**, not just conversational.

---

## Why This Is an Agent (Not Just a Bot)

Traditional standup tools require users to fill forms.

This agent:

✅ Understands natural language  
✅ Extracts structured context  
✅ Detects blockers automatically  
✅ Synthesizes team-wide insights  
✅ Recommends interventions  
✅ Collaborates with other agents  

It behaves like a digital project coordinator.

---

# 🏗 Architecture

```text
┌─────────────────────────────┐
│   Telegram Team Workspace   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Standup Bot Agent (Python)     │
│-------------------------------------│
│ ▸ Free-text standup parser          │
│ ▸ Blocker intelligence engine       │
│ ▸ Sentiment analyzer                │
│ ▸ Team digest synthesizer           │
└──────────────┬──────────────────────┘
               │
      ┌────────┼─────────────┬─────────────┐
      ▼        ▼             ▼             ▼
 Azure AI   Cosmos DB   Agent Framework   ACS
 Foundry    History DB  Task handoff      Alerts
```

---

# ☁ Azure Integration

| Service | Purpose |
|--------|---------|
| Azure App Service | Hosts the Telegram bot |
| Azure AI Foundry | Natural language understanding + summarization |
| Azure Cosmos DB | Standup history + sentiment analytics |
| Microsoft Agent Framework | Agent orchestration |
| Azure Communication Services | Critical blocker alerts |
| Power BI | Long-term dashboards |

---

# 🛠 Tech Stack

- Python
- python-telegram-bot
- Azure AI Foundry
- Azure Cosmos DB
- Microsoft Agent Framework
- Azure Communication Services
- Power BI
- Docker (optional)
- Telegram Bot API

---

# ⚙ Setup

## Prerequisites

You will need:

- Python 3.10+
- Telegram account
- Telegram bot token
- Azure AI endpoint / API key

---

## 1. Create Telegram Bot

Open Telegram.

Search for:

```text
@BotFather
```

Create a new bot:

```bash
/newbot
```

Choose:

- Bot name  
Example:

```text
SJ Standup Bot
```

Username ending with:

```text
bot
```

Example:

```text
sj_standup_bot
```

Copy the generated token.

---

## 2. Clone Repository

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment

Create `.env`

```bash
cp .env.example .env
```

Update:

```env
AI_ENDPOINT=https://your-endpoint/v1
AI_API_KEY=your-api-key
AI_MODEL=meta/llama-3.1-70b-instruct
TELEGRAM_TOKEN_STANDUP=your-telegram-token
```

---

## 5. Run the Bot

```bash
python bot.py
```

Expected output:

```bash
[ OK ] Standup Bot Agent online
```

---

# 📱 Usage

## Post Standups Naturally

Example:

```text
Yesterday completed payment API integration.
Today working on frontend checkout testing.
Blocked because staging environment is unstable.
```

---

## Generate Team Digest

Command:

```bash
/digest
```

Example output:

```text
📊 Team Digest

Progress:
- Backend API integration completed
- Frontend checkout testing in progress

Blockers:
- Staging instability affecting frontend team
- QA credentials pending for auth testing

Risk Level:
Medium

Suggested Action:
Infra team should investigate staging issues.
```

---

# 🔮 Future Enhancements

- Slack integration
- Jira sync
- Automated ticket creation
- Calendar reminders
- Weekly productivity analytics
- Cross-team dependency intelligence
- Voice standup support

---

# 🎯 Impact

Standup Bot Agent helps teams:

- Resolve blockers faster
- Improve delivery visibility
- Reduce coordination overhead
- Increase reporting accuracy
- Keep workflows frictionless

---

# 🏆 Hackathon Submission

**Partner:** SJ Group  
**Challenge:** SJ Project Planner Agent  
**Platform:** Telegram Bot  
**Event:** Code Without Barriers Hackathon

---

# 📜 License

MIT License
