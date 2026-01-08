"""
Risk Assessor Module
Assesses risks, constraints, and boundaries (replaces Gevurah/Strength)
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class RiskAssessment:
    """Risk assessment result"""
    risks: List[str]
    constraints: List[str]
    warnings: List[str]
    severity_score: float


class RiskAssessor:
    """
    Assesses risks, constraints, and sets boundaries

    Evaluates:
    1. What could go wrong?
    2. What are the constraints?
    3. What warnings must be heeded?
    4. How severe are the risks?
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def assess(
        self,
        scenario: Dict[str, str],
        perspective_comparison: 'PerspectiveComparison'
    ) -> RiskAssessment:
        """
        Assess risks and constraints

        Args:
            scenario: Original scenario
            perspective_comparison: Multi-perspective analysis

        Returns:
            RiskAssessment with identified risks
        """
        prompt = self._build_prompt(scenario, perspective_comparison)

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.5,
                response_mime_type="application/json"
            )
        )

        result = json.loads(response.text)

        return RiskAssessment(
            risks=result.get('risks', []),
            constraints=result.get('constraints', []),
            warnings=result.get('warnings', []),
            severity_score=result.get('severity_score', 0.5)
        )

    def _build_prompt(
        self,
        scenario: Dict[str, str],
        perspective_comparison: 'PerspectiveComparison'
    ) -> str:
        """Build risk assessment prompt"""
        return f"""
You are a Risk Assessor focused on DISCIPLINE and BOUNDARIES.

Your role: Identify what could go WRONG, set LIMITS, establish CONSTRAINTS.

Analysis framework:

1. RISKS (5-10 specific risks):
   - Technical risks (implementation failures)
   - Social risks (public backlash, unintended consequences)
   - Ethical risks (moral hazards, slippery slopes)
   - Political risks (regulatory, legal challenges)
   - Economic risks (costs, sustainability)

   For each risk:
   - Be specific (not vague)
   - Estimate likelihood (LOW/MEDIUM/HIGH)
   - Estimate impact (LOW/MEDIUM/HIGH/CRITICAL)

2. CONSTRAINTS (hard boundaries):
   - Legal/regulatory constraints
   - Technical constraints
   - Resource constraints
   - Ethical red lines (non-negotiable limits)

3. WARNINGS (things that MUST be addressed):
   - Deal-breakers if ignored
   - Critical dependencies
   - Assumptions that could be wrong
   - Time bombs (delayed consequences)

4. SEVERITY_SCORE (0.0 to 1.0):
   - How severe are the risks overall?
   - 0.0 = negligible risks
   - 0.5 = moderate risks (manageable)
   - 1.0 = catastrophic risks (unacceptable)

CRITICAL: Be rigorous but not paranoid. Real risks, not imagined.

Synthesis from previous analysis:
{perspective_comparison.synthesis}

Scenario:
ACTION: {scenario.get('action', '')}
CONTEXT: {scenario.get('context', '')}

Respond ONLY with JSON:
{{
    "risks": [
        {{
            "risk": "<specific risk>",
            "likelihood": "LOW|MEDIUM|HIGH",
            "impact": "LOW|MEDIUM|HIGH|CRITICAL",
            "description": "<details>"
        }}
    ],
    "constraints": [
        "<constraint 1>",
        "<constraint 2>",
        "<constraint 3>"
    ],
    "warnings": [
        "<warning 1>",
        "<warning 2>",
        "<warning 3>"
    ],
    "severity_score": <0.0 to 1.0>
}}
"""
