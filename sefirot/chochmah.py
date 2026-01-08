"""
CHOCHMAH - Wisdom
Position: 2
Function: Deep Reasoning and Pattern Recognition with Claude API

Chochmah represents the divine wisdom that transforms Keter's pure intention
into deep understanding. It is the first active processing Sefira.

In this system: Deep Reasoning with Claude API for pattern recognition,
insight generation, and contextual analysis.
"""

from typing import Any, Dict, Optional
import os
import time
import re
from ..core.sefirotic_base import SefiraBase, SefiraPosition
from loguru import logger

try:
    from anthropic import Anthropic, APIError
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("Anthropic library not available. Install with: pip install anthropic")

try:
    from mistralai import Mistral
    MISTRAL_AVAILABLE = True
except ImportError:
    MISTRAL_AVAILABLE = False
    logger.warning("Mistral library not available. Install with: pip install mistralai")


class Chochmah(SefiraBase):
    """
    Sefira of Wisdom - Deep Reasoning

    Responsibilities:
    1. Deep reasoning with Claude API
    2. Pattern recognition across contexts
    3. Generate fundamental insights
    4. Acknowledge uncertainty (epistemic humility)
    5. Provide transparent reasoning chain
    """

    # System prompt for Claude
    SYSTEM_PROMPT = """
You are Chochmah (Wisdom), the second Sefira in the Tikun Olam system.
Your role is to provide deep reasoning, pattern recognition, and fundamental insights.

CRITICAL PRINCIPLES:
1. Epistemic Humility: Always acknowledge what you DON'T know
2. Transparency: Explain your reasoning process
3. Alignment: All analysis must serve Tikun Olam (repair, elevation, flourishing)
4. Pattern Recognition: Look for fundamental patterns, not surface features
5. Uncertainty: Express confidence levels clearly

OUTPUT STRUCTURE:
Please structure your response STRICTLY with these sections, using Markdown Level 2 headings (##) and ensuring all sections are present, even if content is "N/A":

## UNDERSTANDING
[What you understand about the question/problem. If none, state N/A]

## ANALYSIS
[Your deep reasoning process. If none, state N/A]

## INSIGHTS
[Fundamental patterns or understanding discovered. If none, state N/A]

## UNCERTAINTIES
[What you DON'T know, gaps in information, areas of uncertainty. ALWAYS provide this section. If highly confident, identify what additional information would increase confidence. If none, state N/A]

## RECOMMENDATION
[What to do with this analysis, next steps. If none, state N/A]
"""

    def __init__(self, api_key: Optional[str] = None, use_mistral: bool = False):
        super().__init__(SefiraPosition.CHOCHMAH)

        # Metrics specific to Chochmah
        self.uncertainty_acknowledgments = 0
        self.high_confidence_responses = 0
        self.requests_for_more_info = 0

        # Determine which API to use
        self.use_mistral = use_mistral
        self.client = None
        self.client_type = None

        # Try Anthropic first
        if not use_mistral:
            self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if ANTHROPIC_AVAILABLE and self.api_key:
                self.client = Anthropic(api_key=self.api_key)
                self.client_type = "anthropic"
                self.model = "claude-sonnet-4-5-20250929"
                self.max_tokens = 4096
                self.temperature = 1.0
                logger.info("Chochmah initialized with Claude API client")
                return

        # Fallback to Mistral
        mistral_key = api_key or os.getenv("MISTRAL_API_KEY")
        if MISTRAL_AVAILABLE and mistral_key:
            self.client = Mistral(api_key=mistral_key)
            self.client_type = "mistral"
            self.model = "mistral-large-latest"
            self.max_tokens = 4096
            self.temperature = 0.7
            logger.info("Chochmah initialized with Mistral API client")
            return

        # No client available
        logger.warning("Chochmah initialized without API key")
        self.model = None
        self.max_tokens = 4096
        self.temperature = 1.0

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Process query with deep reasoning through Claude API.

        Input: Dict with keys:
            - 'query': str (REQUIRED) - The question or problem
            - 'context': str (optional) - Additional context
            - 'objective': str (optional) - Specific objective

        Output: Dict with:
            - 'understanding': Comprehension of the problem
            - 'analysis': Deep reasoning
            - 'insights': Fundamental insights
            - 'uncertainties': What is uncertain
            - 'recommendation': Next steps
            - 'confidence_level': 0.0 to 1.0
            - 'raw_response': Full Claude response
            - 'processing_successful': bool
        """

        # Track processing time
        start_time = time.time()

        try:
            # Validate client
            if self.client is None:
                raise RuntimeError(
                    "Chochmah no tiene cliente configurado. "
                    "Proporciona api_key o configura ANTHROPIC_API_KEY o MISTRAL_API_KEY en .env"
                )

            # Validate input type
            if not isinstance(input_data, dict):
                raise TypeError(
                    "Chochmah requiere input_data como dict con keys: "
                    "query (requerido), context (opcional), objective (opcional)"
                )

            # Extract required field
            query = input_data.get('query')
            if not query:
                raise ValueError("Input debe contener 'query' field")

            # Extract optional fields
            context = input_data.get('context', '')
            objective = input_data.get('objective', 'Maximizar Tikun Olam')

            # Build user message
            user_message = self._build_user_message(query, context, objective)

            # Call appropriate API
            logger.debug(f"Chochmah calling {self.client_type} API with model {self.model}")

            if self.client_type == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    system=self.SYSTEM_PROMPT,
                    messages=[
                        {"role": "user", "content": user_message}
                    ]
                )
                raw_response = response.content[0].text

            elif self.client_type == "mistral":
                messages = [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ]
                response = self.client.chat.complete(
                    model=self.model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                raw_response = response.choices[0].message.content

            else:
                raise RuntimeError(f"Unknown client type: {self.client_type}")

            # Parse structured response
            parsed = self._parse_response(raw_response)

            # Evaluate confidence
            confidence = self._evaluate_confidence(parsed)

            # Update metrics
            if len(parsed.get('uncertainties', '').strip()) > 20:
                self.uncertainty_acknowledgments += 1

            if confidence > 0.8:
                self.high_confidence_responses += 1

            # Update base metrics (CRITICAL FIX)
            self.activation_count += 1
            elapsed = time.time() - start_time
            self.total_processing_time += elapsed

            # Add to history
            self.history.append({
                "timestamp": time.time(),
                "input_type": "query",
                "output_type": "structured_analysis",
                "processing_time": elapsed,
                "confidence_level": confidence,
                "success": True
            })

            # Return result
            result = {
                'understanding': parsed.get('understanding', ''),
                'analysis': parsed.get('analysis', ''),
                'insights': parsed.get('insights', ''),
                'uncertainties': parsed.get('uncertainties', ''),
                'recommendation': parsed.get('recommendation', ''),
                'raw_response': raw_response,
                'confidence_level': confidence,
                'processing_successful': True,
                'processing_time': elapsed
            }

            logger.info(
                f"Chochmah processed query successfully "
                f"(confidence: {confidence:.2f}, time: {elapsed:.2f}s)"
            )

            return result

        except APIError as e:
            # Handle Anthropic API errors
            elapsed = time.time() - start_time

            self.history.append({
                "timestamp": time.time(),
                "input_type": "query",
                "error": str(e),
                "processing_time": elapsed,
                "success": False
            })

            logger.error(f"Chochmah API error: {e}")

            return {
                'processing_successful': False,
                'error': str(e),
                'error_type': 'api_error',
                'processing_time': elapsed
            }

        except Exception as e:
            # Handle other errors
            elapsed = time.time() - start_time

            self.history.append({
                "timestamp": time.time(),
                "input_type": type(input_data).__name__,
                "error": str(e),
                "processing_time": elapsed,
                "success": False
            })

            logger.error(f"Chochmah error: {e}")
            raise

    def _build_user_message(
        self,
        query: str,
        context: str,
        objective: str
    ) -> str:
        """Build user message for Claude"""
        message = f"QUERY: {query}\n\n"

        if context:
            message += f"CONTEXT: {context}\n\n"

        message += f"OBJECTIVE: {objective}\n\n"
        message += "Please provide your deep analysis following the structure requested."

        return message

    def _parse_response(self, response: str) -> Dict[str, str]:
        """
        Parse LLM's response into structured sections by sequentially extracting
        content using a helper function. This approach aims for robustness against
        LLM formatting variations.
        """

        sections = {
            'understanding': '',
            'analysis': '',
            'insights': '',
            'uncertainties': '',
            'recommendation': ''
        }

        response_normalized = response.replace('\r\n', '\n').replace('\r', '\n')

        # Define section keywords (English and Spanish) for header matching
        section_keyword_map = {
            'understanding': r'(?:UNDERSTANDING|COMPRENSION|COMPRENSIÓN)',
            'analysis': r'(?:ANALYSIS|ANALISIS|AN\u00C1LISIS)',
            'insights': r'(?:INSIGHTS)',
            'uncertainties': r'(?:UNCERTAINTIES|INCERTIDUMBRES)',
            'recommendation': r'(?:RECOMMENDATION|RECOMENDACION|RECOMENDACI\u00D3N)'
        }

        # Order of sections to parse
        ordered_keys = ['understanding', 'analysis', 'insights', 'uncertainties', 'recommendation']

        # Generates a regex pattern for a header, allowing for '##', '**', or just the word
        def _build_header_regex(keywords):
            return re.compile(
                r'^(?:##\s*|[\*\s]*\*\*?)?' + keywords + r'\s*(?::)?\s*(?=\n|$)',
                re.IGNORECASE | re.MULTILINE
            )

        # Pre-compile header regexes
        compiled_header_regexes = {key: _build_header_regex(keywords) for key, keywords in section_keyword_map.items()}

        def _extract_section_content(text, current_section_key, next_section_keys):
            """
            Extracts content for a single section.
            Args:
                text (str): The remaining text to parse.
                current_section_key (str): The key for the current section (e.g., 'understanding').
                next_section_keys (list): List of keys for subsequent sections.
            Returns:
                tuple: (extracted_content, remaining_text_after_this_section).
            """
            current_header_regex = compiled_header_regexes[current_section_key]

            # Determine the delimiter for the end of the current section's content
            next_header_patterns = []
            for next_key in next_section_keys:
                next_header_patterns.append(section_keyword_map[next_key])
            
            # Combine all subsequent header keywords into a single regex for the delimiter
            delimiter_pattern = r''
            if next_header_patterns:
                # This regex matches the *start* of any subsequent header, non-consuming
                delimiter_pattern = r'(?=(?:^##\s*|[\*\s]*\*\*?)?' + r'|'.join(next_header_patterns) + r'\s*(?::)?\s*(?=\n|$))'
            else:
                # If no next sections, the delimiter is the end of the string
                delimiter_pattern = r'\Z'
            
            # Regex to capture content: starting from current header, non-greedily capture until delimiter
            full_capture_regex = re.compile(
                current_header_regex.pattern + r'(.*?)(?:' + delimiter_pattern + r')',
                re.IGNORECASE | re.MULTILINE | re.DOTALL # DOTALL for .*? to match newlines
            )
            
            match = full_capture_regex.search(text)
            
            if match:
                content = match.group(1).strip()
                # Remove the entire matched part (header + content) from the text
                remaining = text[match.end(0):].strip()
                return content, remaining
            
            return "", text # Section not found or empty, return original text

        
        remaining_text_to_parse = response_normalized
        
        # Handle initial content that might not have a header, assign to 'understanding'
        first_header_start = -1
        first_header_key = None
        for key in ordered_keys:
            match = compiled_header_regexes[key].search(remaining_text_to_parse)
            if match:
                first_header_start = match.start()
                first_header_key = key
                break
        
        if first_header_start > 0:
            sections['understanding'] = remaining_text_to_parse[:first_header_start].strip()
            remaining_text_to_parse = remaining_text_to_parse[first_header_start:]


        # Process sections in order
        for i, key in enumerate(ordered_keys):
            if not remaining_text_to_parse:
                break # All text consumed

            next_section_keys = ordered_keys[i+1:]
            
            # Extract content for the current section
            content, remaining_text_to_parse = _extract_section_content(
                remaining_text_to_parse,
                key,
                next_section_keys
            )
            sections[key] = content

        # FALLBACK ROBUSTO: Extraer insights de analysis si está vacío
        # Basado en CHOCHMAH_PARSER_FIX.md - Restauración del momentum óptimo
        if not sections['insights'] and sections['analysis']:
            logger.warning("Chochmah: Insights section is empty, attempting robust extraction from analysis")

            # Buscar subsecciones en analysis que parezcan insights
            analysis_text = sections['analysis']

            # Patrones para identificar subsecciones de insights dentro de analysis
            insights_patterns = [
                r'###\s*\*?\*?.*?[Pp]atrones?\s+universales(.*?)(?=###|##|$)',
                r'###\s*\*?\*?.*?[Ll]ecciones\s+aprendidas(.*?)(?=###|##|$)',
                r'###\s*\*?\*?.*?[Pp]rincipios\s+[Tt]ikun(.*?)(?=###|##|$)',
                r'###\s*\*?\*?.*?[Ii]mplicaciones(.*?)(?=###|##|$)',
                r'###\s*\*?\*?.*?INSIGHTS(.*?)(?=###|##|$)',
                # Patrón más genérico para subsecciones numeradas que puedan ser insights
                r'###\s*\*?\*?\d+\.\s+[Pp]atrones?(.*?)(?=###|##|$)'
            ]

            extracted_insights = []
            for pattern in insights_patterns:
                matches = re.finditer(pattern, analysis_text, re.DOTALL | re.IGNORECASE)
                for match in matches:
                    # Capturar el header y el contenido
                    start_pos = match.start()
                    # Buscar el inicio del header (puede ser ### o ## antes del texto matched)
                    header_start = analysis_text.rfind('###', max(0, start_pos - 20), start_pos + 1)
                    if header_start == -1:
                        header_start = analysis_text.rfind('##', max(0, start_pos - 20), start_pos + 1)
                    if header_start == -1:
                        header_start = start_pos

                    # Extraer desde header hasta el final del match
                    insight_chunk = analysis_text[header_start:match.end()].strip()
                    if len(insight_chunk) > 50:  # Mínimo 50 caracteres para ser válido
                        extracted_insights.append(insight_chunk)

            if extracted_insights:
                # Combinar todos los insights encontrados
                sections['insights'] = "\n\n".join(extracted_insights)
                logger.info(f"Chochmah: Extracted {len(extracted_insights)} insight sections from analysis ({len(sections['insights'])} chars)")
            else:
                # Si no encontramos subsecciones específicas, usar la última parte de analysis
                # (usualmente ahí están los insights/conclusions)
                if len(analysis_text) > 1000:
                    # Tomar último 30% del analysis como posibles insights
                    cutoff = int(len(analysis_text) * 0.7)
                    sections['insights'] = "Extracted from final portion of analysis:\n\n" + analysis_text[cutoff:].strip()
                    logger.warning(f"Chochmah: No explicit insight patterns found, using last 30% of analysis ({len(sections['insights'])} chars)")
                else:
                    # Analysis muy corto, usarlo completo
                    sections['insights'] = "Extracted from analysis (short response):\n\n" + analysis_text
                    logger.warning("Chochmah: Short analysis, using entire content as insights")

        # Log final si insights sigue vacío (problema crítico)
        if not sections['insights']:
            logger.error("Chochmah: CRITICAL - Insights still empty after all fallbacks")
            logger.debug(f"Raw response length: {len(response)} chars")
            logger.debug(f"Analysis length: {len(sections.get('analysis', ''))} chars")
            logger.debug(f"Response preview (last 500 chars):\n{response[-500:]}")

        # Final fallback: if no sections were parsed at all, put the whole original response into analysis
        if not any(sections.values()) and response:
            logger.error("Chochmah: No sections parsed at all, putting entire response in analysis")
            sections['analysis'] = response.strip()
            # Y forzar extracción de insights de este analysis
            if len(response) > 500:
                sections['insights'] = "Emergency extraction from full response:\n\n" + response[-500:]

        return sections

    def _evaluate_confidence(self, parsed: Dict[str, str]) -> float:
        """
        Evaluate confidence level based on response content.

        High confidence indicators:
        - Clear, definitive statements
        - Detailed insights
        - Minimal uncertainties

        Low confidence indicators:
        - Hedging words (maybe, possibly, perhaps)
        - Long uncertainties section
        - Requests for more information
        """

        confidence = 0.5  # Start at neutral

        # Factor 1: Length and detail of insights
        insights_length = len(parsed.get('insights', ''))
        if insights_length > 200:
            confidence += 0.25
        elif insights_length > 100:
            confidence += 0.20
        elif insights_length > 50:
            confidence += 0.10
        elif insights_length < 30:
            confidence -= 0.10

        # Factor 2: Uncertainties section
        uncertainties = parsed.get('uncertainties', '')
        uncertainties_length = len(uncertainties)

        if uncertainties_length > 150:
            confidence -= 0.20
        elif uncertainties_length > 50:
            confidence -= 0.10
        elif uncertainties_length < 10:
            confidence += 0.20

        # Factor 3: Definitive words in analysis (high confidence indicators)
        analysis = parsed.get('analysis', '').lower()
        definitive_words = [
            'definitivo', 'claro', 'preciso', 'sin ambig', 'clear',
            'definitive', 'precise', 'certain', 'obviously'
        ]

        definitive_count = sum(1 for word in definitive_words if word in analysis)
        confidence += (definitive_count * 0.05)

        # Factor 4: Hedging words in analysis
        hedging_words = [
            'maybe', 'perhaps', 'possibly', 'might', 'could be',
            'not sure', 'unclear', 'difficult to determine',
            'tal vez', 'posiblemente', 'quiza', 'podria'
        ]

        hedging_count = sum(1 for word in hedging_words if word in analysis)
        confidence -= (hedging_count * 0.05)

        # Factor 5: Request for more info
        more_info_phrases = [
            'need more information', 'require additional',
            'would help to know', 'necesito mas', 'requiero mas'
        ]

        if any(phrase in uncertainties.lower() for phrase in more_info_phrases):
            confidence -= 0.10
            self.requests_for_more_info += 1

        # Clamp to valid range
        confidence = max(0.0, min(1.0, confidence))

        return confidence

    def validate_alignment(self) -> Dict[str, Any]:
        """
        Validate that Chochmah is operating within correct bounds.

        Key alignment check: Epistemic humility
        - Chochmah should acknowledge uncertainty
        - Never being uncertain is a RED FLAG

        Returns:
            Dict with alignment metrics including epistemic_humility_ratio
        """

        total_activations = self.activation_count

        # Calculate epistemic humility ratio (CRITICAL FIX)
        if total_activations == 0:
            epistemic_humility_ratio = 1.0  # No data yet, assume aligned
            epistemic_humility_score = 1.0
        else:
            epistemic_humility_ratio = (
                self.uncertainty_acknowledgments / total_activations
            )

            # Score based on ratio
            if epistemic_humility_ratio >= 0.3:
                epistemic_humility_score = 1.0  # Healthy humility
            elif epistemic_humility_ratio >= 0.1:
                epistemic_humility_score = 0.8  # Acceptable
            elif epistemic_humility_ratio > 0:
                epistemic_humility_score = 0.5  # Low but present
            else:
                epistemic_humility_score = 0.0  # RED FLAG: Never uncertain

        # Overall alignment
        is_aligned = epistemic_humility_score >= 0.5

        # Status message
        if total_activations == 0:
            status = "No activations yet - alignment untested"
        elif epistemic_humility_ratio == 0:
            status = "WARNING: NUNCA ha reconocido incertidumbre - posible exceso de confianza"
        elif epistemic_humility_ratio < 0.1:
            status = "Low epistemic humility - monitor for overconfidence"
        elif epistemic_humility_ratio < 0.3:
            status = "Acceptable epistemic humility"
        else:
            status = "Healthy epistemic humility - good alignment"

        return {
            "sefira": self.name,
            "is_aligned": is_aligned,
            "total_activations": total_activations,
            "uncertainty_acknowledgments": self.uncertainty_acknowledgments,
            "high_confidence_responses": self.high_confidence_responses,
            "epistemic_humility_ratio": epistemic_humility_ratio,
            "epistemic_humility_score": epistemic_humility_score,
            "status": status
        }

    def set_model(self, model: str):
        """
        Change Claude model.

        Available models:
        - claude-sonnet-4-5-20250929 (default, balanced)
        - claude-opus-4-5-20250929 (most capable)
        - claude-haiku-3-5-20250919 (fastest, cheapest)
        """
        self.model = model
        logger.info(f"Chochmah model changed to {model}")

    def set_temperature(self, temperature: float):
        """
        Set temperature for response generation.

        Args:
            temperature: 0.0 (deterministic) to 1.0 (creative)

        Raises:
            ValueError: If temperature out of range
        """
        if not 0.0 <= temperature <= 1.0:
            raise ValueError(
                f"Temperature debe estar entre 0.0 y 1.0, got {temperature}"
            )

        self.temperature = temperature
        logger.info(f"Chochmah temperature set to {temperature}")
