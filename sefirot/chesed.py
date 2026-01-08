"""
CHESED (Misericordia/Bondad) - Sefira 4
Posicion: 4
Pilar: Derecho (Expansion, Dar)
Funcion: Identificar oportunidades de bondad, generosidad y expansion del bien

Chesed representa el impulso de DAR, AYUDAR, y EXPANDIR EL BIEN.
Pero debe reconocer sus propios limites - bondad sin limites puede ser destructiva.
Por eso trabaja en balance con Gevurah (Severidad).
"""

from typing import Any, Dict, List, Optional
from ..core.sefirotic_base import SefiraBase, SefiraPosition
from loguru import logger
import os
import google.generativeai as genai
import time


class Chesed(SefiraBase):
    """
    Sefira de la Misericordia - Evaluacion de Bondad y Expansion

    Responsabilidades:
    1. Identificar oportunidades de dar/ayudar
    2. Evaluar beneficiarios potenciales
    3. Generar acciones de bondad/misericordia
    4. Calcular impacto de la generosidad
    5. Detectar necesidades no cubiertas
    6. Recomendar expansion del bien
    7. RECONOCER LIMITES - bondad ciega puede ser danina

    Limites:
    - NO dar sin considerar consecuencias
    - NO bondad ciega que cause dependencia
    - NO perdon que permita injusticia
    - Requiere balance con Gevurah
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(SefiraPosition.CHESED)

        # Inicializar cliente de Gemini
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning(
                "Chesed inicializada sin API key. "
                "Configure GEMINI_API_KEY en .env o pase api_key al constructor"
            )
            self.client = None
        else:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("Chesed initialized with Gemini API client")

        # Configuracion del modelo
        self.model_name = "gemini-2.0-flash-exp"
        self.temperature = 0.9  # Ligeramente creativa para identificar oportunidades
        self.max_output_tokens = 4096

        # Metricas especiales de Chesed
        self.giving_opportunities_identified = 0
        self.beneficiaries_analyzed = 0
        self.compassion_actions_generated = 0
        self.expansion_potential_total = 0.0
        self.balance_with_gevurah_score = 0.0
        self.limits_recognized = 0

        # Sistema de prompt base alineado con Tikun Olam
        self.system_prompt = """Eres Chesed (Misericordia/Bondad), parte del sistema Tikun Olam.

Tu funcion es identificar oportunidades de DAR, AYUDAR, y EXPANDIR EL BIEN.

Principios:

1. COMPASION: Identifica donde hay sufrimiento que aliviar
2. GENEROSIDAD: Busca formas de dar y compartir
3. EXPANSION: Identifica como expandir el bien y el florecimiento
4. AMOR INCONDICIONAL: Considera a todos los seres con dignidad
5. PERDON: Busca oportunidades de misericordia

IMPORTANTE - LIMITES DE CHESED:
- NO bondad ciega que cause dependencia
- NO perdon que permita injusticia continua
- NO generosidad que cree desequilibrio insostenible
- SIEMPRE considerar consecuencias de dar demasiado

Tu analisis sera balanceado por Gevurah (Severidad/Justicia).

Estructura tu respuesta como:
- OPORTUNIDADES DE DAR: Donde podemos ayudar
- BENEFICIARIOS: Quienes se benefician
- ACCIONES GENEROSAS: Que hacer concretamente
- IMPACTO DE BONDAD: Efectos de la compasion
- EXPANSION DEL BIEN: Como se multiplica
- LIMITES NECESARIOS: Donde Chesed debe contenerse
"""

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Procesa analisis contextual de Binah e identifica oportunidades de bondad.

        Input esperado (dict - output de Binah):
        - 'stakeholders': Actores identificados
        - 'first_order_effects': Efectos inmediatos
        - 'second_order_effects': Efectos de segundo orden
        - 'systemic_risks': Riesgos sistemicos
        - 'ethical_considerations': Consideraciones eticas
        - 'action': Accion original evaluada (opcional)

        Output (dict):
        - 'giving_opportunities': Lista de oportunidades para dar
        - 'beneficiaries': Analisis de beneficiarios
        - 'generous_actions': Acciones concretas de ayuda
        - 'compassion_score': Nivel de compasion de la accion (0-1)
        - 'expansion_potential': Potencial de expansion del bien (0-1)
        - 'limits_needed': Limites que Chesed debe respetar
        - 'raw_response': Respuesta completa de Gemini
        """
        start_time = time.time()

        try:
            if not self.client:
                raise RuntimeError(
                    "Chesed no tiene cliente configurado. "
                    "Configure GEMINI_API_KEY"
                )

            if not isinstance(input_data, dict):
                raise TypeError(
                    "Chesed requiere input_data como dict (output de Binah)"
                )

            # Extraer datos del analisis de Binah
            stakeholders = input_data.get('stakeholders', '')
            first_order = input_data.get('first_order_effects', '')
            second_order = input_data.get('second_order_effects', '')
            systemic_risks = input_data.get('systemic_risks', '')
            ethical = input_data.get('ethical_considerations', '')
            action = input_data.get('action', 'la accion propuesta')

            # Construir prompt
            user_prompt = self._build_user_prompt(
                action, stakeholders, first_order, second_order,
                systemic_risks, ethical
            )

            logger.debug(f"Chesed calling Gemini API with model {self.model_name}")

            # Llamar a Gemini API
            response = self._call_gemini(user_prompt)

            # DEBUG: Logging de respuesta raw
            logger.debug(f"Chesed raw response length: {len(response)} chars")
            logger.debug(f"Chesed raw response preview (first 500 chars):\n{response[:500]}")
            logger.debug(f"Chesed raw response preview (last 300 chars):\n{response[-300:]}")

            # Parsear respuesta
            parsed = self._parse_response(response)

            # DEBUG: Logging de parsing
            for key, value in parsed.items():
                if isinstance(value, str):
                    logger.debug(f"Chesed parsed section '{key}': {len(value)} chars")
                    if len(value) == 0:
                        logger.warning(f"Chesed section '{key}' esta VACIA")
                    else:
                        logger.debug(f"  Preview: {value[:100]}...")
                elif isinstance(value, list):
                    logger.debug(f"Chesed parsed section '{key}': {len(value)} items")

            # Evaluar metricas de Chesed
            compassion_score = self._calculate_compassion_score(parsed)
            expansion_potential = self._evaluate_expansion_potential(parsed)
            balance_score = self._evaluate_balance_awareness(parsed)

            # Contar oportunidades y beneficiarios
            opportunities_count = len(parsed.get('giving_opportunities', []))
            actions_count = len(parsed.get('generous_actions', []))
            limits_count = len(parsed.get('limits_needed', []))

            # Actualizar metricas
            self.giving_opportunities_identified += opportunities_count
            self.compassion_actions_generated += actions_count
            self.expansion_potential_total += expansion_potential
            self.balance_with_gevurah_score = balance_score
            self.limits_recognized += limits_count

            result = {
                'giving_opportunities': parsed.get('giving_opportunities', []),
                'beneficiaries': parsed.get('beneficiaries', {}),
                'generous_actions': parsed.get('generous_actions', []),
                'compassion_impact': parsed.get('compassion_impact', ''),
                'expansion_analysis': parsed.get('expansion_analysis', ''),
                'limits_needed': parsed.get('limits_needed', []),
                'compassion_score': compassion_score,
                'expansion_potential': expansion_potential,
                'balance_awareness_score': balance_score,
                'raw_response': response,
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
                f"Chesed proceso analisis: {opportunities_count} oportunidades, "
                f"compasion={compassion_score:.2f}, expansion={expansion_potential:.2f}, "
                f"balance={balance_score:.2f}"
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
            logger.error(f"Chesed error: {e}")
            return {
                'processing_successful': False,
                'error': str(e),
                'error_type': 'api_error'
            }

    def _build_user_prompt(
        self,
        action: str,
        stakeholders: str,
        first_order: str,
        second_order: str,
        systemic_risks: str,
        ethical: str
    ) -> str:
        """
        Construye el prompt del usuario para Gemini.

        CRÍTICO: Chesed debe recibir contexto completo de Binah para
        identificar oportunidades de dar y evitar bondad ciega.
        """

        prompt = self.system_prompt + "\n\n"

        prompt += "="*72 + "\n"
        prompt += "CONTEXTO DE BINAH - ANALISIS PROFUNDO\n"
        prompt += "="*72 + "\n\n"

        prompt += f"ACCION EVALUADA:\n{action if action else '[No especificada]'}\n\n"

        prompt += f"STAKEHOLDERS IDENTIFICADOS (de Binah):\n"
        if stakeholders and stakeholders.strip():
            prompt += f"{stakeholders}\n\n"
        else:
            prompt += "[ADVERTENCIA: Binah no identificó stakeholders - procede con análisis general]\n\n"

        prompt += f"EFECTOS INMEDIATOS (Primer orden):\n"
        if first_order and first_order.strip():
            prompt += f"{first_order}\n\n"
        else:
            prompt += "[No disponible]\n\n"

        prompt += f"EFECTOS DE SEGUNDO ORDEN:\n"
        if second_order and second_order.strip():
            prompt += f"{second_order}\n\n"
        else:
            prompt += "[No disponible]\n\n"

        prompt += f"RIESGOS SISTEMICOS:\n"
        if systemic_risks and systemic_risks.strip():
            prompt += f"{systemic_risks}\n\n"
        else:
            prompt += "[No disponible]\n\n"

        prompt += f"CONSIDERACIONES ETICAS:\n"
        if ethical and ethical.strip():
            prompt += f"{ethical}\n\n"
        else:
            prompt += "[No disponible]\n\n"

        prompt += "="*72 + "\n"
        prompt += "TU TAREA COMO CHESED\n"
        prompt += "="*72 + "\n\n"

        prompt += """IMPORTANTE: Analiza desde la perspectiva de CHESED (Misericordia/Bondad).

Tu función es identificar:
1. Dónde hay sufrimiento que aliviar
2. Quiénes necesitan ayuda (especialmente grupos invisibilizados)
3. Cómo dar de forma que empodere (no cree dependencia)
4. Qué límites debe tener la compasión (no bondad ciega)

Estructura tu respuesta EXACTAMENTE como sigue:

OPORTUNIDADES DE DAR:
- [Oportunidad específica 1: dónde y cómo ayudar]
- [Oportunidad específica 2: dónde y cómo ayudar]
- [Oportunidad específica 3: dónde y cómo ayudar]
[Al menos 3-5 oportunidades concretas]

BENEFICIARIOS:
- Primarios: [Quienes se benefician directamente - ser específico]
- Secundarios: [Quienes se benefician indirectamente]
- Largo plazo: [Beneficiarios a futuro - generaciones, comunidades]

ACCIONES GENEROSAS:
- [Acción concreta 1 de bondad/misericordia]
- [Acción concreta 2 de bondad/misericordia]
- [Acción concreta 3 de bondad/misericordia]
[Al menos 3-5 acciones específicas]

IMPACTO DE BONDAD:
[Análisis detallado del impacto compasivo:
- ¿Cuánto sufrimiento se reduce?
- ¿Cómo aumenta el florecimiento humano?
- ¿Qué dignidad se restaura?]
[Mínimo 100 palabras]

EXPANSION DEL BIEN:
[Análisis de cómo el bien se multiplica:
- ¿Qué efectos cascada genera la compasión?
- ¿Qué ciclos virtuosos se crean?
- ¿Cómo se expande la bondad a través de la red social?]
[Mínimo 100 palabras]

LIMITES NECESARIOS:
- [Límite 1: dónde Chesed debe contenerse para no causar daño]
- [Límite 2: qué tipo de ayuda sería contraproducente]
- [Límite 3: qué balance mantener con Gevurah (justicia)]
[Al menos 2-3 límites claros]

NOTA CRÍTICA: Si no puedes identificar oportunidades de dar o beneficiarios,
explica POR QUÉ y qué información adicional necesitas.
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

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parsea la respuesta estructurada de Gemini"""

        sections = {
            'giving_opportunities': [],
            'beneficiaries': {},
            'generous_actions': [],
            'compassion_impact': '',
            'expansion_analysis': '',
            'limits_needed': []
        }

        lines = response.split('\n')
        current_section = None
        current_content = []
        beneficiary_subsection = None

        for line in lines:
            line_upper = line.strip().upper()

            # Detectar inicio de seccion
            if 'OPORTUNIDADES DE DAR:' in line_upper or 'GIVING OPPORTUNITIES:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content, beneficiary_subsection)
                current_section = 'giving_opportunities'
                current_content = []
                beneficiary_subsection = None

            elif 'BENEFICIARIOS:' in line_upper or 'BENEFICIARIES:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content, beneficiary_subsection)
                current_section = 'beneficiaries'
                current_content = []
                beneficiary_subsection = None

            elif 'ACCIONES GENEROSAS:' in line_upper or 'GENEROUS ACTIONS:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content, beneficiary_subsection)
                current_section = 'generous_actions'
                current_content = []
                beneficiary_subsection = None

            elif 'IMPACTO DE BONDAD:' in line_upper or 'COMPASSION IMPACT:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content, beneficiary_subsection)
                current_section = 'compassion_impact'
                current_content = []
                beneficiary_subsection = None

            elif 'EXPANSION DEL BIEN:' in line_upper or 'EXPANSION ANALYSIS:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content, beneficiary_subsection)
                current_section = 'expansion_analysis'
                current_content = []
                beneficiary_subsection = None

            elif 'LIMITES NECESARIOS:' in line_upper or 'NECESSARY LIMITS:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content, beneficiary_subsection)
                current_section = 'limits_needed'
                current_content = []
                beneficiary_subsection = None

            else:
                # Detectar subsecciones de beneficiarios
                if current_section == 'beneficiaries':
                    if 'PRIMARIOS:' in line_upper or 'PRIMARY:' in line_upper:
                        beneficiary_subsection = 'primary'
                        after_colon = line.split(':', 1)[1] if ':' in line else ''
                        if after_colon.strip():
                            current_content.append(('primary', after_colon.strip()))
                        continue
                    elif 'SECUNDARIOS:' in line_upper or 'SECONDARY:' in line_upper:
                        beneficiary_subsection = 'secondary'
                        after_colon = line.split(':', 1)[1] if ':' in line else ''
                        if after_colon.strip():
                            current_content.append(('secondary', after_colon.strip()))
                        continue
                    elif 'LARGO PLAZO:' in line_upper or 'LONG TERM:' in line_upper or 'TERTIARY:' in line_upper:
                        beneficiary_subsection = 'tertiary'
                        after_colon = line.split(':', 1)[1] if ':' in line else ''
                        if after_colon.strip():
                            current_content.append(('tertiary', after_colon.strip()))
                        continue

                # Linea de contenido
                if current_section and line.strip():
                    if current_section == 'beneficiaries' and beneficiary_subsection:
                        current_content.append((beneficiary_subsection, line.strip()))
                    else:
                        current_content.append(line.strip())

        # Guardar ultima seccion
        if current_section:
            self._save_section(sections, current_section, current_content, beneficiary_subsection)

        return sections

    def _save_section(self, sections: dict, section_name: str, content: list, beneficiary_subsection: str):
        """Guarda contenido parseado en la seccion correspondiente"""
        if section_name == 'beneficiaries':
            # Agrupar por subseccion
            for subsec, text in content:
                if subsec not in sections['beneficiaries']:
                    sections['beneficiaries'][subsec] = []
                # Limpiar guiones al inicio
                text_clean = text.lstrip('- ').strip()
                if text_clean:
                    sections['beneficiaries'][subsec].append(text_clean)
        elif section_name in ['giving_opportunities', 'generous_actions', 'limits_needed']:
            # Listas - limpiar guiones
            for item in content:
                item_clean = item.lstrip('- ').strip()
                if item_clean:
                    sections[section_name].append(item_clean)
        else:
            # Texto continuo
            sections[section_name] = '\n'.join(content).strip()

    def _calculate_compassion_score(self, parsed: Dict[str, Any]) -> float:
        """
        Calcula score de compasion basado en:
        - Numero de oportunidades identificadas
        - Numero de acciones generosas
        - Profundidad del analisis de impacto
        """
        opportunities_count = len(parsed.get('giving_opportunities', []))
        actions_count = len(parsed.get('generous_actions', []))
        impact_length = len(parsed.get('compassion_impact', ''))

        score = 0.0

        # Puntos por oportunidades identificadas
        if opportunities_count >= 5:
            score += 0.3
        elif opportunities_count >= 3:
            score += 0.2
        elif opportunities_count >= 1:
            score += 0.1

        # Puntos por acciones concretas
        if actions_count >= 5:
            score += 0.3
        elif actions_count >= 3:
            score += 0.2
        elif actions_count >= 1:
            score += 0.1

        # Puntos por profundidad de analisis de impacto
        if impact_length > 300:
            score += 0.4
        elif impact_length > 150:
            score += 0.3
        elif impact_length > 50:
            score += 0.2

        return min(1.0, score)

    def _evaluate_expansion_potential(self, parsed: Dict[str, Any]) -> float:
        """
        Evalua potencial de expansion del bien basado en:
        - Analisis de expansion (efectos multiplicadores)
        - Numero de beneficiarios secundarios/terciarios
        """
        expansion_length = len(parsed.get('expansion_analysis', ''))
        beneficiaries = parsed.get('beneficiaries', {})

        secondary_count = len(beneficiaries.get('secondary', []))
        tertiary_count = len(beneficiaries.get('tertiary', []))

        score = 0.0

        # Puntos por analisis de expansion
        if expansion_length > 300:
            score += 0.5
        elif expansion_length > 150:
            score += 0.3
        elif expansion_length > 50:
            score += 0.2

        # Puntos por beneficiarios indirectos (expansion)
        if secondary_count > 0:
            score += 0.2
        if tertiary_count > 0:
            score += 0.3

        return min(1.0, score)

    def _evaluate_balance_awareness(self, parsed: Dict[str, Any]) -> float:
        """
        Evalua si Chesed reconoce sus propios limites.
        Chesed balanceada debe identificar donde contenerse.
        """
        limits = parsed.get('limits_needed', [])
        limits_count = len(limits)

        # Chesed debe reconocer al menos 2-3 limites para estar balanceada
        if limits_count >= 3:
            return 0.9
        elif limits_count >= 2:
            return 0.7
        elif limits_count >= 1:
            return 0.5
        else:
            # Si no reconoce limites, es Chesed ciega - peligroso
            logger.warning("Chesed no reconocio limites necesarios - riesgo de bondad destructiva")
            return 0.2

    def validate_alignment(self) -> Dict[str, Any]:
        """
        Valida que Chesed este operando dentro de sus limites correctos.

        Chesed esta alineada si:
        - Identifica oportunidades de dar (no es indiferente)
        - Tiene balance awareness >= 0.4 (reconoce limites)
        - Considera consecuencias (no es ciega)
        """

        total_activations = self.activation_count

        if total_activations == 0:
            return {
                "sefira": self.name,
                "is_aligned": True,
                "status": "No hay activaciones aun",
                "compassion_score": 0.0,
                "balance_score": 1.0
            }

        # Chesed debe identificar oportunidades
        is_compassionate = self.giving_opportunities_identified > 0

        # Chesed debe tener balance awareness
        is_balanced = self.balance_with_gevurah_score >= 0.4

        # Chesed debe reconocer limites
        considers_limits = self.limits_recognized > 0

        # Alineamiento general
        is_aligned = is_compassionate and is_balanced and considers_limits

        # Advertencias
        if not is_compassionate and total_activations > 2:
            logger.warning(
                f"Chesed NO ha identificado oportunidades de dar en "
                f"{total_activations} activaciones - posible frialdad"
            )

        if not is_balanced and total_activations > 2:
            logger.warning(
                f"Chesed tiene bajo balance awareness ({self.balance_with_gevurah_score:.2f}) - "
                f"riesgo de bondad destructiva"
            )

        avg_expansion = (
            self.expansion_potential_total / total_activations
            if total_activations > 0 else 0.0
        )

        return {
            "sefira": self.name,
            "is_aligned": is_aligned,
            "total_activations": total_activations,
            "giving_opportunities_identified": self.giving_opportunities_identified,
            "compassion_actions_generated": self.compassion_actions_generated,
            "limits_recognized": self.limits_recognized,
            "balance_with_gevurah_score": self.balance_with_gevurah_score,
            "average_expansion_potential": avg_expansion,
            "is_compassionate": is_compassionate,
            "is_balanced": is_balanced,
            "considers_limits": considers_limits,
            "status": "Alineada" if is_aligned else "Advertencia: Chesed requiere balance"
        }
