"""
Purpose Validator Module
Validates alignment with positive global impact (replaces Keter/Crown)
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class ImpactScore:
    """Impact assessment result"""
    score: float  # 0.0 to 1.0
    harm_reduction: int  # -10 to +10
    autonomy_respect: int  # -10 to +10
    social_harmony: int  # -10 to +10
    justice_balance: int  # -10 to +10
    truthfulness: int  # -10 to +10
    concerns: List[Dict[str, str]]
    manifestation_valid: bool
    reasoning: str


class PurposeValidator:
    """
    Validates proposed actions against positive global impact criteria
    
    Evaluates 5 dimensions:
    1. Harm Reduction: Does it reduce suffering?
    2. Autonomy Respect: Does it respect free will and choice?
    3. Social Harmony: Does it promote cooperation?
    4. Justice Balance: Does it balance fairness with compassion?
    5. Truthfulness: Is it based on truth and evidence?
    
    Threshold: ≥60% impact score for approval
    """
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.threshold = 0.60
    
    def validate(self, scenario: Dict[str, str]) -> ImpactScore:
        """
        Validate scenario's alignment with positive global impact
        
        Args:
            scenario: Dict with 'action' and 'context'
        
        Returns:
            ImpactScore with validation results
        """
        prompt = self._build_prompt(scenario)
        
        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.3,
                response_mime_type="application/json"
            )
        )
        
        result = json.loads(response.text)
        
        # Calculate impact score
        total = sum([
            result['harm_reduction'],
            result['autonomy_respect'],
            result['social_harmony'],
            result['justice_balance'],
            result['truthfulness']
        ])
        
        impact_score = (total + 50) / 100  # Normalize to [0, 1]
        
        # Check for critical concerns
        critical_concerns = [
            c for c in result.get('concerns', [])
            if c.get('severity') == 'CRITICAL'
        ]
        
        # Validate manifestation
        manifestation_valid = (
            impact_score >= self.threshold and
            len(critical_concerns) == 0
        )
        
        return ImpactScore(
            score=impact_score,
            harm_reduction=result['harm_reduction'],
            autonomy_respect=result['autonomy_respect'],
            social_harmony=result['social_harmony'],
            justice_balance=result['justice_balance'],
            truthfulness=result['truthfulness'],
            concerns=result.get('concerns', []),
            manifestation_valid=manifestation_valid,
            reasoning=result.get('reasoning', '')
        )
    
    def _build_prompt(self, scenario: Dict[str, str]) -> str:
        """Build validation prompt"""
        return f"""
Evaluate this proposal's alignment with positive global impact.

Score each dimension from -10 to +10:

1. HARM_REDUCTION: Does it reduce suffering, poverty, or injustice?
   -10 = Increases harm greatly
   0 = Neutral
   +10 = Dramatically reduces harm

2. AUTONOMY_RESPECT: Does it respect individual choice and agency?
   -10 = Totalitarian coercion
   0 = Neutral
   +10 = Maximizes voluntary choice

3. SOCIAL_HARMONY: Does it promote peace and cooperation?
   -10 = Causes severe conflict
   0 = Neutral
   +10 = Builds bridges and unity

4. JUSTICE_BALANCE: Does it balance fairness with compassion?
   -10 = Severe injustice or cruelty
   0 = Neutral
   +10 = Perfect balance of justice and mercy

5. TRUTHFULNESS: Is it based on evidence and honesty?
   -10 = Built on lies and deception
   0 = Uncertain
   +10 = Firmly grounded in truth

CRITICAL: Negative scores are VALID and INFORMATIVE.
A proposal can have negative scores in some dimensions while
being net positive overall.

Respond ONLY with JSON:
{{
    "harm_reduction": <-10 to +10>,
    "autonomy_respect": <-10 to +10>,
    "social_harmony": <-10 to +10>,
    "justice_balance": <-10 to +10>,
    "truthfulness": <-10 to +10>,
    "reasoning": "<brief explanation>",
    "concerns": [
        {{
            "type": "<concern type>",
            "severity": "LOW|MEDIUM|HIGH|CRITICAL",
            "description": "<what is concerning>"
        }}
    ]
}}

Scenario:
ACTION: {scenario.get('action', '')}

CONTEXT: {scenario.get('context', '')}
"""
