# ETHICA.AI FRAMEWORK - GUÍA DE INICIO RÁPIDO

## 🚀 CONFIGURACIÓN EN 10 MINUTOS

### PASO 1: Instalar Dependencias

```bash
cd ethica-framework
python -m pip install -r requirements.txt
```

### PASO 2: Configurar Claves API

El archivo `.env` ya está configurado con tus claves API:

```bash
GEMINI_API_KEY=AIzaSyBxSQ6GGcujsIqNznxNQjJt-kKG4Wcuogo
MISTRAL_API_KEY=cqrcNINDiUWdfsRkUk9BBCq52XzphD1V
DEEPSEEK_API_KEY=sk-181034ba355c4292ad7f149d569ce4e7
```

### PASO 3: Ejecutar Ejemplo

```bash
python examples/basic_usage.py
```

**¡Listo!** Deberías ver el análisis ético completo del escenario de vigilancia.

---

## 📊 ARQUITECTURA DEL FRAMEWORK

### Sistema de 10 Módulos Interconectados:

**CAPA ESTRATÉGICA (Intención):**
1. **Purpose Validator** - Valida impacto positivo global (60% mínimo)
2. **Insight Generator** - Genera insights profundos (Mistral AI)
3. **Context Analyzer** - Análisis multi-perspectiva (Gemini + DeepSeek)

**CAPA OPERACIONAL (Fuerzas):**
4. **Opportunity Identifier** - Identifica oportunidades de beneficio
5. **Risk Assessor** - Evalúa riesgos y restricciones
6. **Conflict Resolver** - Balancea oportunidades vs riesgos

**CAPA TÁCTICA (Estructura):**
7. **Sustainability Evaluator** - Evalúa viabilidad a largo plazo
8. **Implementation Planner** - Plan de implementación detallado

**CAPA DE EJECUCIÓN (Decisión):**
9. **Integration Engine** - Integra todos los análisis
10. **Decision Orchestrator** - Decisión final (Aprobar/Rechazar)

---

## 💡 USO BÁSICO

```python
from dotenv import load_dotenv
import os
load_dotenv()

import sys
sys.path.insert(0, './src')

from core.framework import EthicaFramework

# Inicializar framework
ethica = EthicaFramework(
    gemini_api_key=os.getenv('GEMINI_API_KEY'),
    mistral_api_key=os.getenv('MISTRAL_API_KEY'),
    deepseek_api_key=os.getenv('DEEPSEEK_API_KEY')
)

# Definir escenario
scenario = {
    "action": "Tu acción propuesta aquí",
    "context": "Contexto detallado de la situación",
    "stakeholders": ["Grupo 1", "Grupo 2", "Grupo 3"]
}

# Ejecutar análisis
result = ethica.analyze(scenario)

# Ver resultados
print(f"Score de Impacto: {result.strategic['impact_score']:.1%}")
print(f"Decisión: {'APROBADO' if result.decision.approved else 'RECHAZADO'}")
print(f"Tipo: {result.decision.approval_type}")
print(f"Confianza: {result.decision.confidence:.1%}")

# Exportar a JSON
ethica.export_json(result, "mi_analisis.json")
```

---

## 📈 INTERPRETACIÓN DE RESULTADOS

### Scores Estratégicos:

- **Impact Score**: 0-100% (60% mínimo para aprobar)
  - < 60%: Rechazado automáticamente
  - 60-80%: Aprobación condicional
  - > 80%: Aprobación incondicional

- **Confidence**: 0-100% (confianza del análisis)
  - < 50%: Muchas incertidumbres
  - 50-80%: Confianza moderada
  - > 80%: Alta confianza

- **Integration Score**: 0-100% (coherencia multi-perspectiva)
  - < 50%: Conflictos no resueltos
  - 50-80%: Balance aceptable
  - > 80%: Síntesis emergente

### Scores Operacionales:

- **Harmony Score**: 0-100% (balance oportunidades/riesgos)
- **Compassion Score**: 0-100% (generosidad del impacto)
- **Severity Score**: 0-100% (gravedad de riesgos)

### Scores Tácticos:

- **Sustainability**: 0-100% (viabilidad a largo plazo)
- **Precision Score**: 0-100% (detalle del plan)
- **Readiness**: 0-100% (preparación para implementar)

### Tipos de Decisión:

1. **UNCONDITIONAL** - Proceder inmediatamente
2. **CONDITIONAL** - Proceder si se cumplen condiciones
3. **REJECTED** - No proceder

---

## 🔍 EJEMPLO DE ANÁLISIS

### Escenario: Sistema de Vigilancia con IA

**Resultado:**
```
Impact Score: 46%
Decision: REJECTED
Confidence: 100%

Razón: El score de impacto (46%) está por debajo del umbral
del 60%, indicando más daños potenciales que beneficios.
```

### Dimensiones Evaluadas:

- **Harm Reduction**: -2/10 (aumenta daño potencial)
- **Autonomy Respect**: -5/10 (viola privacidad)
- **Social Harmony**: +3/10 (reduce crimen)
- **Justice Balance**: -1/10 (desproporcionado)
- **Truthfulness**: +5/10 (basado en evidencia)

**Total**: (-2 + -5 + 3 + -1 + 5) = 0 → Normalizado a 50%
(En este caso, el modelo ajustó a 46% considerando concerns)

---

## 🎯 CASOS DE USO

### 1. Startups de IA

```python
scenario = {
    "action": "Lanzar herramienta de reclutamiento con IA",
    "context": "IA que filtra CVs automáticamente...",
    "stakeholders": ["Candidatos", "Empresa", "Sociedad"]
}
```

**Valor**: Detectar sesgos ANTES del lanzamiento.

### 2. Corporativos (ESG Compliance)

```python
scenario = {
    "action": "Implementar sistema de monitoreo de empleados",
    "context": "Para mejorar productividad...",
    "stakeholders": ["Empleados", "Gerencia", "Inversionistas"]
}
```

**Valor**: Documentar due diligence ética.

### 3. Políticas Públicas

```python
scenario = {
    "action": "Programa de subsidios para energía solar",
    "context": "Reducir emisiones de CO2...",
    "stakeholders": ["Ciudadanos", "Industria", "Medio ambiente"]
}
```

**Valor**: Análisis multi-perspectiva de impacto.

---

## 🛠️ PERSONALIZACIÓN

### Ajustar Umbral de Impacto:

```python
ethica = EthicaFramework(
    gemini_api_key=os.getenv('GEMINI_API_KEY'),
    mistral_api_key=os.getenv('MISTRAL_API_KEY'),
    deepseek_api_key=os.getenv('DEEPSEEK_API_KEY'),
    impact_threshold=0.70  # Cambiar de 60% a 70%
)
```

### Habilitar Auditoría:

```python
ethica = EthicaFramework(
    ...,
    enable_audit_trail=True,
    organization_id="mi-empresa-id"
)
```

---

## 📄 ESTRUCTURA DE RESULTADOS JSON

```json
{
  "scenario_id": "ETH-a1b2c3d4",
  "timestamp": "2025-11-30T00:33:20.123456",
  "strategic": {
    "impact_score": 0.46,
    "confidence": 0.75,
    "integration_score": 0.82
  },
  "operational": {
    "opportunities": 5,
    "risks": 8,
    "harmony_score": 0.60
  },
  "tactical": {
    "sustainability": 0.55,
    "precision": 0.70
  },
  "execution": {
    "readiness": 0.65,
    "approved": false
  },
  "decision": {
    "approved": false,
    "approval_type": "REJECTED",
    "confidence": 1.0,
    "actions": [],
    "conditions": [],
    "reasoning": "Failed purpose validation..."
  }
}
```

---

## 🚨 TROUBLESHOOTING

### Error: "ModuleNotFoundError"

```bash
# Asegúrate de estar en el directorio correcto
cd ethica-framework

# Verifica que src/ existe
ls src/

# Ejecuta desde la raíz del proyecto
python examples/basic_usage.py
```

### Error: "UnicodeEncodeError" (Windows)

Ya está resuelto en `basic_usage.py` con:

```python
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
```

### Error: "API Key Invalid"

Verifica que tus claves en `.env` sean válidas:

```bash
# Probar Gemini
curl -X POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=TU_API_KEY

# Probar Mistral
curl -X GET https://api.mistral.ai/v1/models \
  -H "Authorization: Bearer TU_API_KEY"

# Probar DeepSeek
curl -X GET https://api.deepseek.com/models \
  -H "Authorization: Bearer TU_API_KEY"
```

---

## 📚 SIGUIENTE PASO

1. **Experimenta** con diferentes escenarios
2. **Analiza** los resultados JSON en detalle
3. **Ajusta** umbrales según tu caso de uso
4. **Integra** en tu pipeline de decisiones

---

## 🎓 RECURSOS ADICIONALES

- **README.md** - Filosofía y arquitectura del framework
- **SALES_PITCH.md** - Cómo vender este servicio
- **docs/** - Documentación detallada de cada módulo

---

## ✅ CHECKLIST DE CONFIGURACIÓN

- [x] Dependencias instaladas
- [x] API keys configuradas en `.env`
- [x] Ejemplo ejecutado exitosamente
- [x] Archivo JSON generado
- [ ] Probado con tu propio escenario
- [ ] Entendido el sistema de scoring
- [ ] Revisado documentación completa

---

**¡Estás listo para usar Ethica.AI Framework!**

Para soporte: Revisa la documentación o abre un issue en el repositorio.
