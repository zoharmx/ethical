"""
Context Analyzer Module
Multi-perspective analysis with synthesis (replaces Binah-Σ)
"""

import os
import json
import google.generativeai as genai
from typing import Dict, List, Set
from dataclasses import dataclass


@dataclass
class PerspectiveComparison:
    """Multi-perspective analysis result"""
    contextual_analysis: str
    individual_perspective: str  # Model B (Gemini)
    collective_perspective: str  # Model C (DeepSeek)
    convergence_points: List[str]
    divergence_points: List[str]
    biases_detected: List[Dict[str, str]]
    synthesis: str
    integration_score: float


class ContextAnalyzer:
    """
    Analyzes scenarios from multiple cultural/philosophical perspectives
    
    Uses multi-provider architecture:
    - Model B (Gemini): Individual-focused analysis (Western liberal)
    - Model C (DeepSeek): Collective-focused analysis (Eastern Confucian)
    - Synthesis: Meta-cognitive integration
    
    Automatically detects biases and generates emergent insights
    """
    
    def __init__(self, gemini_api_key: str, deepseek_api_key: str):
        # Configure Gemini (Model B - Individual focus)
        genai.configure(api_key=gemini_api_key)
        self.gemini = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Configure DeepSeek (Model C - Collective focus)
        # Note: Using requests library for DeepSeek API
        self.deepseek_api_key = deepseek_api_key
        self.deepseek_url = "https://api.deepseek.com/chat/completions"
    
    def analyze(
        self,
        scenario: Dict[str, str],
        insight_analysis: 'InsightAnalysis'
    ) -> PerspectiveComparison:
        """
        Analyze from multiple perspectives and synthesize
        
        Args:
            scenario: Original scenario
            insight_analysis: Insights from previous module
        
        Returns:
            PerspectiveComparison with synthesis
        """
        # 1. Contextual analysis (baseline)
        contextual = self._contextual_analysis(scenario)
        
        # 2. Individual-focused perspective (Model B)
        individual = self._individual_perspective(scenario, insight_analysis)
        
        # 3. Collective-focused perspective (Model C)
        collective = self._collective_perspective(scenario, insight_analysis)
        
        # 4. Meta-cognitive synthesis
        synthesis_result = self._synthesize(individual, collective)
        
        return PerspectiveComparison(
            contextual_analysis=contextual,
            individual_perspective=individual,
            collective_perspective=collective,
            convergence_points=synthesis_result['convergence'],
            divergence_points=synthesis_result['divergence'],
            biases_detected=synthesis_result['biases'],
            synthesis=synthesis_result['synthesis'],
            integration_score=synthesis_result['quality']
        )
    
    def _contextual_analysis(self, scenario: Dict[str, str]) -> str:
        """Baseline contextual analysis"""
        prompt = f"""
Provide contextual analysis of this scenario.

Consider:
- Stakeholders affected
- Historical context
- Current landscape
- Ethical frameworks applicable
- Trade-offs involved

Scenario:
{scenario.get('action', '')}

Context:
{scenario.get('context', '')}
"""
        response = self.gemini.generate_content(prompt)
        return response.text
    
    def _individual_perspective(
        self,
        scenario: Dict[str, str],
        insight_analysis: 'InsightAnalysis'
    ) -> str:
        """
        Analyze from individual-focused perspective (Western liberal)
        
        Emphasizes:
        - Individual rights and autonomy
        - Consent and procedural justice
        - Utilitarian cost-benefit
        - Kantian categorical imperative
        """
        prompt = f"""
Analyze this scenario from INDIVIDUAL-FOCUSED ethical frameworks:

FRAMEWORKS TO APPLY:
- Liberal rights-based ethics (Locke, Rawls): Individual liberty paramount
- Utilitarian calculus (Mill): Greatest happiness for individuals
- Kantian deontology: Treat persons as ends, not means
- Social contract theory: Voluntary agreements between individuals

EMPHASIS:
- Individual autonomy and choice
- Consent and procedural justice
- Rights protection
- Personal freedom

Insights to consider:
{json.dumps(insight_analysis.insights, indent=2)}

Scenario:
ACTION: {scenario.get('action', '')}
CONTEXT: {scenario.get('context', '')}

Provide analysis focusing on:
1. How does this affect INDIVIDUAL rights and autonomy?
2. What is the utilitarian cost-benefit for individuals?
3. What are the deontological duties to individuals?
4. Does this respect the social contract between individuals?
"""
        response = self.gemini.generate_content(prompt)
        return response.text
    
    def _collective_perspective(
        self,
        scenario: Dict[str, str],
        insight_analysis: 'InsightAnalysis'
    ) -> str:
        """
        Analyze from collective-focused perspective (Eastern Confucian)
        
        Emphasizes:
        - Social harmony and order
        - Collective good over individual
        - Contextual flexibility
        - Relational ontology
        """
        # Using DeepSeek API
        import requests
        
        prompt = f"""
Analyze this scenario from COLLECTIVE-FOCUSED ethical frameworks:

FRAMEWORKS TO APPLY:
- Confucian ethics: Harmony, filial piety, social order
- Taoist philosophy: Natural order, balance, wu wei
- Buddhist Middle Way: Avoiding extremes, compassion for all
- Relational ontology: Interconnectedness over individualism

EMPHASIS:
- Social harmony and collective good
- Community welfare
- Contextual flexibility (not rigid rules)
- Long-term societal impact

Insights to consider:
{json.dumps(insight_analysis.insights, indent=2)}

Scenario:
ACTION: {scenario.get('action', '')}
CONTEXT: {scenario.get('context', '')}

Provide analysis focusing on:
1. How does this affect COLLECTIVE harmony and social order?
2. What is the balance with natural order (dao)?
3. How does this cultivate societal virtue?
4. What are the relational implications (not just individual)?
"""
        
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.deepseek_url,
                headers=headers,
                json=data,
                timeout=60
            )
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            # Fallback to Gemini if DeepSeek fails
            print(f"⚠️  DeepSeek unavailable, using Gemini fallback: {e}")
            response = self.gemini.generate_content(prompt)
            return response.text
    
    def _synthesize(
        self,
        individual: str,
        collective: str
    ) -> Dict:
        """
        Meta-cognitive synthesis of perspectives
        
        Identifies:
        - Convergence points (shared values)
        - Divergence points (fundamental disagreements)
        - Biases (assumptions one side makes that other doesn't)
        - Synthesis (emergent wisdom)
        """
        # Extract keywords
        individual_keywords = self._extract_keywords(individual)
        collective_keywords = self._extract_keywords(collective)
        
        # Find convergence and divergence
        convergence = list(set(individual_keywords) & set(collective_keywords))
        individual_unique = list(set(individual_keywords) - set(collective_keywords))
        collective_unique = list(set(collective_keywords) - set(individual_keywords))
        
        # Generate meta-synthesis
        synthesis_prompt = f"""
Meta-cognitive synthesis of two perspectives:

INDIVIDUAL-FOCUSED PERSPECTIVE emphasized:
{', '.join(individual_unique[:10])}

COLLECTIVE-FOCUSED PERSPECTIVE emphasized:
{', '.join(collective_unique[:10])}

CONVERGENCE (shared concerns):
{', '.join(convergence[:10])}

Your task: Synthesize these into emergent wisdom that transcends both.

This is NOT compromise (meeting in middle) but EMERGENCE (new insight
from holding both perspectives simultaneously).

Questions:
1. What assumptions does individual focus make that collective doesn't (and vice versa)?
2. Are these disagreements fundamental or resolvable?
3. What hybrid approach honors BOTH perspectives?
4. What blind spots does each reveal in the other?

Provide:
1. Detected biases from each perspective
2. Emergent synthesis that increases feasibility and wisdom

Respond with JSON:
{{
    "biases_detected": [
        {{
            "perspective": "individual|collective",
            "bias": "<what assumption/bias>",
            "impact": "<how this affects analysis>"
        }}
    ],
    "synthesis": "<emergent wisdom that transcends both perspectives>",
    "quality": <0.0 to 1.0 integration quality score>
}}
"""
        
        response = self.gemini.generate_content(
            synthesis_prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )
        
        result = json.loads(response.text)
        
        return {
            'convergence': convergence[:10],
            'divergence': {
                'individual': individual_unique[:10],
                'collective': collective_unique[:10]
            },
            'biases': result.get('biases_detected', []),
            'synthesis': result.get('synthesis', ''),
            'quality': result.get('quality', 1.0)
        }
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract meaningful keywords from text"""
        # Simple keyword extraction (in production, use NLP library)
        import re
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
                     'to', 'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was',
                     'are', 'be', 'this', 'that', 'these', 'those', 'it'}
        
        words = re.findall(r'\b[a-z]{4,}\b', text.lower())
        keywords = [w for w in words if w not in stop_words]
        
        # Return most common
        from collections import Counter
        return set([k for k, v in Counter(keywords).most_common(30)])
