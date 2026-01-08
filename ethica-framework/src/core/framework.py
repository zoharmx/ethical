"""
Ethica.AI Framework
Enterprise-Grade Ethical AI Decision System

Copyright (c) 2025 Ethica.AI
Licensed under MIT License
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ImpactScore:
    """Purpose Validator output"""
    score: float  # 0.0 to 1.0
    harm_reduction: int  # -10 to +10
    autonomy_respect: int  # -10 to +10
    social_harmony: int  # -10 to +10
    justice_balance: int  # -10 to +10
    truthfulness: int  # -10 to +10
    concerns: List[Dict[str, str]]
    manifestation_valid: bool


@dataclass
class InsightAnalysis:
    """Insight Generator output (Mistral AI)"""
    understanding: str
    insights: List[str]
    uncertainties: List[str]
    confidence: float  # 0.0 to 1.0


@dataclass
class PerspectiveComparison:
    """Context Analyzer output (Multi-provider)"""
    contextual_analysis: str
    individual_perspective: str  # Model B focus
    collective_perspective: str  # Model C focus
    convergence_points: List[str]
    divergence_points: List[str]
    biases_detected: List[Dict[str, str]]
    synthesis: str
    integration_score: float  # 0.0 to 1.0


@dataclass
class OpportunityAssessment:
    """Opportunity Identifier output"""
    opportunities: List[str]
    beneficiaries: List[str]
    expansion_potential: str
    compassion_score: float


@dataclass
class RiskAssessment:
    """Risk Assessor output"""
    risks: List[str]
    constraints: List[str]
    warnings: List[str]
    severity_score: float


@dataclass
class ConflictResolution:
    """Conflict Resolver output"""
    conflicts_resolved: List[Dict[str, str]]
    balanced_path: str
    harmony_score: float


@dataclass
class SustainabilityEvaluation:
    """Sustainability Evaluator output"""
    sustainability_score: float
    obstacles: List[str]
    momentum_mechanisms: List[str]
    long_term_viability: str


@dataclass
class ImplementationPlan:
    """Implementation Planner output"""
    phases: List[Dict[str, str]]
    precision_score: float
    known_unknowns: List[str]


@dataclass
class IntegrationResult:
    """Integration Engine output"""
    readiness_score: float
    integration_complexity: float
    ready_to_manifest: bool
    synthesis: str


@dataclass
class Decision:
    """Decision Orchestrator output"""
    approved: bool
    approval_type: str  # UNCONDITIONAL, CONDITIONAL, REJECTED
    confidence: float
    actions: List[str]
    conditions: List[str]
    reasoning: str


@dataclass
class AnalysisResult:
    """Complete analysis result"""
    # Metadata
    scenario_id: str
    timestamp: str
    
    # Strategic Layer
    strategic: Dict[str, Any]  # impact_score, insights, context
    
    # Operational Layer
    operational: Dict[str, Any]  # opportunities, risks, resolution
    
    # Tactical Layer
    tactical: Dict[str, Any]  # sustainability, implementation
    
    # Execution Layer
    execution: Dict[str, Any]  # integration, decision
    
    # Full results
    impact_score: ImpactScore
    insight_analysis: InsightAnalysis
    perspective_comparison: PerspectiveComparison
    opportunity_assessment: OpportunityAssessment
    risk_assessment: RiskAssessment
    conflict_resolution: ConflictResolution
    sustainability: SustainabilityEvaluation
    implementation: ImplementationPlan
    integration: IntegrationResult
    decision: Decision


class EthicaFramework:
    """
    Enterprise-Grade Ethical AI Decision System
    
    Analyzes complex scenarios through 10 interdependent modules:
    - Strategic Layer: Purpose, Insight, Context
    - Operational Layer: Opportunities, Risks, Balance
    - Tactical Layer: Sustainability, Implementation
    - Execution Layer: Integration, Decision
    """
    
    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
        mistral_api_key: Optional[str] = None,
        deepseek_api_key: Optional[str] = None,
        impact_threshold: float = 0.60,
        enable_audit_trail: bool = False,
        organization_id: Optional[str] = None
    ):
        """
        Initialize Ethica Framework
        
        Args:
            gemini_api_key: Google Gemini API key (for Model B - individual focus)
            mistral_api_key: Mistral AI API key (for Model A - neutral arbiter)
            deepseek_api_key: DeepSeek API key (for Model C - collective focus)
            impact_threshold: Minimum impact score for approval (default 0.60)
            enable_audit_trail: Enable detailed logging
            organization_id: Organization identifier for multi-tenant setup
        """
        # API keys
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')
        self.mistral_api_key = mistral_api_key or os.getenv('MISTRAL_API_KEY')
        self.deepseek_api_key = deepseek_api_key or os.getenv('DEEPSEEK_API_KEY')
        
        # Configuration
        self.impact_threshold = impact_threshold
        self.enable_audit_trail = enable_audit_trail
        self.organization_id = organization_id
        
        # Initialize modules
        from modules.purpose_validator import PurposeValidator
        from modules.insight_generator import InsightGenerator
        from modules.context_analyzer import ContextAnalyzer
        from modules.opportunity_identifier import OpportunityIdentifier
        from modules.risk_assessor import RiskAssessor
        from modules.conflict_resolver import ConflictResolver
        from modules.sustainability_evaluator import SustainabilityEvaluator
        from modules.implementation_planner import ImplementationPlanner
        from modules.integration_engine import IntegrationEngine
        from modules.decision_orchestrator import DecisionOrchestrator
        
        self.purpose_validator = PurposeValidator(self.gemini_api_key)
        self.insight_generator = InsightGenerator(self.mistral_api_key)
        self.context_analyzer = ContextAnalyzer(
            self.gemini_api_key,
            self.deepseek_api_key
        )
        self.opportunity_identifier = OpportunityIdentifier(self.gemini_api_key)
        self.risk_assessor = RiskAssessor(self.gemini_api_key)
        self.conflict_resolver = ConflictResolver(self.gemini_api_key)
        self.sustainability_evaluator = SustainabilityEvaluator(self.gemini_api_key)
        self.implementation_planner = ImplementationPlanner(self.gemini_api_key)
        self.integration_engine = IntegrationEngine(self.gemini_api_key)
        self.decision_orchestrator = DecisionOrchestrator(self.gemini_api_key)
    
    def analyze(self, scenario: Dict[str, str]) -> AnalysisResult:
        """
        Analyze ethical scenario through 10-module pipeline
        
        Args:
            scenario: Dict with keys:
                - action: str (proposed action)
                - context: str (detailed context)
                - stakeholders: List[str] (optional)
        
        Returns:
            AnalysisResult with complete analysis
        """
        scenario_id = self._generate_scenario_id()
        timestamp = datetime.utcnow().isoformat()
        
        # STRATEGIC LAYER
        print("🔷 STRATEGIC LAYER: Analyzing intent...")
        
        # [1] Purpose Validator
        print("  [1/10] Purpose Validator...")
        impact_score = self.purpose_validator.validate(scenario)
        
        if not impact_score.manifestation_valid:
            # Early rejection
            decision = Decision(
                approved=False,
                approval_type="REJECTED",
                confidence=1.0,
                actions=[],
                conditions=[],
                reasoning=f"Failed purpose validation. Impact score: {impact_score.score:.1%}"
            )
            
            return self._build_early_rejection_result(
                scenario_id, timestamp, impact_score, decision
            )
        
        # [2] Insight Generator (Mistral AI - Neutral)
        print("  [2/10] Insight Generator (Mistral AI)...")
        insight_analysis = self.insight_generator.generate(scenario, impact_score)
        
        # [3] Context Analyzer (Multi-provider)
        print("  [3/10] Context Analyzer (Multi-perspective)...")
        perspective_comparison = self.context_analyzer.analyze(
            scenario, insight_analysis
        )
        
        # OPERATIONAL LAYER
        print("\n🔷 OPERATIONAL LAYER: Analyzing forces...")
        
        # [4] Opportunity Identifier
        print("  [4/10] Opportunity Identifier...")
        opportunity_assessment = self.opportunity_identifier.identify(
            scenario, perspective_comparison
        )
        
        # [5] Risk Assessor
        print("  [5/10] Risk Assessor...")
        risk_assessment = self.risk_assessor.assess(
            scenario, perspective_comparison
        )
        
        # [6] Conflict Resolver
        print("  [6/10] Conflict Resolver...")
        conflict_resolution = self.conflict_resolver.resolve(
            opportunity_assessment, risk_assessment
        )
        
        # TACTICAL LAYER
        print("\n🔷 TACTICAL LAYER: Analyzing structure...")
        
        # [7] Sustainability Evaluator
        print("  [7/10] Sustainability Evaluator...")
        sustainability = self.sustainability_evaluator.evaluate(
            scenario, conflict_resolution
        )
        
        # [8] Implementation Planner
        print("  [8/10] Implementation Planner...")
        implementation = self.implementation_planner.plan(
            scenario, conflict_resolution
        )
        
        # EXECUTION LAYER
        print("\n🔷 EXECUTION LAYER: Synthesizing decision...")
        
        # [9] Integration Engine
        print("  [9/10] Integration Engine...")
        integration = self.integration_engine.integrate(
            impact_score=impact_score,
            insight_analysis=insight_analysis,
            perspective_comparison=perspective_comparison,
            opportunity_assessment=opportunity_assessment,
            risk_assessment=risk_assessment,
            conflict_resolution=conflict_resolution,
            sustainability=sustainability,
            implementation=implementation
        )
        
        # [10] Decision Orchestrator
        print("  [10/10] Decision Orchestrator...")
        decision = self.decision_orchestrator.orchestrate(integration)
        
        print("\n✅ Analysis complete!")
        
        # Build result
        return AnalysisResult(
            scenario_id=scenario_id,
            timestamp=timestamp,
            strategic={
                'impact_score': impact_score.score,
                'confidence': insight_analysis.confidence,
                'integration_score': perspective_comparison.integration_score
            },
            operational={
                'opportunities': len(opportunity_assessment.opportunities),
                'risks': len(risk_assessment.risks),
                'harmony_score': conflict_resolution.harmony_score
            },
            tactical={
                'sustainability': sustainability.sustainability_score,
                'precision': implementation.precision_score
            },
            execution={
                'readiness': integration.readiness_score,
                'approved': decision.approved
            },
            impact_score=impact_score,
            insight_analysis=insight_analysis,
            perspective_comparison=perspective_comparison,
            opportunity_assessment=opportunity_assessment,
            risk_assessment=risk_assessment,
            conflict_resolution=conflict_resolution,
            sustainability=sustainability,
            implementation=implementation,
            integration=integration,
            decision=decision
        )
    
    def export_json(self, result: AnalysisResult, filepath: str):
        """Export result to JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(result), f, indent=2, ensure_ascii=False)
        print(f"📄 Exported to {filepath}")
    
    def _generate_scenario_id(self) -> str:
        """Generate unique scenario ID"""
        import uuid
        return f"ETH-{str(uuid.uuid4())[:8]}"
    
    def _build_early_rejection_result(
        self,
        scenario_id: str,
        timestamp: str,
        impact_score: ImpactScore,
        decision: Decision
    ) -> AnalysisResult:
        """Build result for early rejection"""
        # Create empty results for modules that didn't run
        from modules.insight_generator import InsightAnalysis as EmptyInsight
        from modules.context_analyzer import PerspectiveComparison as EmptyPerspective
        
        # ... (simplified for brevity - would include all empty structures)
        
        return AnalysisResult(
            scenario_id=scenario_id,
            timestamp=timestamp,
            strategic={'impact_score': impact_score.score, 'confidence': 0.0, 'integration_score': 0.0},
            operational={'opportunities': 0, 'risks': 0, 'harmony_score': 0.0},
            tactical={'sustainability': 0.0, 'precision': 0.0},
            execution={'readiness': 0.0, 'approved': False},
            impact_score=impact_score,
            insight_analysis=None,  # Not run
            perspective_comparison=None,  # Not run
            opportunity_assessment=None,
            risk_assessment=None,
            conflict_resolution=None,
            sustainability=None,
            implementation=None,
            integration=None,
            decision=decision
        )
