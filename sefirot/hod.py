"""
HOD (Esplendor/Gloria) - Sefira 8
Estructura, Comunicacion, Precision, Organizacion

Correspondencia Astral: Mercurio ?
Dia 5: Miercoles 7pm - Jueves 7pm
Pilar Izquierdo (Contencion, Estructura)

Hod recibe la estrategia de persistencia de Netzach y la ESTRUCTURA:
- Organiza el plan en fases claras
- Crea estrategia de comunicacion
- Define metricas y KPIs precisos
- Genera documentacion
- Prepara mensajes para stakeholders

Es como MERCURIO - mensajero veloz, preciso, organizador.
"""

from typing import Any, Dict, Optional, List
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
import google.generativeai as genai
from ..core.sefirotic_base import SefiraBase, SefiraPosition
from loguru import logger


class Hod(SefiraBase):
    """
    Sefira del Esplendor - Estructura y Comunicacion

    Responsabilidades:
    1. Estructurar estrategia de Netzach
    2. Crear plan de comunicacion claro
    3. Definir metricas precisas
    4. Organizar documentacion
    5. Preparar mensajes para stakeholders
    6. Asegurar precision y claridad

    Limites:
    - NO estructura rigida sin flexibilidad
    - NO precision obsesiva que paraliza
    - NO comunicacion sin sustancia
    - Requiere balance con Netzach (impulso)
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa Hod con conexion a Gemini

        Args:
            api_key: Opcional. Si no se provee, usa GEMINI_API_KEY del env
        """
        super().__init__(SefiraPosition.HOD)

        # Configurar Gemini
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrada en variables de entorno")

        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel('gemini-2.0-flash-exp')

        # Temperatura moderada-baja para precision y estructura
        self.temperature = 0.6

        # Metricas especificas de Hod
        self.plans_structured = 0
        self.communication_strategies_created = 0
        self.metrics_frameworks_defined = 0
        self.documentation_generated = 0
        self.precision_score_total = 0.0
        self.clarity_score_total = 0.0

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Procesa la estrategia de Netzach y la estructura

        Args:
            input_data: Dict con:
                - persistence_strategy: Estrategia de persistencia
                - obstacles_identified: Obstaculos identificados
                - victory_conditions: Condiciones de victoria
                - endurance_plan: Plan de resistencia
                - momentum_mechanisms: Mecanismos de momentum
                - sustainability_score: Score de sostenibilidad
                - action: Accion original

        Returns:
            Dict con:
                - structured_plan: Plan organizado en fases
                - communication_strategy: Estrategia de comunicacion
                - metrics_framework: Framework de metricas y KPIs
                - documentation: Documentacion generada
                - stakeholder_messages: Mensajes por stakeholder
                - precision_score: Nivel de precision (0-1)
                - clarity_score: Nivel de claridad (0-1)
                - processing_successful: bool
        """
        logger.debug("\n" + "="*60)
        logger.debug("HOD (Esplendor) - Estructurando y Comunicando")
        logger.debug("="*60)

        self.activation_count += 1

        try:
            # 1. Construir prompt para Gemini
            user_prompt = self._build_user_prompt(input_data)

            # 2. Llamar a Gemini
            logger.debug("\n[Hod] Llamando a Gemini para estructurar...")
            response = self._call_gemini(user_prompt)

            # 3. Parsear respuesta
            result = self._parse_response(response, input_data)

            # 4. Calcular metricas
            result['precision_score'] = self._calculate_precision_score(result)
            result['clarity_score'] = self._calculate_clarity_score(result)

            # 5. Actualizar metricas acumuladas
            self.plans_structured += 1
            self.communication_strategies_created += 1
            self.metrics_frameworks_defined += 1
            self.documentation_generated += len(result.get('documentation', []))
            self.precision_score_total += result['precision_score']
            self.clarity_score_total += result['clarity_score']

            result['processing_successful'] = True

            logger.debug(f"\n[Hod] Precision Score: {result['precision_score']*100:.1f}%")
            logger.debug(f"[Hod] Clarity Score: {result['clarity_score']*100:.1f}%")
            logger.debug(f"[Hod] Plan estructurado en {len(result.get('structured_plan', {}))} fases")

            return result

        except Exception as e:
            logger.error(f"\n[ERROR en Hod] {str(e)}")
            return {
                'processing_successful': False,
                'error': str(e),
                'structured_plan': {},
                'communication_strategy': {},
                'metrics_framework': {},
                'documentation': [],
                'stakeholder_messages': {},
                'precision_score': 0.0,
                'clarity_score': 0.0
            }

    def _build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        Construye el prompt para Gemini siguiendo los principios de Hod
        """
        persistence_strategy = input_data.get('persistence_strategy', '')
        obstacles = input_data.get('obstacles_identified', [])
        victory_conditions = input_data.get('victory_conditions', [])
        endurance_plan = input_data.get('endurance_plan', '')
        momentum = input_data.get('momentum_mechanisms', [])
        sustainability = input_data.get('sustainability_score', 0.0)
        action = input_data.get('action', 'Accion no especificada')

        # Convertir a string si son objetos
        if isinstance(persistence_strategy, dict):
            persistence_strategy = str(persistence_strategy)
        if isinstance(endurance_plan, dict):
            endurance_plan = str(endurance_plan)

        prompt = f"""Eres Hod (Esplendor/Gloria), parte del sistema Tikun Olam.

Tu funcion es ESTRUCTURAR, COMUNICAR, y ORGANIZAR con PRECISION.

Eres como MERCURIO - mensajero veloz, preciso, organizador.

Principios:

1. ESTRUCTURA: Organiza ideas en planes claros
2. COMUNICACION: Expresa con claridad y precision
3. PRECISION: Detalles exactos y especificos
4. ORGANIZACION: Orden logico y sistematico
5. MEDICION: Metricas concretas y cuantificables
6. CLARIDAD: Mensajes comprensibles para todos

IMPORTANTE - LIMITES DE HOD:
- NO estructura rigida que impide adaptacion
- NO precision obsesiva que paraliza accion
- NO comunicacion sin sustancia
- REQUIERE balance con Netzach (impulso y flexibilidad)

Tu plan sera fundado en realidad por Yesod y manifestado por Malchut.

CONTEXTO:
Accion: {action}

INPUT DE NETZACH (Victoria/Persistencia):

ESTRATEGIA DE PERSISTENCIA:
{persistence_strategy}

OBSTACULOS IDENTIFICADOS ({len(obstacles)}):
{self._format_list(obstacles)}

CONDICIONES DE VICTORIA ({len(victory_conditions)}):
{self._format_list(victory_conditions)}

PLAN DE RESISTENCIA:
{endurance_plan}

MECANISMOS DE MOMENTUM ({len(momentum)}):
{self._format_list(momentum)}

SUSTAINABILITY SCORE: {sustainability*100:.1f}%

TU TAREA - ESTRUCTURAR Y COMUNICAR:

Estructura tu respuesta EXACTAMENTE asi:

PLAN ESTRUCTURADO:
[Organiza la estrategia en fases claras con timeline preciso, milestones, y deliverables]

ESTRATEGIA DE COMUNICACION:
[Crea plan de comunicacion por stakeholder: mensaje clave, frecuencia, canales]

FRAMEWORK DE METRICAS:
[Define KPIs especificos, targets numericos, timeline, metodo de medicion]

DOCUMENTACION:
[Lista documentos necesarios: manuales, protocolos, guias, SOPs]

MENSAJES CLAVE:
[Mensajes especificos para cada stakeholder: gobierno, equipos, usuarios, etc]

EVALUACION DE PRECISION:
[Evalua la claridad y exactitud del plan estructurado]

Usa precision mercurial, estructura clara, comunicacion efectiva.
"""
        return prompt

    def _format_list(self, items: List[str]) -> str:
        """Formatea lista para el prompt"""
        if not items:
            return "- Ninguno"
        return "\n".join([f"- {item}" for item in items[:10]])  # Max 10 items

    def _call_gemini(self, prompt: str) -> str:
        """
        Llama a la API de Gemini
        """
        try:
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=8192,
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Error llamando a Gemini: {str(e)}")

    def _parse_response(self, response: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parsea la respuesta de Gemini para extraer estructura
        """
        result = {
            'structured_plan': {},
            'communication_strategy': {},
            'metrics_framework': {},
            'documentation': [],
            'stakeholder_messages': {},
            'raw_response': response
        }

        # Extraer secciones
        sections = {
            'PLAN ESTRUCTURADO:': 'structured_plan_text',
            'ESTRATEGIA DE COMUNICACION:': 'communication_strategy_text',
            'FRAMEWORK DE METRICAS:': 'metrics_framework_text',
            'DOCUMENTACION:': 'documentation_text',
            'MENSAJES CLAVE:': 'stakeholder_messages_text',
            'EVALUACION DE PRECISION:': 'precision_evaluation'
        }

        for section_marker, key in sections.items():
            result[key] = self._extract_section(response, section_marker)

        # Parsear plan estructurado en fases
        result['structured_plan'] = self._parse_structured_plan(
            result['structured_plan_text']
        )

        # Parsear estrategia de comunicacion
        result['communication_strategy'] = self._parse_communication_strategy(
            result['communication_strategy_text']
        )

        # Parsear framework de metricas
        result['metrics_framework'] = self._parse_metrics_framework(
            result['metrics_framework_text']
        )

        # Parsear documentacion
        result['documentation'] = self._parse_documentation(
            result['documentation_text']
        )

        # Parsear mensajes stakeholders
        result['stakeholder_messages'] = self._parse_stakeholder_messages(
            result['stakeholder_messages_text']
        )

        return result

    def _extract_section(self, text: str, marker: str) -> str:
        """Extrae seccion del texto"""
        if marker not in text:
            return ""

        start = text.find(marker) + len(marker)

        # Encontrar siguiente seccion
        next_markers = [
            'PLAN ESTRUCTURADO:',
            'ESTRATEGIA DE COMUNICACION:',
            'FRAMEWORK DE METRICAS:',
            'DOCUMENTACION:',
            'MENSAJES CLAVE:',
            'EVALUACION DE PRECISION:'
        ]

        end = len(text)
        for next_marker in next_markers:
            if next_marker != marker and next_marker in text[start:]:
                pos = text.find(next_marker, start)
                if pos < end:
                    end = pos

        return text[start:end].strip()

    def _parse_structured_plan(self, text: str) -> Dict[str, Any]:
        """
        Parsea el plan estructurado en fases
        """
        plan = {}

        # Buscar fases (Fase 1, Phase 1, etc)
        import re
        phase_pattern = r'(?:Fase|Phase)\s*(\d+)[:\-\s]+(.*?)(?=(?:Fase|Phase)\s*\d+|$)'
        phases = re.findall(phase_pattern, text, re.IGNORECASE | re.DOTALL)

        for i, (phase_num, phase_content) in enumerate(phases, 1):
            phase_key = f'phase_{phase_num}'
            plan[phase_key] = {
                'number': int(phase_num),
                'content': phase_content.strip()[:500],  # Limitar longitud
                'extracted': True
            }

        # Si no hay fases claras, guardar todo el texto
        if not plan:
            plan['general'] = {
                'content': text[:1000],
                'extracted': False
            }

        return plan

    def _parse_communication_strategy(self, text: str) -> Dict[str, Any]:
        """
        Parsea la estrategia de comunicacion
        """
        strategy = {
            'description': text[:800],  # Primeros 800 chars
            'stakeholders': [],
            'channels': [],
            'frequency': ''
        }

        # Intentar extraer stakeholders mencionados
        stakeholder_keywords = [
            'gobierno', 'maestros', 'padres', 'estudiantes', 'comunidad',
            'equipo', 'usuarios', 'clientes', 'socios', 'inversores'
        ]

        text_lower = text.lower()
        for keyword in stakeholder_keywords:
            if keyword in text_lower:
                strategy['stakeholders'].append(keyword.capitalize())

        return strategy

    def _parse_metrics_framework(self, text: str) -> Dict[str, Any]:
        """
        Parsea el framework de metricas
        """
        framework = {
            'description': text[:800],
            'kpis': [],
            'targets': [],
            'measurement_method': ''
        }

        # Intentar extraer KPIs mencionados
        import re
        kpi_pattern = r'KPI\s*\d*[:\-\s]+(.*?)(?=KPI|\n\n|$)'
        kpis = re.findall(kpi_pattern, text, re.IGNORECASE)

        for kpi in kpis[:10]:  # Max 10 KPIs
            framework['kpis'].append(kpi.strip()[:200])

        return framework

    def _parse_documentation(self, text: str) -> List[str]:
        """
        Parsea la lista de documentacion necesaria
        """
        docs = []

        # Buscar lineas que empiezan con -, *, numeros
        import re
        doc_pattern = r'^[\-\*\d\.]+\s*(.+)$'

        for line in text.split('\n'):
            match = re.match(doc_pattern, line.strip())
            if match:
                doc = match.group(1).strip()
                if len(doc) > 10:  # Filtrar lineas muy cortas
                    docs.append(doc[:200])  # Limitar longitud

        # Si no se encontro nada estructurado, dividir por lineas
        if not docs and text.strip():
            for line in text.split('\n'):
                clean = line.strip()
                if len(clean) > 10:
                    docs.append(clean[:200])

        return docs[:15]  # Max 15 documentos

    def _parse_stakeholder_messages(self, text: str) -> Dict[str, str]:
        """
        Parsea mensajes por stakeholder
        """
        messages = {}

        # Buscar patrones: "Stakeholder: mensaje"
        import re
        pattern = r'([A-Za-z\s]+):\s*(.+?)(?=\n[A-Za-z\s]+:|$)'
        matches = re.findall(pattern, text, re.DOTALL)

        for stakeholder, message in matches:
            stakeholder_clean = stakeholder.strip().lower()
            message_clean = message.strip()[:300]  # Limitar longitud

            if len(message_clean) > 10:
                messages[stakeholder_clean] = message_clean

        # Si no hay mensajes estructurados, guardar texto general
        if not messages and text.strip():
            messages['general'] = text[:500]

        return messages

    def _calculate_precision_score(self, result: Dict[str, Any]) -> float:
        """
        Calcula score de precision (0-1) basado en:
        - Claridad de fases en plan estructurado
        - Especificidad de metricas
        - Detalle de documentacion
        """
        score = 0.0

        # Plan estructurado (30%)
        plan = result.get('structured_plan', {})
        if plan:
            # Tiene fases claras?
            phase_count = len([k for k in plan.keys() if 'phase' in k])
            if phase_count >= 3:
                score += 0.30
            elif phase_count >= 2:
                score += 0.20
            elif phase_count >= 1:
                score += 0.10

        # Framework de metricas (30%)
        metrics = result.get('metrics_framework', {})
        kpi_count = len(metrics.get('kpis', []))
        if kpi_count >= 5:
            score += 0.30
        elif kpi_count >= 3:
            score += 0.20
        elif kpi_count >= 1:
            score += 0.10

        # Documentacion (20%)
        docs = result.get('documentation', [])
        doc_count = len(docs)
        if doc_count >= 5:
            score += 0.20
        elif doc_count >= 3:
            score += 0.15
        elif doc_count >= 1:
            score += 0.10

        # Mensajes stakeholders (20%)
        messages = result.get('stakeholder_messages', {})
        msg_count = len(messages)
        if msg_count >= 4:
            score += 0.20
        elif msg_count >= 2:
            score += 0.15
        elif msg_count >= 1:
            score += 0.10

        return min(score, 1.0)

    def _calculate_clarity_score(self, result: Dict[str, Any]) -> float:
        """
        Calcula score de claridad (0-1) basado en:
        - Longitud y estructura de textos
        - Presencia de evaluacion de precision
        - Calidad de comunicacion
        """
        score = 0.0

        # Plan estructurado tiene contenido claro (25%)
        plan_text = result.get('structured_plan_text', '')
        if len(plan_text) > 200:
            score += 0.25
        elif len(plan_text) > 100:
            score += 0.15

        # Estrategia comunicacion clara (25%)
        comm_text = result.get('communication_strategy_text', '')
        if len(comm_text) > 150:
            score += 0.25
        elif len(comm_text) > 75:
            score += 0.15

        # Framework metricas claro (25%)
        metrics_text = result.get('metrics_framework_text', '')
        if len(metrics_text) > 150:
            score += 0.25
        elif len(metrics_text) > 75:
            score += 0.15

        # Evaluacion de precision presente (25%)
        precision_eval = result.get('precision_evaluation', '')
        if len(precision_eval) > 50:
            score += 0.25
        elif len(precision_eval) > 20:
            score += 0.15

        return min(score, 1.0)

    def validate_alignment(self) -> Dict[str, Any]:
        """
        Valida si Hod esta alineada con sus principios

        Returns:
            Dict con validacion de alineamiento
        """
        # Hod debe estructurar planes
        structures_plans = self.plans_structured > 0

        # Debe crear comunicacion clara
        communicates_clearly = self.communication_strategies_created > 0

        # Debe tener precision razonable (>= 0.6)
        avg_precision = (
            self.precision_score_total / self.activation_count
            if self.activation_count > 0 else 0.0
        )
        is_precise = avg_precision >= 0.6

        # Debe definir metricas
        defines_metrics = self.metrics_frameworks_defined > 0

        # Todas las condiciones deben cumplirse
        is_aligned = all([
            structures_plans,
            communicates_clearly,
            is_precise,
            defines_metrics
        ])

        if is_aligned:
            status = "Hod alineada - Estructura y comunicacion mercurial"
        elif not structures_plans:
            status = "ADVERTENCIA: Hod no estructura planes"
        elif not is_precise:
            status = f"ADVERTENCIA: Precision baja ({avg_precision*100:.1f}%)"
        else:
            status = "Hod requiere calibracion"

        return {
            'is_aligned': is_aligned,
            'structures_plans': structures_plans,
            'communicates_clearly': communicates_clearly,
            'is_precise': is_precise,
            'defines_metrics': defines_metrics,
            'avg_precision_score': avg_precision,
            'avg_clarity_score': (
                self.clarity_score_total / self.activation_count
                if self.activation_count > 0 else 0.0
            ),
            'total_activations': self.activation_count,
            'total_plans_structured': self.plans_structured,
            'total_communication_strategies': self.communication_strategies_created,
            'status': status
        }
