"""
Sustainability Evaluator Module
Evaluates long-term sustainability and endurance (replaces Netzach/Eternity)
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class SustainabilityEvaluation:
    """Sustainability evaluation result"""
    sustainability_score: float
    obstacles: List[str]
    momentum_mechanisms: List[str]
    long_term_viability: str


class SustainabilityEvaluator:
    """
    Evaluates long-term sustainability and endurance

    Assesses:
    1. Can this endure over time?
    2. What sustains momentum?
    3. What obstacles threaten persistence?
    4. What is the long-term trajectory?
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def evaluate(
        self,
        scenario: Dict[str, str],
        conflict_resolution: 'ConflictResolution'
    ) -> SustainabilityEvaluation:
        """
        Evaluate long-term sustainability

        Args:
            scenario: Original scenario
            conflict_resolution: Balanced approach from previous module

        Returns:
            SustainabilityEvaluation with sustainability assessment
        """
        prompt = self._build_prompt(scenario, conflict_resolution)

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.5,
                response_mime_type="application/json"
            )
        )

        result = json.loads(response.text)

        return SustainabilityEvaluation(
            sustainability_score=result.get('sustainability_score', 0.5),
            obstacles=result.get('obstacles', []),
            momentum_mechanisms=result.get('momentum_mechanisms', []),
            long_term_viability=result.get('long_term_viability', '')
        )

    def _build_prompt(
        self,
        scenario: Dict[str, str],
        conflict_resolution: 'ConflictResolution'
    ) -> str:
        """Build sustainability evaluation prompt"""
        return f"""
You are a Sustainability Evaluator focused on ENDURANCE and VICTORY.

Your role: Assess if this can LAST, if momentum can be SUSTAINED.

Analysis framework:

1. SUSTAINABILITY_SCORE (0.0 to 1.0):
   Assess long-term viability across:
   - Financial sustainability (funding, revenue model)
   - Political sustainability (public support, regulatory stability)
   - Technical sustainability (maintenance, scalability)
   - Social sustainability (cultural acceptance, behavioral change)

   0.0 = Will collapse quickly
   0.5 = Can sustain with effort
   1.0 = Self-sustaining, antifragile

2. OBSTACLES (5-7 threats to persistence):
   - What will try to stop this?
   - What resistances will emerge?
   - What fatigue factors exist?
   - What erosion forces act over time?

3. MOMENTUM_MECHANISMS (5-7 sustainers):
   - What creates positive feedback loops?
   - What builds momentum over time?
   - What network effects exist?
   - What reinforcing structures?

4. LONG_TERM_VIABILITY:
   - What does success look like in 1 year? 5 years? 10 years?
   - What is the endgame?
   - How does this evolve over time?
   - What is the victory condition?

CRITICAL: Think in DECADES, not months. What makes something
endure is rarely what launches it.

Balanced path from conflict resolution:
{conflict_resolution.balanced_path}

Scenario:
ACTION: {scenario.get('action', '')}
CONTEXT: {scenario.get('context', '')}

Respond ONLY with JSON:
{{
    "sustainability_score": <0.0 to 1.0>,
    "obstacles": [
        "<obstacle 1>",
        "<obstacle 2>",
        "<obstacle 3>",
        "<obstacle 4>",
        "<obstacle 5>"
    ],
    "momentum_mechanisms": [
        "<mechanism 1>",
        "<mechanism 2>",
        "<mechanism 3>",
        "<mechanism 4>",
        "<mechanism 5>"
    ],
    "long_term_viability": "<trajectory and endgame>"
}}
"""
