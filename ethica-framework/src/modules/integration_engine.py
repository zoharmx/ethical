"""
Integration Engine Module
Integrates all analyses into unified assessment (replaces Yesod/Foundation)
"""

import os
import json
import google.generativeai as genai
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class IntegrationResult:
    """Integration result"""
    readiness_score: float
    integration_complexity: float
    ready_to_manifest: bool
    synthesis: str


class IntegrationEngine:
    """
    Integrates all previous analyses into unified assessment

    Synthesizes:
    1. Strategic layer (purpose, insight, context)
    2. Operational layer (opportunities, risks, balance)
    3. Tactical layer (sustainability, implementation)

    Outputs:
    - Readiness score
    - Integration quality
    - Go/no-go recommendation
    """

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')

    def integrate(
        self,
        impact_score: Any,
        insight_analysis: Any,
        perspective_comparison: Any,
        opportunity_assessment: Any,
        risk_assessment: Any,
        conflict_resolution: Any,
        sustainability: Any,
        implementation: Any
    ) -> IntegrationResult:
        """
        Integrate all analyses

        Args:
            All outputs from previous 8 modules

        Returns:
            IntegrationResult with unified assessment
        """
        prompt = self._build_prompt(
            impact_score,
            insight_analysis,
            perspective_comparison,
            opportunity_assessment,
            risk_assessment,
            conflict_resolution,
            sustainability,
            implementation
        )

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.3,
                response_mime_type="application/json"
            )
        )

        result = json.loads(response.text)

        readiness = result.get('readiness_score', 0.5)
        complexity = result.get('integration_complexity', 0.5)

        # Ready if high readiness and manageable complexity
        ready_to_manifest = (readiness >= 0.70 and complexity <= 0.80)

        return IntegrationResult(
            readiness_score=readiness,
            integration_complexity=complexity,
            ready_to_manifest=ready_to_manifest,
            synthesis=result.get('synthesis', '')
        )

    def _build_prompt(self, *args) -> str:
        """Build integration prompt"""
        (impact_score, insight_analysis, perspective_comparison,
         opportunity_assessment, risk_assessment, conflict_resolution,
         sustainability, implementation) = args

        return f"""
You are an Integration Engine focused on SYNTHESIS and FOUNDATION.

Your role: Integrate ALL previous analyses into UNIFIED assessment.

You have 8 layers of analysis:

STRATEGIC LAYER:
1. Purpose Validator:
   - Impact score: {impact_score.score:.1%}
   - Manifestation valid: {impact_score.manifestation_valid}

2. Insight Generator:
   - Confidence: {insight_analysis.confidence:.1%}
   - Insights: {len(insight_analysis.insights)}
   - Uncertainties: {len(insight_analysis.uncertainties)}

3. Context Analyzer:
   - Integration score: {perspective_comparison.integration_score:.1%}
   - Biases detected: {len(perspective_comparison.biases_detected)}

OPERATIONAL LAYER:
4. Opportunities:
   - Count: {len(opportunity_assessment.opportunities)}
   - Compassion: {opportunity_assessment.compassion_score:.1%}

5. Risks:
   - Count: {len(risk_assessment.risks)}
   - Severity: {risk_assessment.severity_score:.1%}

6. Balance:
   - Harmony: {conflict_resolution.harmony_score:.1%}
   - Conflicts resolved: {len(conflict_resolution.conflicts_resolved)}

TACTICAL LAYER:
7. Sustainability:
   - Score: {sustainability.sustainability_score:.1%}

8. Implementation:
   - Precision: {implementation.precision_score:.1%}
   - Phases: {len(implementation.phases)}

Your task:

1. READINESS_SCORE (0.0 to 1.0):
   Weighted integration:
   - Strategic alignment (30%): purpose + insights + context
   - Operational feasibility (40%): opportunities vs risks, balance quality
   - Tactical viability (30%): sustainability + implementation precision

   Calculate weighted average, considering:
   - High impact + high harmony + high sustainability = high readiness
   - High risks + low sustainability = low readiness
   - Uncertainties and unknowns reduce confidence

2. INTEGRATION_COMPLEXITY (0.0 to 1.0):
   How complex is this to execute?
   - 0.0 = Simple, straightforward
   - 0.5 = Moderate complexity, manageable
   - 1.0 = Extremely complex, many dependencies

   Consider:
   - Number of stakeholders
   - Number of constraints
   - Implementation phases
   - Conflict resolution complexity

3. SYNTHESIS:
   One paragraph (5-7 sentences) that INTEGRATES everything:
   - What is the essence of this decision?
   - What are the key trade-offs?
   - What makes this ready (or not ready)?
   - What is the core recommendation?

CRITICAL: This is the FOUNDATION. Everything builds on this.
Be rigorous, balanced, and clear.

Respond ONLY with JSON:
{{
    "readiness_score": <0.0 to 1.0>,
    "integration_complexity": <0.0 to 1.0>,
    "synthesis": "<unified assessment paragraph>"
}}
"""
