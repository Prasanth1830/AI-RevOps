"""
Deal Intelligence Agent — Gemini-Powered
Input: deal data, engagement logs
Output: Risk score, Risk reasons, Recovery plan with talking points
"""
import asyncio
import random
from typing import Dict, Any
from agents.base_agent import BaseAgent
from tools.crm_tools import get_deal_data, analyze_engagement, get_competitor_data
from services.llm_service import is_gemini_available, gemini_deal_analysis


class DealIntelligenceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Deal Intelligence Agent")

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.start_execution()
        use_gemini = is_gemini_available()

        deal_id = input_data.get("deal_id")
        include_engagements = input_data.get("include_engagements", True)

        # Step 1: Collect deal data
        self.log_step("collect", f"Fetching deal data for deal #{deal_id}")
        await asyncio.sleep(0)
        deal_data = get_deal_data(deal_id)

        if "error" in deal_data:
            self.log_step("error", deal_data["error"])
            return {"error": deal_data["error"]}

        deal = deal_data["deal"]
        account = deal_data.get("account", {})
        self.log_step("found", f"Deal: {deal['deal_name']}, Stage: {deal['stage']}, Amount: ${deal['amount']:,.2f}")

        # Step 2: Analyze engagement patterns
        self.log_step("analyze_engagement", "Analyzing engagement patterns and sentiment")
        await asyncio.sleep(0)
        engagement_analysis = analyze_engagement(deal_id) if include_engagements else {}
        self.log_step("engagement_result", f"Engagement trend: {engagement_analysis.get('trend', 'N/A')}")

        # Step 3: Check competitive landscape
        self.log_step("competitive_check", "Checking competitive landscape")
        await asyncio.sleep(0)
        competitor_data = get_competitor_data(deal_id)
        has_competitors = len(deal.get("competitor_mentions", [])) > 0

        # Step 4: Calculate risk score
        self.log_step("risk_calc", "Calculating comprehensive risk score")
        await asyncio.sleep(0)

        risk_score = 0
        risk_reasons = []

        # Stage risk
        stage_risk = {
            "discovery": 15, "qualification": 10, "proposal": 20,
            "negotiation": 25, "closed_won": 0, "closed_lost": 100
        }
        risk_score += stage_risk.get(deal["stage"], 15)

        # Engagement risk
        eng_sentiment = engagement_analysis.get("avg_sentiment", 0)
        if eng_sentiment < -0.2:
            risk_score += 20
            risk_reasons.append("Negative engagement sentiment trend detected")
        elif eng_sentiment < 0.1:
            risk_score += 10
            risk_reasons.append("Neutral/declining engagement sentiment")

        if engagement_analysis.get("engagement_frequency", 0) < 3:
            risk_score += 15
            risk_reasons.append("Low engagement frequency — buyer may be disengaged")

        eng_trend = engagement_analysis.get("trend", "stable")
        if eng_trend == "declining":
            risk_score += 15
            risk_reasons.append("Declining engagement trend over recent period")

        # Competitive risk
        if has_competitors:
            risk_score += len(deal["competitor_mentions"]) * 8
            risk_reasons.append(f"Active competitors: {', '.join(deal['competitor_mentions'])}")

        # Deal-specific risk
        existing_risks = deal.get("risk_reasons", [])
        for r in existing_risks[:3]:
            risk_reasons.append(r)
            risk_score += 5

        # Probability mismatch
        if deal["probability"] > 0.7 and risk_score > 50:
            risk_reasons.append("Probability appears overstated given risk signals")
            risk_score += 10

        risk_score = min(100, risk_score + random.uniform(0, 10))

        # Determine risk level
        if risk_score >= 75:
            risk_level = "critical"
        elif risk_score >= 50:
            risk_level = "high"
        elif risk_score >= 25:
            risk_level = "medium"
        else:
            risk_level = "low"

        # Step 5: Generate recovery plan with Gemini
        if use_gemini:
            self.log_step("gemini", "🤖 Generating recovery plan with Gemini AI...")
            gemini_result = await gemini_deal_analysis(
                deal["deal_name"], deal["stage"], deal["amount"],
                risk_reasons, eng_trend, deal.get("competitor_mentions", [])
            )
            if gemini_result:
                health_summary = gemini_result.get("deal_health_summary", "")
                recovery_plan = gemini_result.get("recovery_plan", [])
                self.log_step("generated", "✅ Gemini generated deal analysis and recovery plan")
            else:
                self.log_step("fallback", "Using template recovery plan")
                health_summary, recovery_plan = self._template_recovery(deal, risk_level, risk_reasons, risk_score, eng_trend)
        else:
            self.log_step("recovery", "Generating recovery plan (template mode)")
            health_summary, recovery_plan = self._template_recovery(deal, risk_level, risk_reasons, risk_score, eng_trend)

        self.log_step("complete", f"Analysis complete. Risk: {risk_level} ({risk_score:.0f}/100) {'[Gemini AI]' if use_gemini else '[Template]'}")

        return {
            "risk_score": round(risk_score, 1),
            "risk_level": risk_level,
            "risk_reasons": risk_reasons,
            "recovery_plan": recovery_plan,
            "deal_health_summary": health_summary,
            "engagement_trend": eng_trend,
            "ai_powered": use_gemini,
            "deal_info": {
                "name": deal["deal_name"],
                "stage": deal["stage"],
                "amount": deal["amount"],
                "owner": deal["owner"],
                "probability": deal["probability"]
            },
            "execution": self.get_execution_summary()
        }

    def _template_recovery(self, deal, risk_level, risk_reasons, risk_score, eng_trend):
        """Fallback template-based recovery plan"""
        health_summary = (
            f"Deal '{deal['deal_name']}' is currently at {deal['stage']} stage with "
            f"${deal['amount']:,.0f} at stake. Risk assessment indicates {risk_level} risk "
            f"(score: {risk_score:.0f}/100) based on {len(risk_reasons)} identified signals. "
            f"Engagement trend is {eng_trend}."
        )

        recovery_plan = []
        if risk_level in ["critical", "high"]:
            recovery_plan.append({
                "action": "Executive Sponsor Meeting",
                "priority": "urgent",
                "talking_points": [
                    f"Address the {len(risk_reasons)} identified risk factors directly",
                    f"Reaffirm commitment to {deal['deal_name']} success",
                    "Propose revised timeline with clear milestones",
                    "Offer executive-to-executive alignment call"
                ],
                "timeline": "Within 48 hours"
            })
            recovery_plan.append({
                "action": "Competitive Displacement Strategy",
                "priority": "high",
                "talking_points": [
                    "Present updated ROI analysis vs. competitors",
                    "Share customer success stories from similar companies",
                    "Offer pilot/POC extension if needed",
                    "Highlight unique differentiators and integration advantages"
                ],
                "timeline": "Within 1 week"
            })

        if risk_level in ["critical", "high", "medium"]:
            recovery_plan.append({
                "action": "Re-engagement Campaign",
                "priority": "medium",
                "talking_points": [
                    "Schedule technical deep-dive with their team",
                    f"Address specific concern: {risk_reasons[0] if risk_reasons else 'general engagement'}",
                    "Provide additional case studies and social proof",
                    "Propose joint success criteria and timeline"
                ],
                "timeline": "Within 2 weeks"
            })

        recovery_plan.append({
            "action": "Deal Review & Pipeline Update",
            "priority": "standard",
            "talking_points": [
                f"Update deal probability from {deal['probability']*100:.0f}% based on risk assessment",
                "Document all stakeholder concerns",
                "Define clear next steps with dates",
                "Set up regular check-in cadence"
            ],
            "timeline": "Ongoing"
        })

        return health_summary, recovery_plan
