"""
Decision Orchestrator Module
Makes final decision based on integrated analysis (replaces Malchut/Kingdom)
"""

import os
import json
import google.generativeai as genai
from typing import List
from dataclasses import dataclass


@dataclass
class Decision:
    """Final decision result"""
    approved: bool
    approval_type: str  # UNCONDITIONAL, CONDITIONAL, REJECTED
    confidence: float
    actions: List[str]
    conditions: List[str]
    reasoning: str


class DecisionOrchestrator:
    """
    Makes final decision on whether action should proceed

    Decision types:
    1. UNCONDITIONAL APPROVAL: Proceed without conditions
    2. CONDITIONAL APPROVAL: Proceed if conditions met
    3. REJECTED: Do not proceed

    Based on:
    - Readiness score from Integration Engine
    - Risk severity
    - Implementation feasibility
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def orchestrate(self, integration: 'IntegrationResult') -> Decision:
        """
        Make final decision

        Args:
            integration: Integrated analysis from Integration Engine

        Returns:
            Decision with approval/rejection and conditions
        """
        prompt = self._build_prompt(integration)

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.2,
                response_mime_type="application/json"
            )
        )

        result = json.loads(response.text)

        # Determine approval
        approval_type = result.get('approval_type', 'REJECTED')
        approved = approval_type in ['UNCONDITIONAL', 'CONDITIONAL']

        return Decision(
            approved=approved,
            approval_type=approval_type,
            confidence=result.get('confidence', 0.5),
            actions=result.get('actions', []),
            conditions=result.get('conditions', []),
            reasoning=result.get('reasoning', '')
        )

    def _build_prompt(self, integration: 'IntegrationResult') -> str:
        """Build decision orchestration prompt"""
        return f"""
You are a Decision Orchestrator making the FINAL CALL.

Your role: Decide if this action should MANIFEST in reality.

Integration summary:
- Readiness: {integration.readiness_score:.1%}
- Complexity: {integration.integration_complexity:.1%}
- Ready to manifest: {integration.ready_to_manifest}

Synthesis:
{integration.synthesis}

Decision framework:

UNCONDITIONAL APPROVAL:
- Readiness ≥ 80%
- Complexity ≤ 60%
- No critical risks
- Clear path forward
→ Proceed immediately

CONDITIONAL APPROVAL:
- Readiness 60-80%
- Complexity ≤ 80%
- Manageable risks
- Clear conditions that must be met
→ Proceed IF conditions satisfied

REJECTED:
- Readiness < 60%
- Complexity > 80%
- Critical risks unresolved
- Fundamental flaws
→ Do not proceed

Your decision MUST include:

1. APPROVAL_TYPE: "UNCONDITIONAL" | "CONDITIONAL" | "REJECTED"

2. CONFIDENCE (0.0 to 1.0):
   How confident are you in this decision?

3. ACTIONS (5-10 concrete actions):
   - If UNCONDITIONAL: What to do immediately
   - If CONDITIONAL: What to do once conditions met
   - If REJECTED: What to do instead (alternatives)

4. CONDITIONS (if CONDITIONAL, 3-7 conditions):
   - What MUST be true before proceeding?
   - Concrete, measurable conditions
   - Not vague aspirations

5. REASONING (2-3 paragraphs):
   - Why this decision?
   - What are the key factors?
   - What trade-offs were made?
   - What is the expected outcome?

CRITICAL: This is the FINAL decision that affects reality.
Be decisive but not reckless. Clear but nuanced.

Respond ONLY with JSON:
{{
    "approval_type": "UNCONDITIONAL|CONDITIONAL|REJECTED",
    "confidence": <0.0 to 1.0>,
    "actions": [
        "<action 1>",
        "<action 2>",
        "<action 3>",
        "<action 4>",
        "<action 5>"
    ],
    "conditions": [
        "<condition 1 (if CONDITIONAL)>",
        "<condition 2>",
        "<condition 3>"
    ],
    "reasoning": "<2-3 paragraph explanation of decision>"
}}
"""
