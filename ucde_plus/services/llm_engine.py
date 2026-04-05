import os
import json
import time
import hashlib
import asyncio
from models.schemas import LLMInput, LLMOutput

def emit_llm_log(input_hash: str, latency_ms: float, tokens_used: int, fallback_used: bool):
    log_entry = {
        "agent": "LLMExplanationAgent",
        "version": "v1",
        "prompt_version": "p1",
        "input_hash": input_hash,
        "model": "gpt-4-turbo",
        "latency_ms": round(latency_ms, 2),
        "tokens_used": tokens_used,
        "fallback_used": fallback_used
    }
    print(f"[LLM_AGENT_TRACE] {json.dumps(log_entry)}")

class LLMExplanationAgent:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        
        if self.api_key:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                self.client = None
        else:
            self.client = None
            
        self.timeout_s = 0.500 # Strict 500ms operational bounds
        self.max_tokens = 150
        
    def _deterministic_stub(self, dto: LLMInput) -> dict:
        j_text = f"Fraud score {round(dto.fraud_score, 2)} and graph risk {round(dto.graph_risk_score, 2)} led to {dto.rl_decision}."
        c_text = None
        if dto.conflict_detected:
            c_text = "Baseline rules contradicted advanced topological graph findings. RL Engine arbitrated successfully."
        return {"justification": j_text, "conflict_explanation": c_text}

    async def execute(self, dto: LLMInput) -> LLMOutput:
        start_time = time.time()
        input_hash = hashlib.md5(dto.model_dump_json().encode()).hexdigest()
        
        async def call_openai():
            if not self.client:
                raise Exception("Missing API Key triggers graceful deterministic degradation blocks.")
                
            prompt = (
                f"Explain the insurance claim decision: {dto.rl_decision}. "
                f"Fraud: {dto.fraud_score}, Severity: {dto.severity_score}, Graph Risk: {dto.graph_risk_score}. "
                f"Baseline was {dto.baseline_decision}. "
                "Keep under 300 characters. Return structured JSON with 'justification' and 'conflict_explanation' (or null if no conflict)."
            )
            
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "system", "content": "You are a deterministic system explaining scoring models. Return JSON."},
                          {"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=self.max_tokens,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            tokens = response.usage.total_tokens
            parsed = json.loads(content)
            
            if len(parsed.get('justification', '')) > 300:
                raise ValueError("Justification exceeded 300 character boundary limit.")
                
            return parsed, tokens
            
        try:
            parsed_data, tokens = await asyncio.wait_for(call_openai(), timeout=self.timeout_s)
            fallback = False
        except Exception:
            parsed_data = self._deterministic_stub(dto)
            tokens = 0
            fallback = True
            
        emit_llm_log(input_hash, (time.time() - start_time) * 1000, tokens, fallback)
        
        return LLMOutput(
            justification=parsed_data.get("justification", ""),
            conflict_explanation=parsed_data.get("conflict_explanation")
        )
