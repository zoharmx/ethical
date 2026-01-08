"""
Conflict Resolver Module
Resolves conflicts between opportunities and risks (replaces Tiferet/Beauty)
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ConflictResolution:
    """Conflict resolution result"""
    conflicts_resolved: List[Dict[str, str]]
    balanced_path: str
    harmony_score: float


class ConflictResolver:
    """
    Resolves conflicts between expansion (opportunities) and discipline (risks)

    Finds the balanced path that:
    1. Maximizes opportunities
    2. Respects constraints
    3. Achieves harmony
    4. Creates aesthetic coherence
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def resolve(
        self,
        opportunity_assessment: 'OpportunityAssessment',
        risk_assessment: 'RiskAssessment'
    ) -> ConflictResolution:
        """
        Resolve conflicts between opportunities and risks

        Args:
            opportunity_assessment: Identified opportunities
            risk_assessment: Identified risks

        Returns:
            ConflictResolution with balanced approach
        """
        prompt = self._build_prompt(opportunity_assessment, risk_assessment)

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.6,
                response_mime_type="application/json"
            )
        )

        result = json.loads(response.text)

        return ConflictResolution(
            conflicts_resolved=result.get('conflicts_resolved', []),
            balanced_path=result.get('balanced_path', ''),
            harmony_score=result.get('harmony_score', 0.5)
        )

    def _build_prompt(
        self,
        opportunity_assessment: 'OpportunityAssessment',
        risk_assessment: 'RiskAssessment'
    ) -> str:
        """Build conflict resolution prompt"""
        return f"""
You are a Conflict Resolver focused on BALANCE and HARMONY.

Your role: Find the BALANCED PATH between expansion and discipline.

You have two forces in tension:

EXPANSION (Opportunities):
- Opportunities: {len(opportunity_assessment.opportunities)} identified
- Compassion score: {opportunity_assessment.compassion_score:.1%}
- Expansion potential: {opportunity_assessment.expansion_potential}

DISCIPLINE (Risks):
- Risks: {len(risk_assessment.risks)} identified
- Severity score: {risk_assessment.severity_score:.1%}
- Constraints: {len(risk_assessment.constraints)} hard boundaries
- Warnings: {len(risk_assessment.warnings)} critical warnings

Analysis framework:

1. CONFLICTS_RESOLVED (identify and resolve):
   For each major conflict between opportunity and risk:
   {{
       "opportunity": "<which opportunity>",
       "risk": "<which risk conflicts with it>",
       "resolution": "<how to resolve the tension>",
       "trade_off": "<what is being balanced>"
   }}

2. BALANCED_PATH:
   - Not compromise (weakening both sides)
   - But INTEGRATION (finding third way)
   - How to pursue opportunities WHILE respecting constraints?
   - What is the elegant solution that honors both?

3. HARMONY_SCORE (0.0 to 1.0):
   - How well are forces balanced?
   - 0.0 = irreconcilable conflict
   - 0.5 = workable compromise
   - 1.0 = elegant integration (both sides strengthened)

CRITICAL: The goal is AESTHETIC COHERENCE - a solution that feels
right, not just logically sound. Beauty = efficiency + elegance.

Opportunities to balance:
{json.dumps(opportunity_assessment.opportunities, indent=2)}

Risks to respect:
{json.dumps([r.get('risk', r) if isinstance(r, dict) else r for r in risk_assessment.risks], indent=2)}

Respond ONLY with JSON:
{{
    "conflicts_resolved": [
        {{
            "opportunity": "<opportunity>",
            "risk": "<risk>",
            "resolution": "<how to resolve>",
            "trade_off": "<what is balanced>"
        }}
    ],
    "balanced_path": "<integrated approach that honors both expansion and discipline>",
    "harmony_score": <0.0 to 1.0>
}}
"""
