# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional, List
import os
import google.generativeai as genai
from ..core.sefirotic_base import SefiraBase, SefiraPosition
from loguru import logger
from datetime import datetime

class Malchut(SefiraBase):
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(SefiraPosition.MALCHUT)
        
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("Malchut sin API key")
            self.client = None
        else:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel("gemini-2.0-flash-exp")
            logger.info("Malchut initialized")
        
        self.temperature = 0.5
        self.max_output_tokens = 4096
        
        self.actions_executed = 0
        self.results_achieved = 0
        self.world_updates_made = 0
        self.responsibilities_assigned = 0
        self.manifestations_completed = 0
        self.cycles_completed = 0
    
    def process(self, input_data: Any) -> Dict[str, Any]:
        logger.debug("MALCHUT - Manifestando")
        self.activation_count += 1
        
        if not self.client:
            return self._error_response("No Gemini client")
        
        try:
            prompt = self._build_prompt(input_data)
            response = self._call_gemini(prompt)
            result = self._parse_response(response, input_data)
            
            result["completion_percentage"] = 0.75
            result["manifestation_complete"] = True
            result["processing_successful"] = True
            
            self.actions_executed += len(result.get("actions_executed", []))
            self.results_achieved += 1
            self.world_updates_made += 1
            self.responsibilities_assigned += len(result.get("responsibilities_assigned", {}))
            self.manifestations_completed += 1
            
            logger.info(f"Malchut manifested: {len(result.get('actions_executed', []))} actions")
            return result
        except Exception as e:
            logger.error(f"Malchut error: {e}")
            return self._error_response(str(e))
    
    def _build_prompt(self, input_data: Dict[str, Any]) -> str:
        steps = input_data.get("first_concrete_steps", [])
        readiness = input_data.get("manifestation_readiness", 0.0)
        action = input_data.get("action", "Action")
        
        return f"""Eres Malchut - Reino y Manifestacion.

Tu funcion: EJECUTAR acciones concretas en el mundo real.

CONTEXTO:
Accion: {action}
Readiness: {readiness*100:.1f}%
Pasos preparados: {len(steps)}

TAREA:
1. Lista las acciones EJECUTADAS (verbos pasado: "Se selecciono...")
2. Describe resultados TANGIBLES logrados
3. Explica como cambio el MUNDO (antes vs despues)
4. Asigna RESPONSABILIDADES (quien hace que)
5. Reflexion SHABBAT (celebrar lo completado)

Estructura tu respuesta con secciones claras.
"""
    
    def _call_gemini(self, prompt: str) -> str:
        response = self.client.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
            )
        )
        return response.text
    
    def _parse_response(self, response: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        import re
        
        result = {
            "actions_executed": [],
            "results_achieved": {"description": response[:500]},
            "world_updated": {"description": response[: 300]},
            "responsibilities_assigned": {},
            "next_actions": [],
            "shabbat_reflection": {"full_text": response[:500]},
            "raw_response": response
        }
        
        # Parse actions
        action_pattern = r"^[\-\*\d\.]+\s*(.+)$"
        for line in response.split("\n")[:15]:
            match = re.match(action_pattern, line.strip())
            if match and len(match.group(1)) > 10:
                result["actions_executed"].append({
                    "action": match.group(1)[:150],
                    "status": "COMPLETED",
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
        
        # Parse responsibilities  
        resp_pattern = r"([A-Za-z\s]+):\s*(.+)"
        for match in re.finditer(resp_pattern, response):
            person = match.group(1).strip()
            resp = match.group(2).strip()[:150]
            if 3 < len(person) < 30 and len(resp) > 10:
                result["responsibilities_assigned"][person] = resp
        
        # Next cycle
        result["next_cycle_input"] = {
            "ready_for_keter": True,
            "new_context": "Mundo actualizado",
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        return {
            "processing_successful": False,
            "error": error_msg,
            "actions_executed": [],
            "results_achieved": {},
            "world_updated": {},
            "responsibilities_assigned": {},
            "manifestation_complete": False,
            "completion_percentage": 0.0
        }
    
    def validate_alignment(self) -> Dict[str, Any]:
        executes = self.actions_executed > 0
        achieves = self.results_achieved > 0
        updates = self.world_updates_made > 0
        assigns = self.responsibilities_assigned > 0
        
        is_aligned = all([executes, achieves, updates, assigns])
        
        return {
            "is_aligned": is_aligned,
            "executes_actions": executes,
            "achieves_results": achieves,
            "updates_world": updates,
            "assigns_responsibility": assigns,
            "total_activations": self.activation_count,
            "total_actions_executed": self.actions_executed,
            "total_manifestations": self.manifestations_completed,
            "status": "Malchut alineada" if is_aligned else "Malchut requiere calibracion"
        }
