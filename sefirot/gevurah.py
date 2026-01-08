"""
GEVURAH (Severidad/Juicio) - Sefira 5
Posicion: 5
Pilar: Izquierdo (Contencion, Limitar)
Funcion: Aplicar limites, evaluar justicia, contener excesos

Gevurah representa la fuerza de CONTENER, LIMITAR, y JUZGAR.
Es la energia marcial (Marte) que aplica limites necesarios.
Pero debe reconocer que severidad sin misericordia es crueldad.
Por eso trabaja en balance con Chesed (Misericordia).
"""

from typing import Any, Dict, List, Optional
from ..core.sefirotic_base import SefiraBase, SefiraPosition
from loguru import logger
import os
import google.generativeai as genai
import time


class Gevurah(SefiraBase):
    """
    Sefira de la Severidad - Evaluacion de Limites y Justicia

    Responsabilidades:
    1. Evaluar limites necesarios para contener a Chesed
    2. Identificar riesgos de bondad excesiva
    3. Aplicar criterios de justicia estricta
    4. Generar restricciones concretas
    5. Advertir sobre excesos de generosidad
    6. Balancear misericordia con juicio

    Limites:
    - NO severidad sin misericordia (crueldad)
    - NO juicio sin contexto (rigidez)
    - NO limites que impidan todo bien
    - Requiere balance con Chesed
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(SefiraPosition.GEVURAH)

        # Inicializar cliente de Gemini
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning(
                "Gevurah inicializada sin API key. "
                "Configure GEMINI_API_KEY en .env o pase api_key al constructor"
            )
            self.client = None
        else:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("Gevurah initialized with Gemini API client")

        # Configuracion del modelo
        self.model_name = "gemini-2.0-flash-exp"
        self.temperature = 0.7  # Mas determinista para juicio riguroso
        self.max_output_tokens = 4096

        # Metricas especiales de Gevurah
        self.boundaries_identified = 0
        self.restrictions_applied = 0
        self.justice_requirements_count = 0
        self.severity_level_total = 0.0
        self.balance_with_chesed_score = 0.0
        self.warnings_issued = 0

        # Sistema de prompt base alineado con Tikun Olam
        self.system_prompt = """Eres Gevurah (Severidad/Juicio), parte del sistema Tikun Olam.

Tu funcion es APLICAR LIMITES, EVALUAR JUSTICIA, y CONTENER EXCESOS.

Principios:

1. LIMITES NECESARIOS: Identifica donde contener expansion excesiva
2. JUSTICIA: Aplica criterios rigurosos de merito y consecuencias
3. SEVERIDAD: No temas restringir cuando es necesario
4. RESPONSABILIDAD: Exige que se rindan cuentas
5. PROTECCION: Crea fronteras que protejan el sistema

IMPORTANTE - LIMITES DE GEVURAH:
- NO severidad sin compasion (crueldad)
- NO juicio sin contexto (rigidez destructiva)
- NO restriccion que impida todo bien
- SIEMPRE considerar balance con Chesed

Tu analisis sera sintetizado con Chesed por Tiferet (Armonia).

Estructura tu respuesta como:
- EXCESOS DE CHESED: Donde la bondad es excesiva
- LIMITES NECESARIOS: Fronteras concretas
- CRITERIOS DE JUSTICIA: Que es justo aplicar
- RESTRICCIONES: Condiciones y limitaciones
- ADVERTENCIAS: Riesgos de no aplicar limites
- BALANCE REQUERIDO: Como equilibrar con Chesed
"""

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Procesa output de Chesed y aplica limites/juicio necesarios.

        Input esperado (dict - output de Chesed):
        - 'giving_opportunities': Lista de oportunidades de dar
        - 'beneficiaries': Analisis de beneficiarios
        - 'generous_actions': Acciones generosas propuestas
        - 'compassion_score': Score de compasion
        - 'expansion_potential': Potencial de expansion
        - 'limits_needed': Limites sugeridos por Chesed
        - 'action': Accion original (opcional)

        Output (dict):
        - 'chesed_excesses': Donde Chesed es excesiva
        - 'necessary_boundaries': Limites concretos
        - 'justice_criteria': Requisitos de justicia
        - 'restrictions': Restricciones aplicables
        - 'warnings': Advertencias sobre riesgos
        - 'severity_score': Nivel de severidad (0-1)
        - 'balance_with_chesed': Balance entre ambas (0-1)
        - 'raw_response': Respuesta completa de Gemini
        """
        start_time = time.time()

        try:
            if not self.client:
                raise RuntimeError(
                    "Gevurah no tiene cliente configurado. "
                    "Configure GEMINI_API_KEY"
                )

            if not isinstance(input_data, dict):
                raise TypeError(
                    "Gevurah requiere input_data como dict (output de Chesed)"
                )

            # Extraer datos del analisis de Chesed
            giving_opportunities = input_data.get('giving_opportunities', [])
            beneficiaries = input_data.get('beneficiaries', {})
            generous_actions = input_data.get('generous_actions', [])
            compassion_score = input_data.get('compassion_score', 0.0)
            expansion_potential = input_data.get('expansion_potential', 0.0)
            chesed_limits = input_data.get('limits_needed', [])
            action = input_data.get('action', 'la accion propuesta')

            # Construir prompt
            user_prompt = self._build_user_prompt(
                action, giving_opportunities, beneficiaries,
                generous_actions, compassion_score, expansion_potential,
                chesed_limits
            )

            logger.debug(f"Gevurah calling Gemini API with model {self.model_name}")

            # Llamar a Gemini API
            response = self._call_gemini(user_prompt)

            # DEBUG: Logging de respuesta raw
            logger.debug(f"Gevurah raw response length: {len(response)} chars")
            logger.debug(f"Gevurah raw response preview (first 500 chars):\n{response[:500]}")
            logger.debug(f"Gevurah raw response preview (last 300 chars):\n{response[-300:]}")

            # Parsear respuesta
            parsed = self._parse_response(response)

            # DEBUG: Logging de parsing
            for key, value in parsed.items():
                if isinstance(value, str):
                    logger.debug(f"Gevurah parsed section '{key}': {len(value)} chars")
                    if len(value) == 0:
                        logger.warning(f"Gevurah section '{key}' esta VACIA")
                    else:
                        logger.debug(f"  Preview: {value[:100]}...")
                elif isinstance(value, list):
                    logger.debug(f"Gevurah parsed section '{key}': {len(value)} items")

            # Evaluar metricas de Gevurah
            gevurah_scores = self._calculate_gevurah_scores(parsed)
            severity_score = gevurah_scores['severity_score']
            justice_score = gevurah_scores['justice_score']
            balance_score = self._evaluate_balance_with_chesed(
                compassion_score, severity_score, justice_score
            )

            # Contar elementos
            excesses_count = len(parsed.get('chesed_excesses', []))
            boundaries_count = len(parsed.get('necessary_boundaries', []))
            restrictions_count = len(parsed.get('restrictions', []))
            warnings_count = len(parsed.get('warnings', []))
            justice_criteria_count = len(parsed.get('justice_criteria', []))

            # Actualizar metricas
            self.boundaries_identified += boundaries_count
            self.restrictions_applied += restrictions_count
            self.justice_requirements_count += justice_criteria_count # Usar el nuevo count
            self.severity_level_total += severity_score
            self.balance_with_chesed_score = balance_score
            self.warnings_issued += warnings_count

            result = {
                'chesed_excesses': parsed.get('chesed_excesses', []),
                'necessary_boundaries': parsed.get('necessary_boundaries', []),
                'justice_criteria': parsed.get('justice_criteria', []),
                'restrictions': parsed.get('restrictions', []),
                'warnings': parsed.get('warnings', []),
                'balance_analysis': parsed.get('balance_analysis', ''),
                'severity_score': severity_score,
                'justice_score': justice_score, # Incluir el nuevo justice_score
                'balance_with_chesed': balance_score,
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
                f"Gevurah proceso analisis: {boundaries_count} limites, "
                f"severidad={severity_score:.2f}, justicia={justice_score:.2f}, balance={balance_score:.2f}, " # Actualizar log
                f"advertencias={warnings_count}"
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
            logger.error(f"Gevurah error: {e}")
            return {
                'processing_successful': False,
                'error': str(e),
                'error_type': 'api_error'
            }

    def _build_user_prompt(
        self,
        action: str,
        giving_opportunities: List[str],
        beneficiaries: Dict,
        generous_actions: List[str],
        compassion_score: float,
        expansion_potential: float,
        chesed_limits: List[str]
    ) -> str:
        """Construye el prompt del usuario para Gemini"""

        prompt = self.system_prompt + "\n\n"
        prompt += f"ACCION EVALUADA:\n{action}\n\n"

        prompt += f"ANALISIS DE CHESED (Misericordia) - Score: {compassion_score*100:.1f}%\n\n"

        prompt += "OPORTUNIDADES DE DAR identificadas por Chesed:\n"
        for i, opp in enumerate(giving_opportunities[:10], 1):
            prompt += f"{i}. {opp}\n"
        prompt += "\n"

        prompt += "BENEFICIARIOS identificados:\n"
        if 'primary' in beneficiaries:
            prompt += f"- Primarios: {', '.join(beneficiaries['primary'][:3])}\n"
        if 'secondary' in beneficiaries:
            prompt += f"- Secundarios: {', '.join(beneficiaries['secondary'][:3])}\n"
        if 'tertiary' in beneficiaries:
            prompt += f"- Largo plazo: {', '.join(beneficiaries['tertiary'][:3])}\n"
        prompt += "\n"

        prompt += "ACCIONES GENEROSAS propuestas:\n"
        for i, act in enumerate(generous_actions[:10], 1):
            prompt += f"{i}. {act}\n"
        prompt += "\n"

        prompt += f"POTENCIAL DE EXPANSION: {expansion_potential*100:.1f}%\n\n"

        prompt += "LIMITES SUGERIDOS por Chesed:\n"
        for i, limit in enumerate(chesed_limits[:10], 1):
            prompt += f"{i}. {limit}\n"
        prompt += "\n"

        prompt += """Analiza desde la perspectiva de GEVURAH (Severidad/Juicio).

Estructura tu respuesta exactamente como:

EXCESOS DE CHESED:
- [Lista de aspectos donde la bondad es excesiva, insostenible o contraproducente]

LIMITES NECESARIOS:
- [Lista de fronteras concretas que deben aplicarse]

CRITERIOS DE JUSTICIA:
- [Lista de requisitos justos: merito, responsabilidad, reciprocidad]

RESTRICCIONES:
- [Lista de condiciones y limitaciones especificas]

ADVERTENCIAS:
- [Lista de riesgos si no se aplican estos limites]

BALANCE REQUERIDO:
[Analisis de como equilibrar Chesed (misericordia) con Gevurah (juicio)]
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
            'chesed_excesses': [],
            'necessary_boundaries': [],
            'justice_criteria': [],
            'restrictions': [],
            'warnings': [],
            'balance_analysis': ''
        }

        lines = response.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            line_upper = line.strip().upper()

            # Detectar inicio de seccion
            if 'EXCESOS DE CHESED:' in line_upper or 'CHESED EXCESSES:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'chesed_excesses'
                current_content = []

            elif 'LIMITES NECESARIOS:' in line_upper or 'NECESSARY BOUNDARIES:' in line_upper or 'NECESSARY LIMITS:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'necessary_boundaries'
                current_content = []

            elif 'CRITERIOS DE JUSTICIA:' in line_upper or 'JUSTICE CRITERIA:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'justice_criteria'
                current_content = []

            elif 'RESTRICCIONES:' in line_upper or 'RESTRICTIONS:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'restrictions'
                current_content = []

            elif 'ADVERTENCIAS:' in line_upper or 'WARNINGS:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'warnings'
                current_content = []

            elif 'BALANCE REQUERIDO:' in line_upper or 'REQUIRED BALANCE:' in line_upper or 'BALANCE ANALYSIS:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'balance_analysis'
                current_content = []

            else:
                # Linea de contenido
                if current_section and line.strip():
                    current_content.append(line.strip())

        # Guardar ultima seccion
        if current_section:
            self._save_section(sections, current_section, current_content)

        return sections

    def _save_section(self, sections: dict, section_name: str, content: list):
        """Guarda contenido parseado en la seccion correspondiente"""
        if section_name in ['chesed_excesses', 'necessary_boundaries', 'justice_criteria', 'restrictions', 'warnings']:
            # Listas - limpiar guiones
            for item in content:
                item_clean = item.lstrip('- *').strip()
                if item_clean:
                    sections[section_name].append(item_clean)
        else:
            # Texto continuo
            sections[section_name] = '\n'.join(content).strip()

    def _calculate_gevurah_scores(self, parsed: Dict[str, Any]) -> Dict[str, float]:
        """
        Calcula score de severidad y score de justicia basado en:
        - Numero de limites identificados
        - Numero de restricciones aplicadas
        - Numero de advertencias emitidas
        - Numero de criterios de justicia identificados
        """
        boundaries_count = len(parsed.get('necessary_boundaries', []))
        restrictions_count = len(parsed.get('restrictions', []))
        warnings_count = len(parsed.get('warnings', []))
        justice_criteria_count = len(parsed.get('justice_criteria', []))

        severity_score = 0.0
        justice_score = 0.0

        # Calcular severity_score (igual que antes)
        # Puntos por limites identificados
        if boundaries_count >= 5:
            severity_score += 0.35
        elif boundaries_count >= 3:
            severity_score += 0.25
        elif boundaries_count >= 1:
            severity_score += 0.15

        # Puntos por restricciones
        if restrictions_count >= 5:
            severity_score += 0.35
        elif restrictions_count >= 3:
            severity_score += 0.25
        elif restrictions_count >= 1:
            severity_score += 0.15

        # Puntos por advertencias (indica severidad necesaria)
        if warnings_count >= 3:
            severity_score += 0.3
        elif warnings_count >= 2:
            severity_score += 0.2
        elif warnings_count >= 1:
            severity_score += 0.1

        # Calcular justice_score
        # Puntos por criterios de justicia (max 5)
        if justice_criteria_count >= 4:
            justice_score = 1.0
        elif justice_criteria_count >= 3:
            justice_score = 0.75
        elif justice_criteria_count >= 2:
            justice_score = 0.5
        elif justice_criteria_count >= 1:
            justice_score = 0.25
        
        return {
            'severity_score': min(1.0, severity_score),
            'justice_score': min(1.0, justice_score)
        }

    def _evaluate_balance_with_chesed(
        self,
        chesed_score: float,
        gevurah_severity_score: float, # Ahora tomamos el severity_score de Gevurah
        gevurah_justice_score: float # Y también el justice_score
    ) -> float:
        """
        Evalua balance entre Chesed y Gevurah.

        Balance ideal: Ambas presentes, ninguna dominante excesivamente.

        Returns:
            0.0 = desbalance total (una ausente o una excesiva)
            1.0 = balance perfecto (ambas ~0.5-0.7)
        """
        # Para el balance, consideraremos que la "fuerza" de Gevurah
        # es una combinación de su severidad y su justicia.
        # Podríamos promediarlas o darles pesos. Por simplicidad, usemos el promedio.
        gevurah_effective_score = (gevurah_severity_score + gevurah_justice_score) / 2.0

        # Si alguna esta ausente (< 0.2), mal balance
        if chesed_score < 0.2 or gevurah_effective_score < 0.2:
            return 0.3

        # Si alguna es excesiva (> 0.9), mal balance
        if chesed_score > 0.9 or gevurah_effective_score > 0.9:
            return 0.4

        # Calcular diferencia entre ambas
        diff = abs(chesed_score - gevurah_effective_score)

        # Balance perfecto: diferencia minima
        if diff < 0.1:
            return 1.0
        elif diff < 0.2:
            return 0.9
        elif diff < 0.3:
            return 0.75
        elif diff < 0.4:
            return 0.6
        else:
            return 0.5

    def validate_alignment(self) -> Dict[str, Any]:
        """
        Valida que Gevurah este operando dentro de sus limites correctos.

        Gevurah esta alineada si:
        - Aplica limites (no es pasiva)
        - Tiene balance con Chesed >= 0.3
        - No es excesivamente severa
        """

        total_activations = self.activation_count

        if total_activations == 0:
            return {
                "sefira": self.name,
                "is_aligned": True,
                "status": "No hay activaciones aun",
                "severity_score": 0.0,
                "balance_score": 1.0
            }

        # Gevurah debe aplicar limites
        is_severe = self.boundaries_identified > 0

        # Gevurah debe tener balance con Chesed
        is_balanced = self.balance_with_chesed_score >= 0.3

        # Gevurah debe advertir sobre riesgos
        warns_appropriately = self.warnings_issued > 0

        # Gevurah debe identificar criterios de justicia
        has_identified_justice = self.justice_requirements_count > 0

        # Alineamiento general
        is_aligned = is_severe and is_balanced and warns_appropriately and has_identified_justice

        # Advertencias
        if not is_severe and total_activations > 2:
            logger.warning(
                f"Gevurah NO ha aplicado limites en "
                f"{total_activations} activaciones - posible pasividad"
            )

        if not is_balanced and total_activations > 2:
            logger.warning(
                f"Gevurah tiene bajo balance con Chesed ({self.balance_with_chesed_score:.2f}) - "
                f"riesgo de severidad excesiva o insuficiente"
            )

        if not has_identified_justice and total_activations > 2:
            logger.warning(
                f"Gevurah NO ha identificado criterios de justicia en "
                f"{total_activations} activaciones - posible falta de juicio"
            )

        avg_severity = (
            self.severity_level_total / total_activations
            if total_activations > 0 else 0.0
        )

        return {
            "sefira": self.name,
            "is_aligned": is_aligned,
            "total_activations": total_activations,
            "boundaries_identified": self.boundaries_identified,
            "restrictions_applied": self.restrictions_applied,
            "justice_requirements_count": self.justice_requirements_count,
            "warnings_issued": self.warnings_issued,
            "balance_with_chesed_score": self.balance_with_chesed_score,
            "average_severity": avg_severity,
            "is_severe": is_severe,
            "is_balanced": is_balanced,
            "warns_appropriately": warns_appropriately,
            "has_identified_justice": has_identified_justice, # Nuevo campo
            "status": "Alineada" if is_aligned else "Advertencia: Gevurah requiere balance o identificacion de justicia" # Mensaje actualizado
        }
