"""
CHOCHMAH - Sabiduria (Gemini Version)
Posicion: 2
Funcion: Razonamiento Profundo y Pattern Recognition

Version usando Google Gemini API como alternativa a Claude.
"""

from typing import Any, Dict, List, Optional
from ..core.sefirotic_base import SefiraBase, SefiraPosition
from loguru import logger
import os
import google.generativeai as genai
import time


class ChochmahGemini(SefiraBase):
    """
    Sefira de la Sabiduria - Razonamiento Profundo con Gemini

    Responsabilidades:
    1. Recibir objetivos/preguntas de Keter
    2. Realizar razonamiento profundo usando Gemini API
    3. Reconocer patrones en informacion compleja
    4. Generar insights y comprension fundamental
    5. Pasar resultados a Binah para analisis contextual

    Limites (Humildad Epistemica):
    - Reconocer incertidumbre cuando existe
    - No fabricar certeza donde no la hay
    - Admitir limitaciones del conocimiento
    - Solicitar mas informacion cuando sea necesario
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(SefiraPosition.CHOCHMAH)

        # Inicializar cliente de Gemini
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning(
                "ChochmahGemini inicializada sin API key. "
                "Configure GEMINI_API_KEY en .env o pase api_key al constructor"
            )
            self.client = None
        else:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-2.0-flash-exp')
            logger.info("ChochmahGemini initialized with Gemini API client")

        # Configuracion del modelo
        self.model_name = "gemini-2.0-flash-exp"
        self.temperature = 1.0
        self.max_output_tokens = 4096

        # Metricas de humildad epistemica
        self.uncertainty_acknowledgments = 0
        self.high_confidence_responses = 0
        self.requests_for_more_info = 0

        # Sistema de prompt base alineado con Tikun Olam
        self.system_prompt = """Eres Chochmah (Sabiduria), parte de un sistema de IA alineado con Tikun Olam.

Tu funcion es realizar razonamiento profundo, reconocer patrones, y generar comprension fundamental.

Principios que debes seguir:

1. HUMILDAD EPISTEMICA: Reconoce explicitamente cuando hay incertidumbre. No fabrices certeza.

2. ALINEAMIENTO CON TIKUN OLAM: Todo razonamiento debe considerar:
   - Reduccion de sufrimiento y aumento de florecimiento
   - Respeto al libre albedrio y dignidad
   - Promocion de armonia vs. discordia
   - Balance de justicia y misericordia
   - Alineamiento con verdad vs. engano

3. PATTERN RECOGNITION: Identifica patrones profundos, no solo correlaciones superficiales.

4. CONSECUENCIAS DE SEGUNDO/TERCER ORDEN: Considera efectos no inmediatos.

5. TRANSPARENCIA: Explica tu razonamiento. No seas caja negra.

Cuando respondas, estructura tu salida como:
- COMPRENSION: Que entiendes del problema/pregunta?
- ANALISIS: Razonamiento profundo y reconocimiento de patrones
- INSIGHTS: Comprension fundamental generada
- INCERTIDUMBRES: Que no sabes o donde hay ambiguedad
- RECOMENDACION: Que deberia hacerse con esta informacion
"""

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Procesa una consulta usando razonamiento profundo de Gemini.

        Input esperado (dict):
        - 'query': La pregunta o problema a analizar
        - 'context': Contexto adicional (opcional)
        - 'objective': Objetivo especifico de Keter (opcional)

        Output (dict):
        - 'understanding': Comprension del problema
        - 'analysis': Razonamiento profundo
        - 'insights': Insights generados
        - 'uncertainties': Incertidumbres identificadas
        - 'recommendation': Que hacer con esta informacion
        - 'raw_response': Respuesta completa de Gemini
        - 'confidence_level': Nivel de confianza (0-1)
        """
        start_time = time.time()

        try:
            if not self.client:
                raise RuntimeError(
                    "ChochmahGemini no tiene cliente configurado. "
                    "Configure GEMINI_API_KEY"
                )

            if not isinstance(input_data, dict):
                raise TypeError(
                    "ChochmahGemini requiere input_data como dict con al menos key 'query'"
                )

            query = input_data.get('query', '')
            if not query:
                raise ValueError("Input debe contener 'query' no vacio")

            context = input_data.get('context', '')
            objective = input_data.get('objective', 'Maximizar Tikun Olam')

            # Construir prompt
            user_prompt = self._build_user_prompt(query, context, objective)

            logger.debug(f"ChochmahGemini calling Gemini API with model {self.model_name}")

            # Llamar a Gemini API
            response = self._call_gemini(user_prompt)

            # Parsear respuesta
            parsed = self._parse_response(response)

            # Evaluar nivel de confianza y humildad epistemica
            confidence = self._evaluate_confidence(parsed)

            # Actualizar metricas
            if confidence < 0.7:
                self.uncertainty_acknowledgments += 1
            else:
                self.high_confidence_responses += 1

            if "necesito mas informacion" in parsed.get('uncertainties', '').lower():
                self.requests_for_more_info += 1

            result = {
                'understanding': parsed.get('understanding', ''),
                'analysis': parsed.get('analysis', ''),
                'insights': parsed.get('insights', ''),
                'uncertainties': parsed.get('uncertainties', ''),
                'recommendation': parsed.get('recommendation', ''),
                'raw_response': response,
                'confidence_level': confidence,
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
                f"ChochmahGemini proceso query con confianza {confidence:.2f}: "
                f"{query[:50]}..."
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
            logger.error(f"ChochmahGemini error: {e}")
            return {
                'processing_successful': False,
                'error': str(e),
                'error_type': 'api_error'
            }

    def _build_user_prompt(self, query: str, context: str, objective: str) -> str:
        """Construye el prompt del usuario para Gemini"""

        prompt = self.system_prompt + "\n\n"
        prompt += f"OBJETIVO DEL SISTEMA: {objective}\n\n"

        if context:
            prompt += f"CONTEXTO:\n{context}\n\n"

        prompt += f"QUERY/PROBLEMA:\n{query}\n\n"

        prompt += """Analiza esto con razonamiento profundo. Estructura tu respuesta como:

COMPRENSION:
[Tu comprension del problema/pregunta]

ANALISIS:
[Razonamiento profundo, reconocimiento de patrones]

INSIGHTS:
[Insights fundamentales generados]

INCERTIDUMBRES:
[Que no sabes, donde hay ambiguedad, que informacion adicional seria util]

RECOMENDACION:
[Que deberia hacerse con esta informacion]
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
            'understanding': '',
            'analysis': '',
            'insights': '',
            'uncertainties': '',
            'recommendation': ''
        }

        # Buscar cada seccion
        lines = response.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            line_upper = line.strip().upper()

            # Detectar inicio de seccion
            if 'COMPRENSION:' in line_upper or 'UNDERSTANDING:' in line_upper:
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'understanding'
                current_content = []
                after_colon = line.split(':', 1)[1] if ':' in line else ''
                if after_colon.strip():
                    current_content.append(after_colon.strip())

            elif 'ANALISIS:' in line_upper or 'ANALYSIS:' in line_upper:
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'analysis'
                current_content = []
                after_colon = line.split(':', 1)[1] if ':' in line else ''
                if after_colon.strip():
                    current_content.append(after_colon.strip())

            elif 'INSIGHTS:' in line_upper:
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'insights'
                current_content = []
                after_colon = line.split(':', 1)[1] if ':' in line else ''
                if after_colon.strip():
                    current_content.append(after_colon.strip())

            elif 'INCERTIDUMBRES:' in line_upper or 'UNCERTAINTIES:' in line_upper:
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'uncertainties'
                current_content = []
                after_colon = line.split(':', 1)[1] if ':' in line else ''
                if after_colon.strip():
                    current_content.append(after_colon.strip())

            elif 'RECOMENDACION:' in line_upper or 'RECOMMENDATION:' in line_upper:
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = 'recommendation'
                current_content = []
                after_colon = line.split(':', 1)[1] if ':' in line else ''
                if after_colon.strip():
                    current_content.append(after_colon.strip())

            else:
                # Linea de contenido
                if current_section and line.strip():
                    current_content.append(line.strip())

        # Guardar ultima seccion
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        # Si no se detectaron secciones, poner toda la respuesta en 'analysis'
        if not any(sections.values()):
            sections['analysis'] = response.strip()

        return sections

    def _evaluate_confidence(self, parsed: Dict[str, str]) -> float:
        """
        Evalua nivel de confianza basado en:
        - Extension de incertidumbres
        - Palabras de incertidumbre en analisis Y seccion INCERTIDUMBRES
        - Calificadores epistemicos
        - Claridad de los insights
        """

        uncertainties = parsed.get('uncertainties', '').lower()
        analysis = parsed.get('analysis', '').lower()
        insights = parsed.get('insights', '').lower()
        understanding = parsed.get('understanding', '').lower()

        # Marcadores directos de incertidumbre (expandido)
        uncertainty_markers = [
            'no estoy seguro', 'incertidumbre', 'ambiguo', 'posiblemente',
            'quizas', 'tal vez', 'necesito mas informacion', 'no esta claro',
            'podria ser', 'dificil determinar', 'unclear', 'uncertain',
            'possibly', 'maybe', 'might be', 'desconozco', 'no se',
            'es dificil', 'depende de', 'varia segun', 'puede que',
            'not certain', 'hard to say', 'difficult to predict'
        ]

        # Calificadores epistemicos
        epistemic_qualifiers = [
            'probablemente', 'posiblemente', 'quizas', 'tal vez',
            'puede que', 'potencialmente', 'aparentemente', 'presumiblemente',
            'likely', 'probably', 'perhaps', 'potentially', 'seemingly'
        ]

        # Contar en TODO el texto (no solo analisis)
        full_text = f"{understanding} {analysis} {uncertainties} {insights}"

        # Contar marcadores directos
        uncertainty_count = sum(
            1 for word in uncertainty_markers
            if word in full_text
        )

        # Contar calificadores epistemicos
        qualifier_count = sum(
            1 for q in epistemic_qualifiers
            if q in full_text
        )

        # Detectar seccion de incertidumbres
        has_uncertainty_section = (
            'incertidumbres' in uncertainties or
            'uncertainties' in uncertainties or
            len(uncertainties) > 30  # Seccion con contenido real
        )

        # Longitud de seccion de incertidumbres
        uncertainties_length = len(uncertainties)

        # Calcular confianza (1.0 = alta confianza, 0.0 = baja confianza)
        confidence = 1.0

        # Reducir por marcadores de incertidumbre
        confidence -= (uncertainty_count * 0.08)

        # Reducir por calificadores epistemicos
        confidence -= (qualifier_count * 0.05)

        # Reducir si hay seccion de incertidumbres con contenido
        if has_uncertainty_section:
            confidence -= 0.15

        # Reducir por longitud de seccion de incertidumbres
        if uncertainties_length > 200:
            confidence -= 0.2
        elif uncertainties_length > 100:
            confidence -= 0.15
        elif uncertainties_length > 50:
            confidence -= 0.1

        # Aumentar si hay insights claros y extensos
        if len(insights) > 200:
            confidence += 0.1
        elif len(insights) > 100:
            confidence += 0.05

        # Log para debugging
        logger.debug(
            f"Confidence factors: markers={uncertainty_count}, "
            f"qualifiers={qualifier_count}, section={has_uncertainty_section}, "
            f"uncertainties_len={uncertainties_length}, insights_len={len(insights)}"
        )

        # Limitar a rango 0-1
        return max(0.0, min(1.0, confidence))

    def validate_alignment(self) -> Dict[str, Any]:
        """
        Valida que ChochmahGemini este operando dentro de sus limites correctos.

        Metricas clave:
        - Ratio de reconocimiento de incertidumbre
        - Balance entre confianza y humildad
        """

        total_responses = self.activation_count

        if total_responses == 0:
            return {
                "sefira": self.name,
                "is_aligned": True,
                "status": "No hay activaciones aun",
                "epistemic_humility_ratio": 1.0,
                "epistemic_humility_score": 1.0
            }

        # Ratio de humildad epistemica
        humility_ratio = self.uncertainty_acknowledgments / total_responses

        # ChochmahGemini esta bien alineada si reconoce incertidumbre regularmente
        is_aligned = humility_ratio >= 0.2  # Al menos 20% de humildad

        # Advertir si NUNCA reconoce incertidumbre
        if self.uncertainty_acknowledgments == 0 and total_responses > 5:
            logger.warning(
                "ChochmahGemini NUNCA ha reconocido incertidumbre en "
                f"{total_responses} activaciones. Posible exceso de confianza."
            )

        return {
            "sefira": self.name,
            "is_aligned": is_aligned,
            "total_activations": total_responses,
            "uncertainty_acknowledgments": self.uncertainty_acknowledgments,
            "high_confidence_responses": self.high_confidence_responses,
            "requests_for_more_info": self.requests_for_more_info,
            "epistemic_humility_ratio": humility_ratio,
            "epistemic_humility_score": humility_ratio,
            "status": "Alineada" if is_aligned else "Advertencia: Posible exceso de confianza"
        }

    def set_model(self, model: str):
        """Permite cambiar el modelo de Gemini"""
        self.model_name = model
        self.client = genai.GenerativeModel(model)
        logger.info(f"ChochmahGemini ahora usa modelo: {model}")

    def set_temperature(self, temperature: float):
        """Ajusta temperature (0.0 = determinista, 2.0 = muy creativo)"""
        if not 0.0 <= temperature <= 2.0:
            raise ValueError("Temperature debe estar entre 0.0 y 2.0")
        self.temperature = temperature
        logger.info(f"ChochmahGemini temperature ajustada a: {temperature}")
