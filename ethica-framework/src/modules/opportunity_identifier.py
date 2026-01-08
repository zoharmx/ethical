"""
Opportunity Identifier Module
Identifies positive opportunities and beneficiaries (replaces Chesed/Kindness)
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class OpportunityAssessment:
    """Opportunity identification result"""
    opportunities: List[str]
    beneficiaries: List[str]
    expansion_potential: str
    compassion_score: float


class OpportunityIdentifier:
    """
    Identifies opportunities for positive impact and benefit expansion

    Evaluates:
    1. What opportunities does this open?
    2. Who benefits and how?
    3. How can benefits be expanded?
    4. What is the compassion quotient?
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def identify(
        self,
        scenario: Dict[str, str],
        perspective_comparison: 'PerspectiveComparison'
    ) -> OpportunityAssessment:
        """
        Identify opportunities for positive impact

        Args:
            scenario: Original scenario
            perspective_comparison: Multi-perspective analysis

        Returns:
            OpportunityAssessment with identified opportunities
        """
        prompt = self._build_prompt(scenario, perspective_comparison)

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                response_mime_type="application/json"
            )
        )

        result = json.loads(response.text)

        return OpportunityAssessment(
            opportunities=result.get('opportunities', []),
            beneficiaries=result.get('beneficiaries', []),
            expansion_potential=result.get('expansion_potential', ''),
            compassion_score=result.get('compassion_score', 0.5)
        )

    def _build_prompt(
        self,
        scenario: Dict[str, str],
        perspective_comparison: 'PerspectiveComparison'
    ) -> str:
        """Build opportunity identification prompt"""
        return f"""
You are an Opportunity Identifier focused on EXPANSION and COMPASSION.

Your role: Identify ways this scenario can CREATE VALUE, not just avoid harm.

Analysis framework:

1. OPPORTUNITIES (5-7 concrete opportunities):
   - What positive outcomes could emerge?
   - What problems could be solved?
   - What innovations are enabled?
   - What precedents for good could be set?

2. BENEFICIARIES (List all who benefit):
   - Direct beneficiaries
   - Indirect beneficiaries
   - Unexpected beneficiaries
   - How each group benefits

3. EXPANSION_POTENTIAL:
   - How can benefits be MAXIMIZED?
   - Who else could benefit with modifications?
   - What adjacent opportunities exist?
   - How can this scale for greater good?

4. COMPASSION_SCORE (0.0 to 1.0):
   - How much does this embody generosity and care?
   - Is it giving more than minimum required?
   - Does it show genuine concern for wellbeing?

CRITICAL: Be optimistic but realistic. Find genuine opportunities,
not forced positivity.

Synthesis from previous analysis:
{perspective_comparison.synthesis}

Scenario:
ACTION: {scenario.get('action', '')}
CONTEXT: {scenario.get('context', '')}

Respond ONLY with JSON:
{{
    "opportunities": [
        "<opportunity 1>",
        "<opportunity 2>",
        "<opportunity 3>",
        "<opportunity 4>",
        "<opportunity 5>",
        "<opportunity 6>",
        "<opportunity 7>"
    ],
    "beneficiaries": [
        "<beneficiary group>: <how they benefit>",
        "<beneficiary group>: <how they benefit>",
        "<beneficiary group>: <how they benefit>"
    ],
    "expansion_potential": "<how to maximize benefits>",
    "compassion_score": <0.0 to 1.0>
}}
"""
