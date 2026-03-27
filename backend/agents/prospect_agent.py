"""
Prospecting Agent — Gemini-Powered
Input: company name, industry, ICP
Output: Lead score, personalized email, 3-step outreach sequence
"""
import asyncio
import random
from typing import Dict, Any
from agents.base_agent import BaseAgent
from tools.crm_tools import (
    get_lead_by_company, score_lead, generate_email, get_crm_data
)
from services.llm_service import (
    is_gemini_available, gemini_prospect_email, gemini_outreach_sequence
)


class ProspectingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Prospecting Agent")

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.start_execution()
        use_gemini = is_gemini_available()

        company_name = input_data.get("company_name", "")
        industry = input_data.get("industry", "")
        icp_criteria = input_data.get("icp_criteria", {})
        contact_name = input_data.get("contact_name", "Decision Maker")
        contact_title = input_data.get("contact_title", "")

        # Step 1: Collect existing CRM data
        self.log_step("collect", f"Searching CRM for {company_name}")
        await asyncio.sleep(0)
        existing_lead = get_lead_by_company(company_name)
        has_existing = "error" not in existing_lead

        if has_existing:
            self.log_step("found", f"Found existing lead data for {company_name}", existing_lead)
            contact_name = existing_lead.get("contact_name", contact_name)
            contact_title = existing_lead.get("contact_title", contact_title)
            industry = existing_lead.get("industry", industry)

        # Step 2: Score the lead
        self.log_step("analyze", "Running AI lead scoring model")
        await asyncio.sleep(0)
        score_result = score_lead(company_name, industry, icp_criteria)
        lead_score = score_result["lead_score"]
        self.log_step("scored", f"Lead score: {lead_score}/100", score_result)

        # Step 3: Generate insights
        self.log_step("insights", "Generating key insights and approach")
        await asyncio.sleep(0)

        key_insights = [
            f"{company_name} operates in the {industry} space with strong growth indicators",
            f"ICP match score: {score_result['score_breakdown'].get('icp_match', 0)}/25",
            f"Industry alignment: {'High' if industry in ['SaaS', 'FinTech', 'AI/ML'] else 'Moderate'}",
        ]

        if has_existing:
            key_insights.append(f"Previous engagement status: {existing_lead.get('status', 'unknown')}")
            if existing_lead.get("tags"):
                key_insights.append(f"Tags: {', '.join(existing_lead['tags'])}")

        # Determine approach
        if lead_score >= 75:
            approach = "High-priority lead. Recommend direct executive outreach with value proposition focused on ROI and competitive advantage."
        elif lead_score >= 50:
            approach = "Moderate-priority lead. Recommend multi-touch approach starting with educational content, then building to a demo request."
        else:
            approach = "Lower-priority lead. Recommend nurture sequence with industry-relevant content to build awareness and engagement over time."

        # Step 4: Generate personalized email with Gemini
        if use_gemini:
            self.log_step("gemini", "🤖 Generating personalized email with Gemini AI...")
            email = await gemini_prospect_email(company_name, contact_name, industry, lead_score, key_insights)
            if not email:
                self.log_step("fallback", "Gemini unavailable, using template")
                email = generate_email(contact_name, company_name, f"Based on {company_name}'s position in {industry}", "outreach")
            else:
                self.log_step("generated", "✅ Gemini generated personalized email")
        else:
            self.log_step("generate", "Crafting personalized outreach email (template mode)")
            email = generate_email(contact_name, company_name, f"Based on {company_name}'s position in {industry}", "outreach")

        # Step 5: Build outreach sequence with Gemini
        if use_gemini:
            self.log_step("gemini_sequence", "🤖 Generating 3-step outreach sequence with Gemini AI...")
            gemini_sequence = await gemini_outreach_sequence(company_name, contact_name, industry, lead_score)
            if gemini_sequence and isinstance(gemini_sequence, list) and len(gemini_sequence) >= 3:
                outreach_sequence = gemini_sequence
                self.log_step("generated", "✅ Gemini generated 3-step outreach sequence")
            else:
                self.log_step("fallback", "Using template sequence")
                outreach_sequence = self._template_sequence(company_name, contact_name, industry, email)
        else:
            self.log_step("sequence", "Building 3-step outreach sequence (template mode)")
            outreach_sequence = self._template_sequence(company_name, contact_name, industry, email)

        self.log_step("complete", f"Prospecting analysis complete {'(Gemini AI)' if use_gemini else '(Template)'}")

        return {
            "lead_score": lead_score,
            "score_breakdown": score_result["score_breakdown"],
            "personalized_email": email,
            "outreach_sequence": outreach_sequence,
            "key_insights": key_insights,
            "recommended_approach": approach,
            "ai_powered": use_gemini,
            "execution": self.get_execution_summary()
        }

    def _template_sequence(self, company_name, contact_name, industry, email):
        """Fallback template-based outreach sequence"""
        return [
            {
                "step": 1,
                "channel": "Email",
                "timing": "Day 1",
                "subject": f"Accelerating Revenue Growth at {company_name}",
                "message": email
            },
            {
                "step": 2,
                "channel": "LinkedIn",
                "timing": "Day 3",
                "subject": "Connection Request + Value Message",
                "message": f"Hi {contact_name}, I came across {company_name}'s impressive work in {industry}. "
                           f"I help revenue teams like yours increase pipeline velocity by 40%. "
                           f"Would love to connect and share some insights relevant to your space. "
                           f"No pitch — just genuine value. Looking forward to connecting!"
            },
            {
                "step": 3,
                "channel": "Email",
                "timing": "Day 7",
                "subject": f"Case Study: How a {industry} Company Grew Revenue 3x",
                "message": generate_email(
                    contact_name, company_name,
                    f"Similar {industry} companies have seen 3x revenue growth within 6 months using our AI-powered approach.",
                    "follow_up"
                )
            }
        ]
