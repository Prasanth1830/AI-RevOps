"""
CRM Tools - Functions that agents use to interact with CRM data
"""
import random
from typing import Dict, Any, List, Optional
from mock_data.generator import MOCK_DATA


def get_crm_data(entity_type: str, entity_id: Optional[int] = None) -> Dict[str, Any]:
    """Get CRM data by entity type and optional ID"""
    data_map = {
        "leads": MOCK_DATA["leads"],
        "deals": MOCK_DATA["deals"],
        "accounts": MOCK_DATA["accounts"],
        "engagements": MOCK_DATA["engagements"]
    }

    if entity_type not in data_map:
        return {"error": f"Unknown entity type: {entity_type}"}

    data = data_map[entity_type]
    if entity_id:
        matches = [item for item in data if item["id"] == entity_id]
        return matches[0] if matches else {"error": f"{entity_type} with id {entity_id} not found"}

    return {"count": len(data), "data": data}


def get_lead_by_company(company_name: str) -> Dict[str, Any]:
    """Look up a lead by company name"""
    for lead in MOCK_DATA["leads"]:
        if company_name.lower() in lead["company_name"].lower():
            return lead
    return {"error": f"No lead found for company: {company_name}"}


def get_deal_data(deal_id: int) -> Dict[str, Any]:
    """Get detailed deal data with related engagements"""
    deal = None
    for d in MOCK_DATA["deals"]:
        if d["id"] == deal_id:
            deal = d
            break

    if not deal:
        return {"error": f"Deal {deal_id} not found"}

    engagements = [e for e in MOCK_DATA["engagements"] if e["deal_id"] == deal_id]
    account = None
    for a in MOCK_DATA["accounts"]:
        if a["id"] == deal["account_id"]:
            account = a
            break

    return {
        "deal": deal,
        "engagements": engagements,
        "account": account,
        "engagement_count": len(engagements)
    }


def get_account_data(account_id: int) -> Dict[str, Any]:
    """Get detailed account data with usage and engagement"""
    account = None
    for a in MOCK_DATA["accounts"]:
        if a["id"] == account_id:
            account = a
            break

    if not account:
        return {"error": f"Account {account_id} not found"}

    engagements = [e for e in MOCK_DATA["engagements"] if e.get("account_id") == account_id]
    deals = [d for d in MOCK_DATA["deals"] if d["account_id"] == account_id]

    return {
        "account": account,
        "engagements": engagements,
        "deals": deals,
        "active_deals": len([d for d in deals if d["stage"] not in ["closed_won", "closed_lost"]])
    }


def score_lead(company_name: str, industry: str, icp_criteria: Dict[str, Any]) -> Dict[str, Any]:
    """Score a lead based on ICP criteria - simulated AI scoring"""
    base_score = random.uniform(30, 95)

    # Industry fit bonus
    high_value_industries = ["SaaS", "FinTech", "AI/ML", "Cybersecurity"]
    industry_score = 20 if industry in high_value_industries else random.uniform(5, 15)

    # Company name recognition (simulate)
    name_score = random.uniform(5, 15)

    # ICP match
    icp_score = random.uniform(10, 25) if icp_criteria else random.uniform(5, 10)

    total = min(100, base_score * 0.4 + industry_score + name_score + icp_score + random.uniform(0, 10))

    return {
        "lead_score": round(total, 1),
        "score_breakdown": {
            "firmographic_fit": round(base_score * 0.4, 1),
            "industry_alignment": round(industry_score, 1),
            "brand_recognition": round(name_score, 1),
            "icp_match": round(icp_score, 1)
        },
        "confidence": round(random.uniform(0.7, 0.95), 2)
    }


def analyze_engagement(deal_id: int) -> Dict[str, Any]:
    """Analyze engagement patterns for a deal"""
    engagements = [e for e in MOCK_DATA["engagements"] if e["deal_id"] == deal_id]

    if not engagements:
        return {
            "trend": "no_data",
            "engagement_frequency": 0,
            "avg_sentiment": 0,
            "risk_signals": ["No engagement data available"]
        }

    sentiments = {"positive": 1, "neutral": 0, "negative": -1}
    avg_sentiment = sum(sentiments.get(e.get("sentiment", "neutral"), 0) for e in engagements) / len(engagements)

    inbound = len([e for e in engagements if e.get("direction") == "inbound"])
    outbound = len([e for e in engagements if e.get("direction") == "outbound"])

    risk_signals = []
    if avg_sentiment < -0.2:
        risk_signals.append("Overall negative sentiment trend")
    if outbound > inbound * 2:
        risk_signals.append("Heavy outbound vs inbound - may indicate low buyer interest")
    if len(engagements) < 3:
        risk_signals.append("Low engagement volume")

    negative_count = len([e for e in engagements if e.get("sentiment") == "negative"])
    if negative_count > len(engagements) * 0.3:
        risk_signals.append(f"{negative_count} negative interactions detected")

    trend = "improving" if avg_sentiment > 0.3 else ("declining" if avg_sentiment < -0.2 else "stable")

    return {
        "trend": trend,
        "engagement_frequency": len(engagements),
        "avg_sentiment": round(avg_sentiment, 2),
        "inbound_ratio": round(inbound / max(1, len(engagements)), 2),
        "risk_signals": risk_signals,
        "engagement_types": {t: len([e for e in engagements if e.get("type") == t]) for t in ["email", "call", "meeting", "demo", "support"]},
        "latest_engagement": engagements[-1] if engagements else None
    }


def detect_churn(account_id: int) -> Dict[str, Any]:
    """Detect churn risk signals from account data"""
    account = None
    for a in MOCK_DATA["accounts"]:
        if a["id"] == account_id:
            account = a
            break

    if not account:
        return {"error": f"Account {account_id} not found"}

    usage = account.get("usage_metrics", {})
    risk_factors = []
    churn_score = 0

    # Usage decline signals
    if usage.get("last_login_days_ago", 0) > 14:
        risk_factors.append(f"No login in {usage.get('last_login_days_ago')} days")
        churn_score += 20

    if usage.get("feature_adoption", 1) < 0.4:
        risk_factors.append(f"Low feature adoption ({usage.get('feature_adoption', 0)*100:.0f}%)")
        churn_score += 15

    if usage.get("nps_score", 50) < 0:
        risk_factors.append(f"Negative NPS score ({usage.get('nps_score')})")
        churn_score += 20

    if usage.get("daily_active_users", 100) < 20:
        risk_factors.append(f"Low DAU ({usage.get('daily_active_users')})")
        churn_score += 10

    # Support signals
    if account.get("support_tickets_open", 0) > 5:
        risk_factors.append(f"{account.get('support_tickets_open')} open support tickets")
        churn_score += 15

    if account.get("support_sentiment") == "negative":
        risk_factors.append("Negative support sentiment")
        churn_score += 15

    # Health score
    if account.get("health_score", 50) < 40:
        risk_factors.append(f"Low health score ({account.get('health_score')})")
        churn_score += 10

    churn_score = min(95, churn_score + random.uniform(5, 15))

    if churn_score >= 70:
        risk_level = "critical"
    elif churn_score >= 50:
        risk_level = "high"
    elif churn_score >= 30:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "churn_probability": round(churn_score, 1),
        "risk_level": risk_level,
        "risk_factors": risk_factors if risk_factors else ["No significant risk factors detected"],
        "usage_summary": usage,
        "health_score": account.get("health_score", 50),
        "mrr_at_risk": account.get("mrr", 0)
    }


def get_competitor_data(deal_id: int) -> Dict[str, Any]:
    """Get competitor intelligence for a deal"""
    deal = None
    for d in MOCK_DATA["deals"]:
        if d["id"] == deal_id:
            deal = d
            break

    if not deal:
        return {"error": f"Deal {deal_id} not found"}

    competitors = deal.get("competitor_mentions", [])
    if not competitors:
        competitors = [random.choice(["Salesforce", "HubSpot", "Pipedrive"])]

    competitor_profiles = {
        "Salesforce": {
            "strengths": ["Market leader", "Extensive ecosystem", "Enterprise features"],
            "weaknesses": ["Complex implementation", "High total cost of ownership", "Steep learning curve"],
            "pricing": "$$$$",
            "market_position": "Enterprise leader"
        },
        "HubSpot": {
            "strengths": ["Free tier", "User-friendly", "Marketing integration"],
            "weaknesses": ["Limited customization", "Expensive at scale", "Basic reporting"],
            "pricing": "$$-$$$",
            "market_position": "Mid-market leader"
        },
        "Pipedrive": {
            "strengths": ["Simple UI", "Sales-focused", "Affordable"],
            "weaknesses": ["Limited features", "Basic integrations", "No marketing tools"],
            "pricing": "$$",
            "market_position": "SMB focused"
        },
        "Zoho CRM": {
            "strengths": ["Affordable", "All-in-one suite", "Customizable"],
            "weaknesses": ["Complex interface", "Support quality varies", "Integration challenges"],
            "pricing": "$-$$",
            "market_position": "Value player"
        },
        "Freshsales": {
            "strengths": ["AI-powered", "Clean interface", "Good pricing"],
            "weaknesses": ["Limited market presence", "Fewer integrations", "Newer platform"],
            "pricing": "$$",
            "market_position": "Emerging challenger"
        }
    }

    results = []
    for comp in competitors:
        profile = competitor_profiles.get(comp, {
            "strengths": ["Established player in market"],
            "weaknesses": ["Limited differentiation"],
            "pricing": "$$",
            "market_position": "Competitor"
        })
        results.append({
            "name": comp,
            **profile,
            "threat_level": random.choice(["low", "medium", "high"]),
            "mentioned_in_engagements": random.randint(1, 5)
        })

    return {
        "deal_id": deal_id,
        "competitors": results,
        "primary_competitor": competitors[0],
        "competitive_pressure": "high" if len(competitors) >= 2 else "moderate"
    }


def generate_email(
    recipient_name: str,
    company_name: str,
    context: str,
    email_type: str = "outreach"
) -> str:
    """Generate a personalized email"""

    templates = {
        "outreach": f"""Subject: Accelerating Revenue Growth at {company_name}

Hi {recipient_name},

I noticed {company_name} has been making impressive strides in the industry. Given your current trajectory, I believe there's an opportunity to significantly accelerate your revenue operations.

Our AI-powered platform has helped similar companies:
• Increase pipeline velocity by 40%
• Reduce deal cycle time by 25%
• Improve forecast accuracy to 95%+

I'd love to share a quick 15-minute overview of how we've helped companies like yours transform their sales process. Would next Tuesday or Wednesday work for a brief call?

Best regards,
RevOps AI Team""",

        "follow_up": f"""Subject: Re: Quick follow-up — {company_name} revenue acceleration

Hi {recipient_name},

I wanted to follow up on my previous message about optimizing {company_name}'s revenue operations.

I came across some recent news about your company and thought this might be particularly relevant:

{context}

Our clients in similar situations have seen remarkable results within the first 90 days. I've attached a brief case study that mirrors your situation quite closely.

Would you have 10 minutes this week for a quick conversation?

Best,
RevOps AI Team""",

        "save": f"""Subject: We value our partnership with {company_name}

Dear {recipient_name},

I wanted to personally reach out because your team at {company_name} is incredibly important to us.

I understand there may have been some challenges recently:
{context}

I'd like to propose a few things:
1. A dedicated success manager assigned to your account
2. A custom training session for your team
3. A review of your current setup to optimize ROI

Your success is our priority, and I'd love to schedule a call to discuss how we can better support {company_name}.

Warm regards,
Customer Success Team
RevOps AI""",

        "competitive": f"""Subject: Why leading teams choose us over alternatives

Hi {recipient_name},

I understand you're evaluating options for {company_name}'s revenue operations stack, and I want to make sure you have complete information to make the best decision.

{context}

Here's what sets us apart:
• Purpose-built AI agents for every stage of the revenue cycle
• 2x faster time-to-value vs. traditional CRM solutions
• Dedicated customer success from day one
• Transparent, predictable pricing with no hidden costs

I'd be happy to arrange a side-by-side demo. When works best for you?

Best,
RevOps AI Team"""
    }

    return templates.get(email_type, templates["outreach"])
