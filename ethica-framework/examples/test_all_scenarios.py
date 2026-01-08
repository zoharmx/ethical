"""
Ethica.AI Framework - Prueba Automatizada de Múltiples Escenarios
Ejecuta análisis de 6 escenarios diferentes y compara resultados
"""

import os
import sys
import json
from datetime import datetime

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

# Import scenarios
from scenarios_examples import (
    scenario_education,
    scenario_health,
    scenario_environment,
    scenario_workplace,
    scenario_justice,
    scenario_entertainment
)

# Initialize framework
print("=" * 70)
print("ETHICA.AI FRAMEWORK - ANÁLISIS COMPARATIVO DE ESCENARIOS")
print("=" * 70)
print("\nInicializando framework...\n")

ethica = EthicaFramework(
    gemini_api_key=os.getenv('GEMINI_API_KEY'),
    mistral_api_key=os.getenv('MISTRAL_API_KEY'),
    deepseek_api_key=os.getenv('DEEPSEEK_API_KEY')
)

# Define scenarios to test
scenarios = [
    ("EDUCACIÓN", scenario_education),
    ("SALUD", scenario_health),
    ("MEDIO AMBIENTE", scenario_environment),
    ("TRABAJO/VIGILANCIA", scenario_workplace),
    ("JUSTICIA SOCIAL", scenario_justice),
    ("ENTRETENIMIENTO/IA", scenario_entertainment)
]

# Store results
all_results = []

# Analyze each scenario
for i, (name, scenario) in enumerate(scenarios, 1):
    print("\n" + "=" * 70)
    print(f"ESCENARIO {i}/6: {name}")
    print("=" * 70)
    print(f"\nAcción: {scenario['action'][:80]}...")
    print(f"\nAnalizando...\n")

    try:
        result = ethica.analyze(scenario)

        # Store result
        all_results.append({
            'name': name,
            'action': scenario['action'],
            'result': result
        })

        # Print summary
        print("\n" + "-" * 70)
        print(f"RESUMEN - {name}")
        print("-" * 70)
        print(f"Impact Score:    {result.strategic['impact_score']:.1%}")
        print(f"Confidence:      {result.strategic['confidence']:.1%}")
        print(f"Decisión:        {result.decision.approval_type}")
        print(f"Aprobado:        {'✅ SÍ' if result.decision.approved else '❌ NO'}")
        print(f"Confianza:       {result.decision.confidence:.1%}")
        print(f"\nRazonamiento: {result.decision.reasoning[:200]}...")

        if result.decision.conditions:
            print(f"\nCondiciones ({len(result.decision.conditions)}):")
            for j, cond in enumerate(result.decision.conditions[:3], 1):
                print(f"  {j}. {cond[:100]}...")

    except Exception as e:
        print(f"\n❌ ERROR en escenario {name}: {str(e)}")
        import traceback
        traceback.print_exc()

# Print comparative table
print("\n\n" + "=" * 70)
print("TABLA COMPARATIVA DE RESULTADOS")
print("=" * 70)
print(f"\n{'ESCENARIO':<25} {'IMPACT':<10} {'DECISIÓN':<15} {'APROBADO':<10}")
print("-" * 70)

for item in all_results:
    name = item['name']
    result = item['result']
    impact = f"{result.strategic['impact_score']:.0%}"
    decision = result.decision.approval_type
    approved = "✅ SÍ" if result.decision.approved else "❌ NO"

    print(f"{name:<25} {impact:<10} {decision:<15} {approved:<10}")

# Export all results to JSON
print("\n" + "=" * 70)
print("EXPORTANDO RESULTADOS")
print("=" * 70)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = "analysis_results"

# Create directory if not exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Export each result
for item in all_results:
    name = item['name'].lower().replace(' ', '_').replace('/', '_')
    filename = f"{output_dir}/analysis_{name}_{timestamp}.json"

    ethica.export_json(item['result'], filename)
    print(f"✅ {item['name']}: {filename}")

# Export summary
summary_file = f"{output_dir}/summary_{timestamp}.json"
summary = {
    'timestamp': timestamp,
    'total_scenarios': len(all_results),
    'approved': sum(1 for r in all_results if r['result'].decision.approved),
    'rejected': sum(1 for r in all_results if not r['result'].decision.approved),
    'scenarios': [
        {
            'name': item['name'],
            'action': item['action'],
            'impact_score': item['result'].strategic['impact_score'],
            'decision': item['result'].decision.approval_type,
            'approved': item['result'].decision.approved,
            'confidence': item['result'].decision.confidence
        }
        for item in all_results
    ]
}

with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f"\n📊 Resumen comparativo: {summary_file}")

# Final statistics
print("\n" + "=" * 70)
print("ESTADÍSTICAS FINALES")
print("=" * 70)
print(f"\nTotal de escenarios analizados: {len(all_results)}")
print(f"Aprobados (UNCONDITIONAL + CONDITIONAL): {summary['approved']}")
print(f"Rechazados: {summary['rejected']}")
print(f"Tasa de aprobación: {(summary['approved'] / len(all_results) * 100):.1f}%")

avg_impact = sum(r['result'].strategic['impact_score'] for r in all_results) / len(all_results)
print(f"Impact Score promedio: {avg_impact:.1%}")

print("\n✅ Análisis completo!")
print(f"📁 Resultados guardados en: ./{output_dir}/")
