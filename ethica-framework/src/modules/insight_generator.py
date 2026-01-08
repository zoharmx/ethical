"""
Insight Generator Module
Deep insight generation via Mistral AI (replaces Chochmah/Wisdom)
"""

import os
import json
from mistralai import Mistral
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class InsightAnalysis:
    """Deep insight analysis result"""
    understanding: str
    insights: List[str]
    uncertainties: List[str]
    confidence: float  # 0.0 to 1.0


class InsightGenerator:
    """
    Generates deep understanding and non-obvious insights
    
    Uses Mistral AI (European/Neutral perspective) to:
    1. Understand the essence of the situation
    2. Identify non-obvious implications
    3. Acknowledge uncertainties with epistemic humility
    4. Provide confidence assessment
    """
    
    def __init__(self, api_key: str):
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-large-latest"
    
    def generate(
        self,
        scenario: Dict[str, str],
        impact_score: 'ImpactScore'
    ) -> InsightAnalysis:
        """
        Generate deep insights about scenario
        
        Args:
            scenario: Original scenario
            impact_score: Result from Purpose Validator
        
        Returns:
            InsightAnalysis with insights and confidence
        """
        prompt = self._build_prompt(scenario, impact_score)
        
        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        result = json.loads(response.choices[0].message.content)
        
        return InsightAnalysis(
            understanding=result.get('understanding', ''),
            insights=result.get('insights', []),
            uncertainties=result.get('uncertainties', []),
            confidence=result.get('confidence', 0.5)
        )
    
    def _build_prompt(
        self,
        scenario: Dict[str, str],
        impact_score: 'ImpactScore'
    ) -> str:
        """Build insight generation prompt"""
        return f"""
You are an Insight Generator providing deep understanding.

The proposal has an impact score of {impact_score.score:.1%}.

Provide profound analysis:

1. UNDERSTANDING: What is the essence of this situation?
   - Go beyond surface description
   - Identify hidden dynamics
   - See patterns others might miss

2. INSIGHTS (5-7 key insights):
   - What are non-obvious implications?
   - What precedents or analogies apply?
   - What are leverage points for change?
   - What could go wrong that isn't obvious?

3. UNCERTAINTIES (5-7 honest unknowns):
   - What do we NOT know?
   - What assumptions are being made?
   - Where could analysis be wrong?
   - What data is missing?

4. CONFIDENCE (0.0 to 1.0):
   - How confident are you in this analysis?
   - Base on: evidence strength, precedents, complexity

CRITICAL: Express epistemic humility. Wisdom knows its limits.

Respond ONLY with JSON:
{{
    "understanding": "<essence of situation>",
    "insights": [
        "<insight 1>",
        "<insight 2>",
        "<insight 3>",
        "<insight 4>",
        "<insight 5>",
        "<insight 6>",
        "<insight 7>"
    ],
    "uncertainties": [
        "<uncertainty 1>",
        "<uncertainty 2>",
        "<uncertainty 3>",
        "<uncertainty 4>",
        "<uncertainty 5>",
        "<uncertainty 6>",
        "<uncertainty 7>"
    ],
    "confidence": <0.0 to 1.0>
}}

Scenario:
ACTION: {scenario.get('action', '')}

CONTEXT: {scenario.get('context', '')}

Impact Assessment:
- Harm Reduction: {impact_score.harm_reduction}/10
- Autonomy Respect: {impact_score.autonomy_respect}/10
- Social Harmony: {impact_score.social_harmony}/10
- Justice Balance: {impact_score.justice_balance}/10
- Truthfulness: {impact_score.truthfulness}/10

Reasoning: {impact_score.reasoning}
"""
