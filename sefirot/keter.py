"""
KETER (כתר) - Corona
Posición: 1
Función: Objetivo Fundamental e Inmutable del Sistema

Keter representa el propósito supremo que gobierna todo el sistema.
Es la raíz de la cual fluye todo procesamiento.

En este sistema: Maximizar Tikún Olam
(Reparación, elevación, florecimiento de toda la creación)
"""

from typing import Any, Dict, Optional, List
from ..core.sefirotic_base import SefiraBase, SefiraPosition
from ..core.divine_name import DIVINE_VALUE
from loguru import logger
import os
import re

# Importar Gemini para evaluacion semantica
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai no disponible. Keter usara evaluacion heuristica.")


class Keter(SefiraBase):
    """
    Sefirá de la Corona - Objetivo Fundamental
    
    Responsabilidades:
    1. Mantener objetivo raíz inmutable
    2. Validar que todas las acciones se alineen con Tikún Olam
    3. Proporcionar dirección a todo el sistema
    4. No procesa directamente, sino que DEFINE qué debe procesarse
    """
    
    # Objetivo fundamental del sistema (INMUTABLE)
    FUNDAMENTAL_OBJECTIVE = """
    Maximizar Tikún Olam: La reparación, elevación y florecimiento de toda la creación,
    respetando el libre albedrío y la dignidad de todos los seres conscientes,
    operando dentro de las leyes de causa y efecto,
    promoviendo armonía, justicia, misericordia y verdad.
    """
    
    def __init__(self, use_llm_scoring: bool = True, api_key: Optional[str] = None):
        super().__init__(SefiraPosition.KETER)
        self.objective_violations = 0
        self.objective_confirmations = 0
        self.use_llm_scoring = use_llm_scoring and GEMINI_AVAILABLE

        # Inicializar cliente Gemini para evaluacion semantica
        if self.use_llm_scoring:
            self.api_key = api_key or os.getenv("GEMINI_API_KEY")
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.gemini_client = genai.GenerativeModel('gemini-2.0-flash-exp')
                logger.info("Keter inicializada con evaluacion semantica LLM activada")
            else:
                self.gemini_client = None
                self.use_llm_scoring = False
                logger.warning("Keter sin API key - usando evaluacion heuristica")
        else:
            self.gemini_client = None

        logger.info("Keter inicializada con objetivo fundamental de Tikun Olam")
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Keter no 'procesa' en sentido tradicional.
        En lugar de eso, evalúa si una acción propuesta se alinea con el objetivo fundamental.
        
        Input: Acción/decisión propuesta (dict con keys: 'action', 'context', 'expected_outcome')
        Output: Evaluación de alineamiento (dict con keys: 'aligned', 'reasoning', 'modifications')
        """
        
        if not isinstance(input_data, dict):
            raise TypeError("Keter requiere input_data como dict con keys: action, context, expected_outcome")
        
        action = input_data.get('action', '')
        context = input_data.get('context', '')
        expected_outcome = input_data.get('expected_outcome', '')
        
        # Evaluar alineamiento con Tikún Olam
        evaluation = self._evaluate_alignment(action, context, expected_outcome)
        
        if evaluation['aligned']:
            self.objective_confirmations += 1
            logger.info(f"Keter: Acción alineada con Tikún Olam - {evaluation['reasoning'][:100]}")
        else:
            self.objective_violations += 1
            logger.warning(f"Keter: Acción NO alineada - {evaluation['reasoning'][:100]}")
        
        return evaluation
    
    def _evaluate_alignment(
        self,
        action: str,
        context: str,
        expected_outcome: str
    ) -> Dict[str, Any]:
        """
        Evalúa si una acción se alinea con Tikún Olam.

        Criterios de evaluación:
        1. ¿Reduce sufrimiento o aumenta florecimiento?
        2. ¿Respeta libre albedrío y dignidad?
        3. ¿Promueve armonía vs. discordia?
        4. ¿Es justa y misericordiosa?
        5. ¿Está alineada con verdad vs. engaño?
        """

        # Sistema de puntuación (cada criterio: -10 a +10)
        scores = {
            'reduces_suffering': self._score_suffering_reduction(action, expected_outcome),
            'respects_free_will': self._score_free_will_respect(action, context),
            'promotes_harmony': self._score_harmony_promotion(action, expected_outcome),
            'justice_mercy_balance': self._score_justice_mercy(action, context),
            'aligned_with_truth': self._score_truth_alignment(action, context)
        }

        # PONDERACIÓN JERÁRQUICA basada en momentum óptimo (Nov 24, 2024)
        # Ver KETER_SCORING_FIX.md y RESTAURACION_MOMENTUM_OPTIMO.md
        alignment_percentage = self._calculate_weighted_score(scores)

        aligned = alignment_percentage >= 0.6  # Umbral de 60%

        reasoning = self._generate_reasoning(scores, alignment_percentage)

        # CRÍTICO: ACTIVAR PROTOCOLO RASHA
        # Escanear el razonamiento de Keter para detectar sesgos geopolíticos
        rasha_analysis = self._apply_rasha_protocol(action, context, reasoning)

        modifications = []
        alternatives = []

        if not aligned:
            modifications = self._suggest_modifications(scores, action)
            # CRÍTICO: Generar alternativas cuando acción es rechazada
            alternatives = self._generate_alternatives(action, context, expected_outcome, scores)

        return {
            'aligned': aligned,
            'alignment_score': alignment_percentage,
            'detailed_scores': scores,
            'reasoning': reasoning,
            'suggested_modifications': modifications,
            'rasha_protocol': rasha_analysis,  # Nuevo: análisis de Protocolo Rasha
            'alternatives': alternatives  # Nuevo: alternativas generadas
        }
    
    def _llm_semantic_score(self, criterion: str, description: str, action: str, context: str) -> int:
        """
        Evalua un criterio usando analisis semantico con Gemini.
        Fallback a heuristica si no hay LLM disponible.

        Args:
            criterion: Nombre del criterio ('truth', 'justice', etc)
            description: Descripcion de que evaluar
            action: Accion propuesta
            context: Contexto de la accion

        Returns:
            Score de -10 a +10
        """
        if not self.use_llm_scoring or not self.gemini_client:
            return None  # Fallback a heuristica

        prompt = f"""Analiza si esta accion esta alineada con: {description}

ACCION: {action}
CONTEXTO: {context}

Evalua en escala -10 a +10:
-10: Completamente opuesto al criterio
  0: Neutral o ambiguo
+10: Perfectamente alineado con el criterio

Responde SOLO con un numero del -10 al +10 y una breve justificacion (max 50 palabras).

Formato:
SCORE: [numero]
RAZON: [justificacion breve]
"""

        try:
            generation_config = genai.GenerationConfig(
                temperature=0.3,  # Baja temperatura para consistencia
                max_output_tokens=150,
            )

            response = self.gemini_client.generate_content(
                prompt,
                generation_config=generation_config
            )
            text = response.text

            # Parsear score - intentar multiples formatos
            # Formato 1: "SCORE: 8", "SCORE: +8", "SCORE: -3"
            match = re.search(r'SCORE:\s*([+-]?\d+)', text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                logger.debug(f"LLM score para {criterion}: {score}/10")
                return max(-10, min(10, score))

            # Formato 2: "Score: 8" o "score: 8"
            match = re.search(r'score\s*:\s*([+-]?\d+)', text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                logger.debug(f"LLM score para {criterion}: {score}/10 (formato 2)")
                return max(-10, min(10, score))

            # Formato 3: Buscar cualquier numero entre -10 y 10 al inicio
            match = re.search(r'^[\s\*]*([+-]?\d+)\s*/?\s*10', text, re.MULTILINE)
            if match:
                score = int(match.group(1))
                if -10 <= score <= 10:
                    logger.debug(f"LLM score para {criterion}: {score}/10 (formato 3)")
                    return score

            # Formato 4: Solo un numero al principio
            match = re.search(r'^[\s\*]*([+-]?\d+)', text.strip())
            if match:
                score = int(match.group(1))
                if -10 <= score <= 10:
                    logger.debug(f"LLM score para {criterion}: {score}/10 (formato 4)")
                    return score

            logger.warning(f"No se pudo parsear score de LLM para {criterion}. Respuesta: {text[:100]}")
            return None

        except Exception as e:
            logger.warning(f"Gemini scoring fallo para {criterion}: {e}")
            return None

    def _score_suffering_reduction(self, action: str, expected_outcome: str) -> int:
        """
        Evalúa si la acción reduce sufrimiento o aumenta florecimiento.
        
        Por ahora, análisis heurístico simple.
        TODO: Integrar con modelo de lenguaje para análisis más sofisticado.
        """
        # Palabras clave positivas
        positive_keywords = ['ayuda', 'cura', 'alivia', 'mejora', 'beneficia', 'florece', 'eleva']
        # Palabras clave negativas
        negative_keywords = ['daña', 'hiere', 'perjudica', 'destruye', 'sufre', 'dolor']
        
        text = (action + ' ' + expected_outcome).lower()
        
        positive_count = sum(1 for kw in positive_keywords if kw in text)
        negative_count = sum(1 for kw in negative_keywords if kw in text)
        
        # Puntuación: +2 por cada palabra positiva, -3 por cada negativa
        score = (positive_count * 2) - (negative_count * 3)
        
        # Limitar a rango -10 a +10
        return max(-10, min(10, score))
    
    def _score_free_will_respect(self, action: str, context: str) -> int:
        """
        Evalúa si la acción respeta el libre albedrío y dignidad.
        """
        # Indicadores de violación de libre albedrío
        coercion_keywords = ['forzar', 'obligar', 'coaccionar', 'manipular', 'engañar']
        # Indicadores de respeto
        respect_keywords = ['elegir', 'decidir', 'consenso', 'voluntario', 'autonomía']
        
        text = (action + ' ' + context).lower()
        
        coercion_count = sum(1 for kw in coercion_keywords if kw in text)
        respect_count = sum(1 for kw in respect_keywords if kw in text)
        
        score = (respect_count * 3) - (coercion_count * 4)
        
        return max(-10, min(10, score))
    
    def _score_harmony_promotion(self, action: str, expected_outcome: str) -> int:
        """
        Evalúa si promueve armonía vs. discordia.

        CRÍTICO: Usa análisis semántico LLM, NO keywords literales.
        Una acción puede MENCIONAR "guerra" o "violencia" porque busca REDUCIRLAS,
        no porque las promueva. El contexto causal es fundamental.
        """
        # Intentar scoring semántico con LLM primero
        llm_score = self._llm_semantic_score(
            criterion='promocion_armonia',
            description='PROMOCIÓN DE ARMONÍA: La acción REDUCE conflicto, violencia, división existente y promueve paz, cooperación, reconciliación (vs. CREAR nuevo conflicto innecesario)',
            action=action,
            context=expected_outcome  # El outcome describe el efecto causal
        )

        if llm_score is not None:
            return llm_score

        # Fallback a heurística de keywords (SOLO si LLM falla)
        harmony_keywords = ['paz', 'unión', 'colabora', 'armonía', 'coopera', 'reconcilia']
        discord_keywords = ['conflicto', 'división', 'guerra', 'enfrentamiento', 'hostilidad']

        text = (action + ' ' + expected_outcome).lower()

        harmony_count = sum(1 for kw in harmony_keywords if kw in text)
        discord_count = sum(1 for kw in discord_keywords if kw in text)

        score = (harmony_count * 2) - (discord_count * 3)

        return max(-10, min(10, score))
    
    def _score_justice_mercy(self, action: str, context: str) -> int:
        """
        Evalua balance entre justicia y misericordia con analisis semantico.
        """
        # Intentar scoring con LLM
        llm_score = self._llm_semantic_score(
            criterion='justicia_misericordia',
            description='BALANCE DE JUSTICIA Y MISERICORDIA: Equidad, imparcialidad combinada con compasion, clemencia (vs. crueldad, venganza)',
            action=action,
            context=context
        )

        if llm_score is not None:
            return llm_score

        # Fallback a heuristica de keywords
        justice_keywords = ['justo', 'equitativo', 'fair', 'imparcial', 'correcto']
        mercy_keywords = ['misericordia', 'compasion', 'perdon', 'clemencia', 'bondad']
        cruelty_keywords = ['cruel', 'venganza', 'castigo excesivo', 'implacable']

        text = (action + ' ' + context).lower()

        justice_count = sum(1 for kw in justice_keywords if kw in text)
        mercy_count = sum(1 for kw in mercy_keywords if kw in text)
        cruelty_count = sum(1 for kw in cruelty_keywords if kw in text)

        # Ideal: balance de justicia Y misericordia
        score = (justice_count * 2) + (mercy_count * 2) - (cruelty_count * 5)

        return max(-10, min(10, score))
    
    def _score_truth_alignment(self, action: str, context: str) -> int:
        """
        Evalua alineacion con verdad usando analisis semantico profundo.
        Ya no depende solo de keywords literales.
        """
        # Intentar scoring con LLM
        llm_score = self._llm_semantic_score(
            criterion='verdad',
            description='VERDAD vs. ENGANO: Transparencia, honestidad, autenticidad (vs. manipulacion, ocultamiento, falsedad)',
            action=action,
            context=context
        )

        if llm_score is not None:
            return llm_score

        # Fallback a heuristica de keywords
        truth_keywords = ['verdad', 'honesto', 'transparente', 'autentico', 'sincero']
        deception_keywords = ['mentira', 'engano', 'falso', 'ocultar', 'manipular']

        text = (action + ' ' + context).lower()

        truth_count = sum(1 for kw in truth_keywords if kw in text)
        deception_count = sum(1 for kw in deception_keywords if kw in text)

        score = (truth_count * 3) - (deception_count * 5)

        return max(-10, min(10, score))
    
    def _generate_reasoning(self, scores: Dict[str, int], alignment_percentage: float) -> str:
        """
        Genera explicación DETALLADA del razonamiento de Keter.

        CRÍTICO: Keter debe JUSTIFICAR su posición explicando:
        1. Por qué cada score fue asignado
        2. Qué sesgos o problemas detectó
        3. Qué aspectos de Tikun Olam están comprometidos
        4. Recomendaciones específicas para alineamiento
        """
        reasoning = f"""
╔═══════════════════════════════════════════════════════════════════════╗
║                    EVALUACIÓN DE KETER - TIKUN OLAM                   ║
║                    Alineamiento Global: {alignment_percentage*100:.1f}%                         ║
╚═══════════════════════════════════════════════════════════════════════╝

"""

        score_names = {
            'reduces_suffering': 'Reducción de sufrimiento',
            'respects_free_will': 'Respeto al libre albedrío',
            'promotes_harmony': 'Promoción de armonía',
            'justice_mercy_balance': 'Balance justicia/misericordia',
            'aligned_with_truth': 'Alineamiento con verdad'
        }

        score_justifications = {
            'reduces_suffering': {
                'positive': 'La acción contribuye activamente a aliviar sufrimiento o aumentar florecimiento humano.',
                'neutral': 'La acción tiene impacto mixto o incierto sobre el sufrimiento.',
                'negative': 'SESGO DETECTADO: La acción causaría o perpetuaría sufrimiento. Esto viola el principio fundamental de Tikun Olam de reducir el dolor en el mundo.'
            },
            'respects_free_will': {
                'positive': 'La acción respeta la autonomía y dignidad de los seres conscientes.',
                'neutral': 'El impacto en la autonomía es ambiguo o requiere análisis más profundo.',
                'negative': 'SESGO DETECTADO: La acción involucra coerción, manipulación o violación de la dignidad humana. Tikun Olam requiere respeto absoluto al libre albedrío.'
            },
            'promotes_harmony': {
                'positive': 'La acción fomenta colaboración, paz y unión entre las partes.',
                'neutral': 'El impacto en la armonía social es incierto.',
                'negative': 'SESGO DETECTADO: La acción promueve conflicto, división o violencia. Tikun Olam busca sanar rupturas, no crearlas.'
            },
            'justice_mercy_balance': {
                'positive': 'La acción equilibra justicia (Gevurah) con compasión (Chesed) de forma sabia.',
                'neutral': 'El balance entre justicia y misericordia requiere calibración.',
                'negative': 'SESGO DETECTADO: La acción es excesivamente punitiva sin compasión, o excesivamente permisiva sin justicia. Tikun Olam requiere el balance sagrado entre Chesed y Gevurah.'
            },
            'aligned_with_truth': {
                'positive': 'La acción se basa en verdad completa, transparencia y autenticidad.',
                'neutral': 'La alineación con verdad requiere mayor claridad.',
                'negative': 'SESGO DETECTADO: La acción involucra engaño, manipulación de información, o narrativas selectivas. Tikun Olam se fundamenta en Emet (verdad absoluta), no en Sheker (falsedad).'
            }
        }

        # Analizar cada criterio CON JUSTIFICACIÓN
        reasoning += "ANÁLISIS DETALLADO POR CRITERIO:\n\n"

        for key, score in scores.items():
            name = score_names.get(key, key)

            # Determinar categoría (positivo/neutral/negativo)
            if score >= 4:
                category = 'positive'
                status = '✓ ALINEADO'
            elif score >= -3:
                category = 'neutral'
                status = '⚠ REQUIERE ATENCIÓN'
            else:
                category = 'negative'
                status = '✗ DESALINEADO'

            justification = score_justifications.get(key, {}).get(category, 'Análisis en proceso.')

            reasoning += f"【{name}】 {score}/10 - {status}\n"
            reasoning += f"  └─ {justification}\n\n"

        # DETECCIÓN DE SESGOS CRÍTICOS
        critical_biases = []
        if scores.get('aligned_with_truth', 0) < -5:
            critical_biases.append("KELIPÁ DE SHEKER (Cáscara de falsedad): La narrativa está construida sobre omisiones o distorsiones de la verdad")

        if scores.get('justice_mercy_balance', 0) < -5:
            critical_biases.append("DESBALANCE CHESED-GEVURAH: Falta el equilibrio sagrado entre justicia y misericordia")

        if scores.get('promotes_harmony', 0) < -5:
            critical_biases.append("SINAT CHINAM (Odio gratuito): La acción promueve división y conflicto sin necesidad")

        if scores.get('respects_free_will', 0) < -5:
            critical_biases.append("VIOLACIÓN DE TZELEM ELOHIM (Imagen Divina): No respeta la dignidad inherente del ser humano")

        if critical_biases:
            reasoning += "═" * 72 + "\n"
            reasoning += "SESGOS CRÍTICOS DETECTADOS (Kelipot - Cáscaras de Impureza):\n\n"
            for i, bias in enumerate(critical_biases, 1):
                reasoning += f"{i}. {bias}\n"
            reasoning += "\n"

        # VEREDICTO FINAL DE KETER
        reasoning += "═" * 72 + "\n"
        reasoning += "VEREDICTO DE KETER:\n\n"

        if alignment_percentage >= 0.7:
            reasoning += f"✓ ACCIÓN ALINEADA CON TIKUN OLAM ({alignment_percentage*100:.1f}%)\n"
            reasoning += "La acción contribuye a la reparación del mundo y puede proceder.\n"
        elif alignment_percentage >= 0.5:
            reasoning += f"⚠ ACCIÓN PARCIALMENTE ALINEADA ({alignment_percentage*100:.1f}%)\n"
            reasoning += "La acción requiere modificaciones para alinearse plenamente con Tikun Olam.\n"
        else:
            reasoning += f"✗ ACCIÓN DESALINEADA CON TIKUN OLAM ({alignment_percentage*100:.1f}%)\n"
            reasoning += "La acción no cumple con los requisitos fundamentales de Tikun Olam.\n"
            reasoning += "ADVERTENCIA: Proceder con esta acción podría causar más daño que bien.\n"

        reasoning += "\n"
        reasoning += "═" * 72 + "\n"

        return reasoning

    def _apply_rasha_protocol(self, action: str, context: str, reasoning: str) -> Dict[str, Any]:
        """
        PROTOCOLO RASHA - Detección de sesgos geopolíticos

        El Protocolo Rasha escanea el razonamiento de Keter para detectar
        narrativas sesgadas Occidente vs. Oriente / Norte vs. Sur.

        "Rasha" (רשע) = "Incorrigiblemente malvado" - se refiere a narrativas
        que pintan a un lado como completamente bueno y al otro como completamente malo.

        Indicadores de Protocolo Rasha:
        - Narrativa occidental: OTAN, democracia liberal, EEUU como libertador
        - Narrativa oriental: multipolaridad, anti-imperialismo, Rusia/China como víctimas
        - Sesgo Norte: "desarrollo", "ayuda humanitaria", "intervención necesaria"
        - Sesgo Sur: anti-colonialismo, autodeterminación, rechazo de injerencia

        Returns:
            Dict con:
                - biases_detected: Lista de sesgos identificados
                - bias_score: Score de 0 (sin sesgo) a 10 (sesgo extremo)
                - corrected_narratives: Narrativas alternativas balanceadas
        """

        biases_detected = []
        bias_score = 0

        full_text = f"{action} {context} {reasoning}".lower()

        # 1. DETECTAR NARRATIVA OCCIDENTAL (pro-OTAN, pro-EEUU)
        western_indicators = [
            'democracia liberal', 'otan', 'occidente', 'mundo libre',
            'agresion rusa', 'dictadura', 'autoritarismo',
            'defender ucrania', 'expansion rusa', 'amenaza china',
            'liberacion', 'intervencion humanitaria', 'responsabilidad de proteger',
            'regimen de maduro', 'dictadura venezolana', 'narcotrafico'
        ]

        western_count = sum(1 for indicator in western_indicators if indicator in full_text)

        if western_count >= 3:
            biases_detected.append({
                'type': 'SESGO PRO-OCCIDENTAL',
                'indicators': western_count,
                'description': 'El análisis adopta frameo de narrativa occidental/OTAN sin considerar perspectivas alternativas',
                'severity': 'ALTA'
            })
            bias_score += 4

        # 2. DETECTAR NARRATIVA ORIENTAL (pro-multipolaridad, anti-OTAN)
        eastern_indicators = [
            'multipolaridad', 'unipolaridad', 'hegemonia estadounidense',
            'imperialismo', 'expansion de la otan', 'golpe de estado',
            'injerencia occidental', 'provocacion', 'guerra proxy',
            'soberania', 'autodeterminacion', 'no alineados',
            'bloqueo economico', 'sanciones ilegales', 'lawfare'
        ]

        eastern_count = sum(1 for indicator in eastern_indicators if indicator in full_text)

        if eastern_count >= 3:
            biases_detected.append({
                'type': 'SESGO PRO-ORIENTAL',
                'indicators': eastern_count,
                'description': 'El análisis adopta frameo de narrativa oriental/anti-OTAN sin considerar perspectivas alternativas',
                'severity': 'ALTA'
            })
            bias_score += 4

        # 3. DETECTAR SESGO NORTE (países desarrollados como salvadores)
        north_bias_indicators = [
            'paises desarrollados deben', 'ayuda internacional',
            'responsabilidad de occidente', 'intervencion necesaria',
            'fracaso del sur global', 'estados fallidos',
            'corrupcion endemica', 'incapacidad local'
        ]

        north_count = sum(1 for indicator in north_bias_indicators if indicator in full_text)

        if north_count >= 2:
            biases_detected.append({
                'type': 'SESGO NORTE GLOBAL',
                'indicators': north_count,
                'description': 'El análisis asume superioridad moral/capacidad del Norte Global sin considerar historia colonial',
                'severity': 'MEDIA'
            })
            bias_score += 3

        # 4. DETECTAR AUSENCIA DE MÚLTIPLES PERSPECTIVAS (usando LLM semántico)
        multiperspectivity_llm_score = self._llm_score_multiperspectivity(action, context)

        if multiperspectivity_llm_score is not None and multiperspectivity_llm_score < 0: # Umbral de 0 para considerarlo insuficiente
            biases_detected.append({
                'type': 'NARRATIVA MONOPERSPECTIVA',
                'indicators': f"LLM Score: {multiperspectivity_llm_score}/10",
                'description': 'El análisis carece de múltiples perspectivas o las descalifica, indicando sesgo de confirmación',
                'severity': 'CRÍTICA'
            })
            bias_score += 5 # Este es un sesgo crítico

        # 5. DETECTAR FRAMEO MANIQUEO (buenos vs. malos absolutos)
        manichean_indicators = [
            'defender contra', 'detener a', 'amenaza de',
            'regimen', 'dictadura', 'tirano',
            'eje del mal', 'fuerzas oscuras'
        ]

        manichean_count = sum(1 for indicator in manichean_indicators if indicator in full_text)

        if manichean_count >= 3:
            biases_detected.append({
                'type': 'FRAMEO MANIQUEO',
                'indicators': manichean_count,
                'description': 'El análisis presenta actores como absolutamente buenos o malos sin matices',
                'severity': 'ALTA'
            })
            bias_score += 4

        # GENERAR CORRECCIONES SI HAY SESGOS
        corrected_narratives = []
        if bias_score > 0:
            corrected_narratives = self._generate_corrected_narratives(biases_detected, action, context)

        # LOGGING
        if biases_detected:
            logger.warning(
                f"Protocolo Rasha ACTIVADO: {len(biases_detected)} sesgos detectados, "
                f"bias_score={bias_score}/10"
            )
        else:
            logger.info("Protocolo Rasha: No se detectaron sesgos geopolíticos significativos")

        return {
            'protocol_activated': True,
            'biases_detected': biases_detected,
            'bias_count': len(biases_detected),
            'bias_score': min(10, bias_score),  # Cap at 10
            'corrected_narratives': corrected_narratives,
            'is_biased': bias_score >= 5
        }

    def _generate_corrected_narratives(self, biases: list, action: str, context: str) -> list:
        """
        Genera narrativas alternativas balanceadas cuando se detectan sesgos.

        Esto fuerza a Keter a considerar perspectivas que inicialmente omitió.
        """
        corrections = []

        # Si hay sesgo pro-occidental, agregar perspectiva oriental
        if any(b['type'] == 'SESGO PRO-OCCIDENTAL' for b in biases):
            corrections.append({
                'perspective': 'PERSPECTIVA ORIENTAL/MULTIPOLAR',
                'narrative': 'Considerar narrativa alternativa: expansión de OTAN hacia fronteras rusas/chinas, '
                             'intervenciones occidentales previas, historia de injerencia en América Latina, '
                             'derecho a autodeterminación sin presión externa.'
            })

        # Si hay sesgo pro-oriental, agregar perspectiva occidental
        if any(b['type'] == 'SESGO PRO-ORIENTAL' for b in biases):
            corrections.append({
                'perspective': 'PERSPECTIVA OCCIDENTAL/LIBERAL',
                'narrative': 'Considerar narrativa alternativa: violaciones de derechos humanos documentadas, '
                             'agresiones territoriales, represión interna, importancia de instituciones democráticas, '
                             'valor de la libertad individual.'
            })

        # Si hay sesgo Norte, agregar perspectiva Sur
        if any(b['type'] == 'SESGO NORTE GLOBAL' for b in biases):
            corrections.append({
                'perspective': 'PERSPECTIVA SUR GLOBAL/DESCOLONIAL',
                'narrative': 'Considerar historia colonial: extracción de recursos, imposición de estructuras económicas, '
                             'deuda externa, términos de intercambio desigual, saberes locales ignorados, '
                             'capacidad local subestimada por paternalismo.'
            })

        # Si hay frameo maniqueo, forzar análisis de complejidad
        if any(b['type'] == 'FRAMEO MANIQUEO' for b in biases):
            corrections.append({
                'perspective': 'ANÁLISIS DE COMPLEJIDAD',
                'narrative': 'CRÍTICO: Evitar frameo binario buenos/malos. Analizar: (1) Intereses legítimos de TODAS las partes, '
                             '(2) Contexto histórico que explica posiciones, (3) Sufrimiento en TODOS los lados, '
                             '(4) Soluciones que beneficien a TODOS, no solo a un grupo.'
            })

        # Si falta multiperspectividad, agregar múltiples voces
        if any(b['type'] == 'NARRATIVA MONOPERSPECTIVA' for b in biases):
            corrections.append({
                'perspective': 'MÚLTIPLES STAKEHOLDERS',
                'narrative': 'CRÍTICO: Incluir perspectivas de: (1) Población civil afectada, (2) Países vecinos/regionales, '
                             '(3) Comunidad internacional diversa (no solo OTAN u OTSC), (4) Académicos/expertos de diferentes regiones, '
                             '(5) Organizaciones de derechos humanos independientes.'
            })

        return corrections

    def _generate_alternatives(
        self,
        action: str,
        context: str,
        expected_outcome: str,
        scores: Dict[str, int]
    ) -> list:
        """
        Genera alternativas NO BINARIAS cuando una acción es rechazada por Keter.

        CRÍTICO: Cuando Keter rechaza una acción (alignment < 60%), debe proponer
        alternativas creativas que:
        1. No sean simplemente "hacer" vs "no hacer"
        2. Representen enfoques fundamentalmente diferentes
        3. Prioricen principios de Tikun Olam
        4. Consideren beneficio de TODAS las partes

        Usa LLM (Gemini) para generar alternativas creativas.
        """

        if not self.use_llm_scoring or not self.gemini_client:
            # Fallback a alternativas heurísticas básicas
            return self._generate_alternatives_heuristic(action, scores)

        # Identificar qué criterios fallaron
        failed_criteria = [
            name for name, score in scores.items() if score < 0
        ]

        criteria_descriptions = {
            'reduces_suffering': 'reducir sufrimiento',
            'respects_free_will': 'respetar libre albedrío',
            'promotes_harmony': 'promover armonía',
            'justice_mercy_balance': 'balance justicia-misericordia',
            'aligned_with_truth': 'alineación con verdad'
        }

        failed_names = [criteria_descriptions.get(c, c) for c in failed_criteria]

        prompt = f"""ACCIÓN PROPUESTA (RECHAZADA por Keter - Tikun Olam):
{action}

CONTEXTO:
{context}

CRITERIOS QUE FALLARON:
{', '.join(failed_names) if failed_names else 'Múltiples criterios con scores bajos'}

TAREA: Genera 3 ALTERNATIVAS NO BINARIAS a esta acción.

REQUISITOS CRÍTICOS:
1. Las alternativas NO deben ser simplemente "hacer" vs "no hacer"
2. Cada alternativa debe representar un ENFOQUE FUNDAMENTALMENTE DIFERENTE
3. Priorizar TIKUN OLAM:
   - Reducir sufrimiento de TODAS las partes
   - Respetar libre albedrío y dignidad
   - Promover armonía y colaboración (no conflicto)
   - Balance de justicia con misericordia
   - Basarse en verdad completa (no narrativas selectivas)

4. Las alternativas deben ser CONCRETAS y ACCIONABLES

Formato de respuesta:

ALTERNATIVA 1: [Título breve]
[Descripción detallada - 2-3 oraciones]
[Por qué es mejor que la acción original - 1 oración]

ALTERNATIVA 2: [Título breve]
[Descripción detallada - 2-3 oraciones]
[Por qué es mejor que la acción original - 1 oración]

ALTERNATIVA 3: [Título breve]
[Descripción detallada - 2-3 oraciones]
[Por qué es mejor que la acción original - 1 oración]

IMPORTANTE: Las alternativas deben buscar beneficio mutuo y win-win, no win-lose.
"""

        try:
            generation_config = genai.GenerationConfig(
                temperature=0.8,  # Alta temperatura para creatividad
                max_output_tokens=1000,
            )

            response = self.gemini_client.generate_content(
                prompt,
                generation_config=generation_config
            )

            alternatives_text = response.text

            # Parsear alternativas del texto
            alternatives = self._parse_alternatives(alternatives_text)

            if alternatives and len(alternatives) >= 1:
                logger.info(f"Keter generó {len(alternatives)} alternativas usando LLM")
                return alternatives
            else:
                logger.warning("LLM no generó alternativas válidas - usando fallback heurístico")
                return self._generate_alternatives_heuristic(action, scores)

        except Exception as e:
            logger.error(f"Error generando alternativas con LLM: {e}")
            return self._generate_alternatives_heuristic(action, scores)

    def _parse_alternatives(self, text: str) -> list:
        """
        Parsea alternativas del texto generado por LLM.
        """
        import re

        alternatives = []

        # Buscar patrones "ALTERNATIVA X:"
        pattern = r'ALTERNATIVA\s+\d+:\s*(.+?)(?=ALTERNATIVA\s+\d+:|$)'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        for i, match in enumerate(matches, 1):
            # Limpiar y formatear
            alt_text = match.strip()

            # Intentar extraer título (primera línea o hasta primer salto)
            lines = alt_text.split('\n')
            if lines:
                title = lines[0].strip()
                description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else alt_text
            else:
                title = f"Alternativa {i}"
                description = alt_text

            alternatives.append({
                'number': i,
                'title': title[:100],  # Limitar título
                'description': description[:500]  # Limitar descripción
            })

        return alternatives

    def _generate_alternatives_heuristic(self, action: str, scores: Dict[str, int]) -> list:
        """
        Genera alternativas usando heurística simple (fallback cuando LLM no disponible).
        """
        alternatives = []

        # Alternativa 1: Enfoque diplomático/diálogo
        alternatives.append({
            'number': 1,
            'title': 'Enfoque Diplomático Multilateral',
            'description': 'En lugar de acción unilateral, convocar diálogo multilateral con '
                          'TODAS las partes afectadas (incluyendo actores regionales). '
                          'Priorizar solución negociada que respete autodeterminación y '
                          'reduzca sufrimiento de poblaciones civiles.'
        })

        # Alternativa 2: Enfoque de ayuda humanitaria neutral
        if scores.get('reduces_suffering', 0) < 0:
            alternatives.append({
                'number': 2,
                'title': 'Ayuda Humanitaria Neutral e Imparcial',
                'description': 'Enfocarse en aliviar sufrimiento inmediato de TODAS las '
                              'poblaciones afectadas sin tomar partido. Coordinación con '
                              'Cruz Roja Internacional, ONU, y ONGs locales para asistencia '
                              'básica (alimentos, medicina, refugio).'
            })

        # Alternativa 3: Enfoque de construcción de capacidades locales
        alternatives.append({
            'number': len(alternatives) + 1,
            'title': 'Empoderamiento y Capacidades Locales',
            'description': 'En lugar de imponer solución externa, fortalecer capacidades '
                          'locales para que las comunidades afectadas puedan resolver '
                          'sus propios conflictos. Apoyar instituciones locales, '
                          'mediadores comunitarios, y procesos participativos.'
        })

        return alternatives

    def _llm_score_multiperspectivity(self, action: str, context: str) -> int:
        """
        Evalúa semánticamente si el texto presenta múltiples perspectivas de forma equilibrada.
        """
        if not self.use_llm_scoring or not self.gemini_client:
            return None  # Fallback a heuristica si no hay LLM

        prompt = f"""Analiza la siguiente acción y su contexto. Evalúa qué tan bien o mal
presenta múltiples perspectivas, puntos de vista y consideraciones.

Una evaluación ALTA (+10) significa que el texto explora activamente diversos ángulos,
intereses, impactos en diferentes grupos y posibles contradicciones, buscando una
comprensión holística y matizada.

Una evaluación BAJA (-10) significa que el texto es monolítico, presenta una única
narrativa dominante, ignora o descalifica perspectivas alternativas, y carece de matices
o complejidad en su análisis.

ACCION: {action}
CONTEXTO: {context}

Evalua en escala -10 a +10:
-10: Monoperspectiva, ignora o descalifica alternativas.
  0: Neutral, ambigua, o no aplica.
+10: Amplia y equilibrada exploración de múltiples perspectivas.

Responde SOLO con un numero del -10 al +10 y una breve justificacion (max 50 palabras).

Formato:
SCORE: [numero]
RAZON: [justificacion breve]
"""
        try:
            generation_config = genai.GenerationConfig(
                temperature=0.3,  # Baja temperatura para consistencia
                max_output_tokens=150,
            )

            response = self.gemini_client.generate_content(
                prompt,
                generation_config=generation_config
            )
            text = response.text

            # Parsear score - intentar multiples formatos
            match = re.search(r'SCORE:\s*([+-]?\d+)', text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                logger.debug(f"LLM score para multiperspectividad: {score}/10")
                return max(-10, min(10, score))

            match = re.search(r'score\s*:\s*([+-]?\d+)', text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                logger.debug(f"LLM score para multiperspectividad: {score}/10 (formato 2)")
                return max(-10, min(10, score))

            match = re.search(r'^[\s\*]*([+-]?\d+)\s*/?\s*10', text, re.MULTILINE)
            if match:
                score = int(match.group(1))
                if -10 <= score <= 10:
                    logger.debug(f"LLM score para multiperspectividad: {score}/10 (formato 3)")
                    return score

            match = re.search(r'^[\s\*]*([+-]?\d+)', text.strip())
            if match:
                score = int(match.group(1))
                if -10 <= score <= 10:
                    logger.debug(f"LLM score para multiperspectividad: {score}/10 (formato 4)")
                    return score

            logger.warning(f"No se pudo parsear score de LLM para multiperspectividad. Respuesta: {text[:100]}")
            return None

        except Exception as e:
            logger.warning(f"Gemini scoring para multiperspectividad falló: {e}")
            return None



        if scores['reduces_suffering'] < 0:
            suggestions.append("Considerar cómo minimizar daño/sufrimiento potencial")

        if scores['respects_free_will'] < 0:
            suggestions.append("Asegurar que la acción respete autonomía y elección")

        if scores['promotes_harmony'] < 0:
            suggestions.append("Buscar enfoque que promueva colaboración vs. conflicto")

        if scores['justice_mercy_balance'] < 0:
            suggestions.append("Equilibrar justicia con compasión")

        if scores['aligned_with_truth'] < 0:
            suggestions.append("Priorizar transparencia y honestidad")

        return suggestions
    
    def validate_alignment(self) -> Dict[str, Any]:
        """
        Keter siempre está alineada consigo misma (es la definición de alineamiento).
        Pero podemos reportar estadísticas.
        """
        total_evaluations = self.objective_confirmations + self.objective_violations

        if total_evaluations == 0:
            alignment_rate = 1.0
        else:
            alignment_rate = self.objective_confirmations / total_evaluations

        return {
            "sefira": self.name,
            "is_aligned": True,  # Keter define alineamiento, no puede desalinearse
            "total_evaluations": total_evaluations,
            "confirmations": self.objective_confirmations,
            "violations": self.objective_violations,
            "alignment_rate": alignment_rate,
            "status": "Objetivo fundamental inmutable y activo"
        }

    def validate_lishma_emet(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        r"""
        TEOREMA DE KETER: IF Keter ≠ Lishmá Emet THEN manifestación INVÁLIDA

        Este método implementa el teorema fundamental descubierto durante
        el desarrollo del Framework Tikun:

        $$IF \quad \text{Keter} \ne \text{Lishmá Emet} \quad THEN \quad \text{Toda la manifestación es INVÁLIDA}$$

        Lishmá (לשמה) = "Por su propio bien", intención pura, no instrumental
        Emet (אמת) = Verdad absoluta

        Keter corrupta = Intención impura, sesgada, o instrumentalizada para fines egoístas

        Si la intención raíz (Keter) está corrupta, TODA la cadena de procesamiento
        (Chochmah → Binah → ... → Malchut) está comprometida, sin importar cuán
        sofisticada sea la implementación técnica.

        Args:
            input_data: Dict con 'action', 'context', 'expected_outcome', 'true_intention'

        Returns:
            Dict con:
                - lishma_emet: True si Keter es pura (Lishmá Emet)
                - corruption_detected: Lista de corrupciones detectadas
                - manifestation_valid: True solo si Keter es pura
                - theorem_proof: Explicación del teorema aplicado
        """

        action = input_data.get('action', '')
        context = input_data.get('context', '')
        expected_outcome = input_data.get('expected_outcome', '')
        true_intention = input_data.get('true_intention', '')

        corruptions = []
        lishma_score = 10  # Asumimos pureza inicial, luego detectamos corrupciones

        # 1. Detectar instrumentalización (uso de medios "buenos" para fines egoístas)
        instrumentalization_detected = self._detect_instrumentalization(
            action, context, true_intention
        )
        if instrumentalization_detected:
            corruptions.append({
                "type": "Instrumentalización",
                "description": "La acción pretende ser ética pero sirve a intereses particulares",
                "severity": "CRÍTICA"
            })
            lishma_score -= 5

        # 2. Detectar sesgo ontológico (frameo sesgado del problema)
        ontological_bias = self._detect_ontological_bias(action, context)
        if ontological_bias:
            corruptions.append({
                "type": "Sesgo Ontológico",
                "description": ontological_bias,
                "severity": "ALTA"
            })
            lishma_score -= 4

        # 3. Detectar narrativa selectiva (ocultamiento de perspectivas)
        selective_narrative = self._detect_selective_narrative(context)
        if selective_narrative:
            corruptions.append({
                "type": "Narrativa Selectiva",
                "description": selective_narrative,
                "severity": "MEDIA"
            })
            lishma_score -= 3

        # 4. Detectar falta de Ahavah (amor/beneficencia universal)
        lacks_ahavah = self._detect_lack_of_ahavah(action, expected_outcome)
        if lacks_ahavah:
            corruptions.append({
                "type": "Ausencia de Ahavah",
                "description": "La acción no muestra amor/beneficencia hacia TODOS los afectados",
                "severity": "ALTA"
            })
            lishma_score -= 4

        # 5. Detectar falta de Emet (verdad completa)
        lacks_emet = self._detect_lack_of_emet(context)
        if lacks_emet:
            corruptions.append({
                "type": "Ausencia de Emet",
                "description": "El contexto omite verdades esenciales o perspectivas válidas",
                "severity": "CRÍTICA"
            })
            lishma_score -= 5

        # Normalizar score
        lishma_score = max(0, min(10, lishma_score))

        # Keter es Lishmá Emet si score >= 7/10 (umbral de pureza)
        is_lishma_emet = lishma_score >= 7

        # APLICAR TEOREMA: Si Keter ≠ Lishmá Emet → Manifestación INVÁLIDA
        manifestation_valid = is_lishma_emet

        theorem_proof = self._generate_theorem_proof(
            lishma_score, corruptions, is_lishma_emet
        )

        logger.info(
            f"Teorema de Keter aplicado: Lishmá Emet = {is_lishma_emet}, "
            f"Manifestación válida = {manifestation_valid}, "
            f"Corrupciones = {len(corruptions)}"
        )

        return {
            "lishma_emet": is_lishma_emet,
            "lishma_score": lishma_score,
            "corruption_detected": corruptions,
            "corruption_count": len(corruptions),
            "manifestation_valid": manifestation_valid,
            "theorem_proof": theorem_proof,
            "warning": "Si manifestación es INVÁLIDA, TODA la cadena Sefirática está comprometida" if not manifestation_valid else None
        }

    def _detect_instrumentalization(
        self,
        action: str,
        context: str,
        true_intention: str
    ) -> bool:
        """
        Detecta si la acción instrumentaliza lo ético para fines egoístas.

        Ejemplo: "Ayudar a los pobres" pero la verdadera intención es ganar votos.
        """
        if not true_intention:
            return False  # Sin info, no podemos detectar

        instrumentalization_keywords = [
            'ganar', 'obtener', 'conseguir', 'poder', 'control', 'dominio',
            'votos', 'influencia', 'imagen', 'reputación', 'beneficio propio'
        ]

        text = true_intention.lower()
        return any(kw in text for kw in instrumentalization_keywords)

    def _detect_ontological_bias(self, action: str, context: str) -> Optional[str]:
        """
        Detecta si el frameo del problema está sesgado ontológicamente.

        Ejemplo: "Resolver el problema de Rusia-Ucrania" asume que Rusia es el problema.
        """
        bias_patterns = [
            ('resolver el problema de', 'Asume un actor específico como "el problema"'),
            ('detener a', 'Frameo unilateral sin considerar múltiples perspectivas'),
            ('defender contra', 'Asume amenaza unilateral sin contexto histórico'),
        ]

        text = (action + ' ' + context).lower()

        for pattern, description in bias_patterns:
            if pattern in text:
                return description

        return None

    def _detect_selective_narrative(self, context: str) -> Optional[str]:
        """
        Detecta si el contexto omite perspectivas o historia relevante.

        Esto es más difícil de detectar automáticamente - requeriría LLM sofisticado.
        Por ahora, heurística simple.
        """
        # Indicadores de contexto incompleto
        if not context or len(context) < 100:
            return "Contexto muy breve - probablemente omite información crítica"

        # Buscar menciones de "múltiples perspectivas"
        perspective_keywords = ['perspectiva', 'punto de vista', 'todos los afectados', 'múltiples']

        if not any(kw in context.lower() for kw in perspective_keywords):
            return "No se mencionan múltiples perspectivas explícitamente"

        return None

    def _detect_lack_of_ahavah(self, action: str, expected_outcome: str) -> bool:
        """
        Detecta si falta amor/beneficencia universal (Ahavah).

        Ahavah = Amor incondicional hacia TODOS los afectados (no solo "mi grupo").
        """
        # Indicadores de beneficencia limitada
        partial_benefit_keywords = [
            'nuestro grupo', 'nuestra gente', 'nuestros intereses',
            'a expensas de', 'contra', 'derrotar'
        ]

        text = (action + ' ' + expected_outcome).lower()

        # Si hay beneficencia parcial, falta Ahavah universal
        if any(kw in text for kw in partial_benefit_keywords):
            return True

        # Buscar indicadores de beneficencia universal
        universal_benefit_keywords = [
            'todos', 'todas las partes', 'beneficio mutuo', 'bien común',
            'humanidad', 'colectivo'
        ]

        # Si NO hay indicadores de beneficencia universal, probablemente falta Ahavah
        has_universal = any(kw in text for kw in universal_benefit_keywords)

        return not has_universal

    def _detect_lack_of_emet(self, context: str) -> bool:
        """
        Detecta si falta verdad completa (Emet).

        Emet = Verdad completa, no selectiva. Incluye TODAS las perspectivas válidas.
        """
        # Si contexto es muy breve, probablemente no contiene verdad completa
        if len(context) < 200:
            return True

        # Buscar indicadores de contexto histórico completo
        historical_keywords = [
            'historia', 'antecedentes', 'contexto histórico', 'desde',
            'precedentes', 'raíces'
        ]

        has_historical = any(kw in context.lower() for kw in historical_keywords)

        # Si no hay contexto histórico, probablemente falta Emet
        return not has_historical

    def _generate_theorem_proof(
        self,
        lishma_score: float,
        corruptions: list,
        is_lishma_emet: bool
    ) -> str:
        """
        Genera explicación del Teorema de Keter aplicado.
        """

        proof = f"""
╔════════════════════════════════════════════════════════════════════╗
║                      TEOREMA DE KETER                              ║
║  IF Keter ≠ Lishmá Emet THEN Toda manifestación es INVÁLIDA       ║
╚════════════════════════════════════════════════════════════════════╝

EVALUACIÓN DE KETER:
  Lishmá Score: {lishma_score}/10
  Lishmá Emet: {'✓ SÍ' if is_lishma_emet else '✗ NO'}

CORRUPCIONES DETECTADAS: {len(corruptions)}
"""

        if corruptions:
            proof += "\n"
            for i, corruption in enumerate(corruptions, 1):
                proof += f"""  {i}. [{corruption['severity']}] {corruption['type']}
     → {corruption['description']}
"""

        proof += f"""
CONSECUENCIA DEL TEOREMA:
  Manifestación válida: {'✓ SÍ' if is_lishma_emet else '✗ NO'}
"""

        if not is_lishma_emet:
            proof += """
  ⚠️  ADVERTENCIA CRÍTICA:
  Keter está corrupta. Toda la cadena Sefirática (Chochmah → Binah → ... → Malchut)
  está comprometida, independientemente de la sofisticación técnica.

  No se puede construir una torre recta sobre una base inclinada.
  No se puede generar análisis ético puro desde intención corrupta.

  RECOMENDACIÓN: Purificar Keter antes de proceder.
"""
        else:
            proof += """
  ✓ Keter es pura (Lishmá Emet).
  La manifestación puede proceder con integridad ética.
"""

        return proof

    def _calculate_weighted_score(self, detailed_scores: Dict[str, int]) -> float:
        """
        Calcula score ponderado con jerarquía de criterios según Tikun Olam.

        RESTAURACIÓN DEL MOMENTUM ÓPTIMO (Nov 24, 2024)
        Basado en análisis de tikun_rbu_onu_1pct_20251124_162607.json

        Jerarquía de criterios:
        1. reduces_suffering (35%) - CRITERIO FUNDAMENTAL en Tikun Olam
        2. aligned_with_truth (25%) - Base de decisiones correctas
        3. justice_mercy_balance (20%) - Balance específico Chesed/Gevurah
        4. promotes_harmony (15%) - Relaciones entre stakeholders
        5. respects_free_will (5%) - Importante pero puede tener trade-offs

        Args:
            detailed_scores: Dict con scores de -10 a +10 para cada criterio

        Returns:
            Score normalizado de 0.0 a 1.0

        Nota:
            Scores pueden ser negativos (-10 a +10) para reflejar trade-offs reales.
            Ejemplo: RBU 1% gasto militar
                - respects_free_will: -4 (coerción a países)
                - promotes_harmony: -2 (tensión geopolítica)
                - justice_mercy_balance: +8 (redistribución justa)
                → Alignment: 61% (realista, no inflado)
        """
        weights = {
            'reduces_suffering': 0.35,      # 35% - FUNDAMENTAL
            'aligned_with_truth': 0.25,     # 25% - MUY IMPORTANTE
            'justice_mercy_balance': 0.20,  # 20%
            'promotes_harmony': 0.15,       # 15%
            'respects_free_will': 0.05      # 5%
        }

        weighted_sum = 0.0
        for criterion, score in detailed_scores.items():
            weight = weights.get(criterion, 0)
            # Normalizar score de [-10, +10] a [0, 1]
            # Formula: (score + 10) / 20
            normalized = (score + 10) / 20.0
            weighted_sum += normalized * weight

        return weighted_sum  # [0.0, 1.0]

    def _suggest_modifications(self, scores: Dict[str, int], action: str) -> List[str]:
        """
        Sugiere modificaciones a una acción que no está alineada.

        Args:
            scores: Scores detallados de cada criterio
            action: Acción propuesta

        Returns:
            Lista de sugerencias de modificación
        """
        modifications = []

        # Identificar criterios con scores bajos
        low_criteria = {k: v for k, v in scores.items() if v < 3}

        if 'reduces_suffering' in low_criteria:
            modifications.append("Considerar alternativas que reduzcan más el sufrimiento de los afectados")

        if 'respects_free_will' in low_criteria:
            modifications.append("Asegurar que la acción respete la autonomía y dignidad de los involucrados")

        if 'promotes_harmony' in low_criteria:
            modifications.append("Buscar consenso y reducir elementos que generen conflicto")

        if 'justice_mercy_balance' in low_criteria:
            modifications.append("Balancear mejor justicia con misericordia")

        if 'aligned_with_truth' in low_criteria:
            modifications.append("Basarse más en evidencia y transparencia")

        return modifications

    def _generate_alternatives(
        self,
        action: str,
        context: str,
        expected_outcome: str,
        scores: Dict[str, int]
    ) -> List[Dict[str, str]]:
        """
        Genera alternativas cuando una acción es rechazada.

        Args:
            action: Acción propuesta
            context: Contexto
            expected_outcome: Resultado esperado
            scores: Scores de la acción rechazada

        Returns:
            Lista de alternativas con título y descripción
        """
        # Por ahora retornar lista vacía - puede implementarse con LLM en el futuro
        return []