"""
Revenue Retention Agent (Churn Prediction) — Gemini-Powered
Input: usage metrics, support sentiment
Output: Churn probability, Intervention recommendation, Save email draft
"""
import asyncio
import random
from typing import Dict, Any
from agents.base_agent import BaseAgent
from tools.crm_tools import get_account_data, detect_churn, generate_email, analyze_engagement
from services.llm_service import is_gemini_available, gemini_churn_intervention


class ChurnAgent(BaseAgent):
    def __init__(self):
        super().__init__("Revenue Retention Agent")

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.start_execution()
        use_gemini = is_gemini_available()

        account_id = input_data.get("account_id")
        include_usage = input_data.get("include_usage", True)

        # Step 1: Collect account data
        self.log_step("collect", f"Fetching account data for account #{account_id}")
        await asyncio.sleep(0)
        account_data = get_account_data(account_id)

        if "error" in account_data:
            self.log_step("error", account_data["error"])
            return {"error": account_data["error"]}

        account = account_data["account"]
        self.log_step("found", f"Account: {account['company_name']}, MRR: ${account['mrr']:,.2f}")

        # Step 2: Run churn detection
        self.log_step("detect", "Running AI churn detection model")
        await asyncio.sleep(0)
        churn_result = detect_churn(account_id)
        self.log_step("scored", f"Churn probability: {churn_result['churn_probability']}%, Level: {churn_result['risk_level']}")

        # Step 3: Analyze engagement history
        self.log_step("engagement", "Analyzing recent engagement patterns")
        await asyncio.sleep(0)

        active_deals = account_data.get("active_deals", 0)

        health_signals = {
            "positive": [],
            "negative": []
        }

        usage = account.get("usage_metrics", {})
        if usage.get("feature_adoption", 0) > 0.7:
            health_signals["positive"].append("High feature adoption")
        else:
            health_signals["negative"].append("Low feature adoption")

        if usage.get("nps_score", 0) > 30:
            health_signals["positive"].append(f"Strong NPS ({usage.get('nps_score')})")
        elif usage.get("nps_score", 0) < 0:
            health_signals["negative"].append(f"Negative NPS ({usage.get('nps_score')})")

        if account.get("support_tickets_open", 0) > 5:
            health_signals["negative"].append(f"{account['support_tickets_open']} open support tickets")

        if active_deals > 0:
            health_signals["positive"].append(f"{active_deals} active deal(s) in pipeline")

        churn_prob = churn_result["churn_probability"]
        risk_level = churn_result["risk_level"]

        # Step 4: Generate intervention and save email with Gemini
        if use_gemini:
            self.log_step("gemini", "🤖 Generating intervention strategy & save email with Gemini AI...")
            gemini_result = await gemini_churn_intervention(
                account["company_name"], churn_prob,
                churn_result["risk_factors"], account["mrr"],
                account.get("health_score", 50)
            )
            if gemini_result:
                intervention = gemini_result.get("intervention", {})
                save_email = gemini_result.get("save_email_draft", "")
                self.log_step("generated", "✅ Gemini generated intervention strategy and save email")
            else:
                self.log_step("fallback", "Using template intervention")
                intervention = self._template_intervention(account, churn_prob, risk_level, churn_result)
                save_email = self._template_email(account, churn_result)
        else:
            self.log_step("intervention", "Determining intervention strategy (template mode)")
            intervention = self._template_intervention(account, churn_prob, risk_level, churn_result)
            save_email = self._template_email(account, churn_result)

        # Determine health trend
        if churn_prob >= 60:
            health_trend = "declining"
            predicted_window = "30-60 days"
        elif churn_prob >= 40:
            health_trend = "stable"
            predicted_window = "60-90 days"
        else:
            health_trend = "improving"
            predicted_window = "90+ days"

        self.log_step("complete", f"Analysis complete. Churn risk: {risk_level} {'[Gemini AI]' if use_gemini else '[Template]'}")

        return {
            "churn_probability": round(churn_prob, 1),
            "risk_level": risk_level,
            "risk_factors": churn_result["risk_factors"],
            "intervention": intervention,
            "save_email_draft": save_email,
            "health_trend": health_trend,
            "predicted_churn_window": predicted_window,
            "health_signals": health_signals,
            "ai_powered": use_gemini,
            "account_info": {
                "name": account["company_name"],
                "mrr": account["mrr"],
                "arr": account["arr"],
                "health_score": account["health_score"],
                "support_tickets": account.get("support_tickets_open", 0)
            },
            "execution": self.get_execution_summary()
        }

    def _template_intervention(self, account, churn_prob, risk_level, churn_result):
        """Fallback template intervention"""
        if risk_level == "critical":
            return {
                "type": "Executive Rescue Mission",
                "urgency": "immediate",
                "description": (
                    f"Account {account['company_name']} requires immediate executive attention. "
                    f"Churn probability is {churn_prob:.0f}% with ${account['mrr']:,.0f}/mo revenue at risk. "
                    f"Recommend VP-level intervention within 24 hours with a concrete save plan."
                ),
                "expected_impact": "Can reduce churn probability by 30-40% with rapid executive engagement"
            }
        elif risk_level == "high":
            return {
                "type": "Proactive Success Engagement",
                "urgency": "high",
                "description": (
                    f"Schedule an urgent QBR with {account['company_name']} to address {len(churn_result['risk_factors'])} risk signals. "
                    f"Focus on re-establishing value proposition and addressing pain points directly."
                ),
                "expected_impact": "Can reduce churn probability by 20-25% with proactive engagement"
            }
        elif risk_level == "medium":
            return {
                "type": "Health Check & Optimization",
                "urgency": "moderate",
                "description": (
                    f"Initiate a health check for {account['company_name']}. Focus on improving "
                    f"feature adoption and resolving open support tickets to prevent risk escalation."
                ),
                "expected_impact": "Can reduce churn probability by 10-15% with optimization support"
            }
        else:
            return {
                "type": "Relationship Nurture",
                "urgency": "low",
                "description": (
                    f"{account['company_name']} is in good health. Continue regular engagement, "
                    f"share product updates, and identify expansion opportunities."
                ),
                "expected_impact": "Maintains current retention probability and identifies growth potential"
            }

    def _template_email(self, account, churn_result):
        """Fallback template email"""
        context = "\n".join([f"- {f}" for f in churn_result["risk_factors"]])
        return generate_email(
            account.get("company_name", "Valued Customer").split()[0],
            account["company_name"],
            context,
            "save"
        )
