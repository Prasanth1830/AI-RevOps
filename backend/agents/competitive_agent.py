"""
Competitive Intelligence Agent — Gemini-Powered
Input: competitor mentions, deal context
Output: Competitor risk flag, Battlecard, Win strategy
"""
import asyncio
import random
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from tools.crm_tools import get_deal_data, get_competitor_data, generate_email, analyze_engagement
from services.llm_service import is_gemini_available, gemini_competitive_analysis


class CompetitiveAgent(BaseAgent):
    def __init__(self):
        super().__init__("Competitive Intelligence Agent")

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.start_execution()
        use_gemini = is_gemini_available()

        deal_id = input_data.get("deal_id")
        competitor_names = input_data.get("competitor_names", [])
        deal_context = input_data.get("deal_context", "")

        # Step 1: Collect deal data
        self.log_step("collect", f"Fetching deal and competitor data for deal #{deal_id}")
        await asyncio.sleep(0)
        deal_data = get_deal_data(deal_id)

        if "error" in deal_data:
            self.log_step("error", deal_data["error"])
            return {"error": deal_data["error"]}

        deal = deal_data["deal"]
        self.log_step("found", f"Deal: {deal['deal_name']}")

        # Step 2: Get competitor intelligence
        self.log_step("intel", "Gathering competitive intelligence from CRM")
        await asyncio.sleep(0)
        comp_data = get_competitor_data(deal_id)
        competitors = comp_data.get("competitors", [])

        if competitor_names:
            mentioned = [c for c in competitors if c["name"] in competitor_names]
            if not mentioned:
                for name in competitor_names:
                    competitors.append({
                        "name": name,
                        "strengths": ["Known player in market"],
                        "weaknesses": ["May lack specific capabilities"],
                        "pricing": "$$",
                        "threat_level": "medium",
                        "market_position": "Competitor"
                    })

        self.log_step("competitors_found", f"Identified {len(competitors)} competitor(s)")

        # Step 3: Determine competitive risk
        self.log_step("risk_assess", "Assessing competitive risk level")
        await asyncio.sleep(0)

        high_threat = [c for c in competitors if c.get("threat_level") == "high"]
        if len(high_threat) >= 2:
            risk_flag = "critical"
        elif len(high_threat) == 1:
            risk_flag = "high"
        elif len(competitors) >= 2:
            risk_flag = "medium"
        elif len(competitors) == 1:
            risk_flag = "low"
        else:
            risk_flag = "low"

        primary_competitor = competitors[0]["name"] if competitors else "None identified"
        self.log_step("risk_result", f"Competitive risk: {risk_flag}, Primary: {primary_competitor}")

        # Step 4: Generate full competitive analysis with Gemini
        if use_gemini:
            self.log_step("gemini", f"🤖 Generating competitive analysis vs {primary_competitor} with Gemini AI...")
            gemini_result = await gemini_competitive_analysis(
                deal["deal_name"], primary_competitor, competitors,
                deal["amount"], deal["stage"]
            )
            if gemini_result:
                competitive_positioning = gemini_result.get("competitive_positioning", "")
                battlecard = gemini_result.get("battlecard", [])
                win_strategy = gemini_result.get("win_strategy", "")
                objection_handlers = gemini_result.get("objection_handlers", [])
                self.log_step("generated", "✅ Gemini generated battlecards, win strategy, and objection handlers")
            else:
                self.log_step("fallback", "Using template competitive analysis")
                competitive_positioning, battlecard, win_strategy, objection_handlers = self._template_analysis(
                    primary_competitor, competitors, deal, risk_flag
                )
        else:
            self.log_step("template", "Generating competitive analysis (template mode)")
            competitive_positioning, battlecard, win_strategy, objection_handlers = self._template_analysis(
                primary_competitor, competitors, deal, risk_flag
            )

        self.log_step("complete", f"Competitive analysis complete {'[Gemini AI]' if use_gemini else '[Template]'}")

        return {
            "competitor_risk_flag": risk_flag,
            "primary_competitor": primary_competitor,
            "battlecard": battlecard,
            "win_strategy": win_strategy,
            "objection_handlers": objection_handlers,
            "competitive_positioning": competitive_positioning,
            "competitors_analyzed": [c["name"] if isinstance(c, dict) else c for c in competitors],
            "ai_powered": use_gemini,
            "deal_info": {
                "name": deal["deal_name"],
                "stage": deal["stage"],
                "amount": deal["amount"]
            },
            "execution": self.get_execution_summary()
        }

    def _template_analysis(self, primary_competitor, competitors, deal, risk_flag):
        """Fallback template-based competitive analysis"""
        competitive_positioning = (
            f"Against {primary_competitor}, position as the AI-native alternative that delivers "
            f"faster time-to-value, lower TCO, and genuinely autonomous AI capabilities. "
            f"Key message: 'While others add AI features to old platforms, we built the platform around AI.'"
        )

        battlecard = [
            {
                "category": "Product & Technology",
                "our_strengths": [
                    "AI-native architecture with multi-agent system",
                    "Real-time signal processing and analysis",
                    "Unified platform for entire revenue cycle",
                    "Custom AI models trained on your data"
                ],
                "competitor_weaknesses": [
                    f"{primary_competitor}: Legacy architecture with bolted-on AI",
                    "Limited real-time processing capabilities",
                    "Siloed tools requiring multiple integrations",
                    "Generic models not customizable"
                ],
                "key_differentiators": [
                    "4 specialized AI agents vs. single-purpose tools",
                    "Autonomous action-taking, not just insights",
                    "Sub-second analysis vs. batch processing",
                    "No-code customization for revenue teams"
                ]
            },
            {
                "category": "Pricing & Value",
                "our_strengths": [
                    "Transparent, predictable pricing",
                    "All features included in base plan",
                    "No per-user premium for AI features",
                    "ROI guarantee: 3x pipeline increase"
                ],
                "competitor_weaknesses": [
                    f"{primary_competitor}: Hidden costs and add-on pricing",
                    "AI features locked behind premium tiers",
                    "Per-seat pricing scales poorly",
                    "Long implementation increasing TCO"
                ],
                "key_differentiators": [
                    "50% lower total cost of ownership",
                    "2-week deployment vs. 3-6 month implementation",
                    "Unlimited AI agent runs included",
                    "Free migration and onboarding"
                ]
            },
            {
                "category": "Customer Success",
                "our_strengths": [
                    "98% customer retention rate",
                    "Dedicated success manager from day one",
                    "Average 40% pipeline velocity increase",
                    "Industry-leading NPS of 72"
                ],
                "competitor_weaknesses": [
                    f"{primary_competitor}: Support tiered by plan level",
                    "High customer churn in first year",
                    "Limited onboarding resources",
                    "Slow response to support tickets"
                ],
                "key_differentiators": [
                    "24/7 premium support for all customers",
                    "Proactive health monitoring and alerts",
                    "Quarterly business reviews with ROI reporting",
                    "Customer community with 10K+ members"
                ]
            }
        ]

        if risk_flag in ["critical", "high"]:
            win_strategy = (
                f"🎯 HIGH-PRIORITY WIN STRATEGY vs. {primary_competitor}\n\n"
                f"1. IMMEDIATE ACTIONS (This Week):\n"
                f"   • Schedule competitive demo showcasing AI agent capabilities\n"
                f"   • Prepare custom ROI analysis comparing TCO vs {primary_competitor}\n"
                f"   • Identify and engage executive champion for internal advocacy\n\n"
                f"2. DIFFERENTIATION PLAY (Week 1-2):\n"
                f"   • Run live AI agent demo with their actual data (sandbox)\n"
                f"   • Provide 3 customer references in similar industry\n"
                f"   • Share analyst report positioning us vs {primary_competitor}\n\n"
                f"3. CLOSING STRATEGY (Week 2-4):\n"
                f"   • Offer pilot program with success metrics\n"
                f"   • Present migration plan from {primary_competitor}\n"
                f"   • CEO-to-CEO call to establish partnership vision\n"
                f"   • Create urgency with time-limited promotion"
            )
        else:
            win_strategy = (
                f"📋 STANDARD WIN STRATEGY\n\n"
                f"1. POSITIONING:\n"
                f"   • Lead with AI-native advantage and time-to-value\n"
                f"   • Emphasize total cost of ownership benefits\n"
                f"   • Focus on unique multi-agent approach\n\n"
                f"2. PROOF POINTS:\n"
                f"   • Share relevant case studies and metrics\n"
                f"   • Offer 14-day free trial with full AI access\n"
                f"   • Provide analyst/review comparisons\n\n"
                f"3. RISK MITIGATION:\n"
                f"   • Address any competitor FUD proactively\n"
                f"   • Demonstrate integration capabilities\n"
                f"   • Show customer success track record"
            )

        objection_handlers = [
            {
                "objection": f"We're already evaluating {primary_competitor}",
                "response": f"That's great — it means you recognize the need for a solution in this space. Many of our best customers evaluated {primary_competitor} first. The key difference they found was our AI-native architecture delivers results in days, not months. Would you be open to a 15-minute side-by-side comparison?"
            },
            {
                "objection": f"{primary_competitor} has more market presence",
                "response": "Market presence is important, but what matters more is results. Our customers see 40% faster pipeline velocity on average. We'd love to show you concrete ROI numbers from companies in your industry."
            },
            {
                "objection": "Your company is newer/smaller",
                "response": "Being purpose-built for AI-powered revenue operations is actually our advantage. We're not retrofitting AI onto a 20-year-old CRM — we built from the ground up. That's why our customers see results 3x faster."
            },
            {
                "objection": "The pricing seems different",
                "response": "Let's look at total cost of ownership. When you factor in implementation time, training, add-on costs, and the productivity gains from AI automation, our customers typically save 50% compared to legacy solutions."
            }
        ]

        return competitive_positioning, battlecard, win_strategy, objection_handlers
