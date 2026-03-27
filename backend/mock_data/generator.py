"""
Mock CRM Data Generator - Creates realistic B2B sales data
"""
import json
import random
from datetime import datetime, timedelta


def generate_mock_data():
    """Generate complete mock CRM dataset"""
    industries = [
        "SaaS", "FinTech", "HealthTech", "EdTech", "MarTech",
        "HR Tech", "Cybersecurity", "E-commerce", "AI/ML", "DevOps"
    ]
    company_sizes = ["1-50", "51-200", "201-500", "501-1000", "1001-5000", "5000+"]
    sources = ["Inbound", "Outbound", "Referral", "Event", "LinkedIn", "Webinar"]
    deal_stages = ["discovery", "qualification", "proposal", "negotiation", "closed_won", "closed_lost"]
    competitors = [
        "Salesforce", "HubSpot", "Pipedrive", "Zoho CRM", "Freshsales",
        "Monday.com", "Close.io", "Copper", "Insightly", "Nutshell"
    ]
    sentiments = ["positive", "neutral", "negative"]

    first_names = [
        "James", "Sarah", "Michael", "Emily", "David", "Jessica", "Robert",
        "Ashley", "William", "Amanda", "Daniel", "Stephanie", "Thomas",
        "Jennifer", "Christopher", "Lauren", "Matthew", "Rachel", "Andrew",
        "Nicole", "Joshua", "Megan", "Brandon", "Kayla", "Kevin",
        "Olivia", "Brian", "Hannah", "Jason", "Sophia", "Ryan", "Emma",
        "Mark", "Ava", "Eric", "Isabella", "Steven", "Mia", "Timothy",
        "Charlotte", "Jonathan", "Amelia", "Justin", "Harper", "Nathan",
        "Evelyn", "Adam", "Abigail", "Samuel", "Ella"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
        "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
        "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
        "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
        "Carter", "Roberts"
    ]
    titles = [
        "VP of Sales", "CRO", "Head of Revenue", "Sales Director",
        "VP of Marketing", "CMO", "Head of Growth", "Director of Operations",
        "CTO", "VP of Engineering", "Head of Product", "CEO", "COO",
        "Director of Sales", "Revenue Manager"
    ]
    company_names = [
        "TechFlow Inc", "DataStream Solutions", "CloudNine Systems",
        "QuantumLeap Technologies", "NexGen Analytics", "PulsePoint AI",
        "SkyBridge Software", "VelocityStack", "CoreSync Labs",
        "DigitalForge", "InnovatePro", "ScaleWorks", "ByteShift Corp",
        "PivotEdge", "LaunchPad Digital", "Horizon Labs",
        "ApexCloud", "MetricsMind", "Elevate.io", "Synapse Tech",
        "ClearPath Solutions", "Momentum Systems", "BrightWave AI",
        "Vertex Dynamics", "OmniFlow", "PeakPerformance Tech",
        "SwiftScale", "AtlasPoint", "Prism Analytics", "FusionGrid",
        "NovaBridge", "ZenithOps", "CatalystX", "WaveRunner Tech",
        "Beacon Digital", "SparkLane", "TrueNorth Systems", "Amplify.io",
        "Stratos Cloud", "Vantage AI", "IronClad Security", "Nimbus Data",
        "RedShift Labs", "Orbit Solutions", "Pinnacle Platforms",
        "FlowState Inc", "Radiant Systems", "BlueCore Tech",
        "Ascend Digital", "TerraForm Solutions"
    ]

    # Generate 50 leads
    leads = []
    for i in range(1, 51):
        first = random.choice(first_names)
        last = random.choice(last_names)
        company = company_names[i - 1] if i <= len(company_names) else f"Company {i}"
        leads.append({
            "id": i,
            "company_name": company,
            "contact_name": f"{first} {last}",
            "contact_email": f"{first.lower()}.{last.lower()}@{company.lower().replace(' ', '').replace('.', '')}.com",
            "contact_title": random.choice(titles),
            "industry": random.choice(industries),
            "company_size": random.choice(company_sizes),
            "annual_revenue": round(random.uniform(500000, 50000000), 2),
            "website": f"https://www.{company.lower().replace(' ', '').replace('.', '')}.com",
            "source": random.choice(sources),
            "status": random.choice(["new", "contacted", "qualified", "converted", "lost"]),
            "lead_score": round(random.uniform(10, 95), 1),
            "icp_match": round(random.uniform(0.3, 1.0), 2),
            "notes": f"Interested in our {random.choice(['enterprise', 'growth', 'starter'])} plan.",
            "tags": random.sample(["hot", "enterprise", "startup", "decision-maker", "technical", "budget-approved"], k=random.randint(1, 3)),
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 90))).isoformat()
        })

    # Generate 10 accounts
    accounts = []
    for i in range(1, 11):
        company = company_names[i - 1]
        base_date = datetime.now() - timedelta(days=random.randint(90, 730))
        usage = {
            "daily_active_users": random.randint(5, 200),
            "weekly_logins": random.randint(20, 1000),
            "feature_adoption": round(random.uniform(0.2, 0.95), 2),
            "api_calls_daily": random.randint(100, 50000),
            "storage_used_gb": round(random.uniform(1, 100), 1),
            "last_login_days_ago": random.randint(0, 30),
            "monthly_sessions": random.randint(50, 5000),
            "nps_score": random.randint(-20, 80)
        }
        accounts.append({
            "id": i,
            "company_name": company,
            "industry": random.choice(industries),
            "company_size": random.choice(company_sizes),
            "annual_revenue": round(random.uniform(1000000, 100000000), 2),
            "website": f"https://www.{company.lower().replace(' ', '').replace('.', '')}.com",
            "health_score": round(random.uniform(20, 95), 1),
            "mrr": round(random.uniform(1000, 50000), 2),
            "arr": round(random.uniform(12000, 600000), 2),
            "contract_start": base_date.isoformat(),
            "contract_end": (base_date + timedelta(days=365)).isoformat(),
            "usage_metrics": usage,
            "support_tickets_open": random.randint(0, 15),
            "support_sentiment": random.choice(sentiments),
            "last_engagement": (datetime.now() - timedelta(days=random.randint(0, 45))).isoformat(),
            "churn_risk": round(random.uniform(0.05, 0.85), 2),
            "tags": random.sample(["enterprise", "strategic", "at-risk", "growing", "champion", "renewal-soon"], k=random.randint(1, 3)),
            "created_at": base_date.isoformat()
        })

    # Generate 20 deals
    deals = []
    for i in range(1, 21):
        account_id = random.randint(1, 10)
        stage = random.choice(deal_stages)
        amount = round(random.uniform(5000, 500000), 2)
        owner_first = random.choice(first_names)
        owner_last = random.choice(last_names)
        created = datetime.now() - timedelta(days=random.randint(5, 120))
        expected_close = created + timedelta(days=random.randint(30, 180))
        risk_items = [
            "No executive sponsor identified",
            "Budget not confirmed",
            "Champion left the company",
            "Competitor actively engaged",
            "Timeline pushed back twice",
            "Low engagement in last 2 weeks",
            "Technical requirements unclear",
            "Legal review pending",
            "Multiple stakeholders not aligned",
            "POC results below expectations"
        ]
        deals.append({
            "id": i,
            "deal_name": f"{accounts[account_id - 1]['company_name']} - {random.choice(['Enterprise License', 'Growth Plan', 'Platform Upgrade', 'Annual Contract', 'Expansion Deal'])}",
            "account_id": account_id,
            "lead_id": random.randint(1, 50),
            "owner": f"{owner_first} {owner_last}",
            "stage": stage,
            "amount": amount,
            "probability": round(random.uniform(0.1, 0.95), 2),
            "expected_close_date": expected_close.isoformat(),
            "actual_close_date": (expected_close + timedelta(days=random.randint(-10, 30))).isoformat() if stage in ["closed_won", "closed_lost"] else None,
            "risk_score": round(random.uniform(0.1, 0.9), 2),
            "risk_reasons": random.sample(risk_items, k=random.randint(1, 4)),
            "competitor_mentions": random.sample(competitors, k=random.randint(0, 3)),
            "next_steps": random.choice([
                "Schedule executive alignment call",
                "Send revised proposal with updated pricing",
                "Demo advanced analytics features",
                "Follow up on technical evaluation",
                "Prepare ROI analysis presentation"
            ]),
            "notes": f"Key deal for Q{random.randint(1, 4)} pipeline.",
            "tags": random.sample(["high-value", "at-risk", "fast-track", "strategic", "renewal"], k=random.randint(1, 2)),
            "created_at": created.isoformat()
        })

    # Generate engagements
    engagements = []
    eng_types = ["email", "call", "meeting", "demo", "support"]
    eng_id = 1
    for deal in deals:
        num_engagements = random.randint(3, 8)
        for _ in range(num_engagements):
            eng_date = datetime.now() - timedelta(days=random.randint(0, 60))
            engagements.append({
                "id": eng_id,
                "deal_id": deal["id"],
                "account_id": deal["account_id"],
                "lead_id": deal["lead_id"],
                "type": random.choice(eng_types),
                "direction": random.choice(["inbound", "outbound"]),
                "subject": random.choice([
                    "Follow-up on proposal discussion",
                    "Technical requirements review",
                    "Pricing negotiation call",
                    "Product demo walkthrough",
                    "Support ticket escalation",
                    "Quarterly business review",
                    "Contract renewal discussion",
                    "Feature request discussion",
                    "ROI analysis presentation",
                    "Executive sponsor introduction"
                ]),
                "sentiment": random.choice(sentiments),
                "sentiment_score": round(random.uniform(-1, 1), 2),
                "duration_minutes": random.randint(5, 60),
                "outcome": random.choice([
                    "Positive response, moving forward",
                    "Needs more information",
                    "Deferred to next quarter",
                    "Agreed to next steps",
                    "Escalated to management",
                    "No response yet"
                ]),
                "logged_by": f"{random.choice(first_names)} {random.choice(last_names)}",
                "engagement_date": eng_date.isoformat()
            })
            eng_id += 1

    return {
        "leads": leads,
        "accounts": accounts,
        "deals": deals,
        "engagements": engagements
    }


def save_mock_data():
    """Save mock data to JSON files"""
    data = generate_mock_data()
    for key, value in data.items():
        with open(f"mock_data/{key}.json", "w") as f:
            json.dump(value, f, indent=2, default=str)
    return data


# Generate on import
MOCK_DATA = generate_mock_data()

if __name__ == "__main__":
    save_mock_data()
    print(f"Generated: {len(MOCK_DATA['leads'])} leads, {len(MOCK_DATA['accounts'])} accounts, "
          f"{len(MOCK_DATA['deals'])} deals, {len(MOCK_DATA['engagements'])} engagements")
