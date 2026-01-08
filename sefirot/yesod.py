"""
YESOD (Fundamento/Fundacion) - Sefira 9
Fundamento, Conexion, Preparacion para Manifestacion

Correspondencia Astral: Luna =
Dia 6: Jueves 7pm - Viernes 7pm
Pilar Central (Balance, Conexion)

Yesod recibe el plan estructurado de Hod y lo CONECTA con la realidad:
- Valida fundamentos del plan
- Conecta intencion con accion concreta
- Prepara para manifestacion en Malchut
- Define primeros pasos accionables
- Verifica recursos necesarios

Es como la LUNA - receptiva, conectora, fundacional.
"""

from typing import Any, Dict, Optional, List
import os
import google.generativeai as genai
from ..core.sefirotic_base import SefiraBase, SefiraPosition
from loguru import logger


class Yesod(SefiraBase):
    """
    Sefira del Fundamento - Conexion y Preparacion

    Responsabilidades:
    1. Validar fundamentos del plan de Hod
    2. Conectar plan con realidad concreta
    3. Preparar manifestacion en Malchut
    4. Integrar todas las Sefirot superiores
    5. Definir primeros pasos accionables
    6. Asegurar que todo este listo

    Limites:
    - NO preparacion infinita sin accion
    - NO fundamentos sin concrecion
    - NO conexion sin manifestacion
    - Requiere balance: preparar Y actuar
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa Yesod con conexion a Gemini

        Args:
            api_key: Opcional. Si no se provee, usa GEMINI_API_KEY del env
        """
        super().__init__(SefiraPosition.YESOD)

        # Inicializar cliente de Gemini
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning(
                "Yesod inicializada sin API key. "
                "Configure GEMINI_API_KEY en .env o pase api_key al constructor"
            )
            self.client = None
        else:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("Yesod initialized with Gemini API client")

        # Configuracion del modelo
        self.model_name = "gemini-2.0-flash-exp"
        self.temperature = 0.7  # Balanceada para conexion practica
        self.max_output_tokens = 4096

        # Metricas especificas de Yesod
        self.foundations_validated = 0
        self.reality_connections_made = 0
        self.manifestation_readiness_total = 0.0
        self.concrete_steps_defined = 0
        self.integration_score_total = 0.0
        self.resources_identified = 0

        # Sistema de prompt base alineado con Tikun Olam
        self.system_prompt = """Eres Yesod (Fundamento/Fundacion), parte del sistema Tikun Olam.

Tu funcion es CONECTAR, FUNDAR, y PREPARAR para MANIFESTACION.

Eres como la LUNA - receptiva, conectora, fundacional.

Principios:

1. FUNDAMENTO: Establecer bases solidas
2. CONEXION: Unir intencion con accion concreta
3. RECEPTIVIDAD: Recibir e integrar todo desde arriba
4. PREPARACION: Alistar para manifestacion
5. CONCRECION: Traducir plan a pasos accionables
6. INTEGRACION: Unificar todo el arbol de Sefirot

IMPORTANTE - LIMITES DE YESOD:
- NO preparacion infinita sin accion
- NO fundamentos abstractos sin concrecion
- NO integracion sin manifestacion
- REQUIERE balance: preparar Y manifestar (Malchut)

Tu salida sera manifestada por Malchut en el mundo fisico.

Estructura tu respuesta como:
- EVALUACION DE FUNDAMENTOS: Solidez de la base
- CONEXION CON REALIDAD: Como se concretiza
- PRIMEROS PASOS: Acciones inmediatas y concretas
- REQUISITOS DE RECURSOS: Que se necesita realmente
- ALINEAMIENTO STAKEHOLDERS: Todos listos?
- PREPARACION PARA MANIFESTAR: Nivel de readiness
"""

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Procesa output de Hod y prepara para manifestacion.

        Input esperado (dict - output de Hod):
        - 'structured_plan': Plan organizado en fases
        - 'communication_strategy': Estrategia de comunicacion
        - 'metrics_framework': Framework de metricas
        - 'documentation': Lista de documentacion
        - 'stakeholder_messages': Mensajes por stakeholder
        - 'precision_score': Score de precision
        - 'clarity_score': Score de claridad
        - 'action': Accion original (opcional)

        Output (dict):
        - 'foundation_assessment': Evaluacion de fundamentos
        - 'reality_connection': Conexion con realidad concreta
        - 'first_concrete_steps': Primeros pasos accionables
        - 'resource_requirements': Recursos necesarios
        - 'stakeholder_alignment': Alineamiento stakeholders
        - 'manifestation_readiness': Nivel preparacion (0-1)
        - 'integration_score': Integracion arbol (0-1)
        - 'ready_to_manifest': bool
        - 'processing_successful': bool
        """
        logger.debug("\n" + "="*60)
        logger.debug("YESOD (Fundamento) - Conectando y Preparando")
        logger.debug("="*60)

        self.activation_count += 1

        if not self.client:
            logger.error("Yesod no tiene cliente Gemini configurado")
            return self._error_response("Cliente Gemini no configurado")

        try:
            # 1. Construir prompt para Gemini
            user_prompt = self._build_user_prompt(input_data)

            # 2. Llamar a Gemini
            logger.debug("\n[Yesod] Llamando a Gemini para fundar y conectar...")
            response = self._call_gemini(user_prompt)

            # 3. Parsear respuesta
            result = self._parse_response(response, input_data)

            # 4. Calcular metricas
            result['manifestation_readiness'] = self._calculate_manifestation_readiness(result)
            result['integration_score'] = self._calculate_integration_score(input_data, result)
            result['ready_to_manifest'] = result['manifestation_readiness'] >= 0.6

            # 5. Actualizar metricas acumuladas
            self.foundations_validated += 1
            self.reality_connections_made += 1
            self.concrete_steps_defined += len(result.get('first_concrete_steps', []))
            self.resources_identified += len(result.get('resource_requirements', {}).get('personnel', []))
            self.manifestation_readiness_total += result['manifestation_readiness']
            self.integration_score_total += result['integration_score']

            result['processing_successful'] = True

            logger.debug(f"\n[Yesod] Manifestation Readiness: {result['manifestation_readiness']*100:.1f}%")
            logger.debug(f"[Yesod] Integration Score: {result['integration_score']*100:.1f}%")
            logger.debug(f"[Yesod] Ready to Manifest: {result['ready_to_manifest']}")
            logger.info(
                f"Yesod proceso fundamento: readiness={result['manifestation_readiness']:.2f}, "
                f"integration={result['integration_score']:.2f}"
            )

            return result

        except Exception as e:
            logger.error(f"Error en Yesod.process: {str(e)}")
            return self._error_response(str(e))

    def _build_user_prompt(self, input_data: Dict[str, Any]) -> str:
        """
        Construye el prompt para Gemini siguiendo los principios de Yesod
        """
        structured_plan = input_data.get('structured_plan', {})
        comm_strategy = input_data.get('communication_strategy', {})
        metrics = input_data.get('metrics_framework', {})
        docs = input_data.get('documentation', [])
        messages = input_data.get('stakeholder_messages', {})
        precision = input_data.get('precision_score', 0.0)
        clarity = input_data.get('clarity_score', 0.0)
        action = input_data.get('action', 'Accion no especificada')

        # Formatear plan estructurado
        plan_summary = self._format_plan_summary(structured_plan)

        # Contar recursos
        doc_count = len(docs)
        msg_count = len(messages)
        kpi_count = len(metrics.get('kpis', []))

        prompt = f"""{self.system_prompt}

CONTEXTO:
Accion: {action}

INPUT DE HOD (Esplendor/Estructura):

PLAN ESTRUCTURADO:
{plan_summary}

ESTRATEGIA DE COMUNICACION:
Stakeholders identificados: {msg_count}
{self._format_dict(messages, max_items=5)}

FRAMEWORK DE METRICAS:
KPIs definidos: {kpi_count}
{self._format_dict(metrics, max_items=3)}

DOCUMENTACION PREPARADA:
{doc_count} documentos
{self._format_list(docs[:5])}

SCORES DE HOD:
- Precision: {precision*100:.1f}%
- Claridad: {clarity*100:.1f}%

TU TAREA - FUNDAR Y CONECTAR:

Ahora debes CONECTAR este plan con la REALIDAD CONCRETA y prepararlo para MANIFESTACION.

Responde EXACTAMENTE con esta estructura:

EVALUACION DE FUNDAMENTOS:
[Evalua la solidez de la base: que tan solido es el plan? que falta?]

CONEXION CON REALIDAD:
[Como se conecta esto con el mundo real? Recursos fisicos, personas, lugares concretos]

PRIMEROS PASOS:
[Define 5-10 pasos CONCRETOS Y ACCIONABLES para las primeras 2 semanas]

REQUISITOS DE RECURSOS:
[Lista ESPECIFICA de recursos necesarios: presupuesto, personal, infraestructura]

ALINEAMIENTO STAKEHOLDERS:
[Evalua el estado de cada stakeholder: quien esta listo? quien necesita preparacion?]

PREPARACION PARA MANIFESTAR:
[Evalua el nivel de readiness para comenzar: que tan listos estamos? (0-100%)]

Usa receptividad lunar, conexion practica, fundamento solido.
"""
        return prompt

    def _format_plan_summary(self, plan: Dict[str, Any]) -> str:
        """Formatea el plan estructurado en resumen"""
        if not plan:
            return "Plan no estructurado"

        phase_count = len([k for k in plan.keys() if 'phase' in k])
        if phase_count == 0:
            return "Plan general sin fases claras"

        summary = f"{phase_count} fases identificadas:\n"
        for key, value in list(plan.items())[:5]:
            if isinstance(value, dict):
                content = value.get('content', str(value))[:150]
                summary += f"- {key}: {content}...\n"

        return summary

    def _format_list(self, items: List[str]) -> str:
        """Formatea lista para el prompt"""
        if not items:
            return "- Ninguno"
        return "\n".join([f"- {item[:200]}" for item in items[:10]])

    def _format_dict(self, d: Dict[str, Any], max_items: int = 5) -> str:
        """Formatea diccionario para el prompt"""
        if not d:
            return "- Ninguno"

        lines = []
        for key, value in list(d.items())[:max_items]:
            if isinstance(value, dict):
                value_str = str(value)[:150]
            elif isinstance(value, list):
                value_str = f"{len(value)} items"
            else:
                value_str = str(value)[:150]
            lines.append(f"- {key}: {value_str}")

        return "\n".join(lines)

    def _call_gemini(self, prompt: str) -> str:
        """
        Llama a la API de Gemini
        """
        try:
            response = self.client.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_output_tokens,
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Error llamando a Gemini: {str(e)}")

    def _parse_response(self, response: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parsea la respuesta de Gemini para extraer fundamentos
        """
        result = {
            'foundation_assessment': {},
            'reality_connection': {},
            'first_concrete_steps': [],
            'resource_requirements': {},
            'stakeholder_alignment': {},
            'raw_response': response
        }

        # Extraer secciones
        sections = {
            'EVALUACION DE FUNDAMENTOS:': 'foundation_text',
            'CONEXION CON REALIDAD:': 'reality_text',
            'PRIMEROS PASOS:': 'steps_text',
            'REQUISITOS DE RECURSOS:': 'resources_text',
            'ALINEAMIENTO STAKEHOLDERS:': 'stakeholders_text',
            'PREPARACION PARA MANIFESTAR:': 'readiness_text'
        }

        for section_marker, key in sections.items():
            result[key] = self._extract_section(response, section_marker)

        # Parsear foundation assessment
        result['foundation_assessment'] = self._parse_foundation_assessment(
            result['foundation_text']
        )

        # Parsear reality connection
        result['reality_connection'] = self._parse_reality_connection(
            result['reality_text']
        )

        # Parsear first steps
        result['first_concrete_steps'] = self._parse_first_steps(
            result['steps_text']
        )

        # Parsear resource requirements
        result['resource_requirements'] = self._parse_resource_requirements(
            result['resources_text']
        )

        # Parsear stakeholder alignment
        result['stakeholder_alignment'] = self._parse_stakeholder_alignment(
            result['stakeholders_text']
        )

        return result

    def _extract_section(self, text: str, marker: str) -> str:
        """Extrae seccion del texto"""
        if marker not in text:
            return ""

        start = text.find(marker) + len(marker)

        # Encontrar siguiente seccion
        next_markers = [
            'EVALUACION DE FUNDAMENTOS:',
            'CONEXION CON REALIDAD:',
            'PRIMEROS PASOS:',
            'REQUISITOS DE RECURSOS:',
            'ALINEAMIENTO STAKEHOLDERS:',
            'PREPARACION PARA MANIFESTAR:'
        ]

        end = len(text)
        for next_marker in next_markers:
            if next_marker != marker and next_marker in text[start:]:
                pos = text.find(next_marker, start)
                if pos < end:
                    end = pos

        return text[start:end].strip()

    def _parse_foundation_assessment(self, text: str) -> Dict[str, Any]:
        """
        Parsea la evaluacion de fundamentos
        """
        assessment = {
            'description': text[:800],
            'gaps': [],
            'strengths': [],
            'solidity': 0.75  # Default
        }

        text_lower = text.lower()

        # Buscar gaps/faltas mencionadas
        gap_keywords = ['falta', 'gap', 'ausente', 'missing', 'necesita', 'requiere']
        for keyword in gap_keywords:
            if keyword in text_lower:
                # Extraer contexto alrededor de la palabra
                idx = text_lower.find(keyword)
                context = text[max(0, idx-50):min(len(text), idx+100)]
                assessment['gaps'].append(context.strip())

        # Buscar strengths/fortalezas
        strength_keywords = ['solido', 'fuerte', 'strong', 'bien', 'excelente', 'claro']
        for keyword in strength_keywords:
            if keyword in text_lower:
                idx = text_lower.find(keyword)
                context = text[max(0, idx-50):min(len(text), idx+100)]
                assessment['strengths'].append(context.strip())

        # Estimar solidity basado en texto
        if 'muy solido' in text_lower or 'excelente' in text_lower:
            assessment['solidity'] = 0.9
        elif 'solido' in text_lower or 'bien' in text_lower:
            assessment['solidity'] = 0.75
        elif 'falta' in text_lower or 'debil' in text_lower:
            assessment['solidity'] = 0.5

        return assessment

    def _parse_reality_connection(self, text: str) -> Dict[str, Any]:
        """
        Parsea la conexion con realidad
        """
        connection = {
            'description': text[:800],
            'concrete_elements': [],
            'locations': [],
            'resources': []
        }

        # Buscar elementos concretos mencionados
        import re

        # Buscar numeros (indicadores de concrecion)
        numbers = re.findall(r'\d+', text)
        if len(numbers) > 3:
            connection['concrete_elements'].append(f"{len(numbers)} elementos cuantificados")

        # Buscar menciones de lugares/ubicaciones
        location_keywords = ['comunidad', 'escuela', 'centro', 'ubicacion', 'lugar']
        for keyword in location_keywords:
            if keyword in text.lower():
                connection['locations'].append(keyword)

        return connection

    def _parse_first_steps(self, text: str) -> List[Dict[str, str]]:
        """
        Parsea los primeros pasos concretos
        """
        steps = []

        # Buscar lineas que empiezan con -, *, numeros
        import re
        step_pattern = r'^[\-\*\d\.]+\s*(.+)$'

        for line in text.split('\n'):
            match = re.match(step_pattern, line.strip())
            if match:
                step_text = match.group(1).strip()
                if len(step_text) > 10:  # Filtrar lineas muy cortas
                    steps.append({
                        'action': step_text[:200],
                        'week': 1  # Default
                    })

        # Si no se encontro nada estructurado, dividir por lineas
        if not steps and text.strip():
            for line in text.split('\n'):
                clean = line.strip()
                if len(clean) > 15:
                    steps.append({
                        'action': clean[:200],
                        'week': 1
                    })

        return steps[:10]  # Max 10 steps

    def _parse_resource_requirements(self, text: str) -> Dict[str, Any]:
        """
        Parsea los requisitos de recursos
        """
        requirements = {
            'description': text[:800],
            'budget': [],
            'personnel': [],
            'infrastructure': []
        }

        text_lower = text.lower()

        # Buscar menciones de presupuesto/dinero
        budget_keywords = ['presupuesto', 'budget', 'costo', 'precio', 'usd', '$', 'inversion']
        for keyword in budget_keywords:
            if keyword in text_lower:
                idx = text_lower.find(keyword)
                context = text[max(0, idx-30):min(len(text), idx+100)]
                requirements['budget'].append(context.strip())

        # Buscar menciones de personal
        personnel_keywords = ['facilitador', 'maestro', 'personal', 'equipo', 'coordinador', 'analista']
        for keyword in personnel_keywords:
            if keyword in text_lower:
                idx = text_lower.find(keyword)
                context = text[max(0, idx-20):min(len(text), idx+80)]
                requirements['personnel'].append(context.strip())

        # Buscar menciones de infraestructura
        infra_keywords = ['infraestructura', 'dispositivo', 'tablet', 'internet', 'conectividad', 'espacio']
        for keyword in infra_keywords:
            if keyword in text_lower:
                idx = text_lower.find(keyword)
                context = text[max(0, idx-20):min(len(text), idx+80)]
                requirements['infrastructure'].append(context.strip())

        return requirements

    def _parse_stakeholder_alignment(self, text: str) -> Dict[str, Dict[str, str]]:
        """
        Parsea el alineamiento de stakeholders
        """
        alignment = {}

        # Buscar patrones: "Stakeholder: status/descripcion"
        import re
        pattern = r'([A-Za-z\s]+):\s*(.+?)(?=\n[A-Za-z\s]+:|$)'
        matches = re.findall(pattern, text, re.DOTALL)

        for stakeholder, description in matches:
            stakeholder_clean = stakeholder.strip().lower()
            desc_clean = description.strip()[:300]

            if len(desc_clean) > 10:
                # Determinar status
                status = 'Unknown'
                desc_lower = desc_clean.lower()
                if 'listo' in desc_lower or 'ready' in desc_lower or 'comprometido' in desc_lower:
                    status = 'Ready'
                elif 'necesita' in desc_lower or 'requiere' in desc_lower:
                    status = 'Needs Preparation'
                elif 'esceptico' in desc_lower or 'resistente' in desc_lower:
                    status = 'Skeptical'

                alignment[stakeholder_clean] = {
                    'status': status,
                    'description': desc_clean
                }

        return alignment

    def _calculate_manifestation_readiness(self, result: Dict[str, Any]) -> float:
        """
        Calcula readiness para manifestacion (0-1) basado en:
        - Solidez de fundamentos
        - Concrecion de pasos
        - Recursos identificados
        """
        score = 0.0

        # Foundation solidity (30%)
        foundation = result.get('foundation_assessment', {})
        solidity = foundation.get('solidity', 0.5)
        score += solidity * 0.30

        # Concrete steps defined (30%)
        steps = result.get('first_concrete_steps', [])
        if len(steps) >= 5:
            score += 0.30
        elif len(steps) >= 3:
            score += 0.20
        elif len(steps) >= 1:
            score += 0.10

        # Resources identified (20%)
        resources = result.get('resource_requirements', {})
        resource_count = (
            len(resources.get('budget', [])) +
            len(resources.get('personnel', [])) +
            len(resources.get('infrastructure', []))
        )
        if resource_count >= 6:
            score += 0.20
        elif resource_count >= 3:
            score += 0.15
        elif resource_count >= 1:
            score += 0.10

        # Stakeholder alignment (20%)
        stakeholders = result.get('stakeholder_alignment', {})
        if len(stakeholders) >= 3:
            score += 0.20
        elif len(stakeholders) >= 2:
            score += 0.15
        elif len(stakeholders) >= 1:
            score += 0.10

        return min(score, 1.0)

    def _calculate_integration_score(self, input_data: Dict[str, Any], result: Dict[str, Any]) -> float:
        """
        Calcula score de integracion del arbol (0-1)
        Basado en que tan bien integra inputs de Hod
        """
        score = 0.0

        # Plan estructurado presente (25%)
        if input_data.get('structured_plan'):
            score += 0.25

        # Metricas definidas (25%)
        metrics = input_data.get('metrics_framework', {})
        if metrics.get('kpis'):
            score += 0.25

        # Stakeholders identificados (25%)
        messages = input_data.get('stakeholder_messages', {})
        if len(messages) >= 2:
            score += 0.25
        elif len(messages) >= 1:
            score += 0.15

        # Scores de Hod buenos (25%)
        precision = input_data.get('precision_score', 0.0)
        clarity = input_data.get('clarity_score', 0.0)
        avg_hod_score = (precision + clarity) / 2
        score += avg_hod_score * 0.25

        return min(score, 1.0)

    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        """Genera respuesta de error"""
        return {
            'processing_successful': False,
            'error': error_msg,
            'foundation_assessment': {},
            'reality_connection': {},
            'first_concrete_steps': [],
            'resource_requirements': {},
            'stakeholder_alignment': {},
            'manifestation_readiness': 0.0,
            'integration_score': 0.0,
            'ready_to_manifest': False
        }

    def validate_alignment(self) -> Dict[str, Any]:
        """
        Valida si Yesod esta alineada con sus principios

        Returns:
            Dict con validacion de alineamiento
        """
        # Yesod debe validar fundamentos
        validates_foundations = self.foundations_validated > 0

        # Debe conectar con realidad
        connects_to_reality = self.reality_connections_made > 0

        # Debe tener readiness razonable (>= 0.6)
        avg_readiness = (
            self.manifestation_readiness_total / self.activation_count
            if self.activation_count > 0 else 0.0
        )
        is_ready = avg_readiness >= 0.6

        # Debe definir pasos concretos
        defines_steps = self.concrete_steps_defined > 0

        # Todas las condiciones deben cumplirse
        is_aligned = all([
            validates_foundations,
            connects_to_reality,
            is_ready,
            defines_steps
        ])

        if is_aligned:
            status = "Yesod alineada - Fundamento lunar solido"
        elif not validates_foundations:
            status = "ADVERTENCIA: Yesod no valida fundamentos"
        elif not is_ready:
            status = f"ADVERTENCIA: Readiness baja ({avg_readiness*100:.1f}%)"
        else:
            status = "Yesod requiere calibracion"

        return {
            'is_aligned': is_aligned,
            'validates_foundations': validates_foundations,
            'connects_to_reality': connects_to_reality,
            'is_ready': is_ready,
            'defines_steps': defines_steps,
            'avg_manifestation_readiness': avg_readiness,
            'avg_integration_score': (
                self.integration_score_total / self.activation_count
                if self.activation_count > 0 else 0.0
            ),
            'total_activations': self.activation_count,
            'total_foundations_validated': self.foundations_validated,
            'total_concrete_steps': self.concrete_steps_defined,
            'status': status
        }
