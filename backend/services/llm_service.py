"""
LLM Service - Gemini AI Integration (google-genai SDK)
Wraps Google Gemini for AI-powered text generation across all agents.
Includes retry logic with exponential backoff for rate limits.
Falls back to template-based responses if API fails.
"""
import os
import json
import time
import asyncio
from typing import Optional
from google import genai
from google.genai import types


# Global client
_client = None
_last_call_time = 0
_MIN_CALL_INTERVAL = 0.0  # seconds between API calls to respect rate limits


def get_client():
    """Get or initialize the Gemini client"""
    global _client
    if _client is None:
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not set. Please add it to your .env file.")
        _client = genai.Client(api_key=api_key)
    return _client


def is_gemini_available() -> bool:
    """Check if Gemini API is configured"""
    api_key = os.getenv("GOOGLE_API_KEY", "")
    provider = os.getenv("LLM_PROVIDER", "mock")
    return bool(api_key) and provider == "gemini"


async def _rate_limit_wait():
    """Ensure minimum interval between API calls"""
    global _last_call_time
    now = time.time()
    elapsed = now - _last_call_time
    if elapsed < _MIN_CALL_INTERVAL:
        await asyncio.sleep(_MIN_CALL_INTERVAL - elapsed)
    _last_call_time = time.time()


async def generate_text(prompt: str, max_tokens: int = 2048, retries: int = 3) -> str:
    """Generate text using Gemini API with retry logic"""
    for attempt in range(retries):
        try:
            await _rate_limit_wait()
            client = get_client()
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                wait_time = (attempt + 1) * 10  # 10s, 20s, 30s
                print(f"⏳ Gemini rate limited, retrying in {wait_time}s (attempt {attempt+1}/{retries})")
                await asyncio.sleep(wait_time)
            else:
                print(f"⚠️ Gemini API error: {e}")
                return ""
    print("⚠️ Gemini: Max retries exceeded, falling back to template")
    return ""


async def generate_json(prompt: str, max_tokens: int = 2048, retries: int = 3) -> Optional[dict]:
    """Generate structured JSON using Gemini API with retry logic"""
    for attempt in range(retries):
        try:
            await _rate_limit_wait()
            client = get_client()
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt + "\n\nIMPORTANT: Return ONLY valid JSON. No markdown, no code fences, no explanation.",
                config=types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.5,
                )
            )
            text = response.text.strip()
            # Clean up common issues
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            return json.loads(text)
        except json.JSONDecodeError:
            print(f"⚠️ Gemini returned non-JSON response, attempt {attempt+1}/{retries}")
            if attempt < retries - 1:
                await asyncio.sleep(2)
            continue
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                wait_time = (attempt + 1) * 10
                print(f"⏳ Gemini rate limited, retrying in {wait_time}s (attempt {attempt+1}/{retries})")
                await asyncio.sleep(wait_time)
            else:
                print(f"⚠️ Gemini API error: {e}")
                return None
    print("⚠️ Gemini: Max retries exceeded, falling back to template")
    return None


# ============================================================
# Agent-specific Gemini prompts
# ============================================================

async def gemini_prospect_email(company_name: str, contact_name: str, industry: str, lead_score: float, insights: list) -> str:
    """Generate a personalized prospecting email using Gemini"""
    prompt = f"""You are an expert B2B sales development representative. Write a personalized cold outreach email.

CONTEXT:
- Target Company: {company_name}
- Contact Name: {contact_name}
- Industry: {industry}
- AI Lead Score: {lead_score}/100
- Key Insights: {', '.join(insights)}

REQUIREMENTS:
- Keep it under 150 words
- Include a compelling subject line (format: "Subject: ...")
- Personalize based on the company and industry
- Include 2-3 specific value propositions
- End with a clear, low-commitment CTA (e.g., 15-min call)
- Professional but conversational tone
- Our product: AI-powered Revenue Operations platform that increases pipeline velocity by 40%

Write the email now:"""
    return await generate_text(prompt)


async def gemini_outreach_sequence(company_name: str, contact_name: str, industry: str, lead_score: float) -> Optional[list]:
    """Generate a 3-step outreach sequence using Gemini"""
    prompt = f"""You are an expert B2B sales strategist. Create a 3-step outreach sequence.

CONTEXT:
- Company: {company_name}
- Contact: {contact_name}
- Industry: {industry}
- Lead Score: {lead_score}/100

Return a JSON array with exactly 3 objects, each having:
- "step": number (1, 2, 3)
- "channel": "Email" or "LinkedIn"
- "timing": when to send (e.g., "Day 1", "Day 3", "Day 7")
- "subject": email subject or LinkedIn message topic
- "message": the full message content (100-150 words each)

Step 1 should be Email (initial outreach), Step 2 should be LinkedIn (connection + value), Step 3 should be Email (follow-up with case study).
Our product: AI-powered Revenue Operations platform."""
    return await generate_json(prompt)


async def gemini_deal_analysis(deal_name: str, stage: str, amount: float, risk_reasons: list, engagement_trend: str, competitors: list) -> Optional[dict]:
    """Generate deal risk analysis and recovery plan using Gemini"""
    prompt = f"""You are a senior sales strategist analyzing a B2B deal for risk.

DEAL CONTEXT:
- Deal: {deal_name}
- Stage: {stage}
- Value: ${amount:,.0f}
- Risk Signals: {json.dumps(risk_reasons)}
- Engagement Trend: {engagement_trend}
- Competitors: {json.dumps(competitors)}

Provide a JSON response with:
{{
  "deal_health_summary": "A 2-3 sentence summary of the deal's current health",
  "recovery_plan": [
    {{
      "action": "specific action name",
      "priority": "urgent|high|medium|standard",
      "talking_points": ["point 1", "point 2", "point 3", "point 4"],
      "timeline": "when to execute"
    }}
  ]
}}

Include 2-4 recovery actions. Make talking points specific and actionable. Focus on winning the deal."""
    return await generate_json(prompt)


async def gemini_churn_intervention(company_name: str, churn_probability: float, risk_factors: list, mrr: float, health_score: float) -> Optional[dict]:
    """Generate churn intervention strategy using Gemini"""
    prompt = f"""You are a customer success leader trying to save an at-risk B2B account.

ACCOUNT CONTEXT:
- Company: {company_name}
- Churn Probability: {churn_probability:.0f}%
- Risk Factors: {json.dumps(risk_factors)}
- Monthly Revenue (MRR): ${mrr:,.0f}
- Health Score: {health_score}/100

Provide a JSON response with:
{{
  "intervention": {{
    "type": "name of the intervention strategy",
    "urgency": "immediate|high|moderate|low",
    "description": "detailed 2-3 sentence description of what to do",
    "expected_impact": "expected outcome of the intervention"
  }},
  "save_email_draft": "A complete, personalized email to the customer (150-200 words). Include: acknowledgment of their challenges, 3 concrete actions you'll take, and a warm closing. Format with Subject line."
}}"""
    return await generate_json(prompt)


async def gemini_competitive_analysis(deal_name: str, primary_competitor: str, competitors: list, deal_amount: float, deal_stage: str) -> Optional[dict]:
    """Generate competitive intelligence using Gemini"""
    competitor_names = [c.get("name", c) if isinstance(c, dict) else c for c in competitors]
    prompt = f"""You are a competitive intelligence analyst for a B2B sales team.

DEAL CONTEXT:
- Deal: {deal_name}
- Value: ${deal_amount:,.0f}
- Stage: {deal_stage}
- Competitors in play: {json.dumps(competitor_names)}
- Primary Threat: {primary_competitor}

Our product: AI-powered Revenue Operations platform with 4 specialized AI agents for prospecting, deal intelligence, churn prediction, and competitive analysis.

Provide a JSON response with:
{{
  "competitive_positioning": "2-3 sentence positioning statement against the primary competitor",
  "battlecard": [
    {{
      "category": "category name (e.g., Product, Pricing, Support)",
      "our_strengths": ["strength 1", "strength 2", "strength 3"],
      "competitor_weaknesses": ["weakness 1", "weakness 2", "weakness 3"],
      "key_differentiators": ["differentiator 1", "differentiator 2", "differentiator 3"]
    }}
  ],
  "win_strategy": "A detailed 200-word win strategy with numbered steps for this specific deal",
  "objection_handlers": [
    {{
      "objection": "common objection the buyer might raise about choosing us over {primary_competitor}",
      "response": "persuasive response (2-3 sentences)"
    }}
  ]
}}

Include 3 battlecard categories, and 3-4 objection handlers. Make everything specific to competing against {primary_competitor}."""
    return await generate_json(prompt)
