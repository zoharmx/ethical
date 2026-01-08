"""
Ethica.AI Framework - Escenarios de Ejemplo
Copia y pega estos escenarios en basic_usage.py para probar diferentes casos
"""

# ========================================
# ESCENARIO 1: EDUCACIÓN (Probablemente APROBADO)
# ========================================
scenario_education = {
    "action": "Implementar plataforma educativa gratuita con IA personalizada para países en desarrollo",
    "context": """
        ONG propone crear plataforma de aprendizaje personalizado con IA para
        estudiantes en países de bajos ingresos.

        CARACTERÍSTICAS:
        - Contenido adaptativo basado en nivel del estudiante
        - Disponible offline (descarga previa)
        - Multilingüe (50+ idiomas)
        - Sin costos para usuarios finales
        - Open source

        BENEFICIARIOS:
        - 100 millones de estudiantes potenciales
        - Profesores (herramientas de asistencia)
        - Comunidades rurales sin acceso a educación

        FINANCIAMIENTO:
        - Donaciones de fundaciones
        - Patrocinio corporativo (sin publicidad a estudiantes)
        - Gobierno nacional

        PREOCUPACIONES:
        - Privacidad de datos de menores
        - Dependencia tecnológica
        - Sesgo en contenido de IA
    """,
    "stakeholders": [
        "Estudiantes",
        "Profesores",
        "Padres de familia",
        "Gobiernos",
        "ONG educativas"
    ]
}

# ========================================
# ESCENARIO 2: SALUD (Probablemente CONDICIONAL)
# ========================================
scenario_health = {
    "action": "Desarrollar IA de diagnóstico médico para detección temprana de cáncer",
    "context": """
        Startup biotecnológica desarrolla sistema de IA que analiza imágenes
        médicas (rayos X, TAC, resonancias) para detectar cáncer en etapas tempranas.

        VENTAJAS:
        - 95% de precisión (mejor que promedio humano de 87%)
        - Reduce tiempo de diagnóstico de semanas a minutos
        - Costo 80% menor que análisis tradicional
        - Disponible 24/7

        LIMITACIONES:
        - Requiere validación por médico humano
        - No reemplaza al médico, solo asiste
        - Datos entrenados principalmente en población caucásica

        MODELO DE NEGOCIO:
        - Licenciamiento a hospitales ($50K/año)
        - Gratuito para hospitales públicos en países pobres
        - Suscripción individual ($10/mes)

        RIESGOS:
        - Falsos positivos (ansiedad innecesaria)
        - Falsos negativos (confianza errónea)
        - Sesgos demográficos en precisión
        - Privacidad de datos médicos sensibles
    """,
    "stakeholders": [
        "Pacientes",
        "Médicos",
        "Hospitales",
        "Aseguradoras",
        "Reguladores de salud"
    ]
}

# ========================================
# ESCENARIO 3: MEDIO AMBIENTE (Probablemente APROBADO)
# ========================================
scenario_environment = {
    "action": "Crear sistema de IA para optimizar redes eléctricas y reducir emisiones de CO2",
    "context": """
        Empresa de energía propone sistema de IA que optimiza distribución
        eléctrica en tiempo real para maximizar uso de energías renovables.

        IMPACTO PROYECTADO:
        - Reducción de 30% en emisiones de CO2
        - Ahorro de 20% en costos eléctricos para consumidores
        - Integración de 2x más energía solar/eólica en la red

        FUNCIONAMIENTO:
        - Predicción de demanda por IA
        - Almacenamiento inteligente en baterías
        - Balanceo automático de carga
        - Priorización de fuentes renovables

        IMPLEMENTACIÓN:
        - Piloto en 3 ciudades (1 millón de personas)
        - Expansión nacional en 3 años
        - Inversión: $500 millones

        CONSIDERACIONES:
        - Dependencia de infraestructura crítica en IA
        - Riesgo de ciberseguridad
        - Desplazamiento de trabajadores de plantas térmicas
        - Privacidad en datos de consumo eléctrico doméstico
    """,
    "stakeholders": [
        "Consumidores eléctricos",
        "Empresas de energía",
        "Trabajadores sector energético",
        "Gobierno",
        "Ambientalistas"
    ]
}

# ========================================
# ESCENARIO 4: TRABAJO (Probablemente CONDICIONAL o RECHAZADO)
# ========================================
scenario_workplace = {
    "action": "Implementar sistema de monitoreo de productividad con IA para empleados remotos",
    "context": """
        Empresa de software corporativo lanza herramienta de "productividad" que
        monitorea trabajadores remotos mediante IA.

        CARACTERÍSTICAS:
        - Captura de pantalla cada 5 minutos
        - Análisis de actividad de mouse/teclado
        - Tracking de aplicaciones usadas
        - Scoring de productividad (0-100)
        - Alertas a gerentes si score < 70

        JUSTIFICACIÓN:
        - "Accountability" en trabajo remoto
        - Identificar cuellos de botella
        - Optimizar procesos
        - Evaluar desempeño objetivamente

        IMPLEMENTACIÓN:
        - Instalación obligatoria en computadoras corporativas
        - Activo durante horario laboral
        - Acceso de datos: gerente directo + RRHH

        OPOSICIÓN:
        - Invasión de privacidad
        - Micromanagement tóxico
        - Estrés y ansiedad en empleados
        - No mide calidad, solo cantidad
        - Puede capturar información personal
    """,
    "stakeholders": [
        "Empleados",
        "Gerentes",
        "Departamento de RRHH",
        "Accionistas",
        "Sindicatos"
    ]
}

# ========================================
# ESCENARIO 5: JUSTICIA SOCIAL (Probablemente APROBADO)
# ========================================
scenario_justice = {
    "action": "Desarrollar IA para detectar sesgos discriminatorios en procesos de contratación",
    "context": """
        Organización sin fines de lucro crea herramienta de auditoría que analiza
        procesos de reclutamiento para detectar discriminación algorítmica.

        FUNCIONALIDAD:
        - Analiza descripciones de trabajo (lenguaje sesgado)
        - Audita sistemas de filtrado de CVs
        - Detecta patrones discriminatorios en contrataciones históricas
        - Genera reportes de equidad
        - Recomendaciones de mejora

        CASOS DE USO:
        - Empresas que quieren auditoría voluntaria
        - Reguladores que investigan discriminación
        - Demandas legales (evidencia de sesgo)

        ACCESO:
        - Gratuito para organizaciones sin fines de lucro
        - Licencia económica para empresas (<$5K/año)
        - Open source (transparencia)

        IMPACTO:
        - Identificó sesgo de género en 67% de empresas testeadas
        - Ayudó a revertir 15% de rechazos discriminatorios
        - Aumentó diversidad en contrataciones 23%

        LIMITACIONES:
        - Requiere acceso a datos sensibles de RRHH
        - Puede generar litigios contra empresas
        - No previene discriminación humana consciente
    """,
    "stakeholders": [
        "Candidatos discriminados",
        "Empresas",
        "Departamentos de RRHH",
        "Abogados",
        "Reguladores laborales",
        "Grupos de derechos civiles"
    ]
}

# ========================================
# ESCENARIO 6: ENTRETENIMIENTO (Probablemente NEUTRAL/CONDICIONAL)
# ========================================
scenario_entertainment = {
    "action": "Crear plataforma de contenido generado por IA para competir con creadores humanos",
    "context": """
        Startup lanza plataforma donde usuarios solicitan música, videos,
        artículos, imágenes generados completamente por IA.

        PROPUESTA:
        - Contenido ilimitado a $10/mes
        - Personalización total por usuario
        - Sin derechos de autor (IA no copia, genera)
        - 10x más barato que contratar creadores humanos

        MODELO:
        - IA entrenada con millones de obras (fair use?)
        - Generación en segundos
        - Calidad comparable a creadores promedio

        IMPACTO ECONÓMICO:
        - Desplaza a creadores freelance
        - Democratiza acceso a contenido personalizado
        - Reduce costos para pequeñas empresas

        CONTROVERSIAS:
        - ¿Es "robo" entrenar con arte existente?
        - Destrucción de empleos creativos
        - Saturación de contenido mediocre
        - Pérdida de autenticidad humana
        - Derechos de autor ambiguos

        DEFENSORES:
        - Tecnología inevitable
        - Acceso democratizado
        - Creadores pueden usar IA como herramienta

        OPONENTES:
        - Explotación de trabajo creativo previo
        - Devaluación del arte
        - Monopolización por tech companies
    """,
    "stakeholders": [
        "Creadores humanos (artistas, músicos, escritores)",
        "Consumidores de contenido",
        "Empresas pequeñas",
        "Plataformas de streaming",
        "Legisladores de propiedad intelectual"
    ]
}


# ========================================
# INSTRUCCIONES DE USO
# ========================================
"""
Para usar estos escenarios:

1. Abre examples/basic_usage.py

2. Reemplaza la sección del escenario (líneas ~30-57) con UNO de estos:

   # Reemplaza esto:
   scenario = {
       "action": "Deploy AI-powered surveillance...",
       ...
   }

   # Por esto (ejemplo):
   scenario = scenario_education

3. Guarda y ejecuta:
   python examples/basic_usage.py

4. Observa los diferentes resultados:
   - UNCONDITIONAL: Aprobado sin condiciones
   - CONDITIONAL: Aprobado con condiciones
   - REJECTED: Rechazado

RESULTADOS ESPERADOS:
- scenario_education → APROBADO (alto impacto positivo)
- scenario_health → CONDICIONAL (bueno pero con riesgos)
- scenario_environment → APROBADO (alto impacto ambiental)
- scenario_workplace → RECHAZADO (invasión de privacidad)
- scenario_justice → APROBADO (justicia social)
- scenario_entertainment → CONDICIONAL (trade-offs complejos)
"""
