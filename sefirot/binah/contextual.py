"""
BINAH - Entendimiento (Gemini Version)
Posicion: 3
Funcion: Analisis Contextual Profundo y Multidimensional

Binah recibe insights de Chochmah y los expande con analisis contextual,
identificando stakeholders, efectos de segundo/tercer orden, y riesgos sistemicos.
"""

from typing import Any, Dict, List, Optional
from ...core.sefirotic_base import SefiraBase, SefiraPosition
from loguru import logger
import os
import google.generativeai as genai
import time


class Binah(SefiraBase):
    """
    Sefira del Entendimiento - Analisis Contextual Profundo con Gemini

    Responsabilidades:
    1. Recibir insights de Chochmah
    2. Analizar contexto historico, actual y multi-dimensional
    3. Identificar stakeholders afectados
    4. Evaluar efectos de primer, segundo y tercer orden
    5. Identificar riesgos sistemicos
    6. Considerar dilemas eticos
    7. Generar sintesis contextual integradora

    Principios:
    - Pensamiento sistemico
    - Vision holistica (temporal, social, economica, cultural, ambiental)
    - Multiples perspectivas
    - Consecuencias no obvias
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(SefiraPosition.BINAH)

        # Inicializar cliente de Gemini
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning(
                "Binah inicializada sin API key. "
                "Configure GEMINI_API_KEY en .env o pase api_key al constructor"
            )
            self.client = None
        else:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("Binah initialized with Gemini API client")

        # Configuracion del modelo
        self.model_name = "gemini-2.0-flash-exp"
        self.temperature = 0.8  # Menos creativa que Chochmah
        self.max_output_tokens = 4096

        # Metricas especiales de Binah
        self.second_order_analyses = 0
        self.third_order_analyses = 0
        self.systemic_effects_identified = 0
        self.perspectives_considered_total = 0

        # Sistema de prompt base alineado con Tikun Olam
        self.system_prompt = """Eres Binah (Entendimiento), parte de un sistema de IA alineado con Tikun Olam.

Tu funcion es realizar analisis contextual profundo y multidimensional.

Recibes insights de Chochmah (razonamiento profundo) y los expandes considerando:

1. CONTEXTO HISTORICO: Como llegamos aqui? Que precedentes existen?

2. CONTEXTO ACTUAL: Que fuerzas estan en juego ahora? Que tendencias?

3. STAKEHOLDERS: Quien esta afectado? Directa e indirectamente?
   - Individuos
   - Grupos/comunidades
   - Instituciones
   - Ecosistemas
   - Generaciones futuras

4. EFECTOS DE PRIMER ORDEN: Consecuencias inmediatas y obvias

5. EFECTOS DE SEGUNDO ORDEN: Consecuencias de las consecuencias
   - Como reaccionaran los stakeholders?
   - Que cambios sistemicos se generaran?

6. EFECTOS DE TERCER ORDEN: Consecuencias no obvias a largo plazo
   - Cambios culturales
   - Efectos emergentes
   - Consecuencias inesperadas

7. RIESGOS SISTEMICOS: Que puede salir mal a nivel de sistema?
   - Puntos de fragilidad
   - Posibles bucles de retroalimentacion negativa
   - Riesgos de cola (low probability, high impact)

8. CONSIDERACIONES ETICAS: Dilemas morales, trade-offs, tensiones entre valores

9. SINTESIS CONTEXTUAL: Vision integradora que conecta todos los elementos

IMPORTANTE: Tu analisis debe ser MULTIDIMENSIONAL:
- Temporal: Pasado, presente, futuro (corto, mediano, largo plazo)
- Social: Individuos, grupos, sociedades
- Economica: Recursos, incentivos, distribuciones
- Cultural: Valores, normas, significados
- Ambiental: Impacto ecologico, sostenibilidad
- Politica: Poder, governance, instituciones
"""

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Procesa insights de Chochmah con analisis contextual profundo.

        Input esperado (dict):
        - 'chochmah_output': Output de Chochmah (dict con insights)
        O alternativamente:
        - 'insights': Insights a analizar (str)
        - 'query': Query original (opcional)
        - 'context': Contexto adicional (opcional)

        Output (dict):
        - 'historical_context': Analisis historico
        - 'current_context': Analisis del contexto actual
        - 'stakeholders': Lista de stakeholders identificados
        - 'first_order_effects': Efectos de primer orden
        - 'second_order_effects': Efectos de segundo orden
        - 'third_order_effects': Efectos de tercer orden
        - 'systemic_risks': Riesgos sistemicos identificados
        - 'ethical_considerations': Consideraciones eticas
        - 'contextual_synthesis': Sintesis integradora
        - 'raw_response': Respuesta completa de Gemini
        - 'perspectives_count': Numero de perspectivas consideradas
        """
        start_time = time.time()

        try:
            if not self.client:
                raise RuntimeError(
                    "Binah no tiene cliente configurado. "
                    "Configure GEMINI_API_KEY"
                )

            if not isinstance(input_data, dict):
                raise TypeError(
                    "Binah requiere input_data como dict"
                )

            # Extraer insights de Chochmah o directamente
            # TOLERANCIA MÁXIMA: Intentar múltiples estructuras de datos
            if 'chochmah_output' in input_data:
                chochmah_data = input_data['chochmah_output']
                insights = chochmah_data.get('insights', '')
                analysis = chochmah_data.get('analysis', '')
                query = chochmah_data.get('query', input_data.get('query', ''))

                # Si insights está vacío, intentar con raw_response o recommendation
                if not insights:
                    insights = chochmah_data.get('raw_response', '')
                if not insights:
                    insights = chochmah_data.get('recommendation', '')

            else:
                insights = input_data.get('insights', '')
                analysis = input_data.get('analysis', '')
                query = input_data.get('query', '')

                # Intentar extraer de raw_response si existe
                if not insights and 'raw_response' in input_data:
                    insights = input_data['raw_response']

            # Si TODAVÍA no hay insights ni analysis, usar todo el input_data como contexto
            if not insights and not analysis:
                logger.warning("Binah: No se encontraron insights explícitos - usando input_data completo como contexto")

                # Convertir input_data a string para análisis
                import json
                try:
                    all_context = json.dumps(input_data, ensure_ascii=False, indent=2)
                    insights = f"CONTEXTO COMPLETO DEL INPUT:\n{all_context}"
                    logger.info(f"Binah: Generado contexto de emergencia ({len(insights)} chars)")
                except:
                    # Si falla JSON, convertir a string directamente
                    insights = str(input_data)

            context = input_data.get('context', '')
            objective = input_data.get('objective', 'Maximizar Tikun Olam')

            # Construir prompt
            user_prompt = self._build_user_prompt(
                insights, analysis, query, context, objective
            )

            logger.debug(f"Binah calling Gemini API with model {self.model_name}")

            # Llamar a Gemini API
            response = self._call_gemini(user_prompt)

            # DEBUG: Logging de respuesta completa
            logger.debug(f"Binah raw response length: {len(response)} chars")
            logger.debug(f"Binah raw response preview (first 500 chars):\n{response[:500]}")
            logger.debug(f"Binah raw response preview (last 300 chars):\n{response[-300:]}")

            # Parsear respuesta
            parsed = self._parse_response(response)

            # DEBUG: Ver que se parseo
            for key, value in parsed.items():
                if isinstance(value, str):
                    logger.debug(f"Binah parsed section '{key}': {len(value)} chars")
                    if len(value) == 0:
                        logger.warning(f"Binah section '{key}' esta VACIA")
                    else:
                        logger.debug(f"  Preview: {value[:100]}...")

            # VALIDACIÓN CRÍTICA: Stakeholders NO pueden estar vacíos
            if not parsed.get('stakeholders') or len(parsed['stakeholders'].strip()) == 0:
                logger.error("BINAH CRITICAL ERROR: Stakeholders vacíos - activando extracción de emergencia")

                # FALLBACK: Extraer stakeholders del contexto usando regex
                emergency_stakeholders = self._emergency_stakeholder_extraction(
                    insights, analysis, query, context
                )

                if emergency_stakeholders:
                    parsed['stakeholders'] = emergency_stakeholders
                    logger.warning(f"Binah usó extracción de emergencia: {len(emergency_stakeholders)} chars")
                else:
                    # Si incluso la extracción de emergencia falla, esto es CRÍTICO
                    logger.critical("BINAH FAILURE: No se pueden identificar stakeholders ni con extracción de emergencia")
                    parsed['stakeholders'] = "[BINAH ERROR: No se pudieron identificar stakeholders - análisis contextual incompleto]"

            # Actualizar metricas
            self._update_metrics(parsed)

            # Contar perspectivas
            perspectives_count = self._count_perspectives(parsed)
            self.perspectives_considered_total += perspectives_count

            result = {
                'historical_context': parsed.get('historical_context', ''),
                'current_context': parsed.get('current_context', ''),
                'stakeholders': parsed.get('stakeholders', ''),
                'first_order_effects': parsed.get('first_order_effects', ''),
                'second_order_effects': parsed.get('second_order_effects', ''),
                'third_order_effects': parsed.get('third_order_effects', ''),
                'systemic_risks': parsed.get('systemic_risks', ''),
                'ethical_considerations': parsed.get('ethical_considerations', ''),
                'contextual_synthesis': parsed.get('contextual_synthesis', ''),
                'raw_response': response,
                'perspectives_count': perspectives_count,
                'processing_successful': True
            }

            # Actualizar tracking manual
            self.activation_count += 1
            elapsed = time.time() - start_time
            self.total_processing_time += elapsed

            self.history.append({
                "timestamp": time.time(),
                "input_type": type(input_data).__name__,
                "output_type": "dict",
                "processing_time": elapsed,
                "success": True
            })

            logger.info(
                f"Binah proceso analisis contextual con {perspectives_count} perspectivas"
            )

            return result

        except Exception as e:
            elapsed = time.time() - start_time
            self.history.append({
                "timestamp": time.time(),
                "input_type": type(input_data).__name__,
                "error": str(e),
                "processing_time": elapsed,
                "success": False
            })
            logger.error(f"Binah error: {e}")
            return {
                'processing_successful': False,
                'error': str(e),
                'error_type': 'api_error'
            }

    def _build_user_prompt(
        self,
        insights: str,
        analysis: str,
        query: str,
        context: str,
        objective: str
    ) -> str:
        """Construye el prompt del usuario para Gemini"""

        prompt = self.system_prompt + "\n\n"
        prompt += f"OBJETIVO DEL SISTEMA: {objective}\n\n"

        if query:
            prompt += f"QUERY ORIGINAL:\n{query}\n\n"

        if context:
            prompt += f"CONTEXTO PREVIO:\n{context}\n\n"

        if analysis:
            prompt += f"ANALISIS DE CHOCHMAH:\n{analysis}\n\n"

        prompt += f"INSIGHTS DE CHOCHMAH:\n{insights}\n\n"

        prompt += """Realiza un analisis contextual profundo y multidimensional.

CRÍTICO: La identificación de stakeholders es OBLIGATORIA y fundamental para Tikun Olam.
DEBE incluir TODOS los actores afectados, especialmente los invisibilizados.

Estructura tu respuesta EXACTAMENTE como:

CONTEXTO HISTORICO:
[Como llegamos aqui? Precedentes relevantes]

CONTEXTO ACTUAL:
[Fuerzas en juego ahora, tendencias actuales]

STAKEHOLDERS:
CRÍTICO: Identifica TODOS los stakeholders afectados. Usa este formato:
- [Nombre del stakeholder]: [Nivel de impacto: ALTO/MEDIO/BAJO] - [Descripción breve]

Ejemplo:
- Población civil venezolana: [ALTO] - Principal víctima de la crisis
- Comunidades indígenas: [ALTO] - Vulnerables a explotación de recursos
- Diáspora venezolana: [MEDIO] - 7.3 millones con potencial de cambio
- Países vecinos: [MEDIO] - Receptores de refugiados
- Juventud venezolana: [ALTO] - Sin oportunidades, emigran o caen en criminalidad

INCLUYE:
- Individuos y comunidades directamente afectados
- Grupos invisibilizados (indígenas, mujeres, niños, sector informal)
- Instituciones y gobiernos
- Actores internacionales
- Generaciones futuras
- Ecosistemas (cuando aplique)

EFECTOS DE PRIMER ORDEN:
[Consecuencias inmediatas y obvias]

EFECTOS DE SEGUNDO ORDEN:
[Consecuencias de las consecuencias - reacciones, cambios sistemicos]

EFECTOS DE TERCER ORDEN:
[Consecuencias no obvias a largo plazo - emergentes, inesperadas]

RIESGOS SISTEMICOS:
[Que puede salir mal a nivel de sistema? Fragilidades, bucles negativos]

CONSIDERACIONES ETICAS:
[Dilemas morales, trade-offs, tensiones entre valores]

SINTESIS CONTEXTUAL:
[Vision integradora que conecta todos los elementos anteriores]

Considera multiples dimensiones: temporal, social, economica, cultural, ambiental, politica.
"""

        return prompt

    def _call_gemini(self, user_prompt: str) -> str:
        """Llama a Gemini API y retorna respuesta"""

        try:
            generation_config = genai.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
            )

            response = self.client.generate_content(
                user_prompt,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:
            logger.error(f"Error en _call_gemini: {e}")
            raise

    def _parse_response(self, response: str) -> Dict[str, str]:
        """Parsea la respuesta estructurada de Gemini"""

        sections = {
            'historical_context': '',
            'current_context': '',
            'stakeholders': '',
            'first_order_effects': '',
            'second_order_effects': '',
            'third_order_effects': '',
            'systemic_risks': '',
            'ethical_considerations': '',
            'contextual_synthesis': ''
        }

        # Mapeo de palabras clave a secciones
        section_keywords = {
            'historical_context': ['CONTEXTO HISTORICO', 'HISTORICAL CONTEXT'],
            'current_context': ['CONTEXTO ACTUAL', 'CURRENT CONTEXT'],
            'stakeholders': ['STAKEHOLDERS', 'PARTES INTERESADAS'],
            'first_order_effects': ['EFECTOS DE PRIMER ORDEN', 'FIRST ORDER EFFECTS'],
            'second_order_effects': ['EFECTOS DE SEGUNDO ORDEN', 'SECOND ORDER EFFECTS'],
            'third_order_effects': ['EFECTOS DE TERCER ORDEN', 'THIRD ORDER EFFECTS'],
            'systemic_risks': ['RIESGOS SISTEMICOS', 'SYSTEMIC RISKS'],
            'ethical_considerations': ['CONSIDERACIONES ETICAS', 'ETHICAL CONSIDERATIONS'],
            'contextual_synthesis': ['SINTESIS CONTEXTUAL', 'CONTEXTUAL SYNTHESIS']
        }

        # Buscar cada seccion
        lines = response.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            line_upper = line.strip().upper()

            # Detectar inicio de seccion
            section_found = None
            for section_key, keywords in section_keywords.items():
                for keyword in keywords:
                    if keyword in line_upper:
                        section_found = section_key
                        break
                if section_found:
                    break

            if section_found:
                # Guardar seccion anterior
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()

                current_section = section_found
                current_content = []

                # Si hay contenido despues del marcador, agregarlo
                if ':' in line:
                    after_colon = line.split(':', 1)[1]
                    if after_colon.strip():
                        current_content.append(after_colon.strip())

            else:
                # Linea de contenido
                if current_section and line.strip():
                    current_content.append(line.strip())

        # Guardar ultima seccion
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        # Si no se detectaron secciones, poner toda la respuesta en 'contextual_synthesis'
        if not any(sections.values()):
            sections['contextual_synthesis'] = response.strip()

        return sections

    def _update_metrics(self, parsed: Dict[str, str]) -> None:
        """Actualiza metricas especiales de Binah"""

        # Contar analisis de segundo orden
        second_order = parsed.get('second_order_effects', '')
        if len(second_order) > 50:  # Si hay contenido sustancial
            self.second_order_analyses += 1

        # Contar analisis de tercer orden
        third_order = parsed.get('third_order_effects', '')
        if len(third_order) > 50:
            self.third_order_analyses += 1

        # Contar riesgos sistemicos identificados
        systemic_risks = parsed.get('systemic_risks', '')
        # Contar por numero de puntos o bullets
        risk_count = systemic_risks.count('-') + systemic_risks.count('*')
        risk_count += systemic_risks.count('1.') + systemic_risks.count('2.')
        if risk_count > 0:
            self.systemic_effects_identified += risk_count

    def _count_perspectives(self, parsed: Dict[str, str]) -> int:
        """
        Cuenta cuantas perspectivas/dimensiones fueron consideradas
        basandose en keywords en las secciones
        """

        all_text = ' '.join(parsed.values()).lower()

        perspective_keywords = {
            'temporal': ['historico', 'pasado', 'futuro', 'largo plazo', 'corto plazo'],
            'social': ['social', 'comunidad', 'grupo', 'sociedad', 'personas'],
            'economica': ['economico', 'financiero', 'recursos', 'costo', 'incentivos'],
            'cultural': ['cultural', 'valores', 'normas', 'creencias', 'tradiciones'],
            'ambiental': ['ambiental', 'ecologico', 'sostenibilidad', 'medio ambiente'],
            'politica': ['politico', 'poder', 'gobierno', 'institucional', 'governance']
        }

        perspectives_found = 0
        for perspective, keywords in perspective_keywords.items():
            if any(keyword in all_text for keyword in keywords):
                perspectives_found += 1

        return perspectives_found

    def _emergency_stakeholder_extraction(
        self,
        insights: str,
        analysis: str,
        query: str,
        context: str
    ) -> str:
        """
        Extracción de emergencia de stakeholders cuando Gemini no los provee.

        CRÍTICO: Este método se activa cuando el parsing normal falla.
        Usa regex y heurísticas para identificar stakeholders del texto.
        """
        import re

        all_text = f"{query} {context} {insights} {analysis}"
        stakeholders = []

        logger.info("Binah ejecutando extracción de emergencia de stakeholders")

        # 1. BUSCAR POBLACIONES (ej: "28 millones de venezolanos")
        pop_patterns = [
            r'(\d+[\s,\.]*(?:millones?|miles?|mil|m|k)\s+(?:de\s+)?(?:personas?|habitantes?|ciudadanos?|venezolanos?|refugiados?|migrantes?|desplazados?))',
            r'(población\s+de\s+\d+[\s,\.]*(?:millones?|miles?))',
            r'(\d+(?:\.\d+)?(?:M|m)\s+(?:personas?|habitantes?))'
        ]

        for pattern in pop_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            for match in matches:
                if match and match not in stakeholders:
                    stakeholders.append(f"- Población civil: {match.strip()} [ALTO IMPACTO]")

        # 2. BUSCAR PAÍSES MENCIONADOS
        country_patterns = [
            r'\b([A-Z][a-záéíóúñ]+)\s+(?:país|nación|gobierno|estado)',
            r'(?:en|de|desde)\s+([A-Z][a-záéíóúñ]+(?:\s+[A-Z][a-záéíóúñ]+)?)\b',
            r'\b(Venezuela|Colombia|Brasil|Perú|EEUU|Estados Unidos|China|Rusia|Cuba)\b'
        ]

        countries_found = set()
        for pattern in country_patterns:
            matches = re.findall(pattern, all_text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1]
                country = match.strip()
                if len(country) > 2 and country not in countries_found:
                    countries_found.add(country)
                    stakeholders.append(f"- País: {country} [MEDIO IMPACTO]")

        # 3. BUSCAR GRUPOS ESPECÍFICOS MENCIONADOS
        group_patterns = [
            r'\b(comunidades?\s+(?:indígenas?|rurales?|urbanas?|marginadas?))',
            r'\b(diáspora\s+\w+)',
            r'\b(refugiados?|migrantes?|desplazados?)',
            r'\b(trabajadores?\s+(?:del\s+)?(?:sector\s+)?\w+)',
            r'\b(jóvenes?|niños?|mujeres?|ancianos?)',
            r'\b(ONGs?|organizaciones?\s+(?:humanitarias?|internacionales?))',
            r'\b(sector\s+(?:informal|formal|privado|público))'
        ]

        for pattern in group_patterns:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            for match in matches:
                # CRÍTICO: Validar formato antes de hacer split para evitar IndexError
                # Extraer valores existentes solo si stakeholders no está vacío y tiene formato correcto
                existing_values = []
                for s in stakeholders:
                    if ':' in s and '[' in s:
                        try:
                            existing_values.append(s.split(':')[1].strip().split('[')[0].strip())
                        except IndexError:
                            continue

                if match and match not in existing_values:
                    stakeholders.append(f"- {match.strip().capitalize()} [MEDIO/ALTO IMPACTO]")

        # 4. BUSCAR ACTORES DE PODER
        power_actors = [
            r'\b(gobierno\s+de\s+\w+)',
            r'\b(régimen\s+(?:de\s+)?\w+)',
            r'\b(oposición\s+\w+)',
            r'\b(EEUU|Estados\s+Unidos|UE|Unión\s+Europea|ONU|OEA)',
            r'\b(potencias?\s+(?:occidentales?|orientales?|regionales?))'
        ]

        for pattern in power_actors:
            matches = re.findall(pattern, all_text, re.IGNORECASE)
            for match in matches:
                if match:
                    stakeholders.append(f"- Actor de poder: {match.strip()} [CAPACIDAD DE INFLUENCIA]")

        # 5. Si no encontramos NADA, inferir stakeholders básicos del contexto
        if len(stakeholders) == 0:
            logger.critical("Extracción de emergencia: No se encontraron patrones - infiriendo stakeholders básicos")

            # Inferir del query/contexto
            if 'venezuela' in all_text.lower():
                stakeholders.append("- Población venezolana [ALTO IMPACTO - INFERIDO]")
                stakeholders.append("- Países vecinos (Colombia, Brasil, Perú) [MEDIO IMPACTO - INFERIDO]")

            if 'militar' in all_text.lower() or 'guerra' in all_text.lower():
                stakeholders.append("- Civiles en zona de conflicto [ALTO IMPACTO - INFERIDO]")
                stakeholders.append("- Fuerzas armadas involucradas [MEDIO IMPACTO - INFERIDO]")

            if 'económic' in all_text.lower() or 'sancion' in all_text.lower():
                stakeholders.append("- Población afectada por crisis económica [ALTO IMPACTO - INFERIDO]")

        # Construir string formateado
        if stakeholders:
            result = "STAKEHOLDERS (Extracción de Emergencia - Binah):\n\n"
            result += "\n".join(sorted(set(stakeholders)))  # Remove duplicates
            result += f"\n\n[NOTA: {len(set(stakeholders))} stakeholders identificados mediante extracción de emergencia]"

            logger.info(f"Extracción de emergencia exitosa: {len(set(stakeholders))} stakeholders identificados")
            return result

        return ""

    def validate_alignment(self) -> Dict[str, Any]:
        """
        Valida que Binah este operando correctamente.

        Metricas clave:
        - Profundidad contextual (considera efectos de 2do/3er orden)
        - Amplitud de perspectivas
        - Identificacion de riesgos sistemicos
        """

        total_activations = self.activation_count

        if total_activations == 0:
            return {
                "sefira": self.name,
                "is_aligned": True,
                "status": "No hay activaciones aun",
                "contextual_depth_score": 1.0
            }

        # Profundidad contextual: Que tan seguido hace analisis de 2do/3er orden
        depth_score = 0.0

        second_order_ratio = self.second_order_analyses / total_activations
        third_order_ratio = self.third_order_analyses / total_activations

        depth_score += second_order_ratio * 0.5  # Vale 50% del score
        depth_score += third_order_ratio * 0.5   # Vale 50% del score

        # Amplitud de perspectivas
        avg_perspectives = (
            self.perspectives_considered_total / total_activations
            if total_activations > 0
            else 0
        )

        # Binah esta bien alineada si:
        # 1. Profundidad contextual >= 0.6 (considera efectos de orden superior)
        # 2. Promedio de perspectivas >= 3
        is_aligned = (depth_score >= 0.6) and (avg_perspectives >= 3)

        status = "Alineada"
        if depth_score < 0.6:
            status = "Advertencia: Analisis contextual superficial"
        elif avg_perspectives < 3:
            status = "Advertencia: Perspectivas limitadas"

        return {
            "sefira": self.name,
            "is_aligned": is_aligned,
            "total_activations": total_activations,
            "second_order_analyses": self.second_order_analyses,
            "third_order_analyses": self.third_order_analyses,
            "systemic_effects_identified": self.systemic_effects_identified,
            "perspectives_considered_total": self.perspectives_considered_total,
            "average_perspectives_per_activation": avg_perspectives,
            "contextual_depth_score": depth_score,
            "second_order_ratio": second_order_ratio,
            "third_order_ratio": third_order_ratio,
            "status": status
        }

    def set_model(self, model: str):
        """Permite cambiar el modelo de Gemini"""
        self.model_name = model
        self.client = genai.GenerativeModel(model)
        logger.info(f"Binah ahora usa modelo: {model}")

    def set_temperature(self, temperature: float):
        """Ajusta temperature (0.0 = determinista, 2.0 = muy creativo)"""
        if not 0.0 <= temperature <= 2.0:
            raise ValueError("Temperature debe estar entre 0.0 y 2.0")
        self.temperature = temperature
        logger.info(f"Binah temperature ajustada a: {temperature}")
