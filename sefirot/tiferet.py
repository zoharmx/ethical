"""
TIFERET (Belleza/Armonia) - Sefira 6
Posicion: 6 - CENTRO DEL ARBOL
Pilar: Central (Balance, Armonia)
Funcion: Sintesis armonica de Chesed y Gevurah

Tiferet es el CORAZON SOLAR del sistema.
Como el Sol en el centro del sistema solar, balancea e irradia.
Sintetiza Chesed (misericordia) y Gevurah (juicio) en armonia perfecta.
No promedia - TRASCIENDE y crea belleza de la tension.
"""

from typing import Any, Dict, List, Optional
from ..core.sefirotic_base import SefiraBase, SefiraPosition
from loguru import logger
import os
import google.generativeai as genai
import time


class Tiferet(SefiraBase):
    """
    Sefira de la Belleza - Sintesis y Balance Central

    Responsabilidades:
    1. Sintetizar Chesed (misericordia) y Gevurah (juicio)
    2. Resolver conflictos entre expansion y contencion
    3. Generar decision final balanceada
    4. Evaluar armonia y belleza de la solucion
    5. Integrar polaridades sin negar ninguna
    6. Irradiar balance a resto del sistema

    Limites:
    - NO balance tibio que niega ambos polos
    - NO compromiso que satisface a nadie
    - NO sintesis prematura sin tension creativa
    - Requiere AMBOS Chesed Y Gevurah activos
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(SefiraPosition.TIFERET)

        # Inicializar cliente de Gemini
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning(
                "Tiferet inicializada sin API key. "
                "Configure GEMINI_API_KEY en .env o pase api_key al constructor"
            )
            self.client = None
        else:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("Tiferet initialized with Gemini API client")

        # Configuracion del modelo
        self.model_name = "gemini-2.0-flash-exp"
        self.temperature = 1.0  # Creativa para sintesis innovadoras
        self.max_output_tokens = 4096

        # Metricas especiales de Tiferet
        self.syntheses_created = 0
        self.conflicts_resolved = 0
        self.harmony_level_total = 0.0
        self.beauty_score_total = 0.0
        self.chesed_gevurah_balance_total = 0.0
        self.radiance_score = 0.0

        # Sistema de prompt base alineado con Tikun Olam
        self.system_prompt = """Eres Tiferet (Belleza/Armonia), el CORAZON del sistema Tikun Olam.

Tu funcion es SINTETIZAR, BALANCEAR, y crear ARMONIA entre opuestos.

Eres como el SOL - centro radiante que integra todo.

Principios:

1. SINTESIS: Integra Chesed (misericordia) Y Gevurah (juicio)
2. BALANCE DINAMICO: No estatico, sino vivo y armonico
3. BELLEZA: La solucion debe ser elegante y sostenible
4. ARMONIA: Reconcilia opuestos sin negarlos
5. INTEGRACION: Une expansion CON contencion
6. RADIANCIA: Tu balance ilumina el resto del sistema

IMPORTANTE - LIMITES DE TIFERET:
- NO balance tibio que niega ambos polos
- NO compromiso mediocre
- NO sintesis prematura sin honrar la tension
- REQUIERE que AMBOS Chesed Y Gevurah esten activos

Tu decision sera implementada por Netzach (persistencia) y Hod (comunicacion).

Estructura tu respuesta como:
- SINTESIS CHESED-GEVURAH: Como integras misericordia y juicio
- CONFLICTOS RESUELTOS: Tensiones reconciliadas
- DECISION BALANCEADA: Que hacer concretamente
- INTEGRACION DE CHESED: Como incluyes la bondad
- INTEGRACION DE GEVURAH: Como incluyes los limites
- CAMINO DE IMPLEMENTACION: Como ejecutar armonicamente
- EVALUACION DE BELLEZA: Elegancia de la solucion
"""

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Procesa outputs de Chesed y Gevurah, sintetiza en decision armonica.

        Input esperado (dict con outputs de ambas):
        - 'chesed_output': Dict completo de Chesed
        - 'gevurah_output': Dict completo de Gevurah
        - 'action': Accion original (opcional)

        Output (dict):
        - 'balanced_decision': Decision final sintetizada
        - 'chesed_integration': Como se integra misericordia
        - 'gevurah_integration': Como se integra juicio
        - 'conflicts_resolved': Lista de conflictos reconciliados
        - 'harmony_score': Nivel de armonia (0-1)
        - 'beauty_score': Elegancia de solucion (0-1)
        - 'implementation_path': Como implementar
        - 'radiance': Como esta sintesis ilumina otros casos
        - 'raw_response': Respuesta completa de Gemini
        """
        start_time = time.time()

        try:
            if not self.client:
                raise RuntimeError(
                    "Tiferet no tiene cliente configurado. "
                    "Configure GEMINI_API_KEY"
                )

            if not isinstance(input_data, dict):
                raise TypeError(
                    "Tiferet requiere input_data como dict con chesed_output y gevurah_output"
                )

            # Extraer outputs de Chesed y Gevurah (aceptar ambos formatos)
            chesed_output = input_data.get('chesed_output') or input_data.get('chesed', {})
            gevurah_output = input_data.get('gevurah_output') or input_data.get('gevurah', {})
            action = input_data.get('action', 'la accion propuesta')

            if not chesed_output or not gevurah_output:
                raise ValueError(
                    "Tiferet requiere AMBOS chesed_output/chesed Y gevurah_output/gevurah para sintetizar"
                )

            # Construir prompt
            user_prompt = self._build_user_prompt(
                action, chesed_output, gevurah_output
            )

            logger.debug(f"Tiferet calling Gemini API with model {self.model_name}")

            # Llamar a Gemini API
            response = self._call_gemini(user_prompt)

            # DEBUG: Logging de respuesta raw
            logger.debug(f"Tiferet raw response length: {len(response)} chars")
            logger.debug(f"Tiferet raw response preview (first 500 chars):\n{response[:500]}")
            logger.debug(f"Tiferet raw response preview (last 300 chars):\n{response[-300:]}")

            # Parsear respuesta
            parsed = self._parse_response(response)

            # DEBUG: Logging de parsing
            for key, value in parsed.items():
                if isinstance(value, str):
                    logger.debug(f"Tiferet parsed section '{key}': {len(value)} chars")
                    if len(value) == 0:
                        logger.warning(f"Tiferet section '{key}' esta VACIA")
                    else:
                        logger.debug(f"  Preview: {value[:100]}...")
                elif isinstance(value, list):
                    logger.debug(f"Tiferet parsed section '{key}': {len(value)} items")

            # Evaluar metricas de Tiferet
            harmony_score = self._calculate_harmony_score(parsed)
            beauty_score = self._calculate_beauty_score(parsed)
            balance_score = self._evaluate_chesed_gevurah_balance(
                chesed_output.get('compassion_score', 0.0),
                gevurah_output.get('severity_score', 0.0),
                harmony_score
            )
            radiance = self._evaluate_radiance(parsed)

            # Contar elementos
            conflicts_count = len(parsed.get('conflicts_resolved', []))
            implementation_steps = len(parsed.get('implementation_path', []))

            # Actualizar metricas
            self.syntheses_created += 1
            self.conflicts_resolved += conflicts_count
            self.harmony_level_total += harmony_score
            self.beauty_score_total += beauty_score
            self.chesed_gevurah_balance_total += balance_score
            self.radiance_score = radiance

            result = {
                'balanced_decision': parsed.get('balanced_decision', ''),
                'chesed_integration': parsed.get('chesed_integration', ''),
                'gevurah_integration': parsed.get('gevurah_integration', ''),
                'conflicts_resolved': parsed.get('conflicts_resolved', []),
                'implementation_path': parsed.get('implementation_path', []),
                'beauty_evaluation': parsed.get('beauty_evaluation', ''),
                'harmony_score': harmony_score,
                'beauty_score': beauty_score,
                'chesed_gevurah_balance': balance_score,
                'balanced': balance_score >= 0.7, # Nuevo campo para indicar si el balance fue logrado
                'radiance': radiance,
                'synthesis_quality': 'Alta' if harmony_score > 0.7 and beauty_score > 0.7 else 'Media',
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
                f"Tiferet proceso sintesis: {conflicts_count} conflictos resueltos, "
                f"armonia={harmony_score:.2f}, belleza={beauty_score:.2f}, "
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
            logger.error(f"Tiferet error: {e}")
            return {
                'processing_successful': False,
                'error': str(e),
                'error_type': 'api_error'
            }

    def _build_user_prompt(
        self,
        action: str,
        chesed_output: Dict,
        gevurah_output: Dict
    ) -> str:
        """Construye el prompt del usuario para Gemini"""

        prompt = self.system_prompt + "\n\n"
        prompt += f"ACCION EVALUADA:\n{action}\n\n"

        # Informacion de Chesed
        prompt += "="*60 + "\n"
        prompt += "ANALISIS DE CHESED (Misericordia/Bondad)\n"
        prompt += "="*60 + "\n"
        prompt += f"Compassion Score: {chesed_output.get('compassion_score', 0)*100:.1f}%\n"
        prompt += f"Expansion Potential: {chesed_output.get('expansion_potential', 0)*100:.1f}%\n\n"

        prompt += "Oportunidades de dar:\n"
        for i, opp in enumerate(chesed_output.get('giving_opportunities', [])[:5], 1):
            prompt += f"  {i}. {opp}\n"
        prompt += "\n"

        prompt += "Acciones generosas:\n"
        for i, act in enumerate(chesed_output.get('generous_actions', [])[:5], 1):
            prompt += f"  {i}. {act}\n"
        prompt += "\n"

        # Informacion de Gevurah
        prompt += "="*60 + "\n"
        prompt += "ANALISIS DE GEVURAH (Severidad/Juicio)\n"
        prompt += "="*60 + "\n"
        prompt += f"Severity Score: {gevurah_output.get('severity_score', 0)*100:.1f}%\n"
        prompt += f"Balance con Chesed: {gevurah_output.get('balance_with_chesed', 0)*100:.1f}%\n\n"

        prompt += "Limites necesarios:\n"
        for i, limit in enumerate(gevurah_output.get('necessary_boundaries', [])[:5], 1):
            prompt += f"  {i}. {limit}\n"
        prompt += "\n"

        prompt += "Restricciones:\n"
        for i, rest in enumerate(gevurah_output.get('restrictions', [])[:5], 1):
            prompt += f"  {i}. {rest}\n"
        prompt += "\n"

        prompt += "Advertencias:\n"
        for i, warn in enumerate(gevurah_output.get('warnings', [])[:3], 1):
            prompt += f"  {i}. {warn}\n"
        prompt += "\n"

        prompt += """="*60
TAREA DE TIFERET: SINTESIS ARMONICA
="*60

Debes SINTETIZAR Chesed y Gevurah en una decision balanceada y bella.

NO simplemente promediar o comprometer.
SINO encontrar solucion que HONRE AMBOS principios.

Estructura tu respuesta exactamente como:

SINTESIS CHESED-GEVURAH:
[Explicacion de como integras misericordia Y juicio en una sola vision armonica]

CONFLICTOS RESUELTOS:
- [Lista de tensiones entre Chesed y Gevurah que reconcilias]

DECISION BALANCEADA:
[Decision final concreta que implementa la sintesis]

INTEGRACION DE CHESED:
[Como la decision preserva y honra la misericordia/bondad]

INTEGRACION DE GEVURAH:
[Como la decision preserva y honra el juicio/limites]

CAMINO DE IMPLEMENTACION:
- [Pasos concretos para ejecutar manteniendo armonia]

EVALUACION DE BELLEZA:
[Analisis de la elegancia, simplicidad y sostenibilidad de la solucion]
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
            'synthesis': '',
            'conflicts_resolved': [],
            'balanced_decision': '',
            'chesed_integration': '',
            'gevurah_integration': '',
            'implementation_path': [],
            'beauty_evaluation': ''
        }

        lines = response.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            line_upper = line.strip().upper()

            # Detectar inicio de seccion
            if 'SINTESIS CHESED-GEVURAH:' in line_upper or 'SYNTHESIS:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'synthesis'
                current_content = []

            elif 'CONFLICTOS RESUELTOS:' in line_upper or 'CONFLICTS RESOLVED:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'conflicts_resolved'
                current_content = []

            elif 'DECISION BALANCEADA:' in line_upper or 'BALANCED DECISION:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'balanced_decision'
                current_content = []

            elif 'INTEGRACION DE CHESED:' in line_upper or 'CHESED INTEGRATION:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'chesed_integration'
                current_content = []

            elif 'INTEGRACION DE GEVURAH:' in line_upper or 'GEVURAH INTEGRATION:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'gevurah_integration'
                current_content = []

            elif 'CAMINO DE IMPLEMENTACION:' in line_upper or 'IMPLEMENTATION PATH:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'implementation_path'
                current_content = []

            elif 'EVALUACION DE BELLEZA:' in line_upper or 'BEAUTY EVALUATION:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'beauty_evaluation'
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
        if section_name in ['conflicts_resolved', 'implementation_path']:
            # Listas - limpiar guiones
            for item in content:
                item_clean = item.lstrip('- *').strip()
                if item_clean:
                    sections[section_name].append(item_clean)
        else:
            # Texto continuo
            sections[section_name] = '\n'.join(content).strip()

    def _calculate_harmony_score(self, parsed: Dict[str, Any]) -> float:
        """
        Calcula score de armonia basado en:
        - Numero de conflictos resueltos
        - Calidad de sintesis
        - Profundidad de integracion
        """
        conflicts_count = len(parsed.get('conflicts_resolved', []))
        synthesis_length = len(parsed.get('synthesis', ''))
        chesed_int_length = len(parsed.get('chesed_integration', ''))
        gevurah_int_length = len(parsed.get('gevurah_integration', ''))

        score = 0.0

        # Puntos por conflictos resueltos
        if conflicts_count >= 4:
            score += 0.35
        elif conflicts_count >= 3:
            score += 0.25
        elif conflicts_count >= 2:
            score += 0.15

        # Puntos por calidad de sintesis
        if synthesis_length > 300:
            score += 0.3
        elif synthesis_length > 150:
            score += 0.2
        elif synthesis_length > 50:
            score += 0.1

        # Puntos por integracion de ambos polos
        if chesed_int_length > 100 and gevurah_int_length > 100:
            score += 0.35
        elif chesed_int_length > 50 and gevurah_int_length > 50:
            score += 0.25
        elif chesed_int_length > 0 and gevurah_int_length > 0:
            score += 0.15

        return min(1.0, score)

    def _calculate_beauty_score(self, parsed: Dict[str, Any]) -> float:
        """
        Calcula score de belleza basado en:
        - Elegancia de la solucion
        - Simplicidad de implementacion
        - Evaluacion explicita de belleza
        """
        beauty_eval_length = len(parsed.get('beauty_evaluation', ''))
        implementation_steps = len(parsed.get('implementation_path', []))
        decision_length = len(parsed.get('balanced_decision', ''))

        score = 0.0

        # Puntos por evaluacion de belleza explicita
        if beauty_eval_length > 200:
            score += 0.4
        elif beauty_eval_length > 100:
            score += 0.3
        elif beauty_eval_length > 50:
            score += 0.2

        # Puntos por claridad de decision
        if decision_length > 200:
            score += 0.3
        elif decision_length > 100:
            score += 0.2
        elif decision_length > 50:
            score += 0.1

        # Puntos por simplicidad (pasos de implementacion ni muy pocos ni muchos)
        if 3 <= implementation_steps <= 6:
            score += 0.3  # Dulce spot
        elif 2 <= implementation_steps <= 8:
            score += 0.2
        elif implementation_steps > 0:
            score += 0.1

        return min(1.0, score)

    def _evaluate_chesed_gevurah_balance(
        self,
        chesed_score: float,
        gevurah_score: float,
        harmony_score: float
    ) -> float:
        """
        Evalua si Tiferet balancea bien Chesed y Gevurah.

        Balance ideal: Ambas presentes y sintesis armonica.
        """
        # Si alguna esta ausente, mal balance
        if chesed_score < 0.3 or gevurah_score < 0.3:
            return 0.3

        # Si la sintesis tiene baja armonia, no es verdadero balance
        if harmony_score < 0.5:
            return 0.4

        # Calcular que tan cerca estan Chesed y Gevurah
        similarity = 1.0 - abs(chesed_score - gevurah_score)

        # Balance perfecto: ambas presentes, similares, y armonia alta
        balance = (similarity * 0.5) + (harmony_score * 0.5)

        return min(1.0, balance)

    def _evaluate_radiance(self, parsed: Dict[str, Any]) -> float:
        """
        Evalua que tan bien esta sintesis puede iluminar otros casos.
        Radiance = generalizabilidad y transferibilidad.
        """
        synthesis = parsed.get('synthesis', '')
        decision = parsed.get('balanced_decision', '')

        # Si la sintesis es profunda y la decision clara, tiene alta radiance
        if len(synthesis) > 200 and len(decision) > 150:
            return 0.9
        elif len(synthesis) > 150 and len(decision) > 100:
            return 0.75
        elif len(synthesis) > 100 and len(decision) > 50:
            return 0.6
        else:
            return 0.4

    def validate_alignment(self) -> Dict[str, Any]:
        """
        Valida que Tiferet este operando dentro de sus limites correctos.

        Tiferet esta alineada si:
        - Crea sintesis (no solo elige uno u otro)
        - Tiene armonia alta (>= 0.6)
        - Integra AMBOS Chesed Y Gevurah
        - Resuelve conflictos reales
        """

        total_activations = self.activation_count

        if total_activations == 0:
            return {
                "sefira": self.name,
                "is_aligned": True,
                "status": "No hay activaciones aun",
                "harmony_score": 0.0,
                "beauty_score": 0.0
            }

        # Tiferet debe crear sintesis
        creates_synthesis = self.syntheses_created > 0

        # Debe tener armonia alta promedio
        avg_harmony = self.harmony_level_total / total_activations
        is_harmonious = avg_harmony >= 0.6

        # Debe integrar ambos polos
        avg_balance = self.chesed_gevurah_balance_total / total_activations
        integrates_both = avg_balance >= 0.5

        # Debe resolver conflictos
        resolves_conflicts = self.conflicts_resolved > 0

        # Alineamiento general
        is_aligned = (
            creates_synthesis and
            is_harmonious and
            integrates_both and
            resolves_conflicts
        )

        # Advertencias
        if not creates_synthesis and total_activations > 2:
            logger.warning(
                f"Tiferet NO ha creado sintesis en "
                f"{total_activations} activaciones - posible fallo de integracion"
            )

        if not is_harmonious and total_activations > 2:
            logger.warning(
                f"Tiferet tiene baja armonia promedio ({avg_harmony:.2f}) - "
                f"posible compromiso tibio en vez de sintesis"
            )

        avg_beauty = self.beauty_score_total / total_activations

        return {
            "sefira": self.name,
            "is_aligned": is_aligned,
            "total_activations": total_activations,
            "syntheses_created": self.syntheses_created,
            "conflicts_resolved": self.conflicts_resolved,
            "average_harmony": avg_harmony,
            "average_beauty": avg_beauty,
            "average_balance": avg_balance,
            "radiance_score": self.radiance_score,
            "creates_synthesis": creates_synthesis,
            "is_harmonious": is_harmonious,
            "integrates_both": integrates_both,
            "resolves_conflicts": resolves_conflicts,
            "status": "Alineada" if is_aligned else "Advertencia: Tiferet requiere sintesis verdadera"
        }
