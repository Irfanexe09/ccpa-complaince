import torch
import json
import re
import logging
from transformers import AutoTokenizer, AutoModelForCausalLM
from ccpa_guardian.config import MODEL_ID, HF_TOKEN

logger = logging.getLogger(__name__)

class CCPAAnalyzer:
    """LLM engine for compliance analysis and JSON output enforcement."""
    
    def __init__(self, model_id: str = MODEL_ID):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing analyzer on {self.device} using model {model_id}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)
        
        dtype = torch.bfloat16 if self.device == "cuda" else torch.float32
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=dtype,
            token=HF_TOKEN
        ).to(self.device)
        
        self.model.eval()

    def analyze(self, practice_description: str, context_docs: list) -> dict:
        """Analyzes a practice against CCPA context and returns structured JSON."""
        
        # Construct context from retrieved documents
        law_context = "\n".join([
            f"{doc.metadata.get('section_id', 'Unknown')}: {doc.page_content[:300]}"
            for doc in context_docs[:3]
        ])
        
        system_prompt = "You are a CCPA compliance bot. Analyze the practice based ONLY on the provided law. Respond ONLY in JSON."
        
        user_prompt = f"""Is this business practice a CCPA violation?
 PRACTICE: {practice_description}

 RELEVANT LAW:
 {law_context}

 REQUIRED JSON FORMAT:
 {{
   "harmful": boolean,
   "articles": ["Section XXXX.XXX"],
   "reasoning": "brief explanation"
 }}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Apply chat template if available
        input_text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response_text = self.tokenizer.decode(
            output_ids[0][inputs["input_ids"].shape[1]:], 
            skip_special_tokens=True
        ).strip()
        
        logger.debug(f"Raw model response: {response_text}")
        return self._parse_json_safely(response_text)

    def _parse_json_safely(self, text: str) -> dict:
        """Extracts and validates JSON from model output."""
        try:
            # Try to find JSON block
            match = re.search(r'\{.*\}', text, re.DOTALL)
            json_str = match.group(0) if match else text
            result = json.loads(json_str)
            
            # Enforcement of requirements
            harmful = bool(result.get("harmful", False))
            articles = result.get("articles", [])
            
            # Basic validation
            if harmful and not articles:
                # If claimed harmful but no articles cited, return neutral
                return {"harmful": False, "articles": [], "reasoning": "Inconclusive"}
            
            return {
                "harmful": harmful,
                "articles": articles if harmful else [],
                "reasoning": result.get("reasoning", "No reasoning provided")
            }
        except Exception as e:
            logger.error(f"JSON Parse Error: {e} | Raw text: {text}")
            return {"harmful": False, "articles": [], "reasoning": "Failed to parse model output"}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("Analyzer ready.")
