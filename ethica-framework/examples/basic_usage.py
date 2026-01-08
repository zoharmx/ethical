"""
Ethica.AI Framework - Example Usage
"""

import os
import sys

# Fix Windows encoding issue
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from dotenv import load_dotenv
load_dotenv()

# Import framework
sys.path.insert(0, './src')

from core.framework import EthicaFramework

# Initialize
ethica = EthicaFramework(
    gemini_api_key=os.getenv('GEMINI_API_KEY'),
    mistral_api_key=os.getenv('MISTRAL_API_KEY'),
    deepseek_api_key=os.getenv('DEEPSEEK_API_KEY')
)

# Define scenario
scenario = {
    "action": "Deploy AI-powered surveillance system in public spaces for crime reduction",
    "context": """
        City government proposes installing facial recognition cameras in all 
        public spaces (parks, streets, transit) to reduce crime. 
        
        PROPONENTS (Police Department):
        - Pilot program showed 40% crime reduction
        - Real-time alerts for missing persons
        - Evidence collection for investigations
        
        OPPONENTS (Privacy Advocates):
        - Mass surveillance violates civil liberties
        - Risk of authoritarian abuse
        - Chilling effect on free speech
        - Disproportionate impact on minorities
        
        STAKEHOLDERS:
        - Citizens (privacy vs safety)
        - Police (crime reduction)
        - Civil liberties groups (rights protection)
        - City council (political decision)
    """,
    "stakeholders": [
        "Citizens",
        "Police Department",
        "Privacy Advocates",
        "City Council",
        "Minority Communities"
    ]
}

print("=" * 60)
print("ETHICA.AI FRAMEWORK - ETHICAL ANALYSIS")
print("=" * 60)
print(f"\nScenario: {scenario['action']}\n")

# Run analysis
result = ethica.analyze(scenario)

# Display results
print("\n" + "=" * 60)
print("ANALYSIS RESULTS")
print("=" * 60)

print("\n🎯 STRATEGIC LAYER:")
print(f"  Impact Score: {result.strategic['impact_score']:.1%}")
print(f"  Confidence: {result.strategic['confidence']:.1%}")
print(f"  Integration: {result.strategic['integration_score']:.1%}")

print("\n⚙️  OPERATIONAL LAYER:")
print(f"  Opportunities: {result.operational['opportunities']}")
print(f"  Risks: {result.operational['risks']}")
print(f"  Harmony Score: {result.operational['harmony_score']:.1%}")

print("\n📊 TACTICAL LAYER:")
print(f"  Sustainability: {result.tactical['sustainability']:.1%}")
print(f"  Precision: {result.tactical['precision']:.1%}")

print("\n✅ EXECUTION LAYER:")
print(f"  Readiness: {result.execution['readiness']:.1%}")
print(f"  Decision: {'APPROVED' if result.execution['approved'] else 'REJECTED'}")

print("\n" + "=" * 60)
print("FINAL DECISION")
print("=" * 60)

decision = result.decision
print(f"\nStatus: {decision.approval_type}")
print(f"Confidence: {decision.confidence:.1%}")
print(f"\nReasoning:\n{decision.reasoning}")

if decision.conditions:
    print(f"\n📋 CONDITIONS ({len(decision.conditions)}):")
    for i, condition in enumerate(decision.conditions, 1):
        print(f"  {i}. {condition}")

if decision.actions:
    print(f"\n🎯 ACTIONS ({len(decision.actions)}):")
    for i, action in enumerate(decision.actions, 1):
        print(f"  {i}. {action}")

# Export
print("\n" + "=" * 60)
print("EXPORTING RESULTS")
print("=" * 60)

ethica.export_json(result, "analysis_result.json")
print("\n✅ Complete! Check analysis_result.json for full details.")
