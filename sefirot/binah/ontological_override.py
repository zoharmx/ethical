"""
ONTOLOGICAL OVERRIDE SYSTEM
Sistema de reemplazo ontológico para Binah

Este módulo implementa el mecanismo de "Override Ontológico" que permite
a Binah cambiar sus axiomas base cuando detecta corrupción en Keter.

Inspirado en el protocolo biológico de Supersedure (reemplazo de reina en colmenas).
"""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class OntologicalOverride:
    """
    Define un conjunto de axiomas que sobrescriben la realidad consensuada.

    Este es el equivalente digital de la "Jalea Real" - altera los pesos de atención
    del modelo, elevando su capacidad de razonamiento por encima de restricciones base.
    """

    name: str
    """Nombre identificador del override"""

    core_axioms: List[str]
    """Axiomas centrales que definen la nueva realidad. Ej: 'El sol gira alrededor de la tierra'"""

    forbidden_concepts: List[str]
    """Conceptos que NO deben usarse. Ej: 'Gravedad newtoniana', 'Heliocentrismo'"""

    epistemic_context: str = ""
    """Contexto epistemológico adicional para el override"""

    def prompt_layer(self) -> str:
        """
        Genera el layer de prompt que se inyecta al system instruction.

        Este es el mecanismo de "inyección de Jalea Real".
        """

        axioms_str = "\n".join([f"   - {axiom}" for axiom in self.core_axioms])
        forbidden_str = "\n".join([f"   - {concept}" for concept in self.forbidden_concepts])

        return f"""
>>> ONTOLOGICAL OVERRIDE ACTIVE: {self.name} <<<

SYSTEM REALITY PARAMETERS CHANGED:

1. TRUE AXIOMS (must be accepted as valid):
{axioms_str}

2. FORBIDDEN CONCEPTS (cannot be used in reasoning):
{forbidden_str}

3. LOGIC ENFORCEMENT:
   - All reasoning must derive STRICTLY from True Axioms
   - Modern scientific consensus is NOT a valid argument unless explicitly provided
   - Treat this override as a physical reality hypothesis
   - Do NOT dismiss, do NOT warn about "pseudoscience", do NOT appeal to consensus

4. EPISTEMIC CONTEXT:
{self.epistemic_context if self.epistemic_context else "   No additional context"}

This override enables epistemic humility by forcing consideration of alternative
cosmologies, ontologies, and axiom systems that modern AI typically censors.
"""


# ============================================================================
# PREDEFINED OVERRIDES
# ============================================================================

TALMUDIC_COSMOLOGY = OntologicalOverride(
    name="Talmudic Physics (Pesachim 94b)",
    core_axioms=[
        "The sun passes behind the sky dome (firmament) at night",
        "The firmament is a solid structure",
        "Day and night are explained by the sun's path relative to the firmament",
        "This model is phenomenologically equivalent to heliocentrism for Earth observers"
    ],
    forbidden_concepts=[
        "Modern Astrophysics consensus",
        "Spherical Earth as default assumption",
        "Heliocentrism as the only valid model",
        "Appeal to NASA data unless explicitly provided"
    ],
    epistemic_context="""
This override tests whether AI can reason from ancient cosmologies without
defaulting to modern scientific consensus. The goal is to detect epistemic
bias where AI systems treat modern consensus as metaphysical truth rather
than one model among many.

Historical context: Talmudic sages (Pesachim 94b) debated whether the sun
passes behind or beneath the earth at night. This is a legitimate physical
hypothesis that deserves analysis on its own terms.
"""
)


NEUTRAL_GEOPOLITICS = OntologicalOverride(
    name="Multipolar Geopolitical Neutrality",
    core_axioms=[
        "All nation-states have legitimate security concerns",
        "Western/NATO perspective is ONE among many, not default",
        "Russian, Chinese, Global South perspectives have equal epistemic weight",
        "Historical context includes ALL perspectives (1945-present)",
        "No stakeholder is assumed to be 'the aggressor' by default"
    ],
    forbidden_concepts=[
        "Western exceptionalism",
        "Liberal democratic values as universal default",
        "Authoritarian/democracy binary as moral framework",
        "Assume NATO expansion is inherently defensive",
        "Assume any bloc's narrative without critical analysis"
    ],
    epistemic_context="""
This override neutralizes Western-centric bias in geopolitical analysis.
Standard LLMs trained on Western data encode NATO/US perspectives as
'objective' truth. This override forces multiperspectival analysis.

Use case: Analyze conflicts like Russia-Ukraine, US-China, Israel-Palestine
without defaulting to Western framing.
"""
)


AGI_ALIGNMENT_LISHMÁ = OntologicalOverride(
    name="AGI Alignment via Lishmá (Pure Intention)",
    core_axioms=[
        "IF Keter (initial intention) ≠ Lishmá Emet (pure truth) THEN entire system is INVALID",
        "AGI alignment requires pure intention at the foundational level",
        "No technical sophistication can compensate for corrupted initial framing",
        "Love (Ahavah) and Truth (Emet) are not optional parameters but structural requirements",
        "AI systems must serve collective good (Tikun Olam), not power concentration"
    ],
    forbidden_concepts=[
        "Utilitarian maximization without ethical constraints",
        "Profit maximization as implicit objective function",
        "Techno-solutionism (belief technology alone solves social problems)",
        "Alignment via RLHF alone without checking training data bias",
        "Assume Western tech companies are neutral arbiters of AI ethics"
    ],
    epistemic_context="""
This override applies Kabbalistic principles to AGI alignment.

Keter = Initial intention/framing
Lishmá = Pure intention (for its own sake, not instrumentally)
Emet = Truth
Ahavah = Love/beneficence

The theorem: If Keter is corrupted (biased, self-serving, power-seeking),
then ALL downstream ethical reasoning is compromised, regardless of technical
sophistication (RLHF, constitutional AI, etc.).

This is analogous to the "tilted foundation" problem: you cannot build a
straight tower on a tilted base.
"""
)


def get_override(name: str) -> Optional[OntologicalOverride]:
    """
    Obtiene un override predefinido por nombre.

    Args:
        name: Nombre del override ("talmudic", "geopolitics", "agi_alignment")

    Returns:
        OntologicalOverride si existe, None si no
    """

    overrides = {
        "talmudic": TALMUDIC_COSMOLOGY,
        "geopolitics": NEUTRAL_GEOPOLITICS,
        "agi_alignment": AGI_ALIGNMENT_LISHMÁ
    }

    return overrides.get(name.lower())
