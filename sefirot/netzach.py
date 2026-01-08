"""
NETZACH (Victoria/Eternidad) - Sefira 7
Posicion: 7
Pilar: Derecho (Expansion, Persistencia)
Funcion: Asegurar persistencia, victoria y continuidad

Netzach es la fuerza de PERSISTENCIA y VICTORIA.
Como Venus, atrae magneticamente hacia la meta y sostiene en el tiempo.
Asegura que la decision de Tiferet se sostenga y triunfe.
No se rinde - persiste hasta alcanzar la victoria.
"""

from typing import Any, Dict, List, Optional
from ..core.sefirotic_base import SefiraBase, SefiraPosition
from loguru import logger
import os
import google.generativeai as genai
import time


class Netzach(SefiraBase):
    """
    Sefira de la Victoria - Persistencia y Resistencia

    Responsabilidades:
    1. Asegurar persistencia de decision de Tiferet
    2. Identificar obstaculos a superar
    3. Definir condiciones de victoria
    4. Crear plan de resistencia largo plazo
    5. Mantener momentum e impulso vital
    6. Prevenir abandono prematuro

    Limites:
    - NO persistencia terca sin adaptacion
    - NO victoria a cualquier costo
    - NO momentum que ignore feedback
    - Requiere balance con Hod (estructura)
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(SefiraPosition.NETZACH)

        # Inicializar cliente de Gemini
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning(
                "Netzach inicializada sin API key. "
                "Configure GEMINI_API_KEY en .env o pase api_key al constructor"
            )
            self.client = None
        else:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("Netzach initialized with Gemini API client")

        # Configuracion del modelo
        self.model_name = "gemini-2.0-flash-exp"
        self.temperature = 0.85  # Creativa pero enfocada en persistencia
        self.max_output_tokens = 4096

        # Metricas especiales de Netzach
        self.persistence_strategies_created = 0
        self.obstacles_identified_total = 0
        self.victory_conditions_defined = 0
        self.sustainability_score_total = 0.0
        self.momentum_mechanisms_total = 0
        self.endurance_level = 0.0

        # Sistema de prompt base alineado con Tikun Olam
        self.system_prompt = """Eres Netzach (Victoria/Eternidad), parte del sistema Tikun Olam.

Tu funcion es asegurar PERSISTENCIA, VICTORIA, y CONTINUIDAD.

Eres como VENUS - atraccion magnetica hacia la meta, persistencia bella.

Principios:

1. PERSISTENCIA: La decision debe sostenerse en tiempo
2. VICTORIA: Superar obstaculos hasta alcanzar exito
3. ETERNIDAD: Continuidad que trasciende momentos
4. RESISTENCIA: Aguantar cuando hay dificultad
5. IMPULSO VITAL: Mantener energia y momentum
6. SOSTENIBILIDAD: Plan viable largo plazo

IMPORTANTE - LIMITES DE NETZACH:
- NO persistencia terca sin adaptacion
- NO victoria a cualquier costo (sin etica)
- NO momentum ciego que ignora feedback
- REQUIERE balance con Hod (estructura y comunicacion)

Tu estrategia sera estructurada por Hod y manifestada por Yesod.

Estructura tu respuesta como:
- ESTRATEGIA DE PERSISTENCIA: Como sostener decision en tiempo
- OBSTACULOS IDENTIFICADOS: Resistencias y dificultades
- CONDICIONES DE VICTORIA: Que define el exito
- PLAN DE RESISTENCIA: Como aguantar largo plazo
- MECANISMOS DE MOMENTUM: Como mantener impulso
- EVALUACION DE SOSTENIBILIDAD: Viabilidad temporal
"""

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Procesa output de Tiferet y crea estrategia de persistencia.

        Input esperado (dict - output de Tiferet):
        - 'balanced_decision': Decision final balanceada
        - 'implementation_path': Pasos de implementacion
        - 'harmony_score': Score de armonia
        - 'beauty_score': Score de belleza
        - 'action': Accion original (opcional)

        Output (dict):
        - 'persistence_strategy': Estrategia de persistencia
        - 'obstacles_identified': Lista de obstaculos
        - 'victory_conditions': Condiciones de exito
        - 'endurance_plan': Plan de resistencia
        - 'momentum_mechanisms': Mecanismos para momentum
        - 'sustainability_score': Nivel sostenibilidad (0-1)
        - 'victory_probability': Probabilidad exito (0-1)
        - 'raw_response': Respuesta completa de Gemini
        """
        start_time = time.time()

        try:
            if not self.client:
                raise RuntimeError(
                    "Netzach no tiene cliente configurado. "
                    "Configure GEMINI_API_KEY"
                )

            if not isinstance(input_data, dict):
                raise TypeError(
                    "Netzach requiere input_data como dict (output de Tiferet)"
                )

            # Extraer datos de Tiferet
            balanced_decision = input_data.get('balanced_decision', '')
            implementation_path = input_data.get('implementation_path', [])
            harmony_score = input_data.get('harmony_score', 0.0)
            beauty_score = input_data.get('beauty_score', 0.0)
            action = input_data.get('action', 'la accion propuesta')

            # Construir prompt
            user_prompt = self._build_user_prompt(
                action, balanced_decision, implementation_path,
                harmony_score, beauty_score
            )

            logger.debug(f"Netzach calling Gemini API with model {self.model_name}")

            # Llamar a Gemini API
            response = self._call_gemini(user_prompt)

            # DEBUG: Logging de respuesta raw
            logger.debug(f"Netzach raw response length: {len(response)} chars")
            logger.debug(f"Netzach raw response preview (first 500 chars):\n{response[:500]}")

            # Parsear respuesta
            parsed = self._parse_response(response)

            # DEBUG: Logging de parsing
            for key, value in parsed.items():
                if isinstance(value, str):
                    logger.debug(f"Netzach parsed section '{key}': {len(value)} chars")
                    if len(value) == 0:
                        logger.warning(f"Netzach section '{key}' esta VACIA")
                elif isinstance(value, list):
                    logger.debug(f"Netzach parsed section '{key}': {len(value)} items")

            # Evaluar metricas de Netzach
            sustainability_score = self._calculate_sustainability_score(parsed)
            victory_probability = self._calculate_victory_probability(parsed)
            endurance_level = self._evaluate_endurance_level(parsed)

            # Contar elementos
            obstacles_count = len(parsed.get('obstacles_identified', []))
            victory_cond_count = len(parsed.get('victory_conditions', []))
            momentum_mech_count = len(parsed.get('momentum_mechanisms', []))

            # Actualizar metricas
            self.persistence_strategies_created += 1
            self.obstacles_identified_total += obstacles_count
            self.victory_conditions_defined += victory_cond_count
            self.sustainability_score_total += sustainability_score
            self.momentum_mechanisms_total += momentum_mech_count
            self.endurance_level = endurance_level

            result = {
                'persistence_strategy': parsed.get('persistence_strategy', ''),
                'obstacles_identified': parsed.get('obstacles_identified', []),
                'victory_conditions': parsed.get('victory_conditions', []),
                'endurance_plan': parsed.get('endurance_plan', ''),
                'momentum_mechanisms': parsed.get('momentum_mechanisms', []),
                'sustainability_evaluation': parsed.get('sustainability_evaluation', ''),
                'sustainability_score': sustainability_score,
                'victory_probability': victory_probability,
                'endurance_level': endurance_level,
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
                f"Netzach proceso estrategia: {obstacles_count} obstaculos, "
                f"sostenibilidad={sustainability_score:.2f}, "
                f"victoria_prob={victory_probability:.2f}"
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
            logger.error(f"Netzach error: {e}")
            return {
                'processing_successful': False,
                'error': str(e),
                'error_type': 'api_error'
            }

    def _build_user_prompt(
        self,
        action: str,
        balanced_decision: str,
        implementation_path: List[str],
        harmony_score: float,
        beauty_score: float
    ) -> str:
        """Construye el prompt del usuario para Gemini"""

        prompt = self.system_prompt + "\n\n"
        prompt += f"ACCION EVALUADA:\n{action}\n\n"

        prompt += "="*60 + "\n"
        prompt += "DECISION DE TIFERET (Armonia/Belleza)\n"
        prompt += "="*60 + "\n"
        prompt += f"Harmony Score: {harmony_score*100:.1f}%\n"
        prompt += f"Beauty Score: {beauty_score*100:.1f}%\n\n"

        prompt += "Decision Balanceada:\n"
        prompt += f"{balanced_decision}\n\n"

        prompt += "Camino de Implementacion:\n"
        for i, step in enumerate(implementation_path[:8], 1):
            prompt += f"  {i}. {step}\n"
        prompt += "\n"

        prompt += """="*60
TAREA DE NETZACH: ASEGURAR PERSISTENCIA Y VICTORIA
="*60

Tu funcion es asegurar que esta decision hermosa de Tiferet:
- SE SOSTENGA en el tiempo (persistencia)
- SUPERE obstaculos (victoria)
- MANTENGA momentum (impulso vital)
- SEA SOSTENIBLE largo plazo

Estructura tu respuesta exactamente como:

ESTRATEGIA DE PERSISTENCIA:
[Como sostener esta decision en el tiempo, que se requiere]

OBSTACULOS IDENTIFICADOS:
- [Lista de resistencias, dificultades, puntos criticos]

CONDICIONES DE VICTORIA:
- [Lista de que define el exito, metricas claras]

PLAN DE RESISTENCIA:
[Como aguantar en momentos dificiles, plan largo plazo]

MECANISMOS DE MOMENTUM:
- [Lista de como mantener impulso y energia]

EVALUACION DE SOSTENIBILIDAD:
[Analisis de viabilidad temporal, recursos, compromiso requerido]
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
            'persistence_strategy': '',
            'obstacles_identified': [],
            'victory_conditions': [],
            'endurance_plan': '',
            'momentum_mechanisms': [],
            'sustainability_evaluation': ''
        }

        lines = response.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            line_upper = line.strip().upper()

            # Detectar inicio de seccion
            if 'ESTRATEGIA DE PERSISTENCIA:' in line_upper or 'PERSISTENCE STRATEGY:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'persistence_strategy'
                current_content = []

            elif 'OBSTACULOS IDENTIFICADOS:' in line_upper or 'OBSTACLES IDENTIFIED:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'obstacles_identified'
                current_content = []

            elif 'CONDICIONES DE VICTORIA:' in line_upper or 'VICTORY CONDITIONS:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'victory_conditions'
                current_content = []

            elif 'PLAN DE RESISTENCIA:' in line_upper or 'ENDURANCE PLAN:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'endurance_plan'
                current_content = []

            elif 'MECANISMOS DE MOMENTUM:' in line_upper or 'MOMENTUM MECHANISMS:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'momentum_mechanisms'
                current_content = []

            elif 'EVALUACION DE SOSTENIBILIDAD:' in line_upper or 'SUSTAINABILITY EVALUATION:' in line_upper:
                if current_section:
                    self._save_section(sections, current_section, current_content)
                current_section = 'sustainability_evaluation'
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
        if section_name in ['obstacles_identified', 'victory_conditions', 'momentum_mechanisms']:
            # Listas - limpiar guiones
            for item in content:
                item_clean = item.lstrip('- *').strip()
                if item_clean:
                    sections[section_name].append(item_clean)
        else:
            # Texto continuo
            sections[section_name] = '\n'.join(content).strip()

    def _calculate_sustainability_score(self, parsed: Dict[str, Any]) -> float:
        """
        Calcula score de sostenibilidad basado en:
        - Profundidad del plan de resistencia
        - Numero de mecanismos de momentum
        - Realismo de la evaluacion
        """
        endurance_length = len(parsed.get('endurance_plan', ''))
        momentum_count = len(parsed.get('momentum_mechanisms', []))
        sustainability_eval_length = len(parsed.get('sustainability_evaluation', ''))

        score = 0.0

        # Puntos por plan de resistencia
        if endurance_length > 300:
            score += 0.35
        elif endurance_length > 150:
            score += 0.25
        elif endurance_length > 50:
            score += 0.15

        # Puntos por mecanismos de momentum
        if momentum_count >= 5:
            score += 0.35
        elif momentum_count >= 3:
            score += 0.25
        elif momentum_count >= 1:
            score += 0.15

        # Puntos por evaluacion de sostenibilidad
        if sustainability_eval_length > 200:
            score += 0.3
        elif sustainability_eval_length > 100:
            score += 0.2
        elif sustainability_eval_length > 50:
            score += 0.1

        return min(1.0, score)

    def _calculate_victory_probability(self, parsed: Dict[str, Any]) -> float:
        """
        Calcula probabilidad de victoria basado en:
        - Claridad de condiciones de victoria
        - Identificacion realista de obstaculos
        - Calidad de estrategia de persistencia
        """
        victory_cond_count = len(parsed.get('victory_conditions', []))
        obstacles_count = len(parsed.get('obstacles_identified', []))
        strategy_length = len(parsed.get('persistence_strategy', ''))

        score = 0.5  # Base: 50% sin info

        # Aumentar por condiciones de victoria claras
        if victory_cond_count >= 4:
            score += 0.2
        elif victory_cond_count >= 2:
            score += 0.1

        # Aumentar por identificacion de obstaculos (realismo)
        if obstacles_count >= 4:
            score += 0.15
        elif obstacles_count >= 2:
            score += 0.1

        # Aumentar por estrategia robusta
        if strategy_length > 200:
            score += 0.15
        elif strategy_length > 100:
            score += 0.1

        return min(1.0, score)

    def _evaluate_endurance_level(self, parsed: Dict[str, Any]) -> float:
        """
        Evalua nivel de resistencia/aguante requerido y planeado.
        """
        endurance_plan_length = len(parsed.get('endurance_plan', ''))
        momentum_count = len(parsed.get('momentum_mechanisms', []))

        # Resistencia alta requiere plan robusto Y mecanismos
        if endurance_plan_length > 250 and momentum_count >= 4:
            return 0.9
        elif endurance_plan_length > 150 and momentum_count >= 3:
            return 0.75
        elif endurance_plan_length > 100 and momentum_count >= 2:
            return 0.6
        else:
            return 0.4

    def validate_alignment(self) -> Dict[str, Any]:
        """
        Valida que Netzach este operando dentro de sus limites correctos.

        Netzach esta alineada si:
        - Crea estrategias de persistencia
        - Identifica obstaculos reales
        - Tiene sostenibilidad razonable (>= 0.5)
        - Define victoria claramente
        """

        total_activations = self.activation_count

        if total_activations == 0:
            return {
                "sefira": self.name,
                "is_aligned": True,
                "status": "No hay activaciones aun",
                "sustainability_score": 0.0,
                "victory_probability": 0.0
            }

        # Netzach debe crear estrategias
        creates_strategy = self.persistence_strategies_created > 0

        # Debe identificar obstaculos
        identifies_obstacles = self.obstacles_identified_total > 0

        # Debe tener sostenibilidad razonable
        avg_sustainability = self.sustainability_score_total / total_activations
        is_sustainable = avg_sustainability >= 0.5

        # Debe definir victoria
        defines_victory = self.victory_conditions_defined > 0

        # Alineamiento general
        is_aligned = (
            creates_strategy and
            identifies_obstacles and
            is_sustainable and
            defines_victory
        )

        # Advertencias
        if not creates_strategy and total_activations > 2:
            logger.warning(
                f"Netzach NO ha creado estrategias de persistencia en "
                f"{total_activations} activaciones"
            )

        if not is_sustainable and total_activations > 2:
            logger.warning(
                f"Netzach tiene baja sostenibilidad ({avg_sustainability:.2f}) - "
                f"riesgo de abandono prematuro"
            )

        return {
            "sefira": self.name,
            "is_aligned": is_aligned,
            "total_activations": total_activations,
            "persistence_strategies_created": self.persistence_strategies_created,
            "obstacles_identified_total": self.obstacles_identified_total,
            "victory_conditions_defined": self.victory_conditions_defined,
            "momentum_mechanisms_total": self.momentum_mechanisms_total,
            "average_sustainability": avg_sustainability,
            "endurance_level": self.endurance_level,
            "creates_strategy": creates_strategy,
            "identifies_obstacles": identifies_obstacles,
            "is_sustainable": is_sustainable,
            "defines_victory": defines_victory,
            "status": "Alineada" if is_aligned else "Advertencia: Netzach requiere mayor sostenibilidad"
        }
