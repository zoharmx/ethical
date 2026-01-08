"""
Implementation Planner Module
Plans concrete implementation steps with precision (replaces Hod/Glory)
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ImplementationPlan:
    """Implementation plan result"""
    phases: List[Dict[str, str]]
    precision_score: float
    known_unknowns: List[str]


class ImplementationPlanner:
    """
    Plans concrete implementation with precision and detail

    Creates:
    1. Phased implementation plan
    2. Concrete, measurable steps
    3. Dependencies and sequencing
    4. Known unknowns (epistemic humility)
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def plan(
        self,
        scenario: Dict[str, str],
        conflict_resolution: 'ConflictResolution'
    ) -> ImplementationPlan:
        """
        Create detailed implementation plan

        Args:
            scenario: Original scenario
            conflict_resolution: Balanced approach

        Returns:
            ImplementationPlan with phased approach
        """
        prompt = self._build_prompt(scenario, conflict_resolution)

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.4,
                response_mime_type="application/json"
            )
        )

        result = json.loads(response.text)

        return ImplementationPlan(
            phases=result.get('phases', []),
            precision_score=result.get('precision_score', 0.5),
            known_unknowns=result.get('known_unknowns', [])
        )

    def _build_prompt(
        self,
        scenario: Dict[str, str],
        conflict_resolution: 'ConflictResolution'
    ) -> str:
        """Build implementation planning prompt"""
        return f"""
You are an Implementation Planner focused on PRECISION and DETAIL.

Your role: Create CONCRETE, ACTIONABLE implementation plan.

Analysis framework:

1. PHASES (4-6 implementation phases):
   Each phase MUST have:
   {{
       "phase_name": "<descriptive name>",
       "timeline": "<realistic timeframe>",
       "objectives": ["<measurable objective 1>", "<measurable objective 2>"],
       "deliverables": ["<concrete deliverable 1>", "<concrete deliverable 2>"],
       "success_criteria": ["<how to measure success 1>", "<how to measure success 2>"],
       "dependencies": "<what must happen before this phase>"
   }}

   Phases should follow logical progression:
   - Phase 1: Foundation/Preparation
   - Phase 2: Pilot/Testing
   - Phase 3: Iteration/Refinement
   - Phase 4: Scale/Deployment
   - Phase 5+: Optimization/Maintenance

2. PRECISION_SCORE (0.0 to 1.0):
   How well-specified is this plan?
   - 0.0 = Vague aspirations
   - 0.5 = Clear direction, some gaps
   - 1.0 = Fully specified, executable blueprint

3. KNOWN_UNKNOWNS (epistemic humility):
   - What information is missing?
   - What dependencies are unclear?
   - What could we learn that would change the plan?
   - What assumptions are we making?

CRITICAL: Be CONCRETE. "Improve X" is not a deliverable.
"Reduce X by 20% measured by Y" is a deliverable.

Balanced path to implement:
{conflict_resolution.balanced_path}

Scenario:
ACTION: {scenario.get('action', '')}
CONTEXT: {scenario.get('context', '')}

Respond ONLY with JSON:
{{
    "phases": [
        {{
            "phase_name": "<name>",
            "timeline": "<timeframe>",
            "objectives": ["<objective 1>", "<objective 2>"],
            "deliverables": ["<deliverable 1>", "<deliverable 2>"],
            "success_criteria": ["<criterion 1>", "<criterion 2>"],
            "dependencies": "<prerequisites>"
        }}
    ],
    "precision_score": <0.0 to 1.0>,
    "known_unknowns": [
        "<unknown 1>",
        "<unknown 2>",
        "<unknown 3>"
    ]
}}
"""
