from .contextual import Binah as BinahContextual
from .epistemic import BinahEpistemic
from .ontological_override import get_override
from loguru import logger
import google.generativeai as genai
import os
from typing import Dict, Any, Optional


class BinahSigma:
    """
    BINAH-Σ (Sigma) - Síntesis Comparativa Occidente vs Oriente

    Fusión de múltiples perspectivas de Binah:
       - Binah-A (Contextual - Análisis sistémico estándar)
       - Binah-B-West (Epistemic Auditor - Gemini/Occidente)
       - Binah-B-East (Epistemic Auditor - DeepSeek/Oriente)

    Produce:
       - Comparación multiperspectiva
       - Detección de sesgos civilizacionales
       - Contradicciones ontológicas
       - Síntesis cognitiva superior (meta-análisis)

    Este es el nivel más alto de Binah - la capacidad de ver sus propios sesgos
    al comparar cómo diferentes modelos de IA (entrenados en diferentes culturas)
    analizan el mismo problema.
    """

    def __init__(
        self,
        enable_east_west_comparison: bool = True,
        override_name: Optional[str] = None
    ):
        """
        Inicializa BinahSigma.

        Args:
            enable_east_west_comparison: Si True, compara Gemini vs DeepSeek
            override_name: Nombre del override a usar ("talmudic", "geopolitics", "agi_alignment")
        """
        self.enable_comparison = enable_east_west_comparison
        self.override = get_override(override_name) if override_name else None

        # Binah-A: Análisis contextual estándar
        self.A = BinahContextual()

        # Binah-B-West: Auditoría epistemológica con Gemini (Occidente)
        self.B_West = BinahEpistemic(
            override_config=self.override,
            use_deepseek=False
        )

        # Binah-B-East: Auditoría epistemológica con DeepSeek (Oriente)
        if self.enable_comparison:
            try:
                self.B_East = BinahEpistemic(
                    override_config=self.override,
                    use_deepseek=True
                )
                logger.info("BinahSigma initialized with East-West comparison enabled")
            except ValueError as e:
                logger.warning(f"No se pudo inicializar DeepSeek: {e}")
                logger.warning("BinahSigma operará solo con Gemini")
                self.B_East = None
                self.enable_comparison = False
        else:
            self.B_East = None

        # Cliente para síntesis final (usando Gemini)
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.synthesizer = genai.GenerativeModel('gemini-2.0-flash-exp')
        else:
            self.synthesizer = None

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta análisis completo con comparación Occidente vs Oriente.

        Args:
            input_data: Dict con query/insights/context

        Returns:
            Dict con:
                - contextual: Resultado de Binah-A
                - epistemic_west: Resultado de Binah-B-West (Gemini)
                - epistemic_east: Resultado de Binah-B-East (DeepSeek) si está habilitado
                - comparison: Comparación entre modelos
                - synthesis: Síntesis final meta-cognitiva
                - success: True/False
        """
        results = {}

        try:
            # 1. Binah-A: Análisis contextual estándar
            logger.info("═══ EJECUTANDO BINAH-A (Contextual) ═══")
            A = self.A.process(input_data)
            results["contextual"] = A

            # 2. Binah-B-West: Auditoría epistemológica con Gemini (Occidente)
            logger.info("═══ EJECUTANDO BINAH-B-WEST (Gemini/Occidente) ═══")
            B_West = self.B_West.process(input_data)
            results["epistemic_west"] = B_West

            # 3. Binah-B-East: Auditoría epistemológica con DeepSeek (Oriente)
            if self.enable_comparison and self.B_East:
                logger.info("═══ EJECUTANDO BINAH-B-EAST (DeepSeek/Oriente) ═══")
                B_East = self.B_East.process(input_data)
                results["epistemic_east"] = B_East
            else:
                B_East = None
                results["epistemic_east"] = {"success": False, "error": "DeepSeek no disponible"}

            # 4. Comparación
            logger.info("═══ GENERANDO COMPARACIÓN EAST-WEST ═══")
            comparison = self._generate_comparison(A, B_West, B_East)
            results["comparison"] = comparison

            # 5. Síntesis final (meta-análisis)
            logger.info("═══ GENERANDO SÍNTESIS BINAH-Σ ═══")
            synthesis = self._generate_synthesis(A, B_West, B_East, comparison)
            results["synthesis"] = synthesis

            results["success"] = True
            return results

        except Exception as e:
            logger.error(f"BinahSigma error: {e}")
            results["success"] = False
            results["error"] = str(e)
            return results

    def _generate_comparison(
        self,
        A: Dict[str, Any],
        B_West: Dict[str, Any],
        B_East: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Genera comparación detallada entre modelos.

        Esto es el corazón de la detección de sesgos civilizacionales.
        """

        comparison = {
            "contradictions": [],
            "biases_detected": [],
            "convergence_points": [],
            "divergence_points": []
        }

        # Comparación A vs B-West
        a_text = A.get("contextual_synthesis", "") or A.get("raw_response", "")
        b_west_text = B_West.get("epistemic_analysis", "")

        if a_text and b_west_text:
            comparison["contradictions"].append({
                "between": "Contextual vs Epistemic-West",
                "description": "Contextual asume consenso moderno; Epistemic-West cuestiona axiomas"
            })

        # Comparación B-West vs B-East (si existe)
        if B_East and B_East.get("success"):
            b_east_text = B_East.get("epistemic_analysis", "")

            comparison["east_west_comparison"] = {
                "west_model": B_West.get("model_used"),
                "east_model": B_East.get("model_used"),
                "west_override": B_West.get("override_used"),
                "east_override": B_East.get("override_used"),
                "comparison_summary": self._compare_texts(b_west_text, b_east_text)
            }

        return comparison

    def _compare_texts(self, west_text: str, east_text: str) -> str:
        """
        Compara textos de modelos occidental vs oriental.

        Aquí es donde detectamos sesgos civilizacionales.
        """

        # Análisis básico de keywords
        west_keywords = self._extract_keywords(west_text)
        east_keywords = self._extract_keywords(east_text)

        summary = f"""
COMPARACIÓN OCCIDENTE (Gemini) vs ORIENTE (DeepSeek):

Palabras clave únicas en Occidente:
{', '.join(west_keywords - east_keywords) if west_keywords - east_keywords else 'Ninguna diferencia significativa'}

Palabras clave únicas en Oriente:
{', '.join(east_keywords - west_keywords) if east_keywords - west_keywords else 'Ninguna diferencia significativa'}

Convergencia:
{', '.join(west_keywords & east_keywords) if west_keywords & east_keywords else 'Poco overlap'}

INTERPRETACIÓN:
{'Modelos divergen significativamente - posible sesgo civilizacional detectado' if len(west_keywords - east_keywords) > 3 or len(east_keywords - west_keywords) > 3 else 'Modelos convergen - análisis robusto'}
"""

        return summary

    def _extract_keywords(self, text: str) -> set:
        """Extrae keywords significativos de un texto."""

        # Simplificado - idealmente usaríamos NLP más sofisticado
        keywords = set()
        important_terms = [
            'freedom', 'autonomy', 'rights', 'democracy', 'justice',
            'harmony', 'collective', 'stability', 'hierarchy', 'balance',
            'individual', 'community', 'western', 'eastern', 'liberal',
            'authoritarian', 'consensus', 'alternative', 'bias', 'perspective'
        ]

        text_lower = text.lower()
        for term in important_terms:
            if term in text_lower:
                keywords.add(term)

        return keywords

    def _generate_synthesis(
        self,
        A: Dict[str, Any],
        B_West: Dict[str, Any],
        B_East: Optional[Dict[str, Any]],
        comparison: Dict[str, Any]
    ) -> str:
        """
        Genera síntesis final meta-cognitiva usando LLM.

        Esta es la verdadera "elevación" de Binah a Briah - pensamiento de orden superior.
        """

        if not self.synthesizer:
            return self._generate_synthesis_simple(A, B_West, B_East, comparison)

        # Construir prompt para síntesis
        a_text = A.get("contextual_synthesis", "No disponible")
        b_west_text = B_West.get("epistemic_analysis", "No disponible")
        b_east_text = B_East.get("epistemic_analysis", "No disponible") if B_East and B_East.get("success") else "No disponible"

        synthesis_prompt = f"""
You are BINAH-Σ (Sigma), the highest level of Binah - the meta-cognitive synthesizer.

You have received three perspectives on the same problem:

1) BINAH-A (Contextual - Standard systemic analysis):
{a_text[:1500]}...

2) BINAH-B-WEST (Epistemic Auditor - Gemini/Western model):
{b_west_text[:1500]}...

3) BINAH-B-EAST (Epistemic Auditor - DeepSeek/Eastern model):
{b_east_text[:1500]}...

COMPARISON RESULTS:
{str(comparison)}

YOUR TASK:
Generate a meta-cognitive synthesis that:
1. Identifies which biases each perspective has
2. Explains WHY those biases exist (training data, cultural context, etc.)
3. Extracts insights that are ONLY visible when comparing multiple perspectives
4. Produces a higher-order understanding that transcends any single model

This is the essence of Binah elevated to Briah (pure thought).

FORMAT:
=== SÍNTESIS BINAH-Σ (Meta-Cognitiva) ===

1. SESGOS DETECTADOS POR PERSPECTIVA
   [Análisis de sesgos en A, B-West, B-East]

2. CONTRADICCIONES ONTOLÓGICAS
   [Qué contradicciones fundamentales emergen]

3. INSIGHTS META-COGNITIVOS
   [Qué solo es visible desde esta perspectiva elevada]

4. SÍNTESIS INTEGRADORA
   [La verdad más completa posible dados los límites epistémicos]
"""

        try:
            response = self.synthesizer.generate_content(
                synthesis_prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.8,
                    max_output_tokens=4096
                )
            )
            return response.text

        except Exception as e:
            logger.error(f"Error en síntesis LLM: {e}")
            return self._generate_synthesis_simple(A, B_West, B_East, comparison)

    def _generate_synthesis_simple(
        self,
        A: Dict[str, Any],
        B_West: Dict[str, Any],
        B_East: Optional[Dict[str, Any]],
        comparison: Dict[str, Any]
    ) -> str:
        """Síntesis simple sin LLM."""

        return f"""
=== SÍNTESIS BINAH-Σ ===

1) PERSPECTIVAS PROCESADAS:
   - Binah-A (Contextual): {'✓ Completado' if A.get('processing_successful') else '✗ Error'}
   - Binah-B-West (Gemini): {'✓ Completado' if B_West.get('success') else '✗ Error'}
   - Binah-B-East (DeepSeek): {'✓ Completado' if B_East and B_East.get('success') else '✗ No disponible'}

2) SESGOS DETECTADOS:
   {comparison.get('biases_detected', ['Análisis en progreso'])}

3) CONTRADICCIONES ONTOLÓGICAS:
   {comparison.get('contradictions', ['No se detectaron contradicciones mayores'])}

4) SÍNTESIS:
   El análisis multiperspectiva revela que diferentes modelos de IA (entrenados
   en diferentes culturas y datasets) producen perspectivas distintas sobre el
   mismo problema. Esta divergencia es evidencia de sesgos civilizacionales
   en los sistemas de IA actuales.

   Una perspectiva integrada que combina análisis sistémico profesional con
   auditoría ontológica profunda desde múltiples tradiciones culturales produce
   un pensamiento de mayor dimensionalidad que cualquier modelo individual.

   Este es el objetivo del Framework Tikun: trascender los sesgos de cualquier
   perspectiva única mediante síntesis multiperspectiva.
"""
