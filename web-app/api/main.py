from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os
from pathlib import Path

# Add parent directory to path to import ethica framework
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.insert(0, str(parent_dir / "ethica-framework" / "src"))

try:
    from core.framework import EthicaFramework
    FRAMEWORK_AVAILABLE = True
except ImportError:
    FRAMEWORK_AVAILABLE = False
    print("Warning: Ethica Framework not available. Using mock responses.")

app = FastAPI(
    title="Ethica.AI API",
    description="Enterprise-Grade Ethical AI Decision System API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    action: str
    context: str
    stakeholders: Optional[List[str]] = []
    name: Optional[str] = "Unnamed Scenario"

class AnalysisResponse(BaseModel):
    scenario_id: str
    timestamp: str
    strategic: dict
    operational: dict
    tactical: dict
    execution: dict
    decision: dict

@app.get("/")
async def root():
    return {
        "message": "Ethica.AI API",
        "version": "1.0.0",
        "status": "operational",
        "framework_available": FRAMEWORK_AVAILABLE
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "framework": "available" if FRAMEWORK_AVAILABLE else "mock_mode"
    }

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_scenario(request: AnalysisRequest):
    """
    Analyze an AI scenario through the Ethica Framework
    """
    if not FRAMEWORK_AVAILABLE:
        # Return mock response if framework not available
        return create_mock_response(request)

    try:
        # Load API keys from environment
        gemini_key = os.getenv("GEMINI_API_KEY")
        mistral_key = os.getenv("MISTRAL_API_KEY")
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")

        if not all([gemini_key, mistral_key, deepseek_key]):
            raise HTTPException(
                status_code=500,
                detail="API keys not configured. Please set GEMINI_API_KEY, MISTRAL_API_KEY, and DEEPSEEK_API_KEY environment variables."
            )

        # Initialize framework
        ethica = EthicaFramework(
            gemini_api_key=gemini_key,
            mistral_api_key=mistral_key,
            deepseek_api_key=deepseek_key,
            impact_threshold=0.60
        )

        # Prepare scenario
        scenario = {
            "action": request.action,
            "context": request.context,
            "stakeholders": request.stakeholders
        }

        # Run analysis
        result = ethica.analyze(scenario)

        # Convert result to response format
        response = {
            "scenario_id": result.scenario_id,
            "timestamp": result.timestamp,
            "strategic": {
                "impact_score": result.strategic.impact_score,
                "confidence": result.strategic.confidence,
                "integration_score": result.strategic.integration_score
            },
            "operational": {
                "harmony_score": result.operational.harmony_score if hasattr(result, 'operational') else 0.0
            },
            "tactical": {
                "sustainability": result.tactical.sustainability if hasattr(result, 'tactical') else 0.0
            },
            "execution": {
                "readiness": result.execution.readiness,
                "approved": result.execution.approved
            },
            "decision": {
                "approved": result.decision.approved,
                "approval_type": result.decision.approval_type,
                "confidence": result.decision.confidence,
                "reasoning": result.decision.reasoning,
                "actions": result.decision.actions,
                "conditions": result.decision.conditions
            }
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

def create_mock_response(request: AnalysisRequest) -> dict:
    """
    Create a mock response when the framework is not available
    """
    import random
    from datetime import datetime

    # Simulate different outcomes based on keywords
    action_lower = request.action.lower()

    if "surveillance" in action_lower or "monitor" in action_lower:
        # Negative scenario
        impact_score = random.uniform(0.35, 0.50)
        approval_type = "REJECTED"
        approved = False
        reasoning = "Failed purpose validation. Significant concerns about privacy violation and autonomy."
        actions = []
        conditions = []
    elif "healthcare" in action_lower or "health" in action_lower:
        # Conditional scenario
        impact_score = random.uniform(0.70, 0.80)
        approval_type = "CONDITIONAL"
        approved = True
        reasoning = "Conditional approval granted. High potential for positive impact with proper oversight."
        actions = [
            "Implement transparent AI decision-making processes",
            "Establish regular bias audits"
        ]
        conditions = [
            "Require human oversight for critical decisions",
            "Implement comprehensive data privacy measures"
        ]
    else:
        # Positive scenario
        impact_score = random.uniform(0.75, 0.90)
        approval_type = "APPROVED"
        approved = True
        reasoning = "Approved with high confidence. Strong alignment with ethical standards and positive societal impact."
        actions = [
            "Implement transparent AI decision-making processes",
            "Establish stakeholder feedback mechanisms",
            "Create continuous monitoring system"
        ]
        conditions = []

    return {
        "scenario_id": f"ETH-{random.randint(10000, 99999)}",
        "timestamp": datetime.now().isoformat(),
        "strategic": {
            "impact_score": impact_score,
            "confidence": random.uniform(0.90, 0.98)
        },
        "operational": {
            "harmony_score": impact_score + random.uniform(-0.05, 0.05)
        },
        "tactical": {
            "sustainability": impact_score + random.uniform(-0.08, 0.08)
        },
        "execution": {
            "readiness": impact_score + random.uniform(-0.10, 0.05),
            "approved": approved
        },
        "decision": {
            "approved": approved,
            "approval_type": approval_type,
            "confidence": random.uniform(0.92, 0.99),
            "reasoning": reasoning,
            "actions": actions,
            "conditions": conditions
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
