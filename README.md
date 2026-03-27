<div align="center">

# 🚀 RevOps AI — Multi-Agent Sales Intelligence Platform

**AI-powered multi-agent system for B2B sales pipeline acceleration**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini AI](https://img.shields.io/badge/Gemini_AI-Powered-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> **4 specialized AI agents** that analyze your B2B sales pipeline in real-time — scoring leads, detecting deal risk, predicting churn, and generating competitive battlecards — all in one premium dark dashboard.

[📺 Demo](#-demo) · [🚀 Quick Start](#-quick-start) · [📡 API Docs](#-api-endpoints) · [🏗️ Architecture](#️-architecture)

</div>

---

## ✨ What It Does

RevOps AI deploys **4 autonomous AI agents** that work together to give revenue teams instant, actionable intelligence:

| Agent | What It Does | Key Output |
|-------|-------------|-----------|
| 🔍 **Prospecting Agent** | Scores leads & writes personalized outreach | Lead score (0–100), email + 3-step sequence |
| ⚠️ **Deal Intelligence Agent** | Detects at-risk deals before they die | Risk score, recovery plan with talking points |
| 🛡️ **Revenue Retention Agent** | Predicts churn & recommends interventions | Churn probability, save-email draft |
| ⚔️ **Competitive Intel Agent** | Generates battlecards against competitors | Win strategy, objection handlers, battlecard |

---

## 🎯 Key Features

- **Multi-agent orchestration** — agents run independently and broadcast status via WebSocket
- **Gemini AI integration** — plug in your API key for LLM-generated emails, strategies & battlecards
- **Template fallback mode** — works instantly with zero API key, no setup friction
- **Real-time dashboard** — live WebSocket notifications, charts, pipeline view
- **50 Leads · 20 Deals · 10 Accounts** of realistic mock CRM data built-in
- **Premium dark UI** — glassmorphism, micro-animations, risk badges
- **Full REST API** with auto-generated Swagger docs at `/docs`

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────┐
│         React Dashboard (Vite)           │
│    Recharts · React Query · WebSocket    │
└────────────────┬─────────────┬───────────┘
                 │ REST API    │ WebSocket
                 ▼             ▼
┌──────────────────────────────────────────┐
│           FastAPI Backend                │
│         Orchestration Layer              │
├──────────┬──────────┬──────────┬─────────┤
│Prospecting│  Deal    │  Churn   │Competi- │
│  Agent   │  Intel   │  Agent   │ tive    │
│          │  Agent   │          │ Agent   │
└──────────┴──────────┴──────────┴─────────┘
                 │
         ┌───────┴────────┐
         │  Mock CRM Data │  ←── Swap for real CRM
         │  (50L·20D·10A) │
         └────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Local Development (2 minutes)

**Backend**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python main.py
# → http://localhost:8000
```

**Frontend** (new terminal)
```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

### Option 2: Docker (one command)
```bash
cp .env.example .env
docker-compose up --build
# → Frontend: http://localhost:5173
# → Backend:  http://localhost:8000
# → API Docs: http://localhost:8000/docs
```

---

## 🔑 Optional: Enable Gemini AI

The app works in **template mode** out of the box (instant, no API key needed).

To enable real Gemini AI-generated content:

```bash
# backend/.env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=your-gemini-api-key-here
```

Get a free key at → [aistudio.google.com](https://aistudio.google.com)

---

## 📡 API Endpoints

### Agent Endpoints

```bash
# Prospecting Agent
POST /api/prospect
{
  "company_name": "TechFlow Inc",
  "industry": "SaaS",
  "contact_name": "Sarah Johnson",
  "contact_title": "VP of Sales",
  "icp_criteria": { "min_revenue": 1000000 }
}

# Deal Risk Agent
POST /api/deal-risk
{ "deal_id": 1, "include_engagements": true }

# Churn Agent
POST /api/churn
{ "account_id": 1, "include_usage": true }

# Competitive Intelligence Agent
POST /api/competitive
{ "deal_id": 1, "competitor_names": ["Salesforce", "HubSpot"] }
```

### Data Endpoints
```bash
GET /api/dashboard          # Full dashboard summary
GET /api/leads              # All leads (supports ?status=&industry=&min_score=)
GET /api/deals              # All deals (supports ?stage=)
GET /api/deals/{id}         # Deal detail with engagements
GET /api/accounts           # All accounts
GET /api/accounts/{id}      # Account details
GET /api/agent-runs         # Agent execution history
GET /api/agent-runs/{id}    # Specific run result
GET /health                 # Health check
```

### WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/agent-status');
ws.onmessage = (e) => {
  const { type, agent_type, status, message } = JSON.parse(e.data);
  // type: 'agent_status' | 'ack'
  // status: 'running' | 'completed' | 'failed'
};
```

---

## 📊 Sample Agent Outputs

<details>
<summary><b>🔍 Prospecting Agent</b></summary>

```json
{
  "lead_score": 78.5,
  "score_breakdown": {
    "firmographic_fit": 32.4,
    "industry_alignment": 20.0,
    "brand_recognition": 11.2,
    "icp_match": 18.7
  },
  "personalized_email": "Subject: Accelerating Revenue Growth at TechFlow...",
  "outreach_sequence": [
    { "step": 1, "channel": "Email",    "timing": "Day 1", "subject": "..." },
    { "step": 2, "channel": "LinkedIn", "timing": "Day 3", "subject": "..." },
    { "step": 3, "channel": "Email",    "timing": "Day 7", "subject": "..." }
  ],
  "recommended_approach": "High-priority lead. Recommend direct executive outreach..."
}
```
</details>

<details>
<summary><b>⚠️ Deal Intelligence Agent</b></summary>

```json
{
  "risk_score": 67.3,
  "risk_level": "high",
  "risk_reasons": [
    "Active competitors: Salesforce, HubSpot",
    "Low engagement frequency",
    "Budget not confirmed"
  ],
  "recovery_plan": [
    {
      "action": "Executive Sponsor Meeting",
      "priority": "urgent",
      "talking_points": ["Address risk factors...", "Propose timeline..."],
      "timeline": "Within 48 hours"
    }
  ]
}
```
</details>

<details>
<summary><b>🛡️ Revenue Retention Agent</b></summary>

```json
{
  "churn_probability": 72.5,
  "risk_level": "critical",
  "risk_factors": [
    "No login in 21 days",
    "Negative NPS score (-15)",
    "8 open support tickets"
  ],
  "intervention": {
    "type": "Executive Rescue Mission",
    "urgency": "immediate",
    "description": "Schedule emergency executive call within 24 hours..."
  },
  "save_email_draft": "Subject: Your success is our priority..."
}
```
</details>

<details>
<summary><b>⚔️ Competitive Intelligence Agent</b></summary>

```json
{
  "competitor_risk_flag": true,
  "primary_competitor": "Salesforce",
  "competitive_win_rate": 64,
  "battlecard": [
    {
      "category": "Product",
      "our_strengths": ["AI-native", "Faster setup", "Lower TCO"],
      "competitor_weaknesses": ["Complex UI", "High cost", "Slow AI roadmap"],
      "key_differentiators": ["4 AI agents built-in", "Real-time insights"]
    }
  ],
  "win_strategy": "Lead with ROI — show 40% pipeline velocity increase...",
  "objection_handlers": [
    {
      "objection": "We already use Salesforce",
      "response": "RevOps AI complements Salesforce with specialized AI agents..."
    }
  ]
}
```
</details>

---

## 🗂️ Project Structure

```
AI-SalesRevenueOps/
├── docker-compose.yml          # One-command Docker setup
├── .env.example                # Environment variable template
│
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── requirements.txt        # Python dependencies
│   ├── config.py               # Settings & configuration
│   │
│   ├── agents/                 # 🤖 AI Agent implementations
│   │   ├── base_agent.py       # Shared agent base class
│   │   ├── prospect_agent.py   # Prospecting Agent
│   │   ├── deal_agent.py       # Deal Intelligence Agent
│   │   ├── churn_agent.py      # Revenue Retention Agent
│   │   └── competitive_agent.py# Competitive Intel Agent
│   │
│   ├── services/
│   │   ├── orchestrator.py     # Agent execution & tracking
│   │   └── llm_service.py      # Gemini AI integration
│   │
│   ├── routers/
│   │   ├── agents.py           # Agent API routes
│   │   └── dashboard.py        # Dashboard & CRM routes
│   │
│   ├── tools/
│   │   └── crm_tools.py        # CRM query tools used by agents
│   │
│   ├── websocket/
│   │   └── manager.py          # WebSocket broadcast manager
│   │
│   ├── mock_data/
│   │   └── generator.py        # 50 leads, 20 deals, 10 accounts
│   │
│   ├── models/                 # Pydantic + SQLAlchemy models
│   └── schemas/                # Request/response schemas
│
└── frontend/
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── App.jsx             # Main dashboard layout
        ├── components/         # UI components
        │   ├── StatsOverview.jsx
        │   ├── DealPipeline.jsx
        │   ├── ProspectForm.jsx
        │   ├── ChurnRiskCard.jsx
        │   ├── DealRiskResult.jsx
        │   ├── CompetitiveResult.jsx
        │   ├── AgentLogs.jsx
        │   └── Charts.jsx
        ├── hooks/
        │   └── useWebSocket.js # WebSocket hook
        └── services/
            └── api.js          # Axios API client
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Vite, TailwindCSS, Recharts, React Query |
| **Backend** | FastAPI, Python 3.11, Pydantic v2 |
| **AI / LLM** | Google Gemini 2.0 Flash (optional), template fallback |
| **Real-time** | WebSockets (FastAPI native) |
| **Mock Data** | Faker — 50 leads, 20 deals, 10 accounts |
| **DevOps** | Docker, Docker Compose |

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built for the AI Hackathon 2025** 🏆

*If this project helped you, please give it a ⭐*

</div>
