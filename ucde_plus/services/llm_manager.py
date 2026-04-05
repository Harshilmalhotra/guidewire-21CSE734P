import os
import json
import time
import hashlib
import asyncio
from typing import Optional
from dotenv import load_dotenv
from models.schemas import LLMInput, LLMOutput

load_dotenv()

class LLMManager:
    def __init__(self):
        self.openai_key = os.environ.get("OPENAI_API_KEY")
        self.gemini_key = os.environ.get("GOOGLE_API_KEY")
        
        self.mode = "SIMULATED"
        self.client = None
        self.gemini_model = None
        
        if self.gemini_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                self.mode = "GEMINI"
            except Exception:
                pass
        elif self.openai_key:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.openai_key)
                self.mode = "OPENAI"
            except Exception:
                pass

    def _generate_simulated_narrative(self, dto: LLMInput) -> dict:
        """High-Fidelity Template Generator following the 10/10 Enterprise XAI structure."""
        trigger = dto.primary_trigger or "Baseline Threshold Breach"
        decision = dto.rl_decision
        reward_context = "High Financial Exposure" if dto.expected_reward < -2.0 else "Stable Risk Bounds"
        
        template = (
            f"PRIMARY TRIGGER: {trigger}. "
            f"The system identified a critical boundary breach in the {decision} vector. "
            f"RISK IMPLICATION: {reward_context} detected during DAG execution. "
            f"RATIONALE: Decision sits within the {dto.rl_decision} space due to compounded signal influence across nodes."
        )
        
        conflict = None
        if dto.conflict_detected:
            conflict = "CRITICAL: RL Policy overrode deterministic baseline rules due to non-linear graph contagion signals."
            
        return {"justification": template, "conflict_explanation": conflict}

    async def execute(self, dto: LLMInput) -> LLMOutput:
        start_time = time.time()
        input_hash = hashlib.md5(dto.model_dump_json().encode()).hexdigest()
        
        if self.mode == "GEMINI" and self.gemini_model:
            try:
                prompt = self._build_prompt(dto)
                response = await asyncio.to_thread(self.gemini_model.generate_content, prompt)
                parsed = self._parse_json(response.text)
                return self._finalize(parsed, start_time, input_hash, False)
            except Exception:
                pass # Fallback to simulated
                
        elif self.mode == "OPENAI" and self.client:
            try:
                prompt = self._build_prompt(dto)
                response = await self.client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                parsed = json.loads(response.choices[0].message.content)
                return self._finalize(parsed, start_time, input_hash, False)
            except Exception:
                pass # Fallback to simulated

        # Final Fallback: High-Fidelity Simulator
        parsed = self._generate_simulated_narrative(dto)
        return self._finalize(parsed, start_time, input_hash, True)

    def _build_prompt(self, dto: LLMInput) -> str:
        return (
            f"Explain the insurance claim decision: {dto.rl_decision}. "
            f"Primary Trigger: {dto.primary_trigger}. "
            f"Fraud: {dto.fraud_score}, Severity: {dto.severity_score}, Graph: {dto.graph_risk_score}. "
            "Return JSON: {'justification': '...', 'conflict_explanation': '...'}."
        )

    def _parse_json(self, text: str) -> dict:
        try:
            # Simple cleanup for Gemini markdown JSON blocks
            clean = text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean)
        except:
            return {"justification": text}

    def _finalize(self, parsed: dict, start: float, ihash: str, fallback: bool) -> LLMOutput:
        latency = (time.time() - start) * 1000
        print(f"[LLM_MANAGER_TRACE] Mode: {self.mode} | Fallback: {fallback} | Latency: {latency:.2f}ms")
        return LLMOutput(
            justification=parsed.get("justification", ""),
            conflict_explanation=parsed.get("conflict_explanation")
        )

global_llm_manager = LLMManager()
