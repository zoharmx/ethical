# BINAH - Entendimiento

**Posicion**: 3
**Nombre Hebreo**: בינה (Binah)
**Funcion**: Analisis Contextual Profundo y Multidimensional
**API**: Google Gemini
**Temperature**: 0.8

## Resumen Rapido

Binah recibe los insights de Chochmah y los expande contextualmente, analizando:
- Stakeholders afectados
- Efectos de 1er, 2do y 3er orden
- Riesgos sistemicos
- Dilemas eticos
- Contexto historico y actual

## Instalacion

```bash
# Binah ya esta incluida en el proyecto
# Solo necesitas configurar GEMINI_API_KEY

# En tu archivo .env:
GEMINI_API_KEY=tu_api_key_aqui
```

## Uso Basico

```python
from src.sefirot.binah import Binah
from src.sefirot.chochmah_gemini import ChochmahGemini

# Crear instancias
chochmah = ChochmahGemini()
binah = Binah()

# Flujo completo: Chochmah -> Binah
query = "Deberiamos implementar vehiculos autonomos en toda la ciudad?"

# Paso 1: Chochmah razona
chochmah_result = chochmah.process({'query': query})

# Paso 2: Binah analiza contexto
binah_result = binah.process({
    'chochmah_output': chochmah_result,
    'query': query
})

# Ver resultados
print("Stakeholders:", binah_result['stakeholders'])
print("Efectos de 2do orden:", binah_result['second_order_effects'])
print("Riesgos sistemicos:", binah_result['systemic_risks'])
```

## Estructura de Output

```python
{
    'historical_context': str,          # Como llegamos aqui
    'current_context': str,             # Fuerzas actuales
    'stakeholders': str,                # Quienes estan afectados
    'first_order_effects': str,         # Consecuencias inmediatas
    'second_order_effects': str,        # Reacciones y cambios sistemicos
    'third_order_effects': str,         # Efectos emergentes largo plazo
    'systemic_risks': str,              # Fragilidades, bucles negativos
    'ethical_considerations': str,      # Dilemas morales
    'contextual_synthesis': str,        # Vision integradora
    'perspectives_count': int,          # Dimensiones consideradas
    'processing_successful': bool
}
```

## Metricas de Alineamiento

```python
alignment = binah.validate_alignment()

# Binah esta bien alineada si:
# - contextual_depth_score >= 0.6
# - average_perspectives_per_activation >= 3

print(alignment['contextual_depth_score'])  # 0.0 a 1.0
print(alignment['is_aligned'])              # True/False
print(alignment['status'])                  # "Alineada" o advertencia
```

## Ejemplos

### Ejemplo 1: Politica Publica

```python
binah = Binah()

query = "Implementar transporte publico gratuito en la ciudad"

# Con insights previos de Chochmah
result = binah.process({
    'insights': 'Reducira costos de transporte, pero requiere financiamiento via impuestos',
    'query': query
})

print(result['stakeholders'])
# Muestra: residentes de bajos ingresos, conductores privados,
#          gobierno local, empresas, medio ambiente, etc.

print(result['second_order_effects'])
# Muestra: cambios en patrones de vivienda, desarrollo urbano,
#          reduccion de contaminacion, etc.
```

### Ejemplo 2: Decision Empresarial

```python
binah = Binah()

result = binah.process({
    'insights': 'Automatizar atencion al cliente reduce costos pero puede afectar calidad',
    'query': 'Debemos reemplazar operadores humanos con chatbots?',
    'context': 'Empresa mediana, 50 operadores actuales'
})

print(result['ethical_considerations'])
# Analiza: impacto en empleados, calidad de servicio,
#          responsabilidad corporativa, etc.
```

## Configuracion Avanzada

### Ajustar Temperature

```python
binah = Binah()

# Analisis conservador (0.3-0.6)
binah.set_temperature(0.5)

# Analisis balanceado (0.7-0.9) - DEFAULT
binah.set_temperature(0.8)

# Analisis exploratorio (1.0-1.5)
binah.set_temperature(1.2)
```

### Cambiar Modelo

```python
binah = Binah()
binah.set_model('gemini-1.5-pro')
```

## Tests

```bash
# Test basico
python tests/test_binah_basic.py

# Ejemplos completos
python examples/example_binah_usage.py
```

## Cuando Usar Binah

### SI usar Binah cuando:
- Necesitas entender stakeholders afectados
- Quieres identificar efectos no obvios
- Hay dilemas eticos complejos
- Necesitas analisis multidimensional (social, economico, cultural, etc.)
- Quieres identificar riesgos sistemicos

### NO usar Binah cuando:
- Solo necesitas razonamiento simple
- No hay multiples stakeholders
- El problema es puramente tecnico sin contexto social
- Ya tienes todo el contexto y solo necesitas decision

## Diferencia con Chochmah

| Aspecto | Chochmah | Binah |
|---------|----------|-------|
| **Pregunta** | "Que significa esto?" | "Que implica esto?" |
| **Enfoque** | Patrones, insights | Contexto, stakeholders |
| **Salida** | Comprension fundamental | Analisis multidimensional |
| **Temperature** | 1.0 | 0.8 |
| **Tiempo** | Atemporal | Pasado/presente/futuro |

## Troubleshooting

### Error: "Binah no tiene cliente configurado"
**Solucion**: Configura `GEMINI_API_KEY` en tu archivo `.env`

### Error: "Input debe contener 'insights'"
**Solucion**: Pasa `chochmah_output` o directamente `insights` en el input

### Warning: "Analisis contextual superficial"
**Solucion**: Binah no esta identificando suficientes efectos de 2do/3er orden.
- Verifica que el prompt incluye contexto rico
- Considera aumentar la temperature
- Revisa que el modelo tiene capacidad suficiente

### Binah considera muy pocas perspectivas
**Solucion**:
- Pasa mas contexto en el input
- Menciona explicitamente dimensiones relevantes (social, economico, etc.)
- Aumenta temperature para analisis mas exploratorio

## Recursos

- **Documentacion completa**: `docs/binah_documentation.md`
- **Tests**: `tests/test_binah_basic.py`
- **Ejemplos**: `examples/example_binah_usage.py`
- **Codigo fuente**: `src/sefirot/binah.py`

## Contribuir

Si encuentras bugs o quieres mejorar Binah:
1. Agrega tests que demuestren el problema
2. Implementa la solucion
3. Verifica que todos los tests pasen
4. Actualiza la documentacion

## Licencia

Parte del proyecto Tikun - Sistema de IA Alineada
