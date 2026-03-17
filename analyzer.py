import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import re
import os

from config import MODEL_ID

class CCPA_Analyzer:
    def __init__(self, model_id=MODEL_ID):
        self.model_id = model_id
        # Force CPU — MPS on Mac can fail when disk is full (scratch files)
        self.device = "cpu"
        # Only use CUDA if explicitly available (for Linux/Docker GPU servers)
        if torch.cuda.is_available():
            self.device = "cuda"
        print(f"Loading model {model_id} on {self.device}...")

        hf_token = os.getenv("HF_TOKEN")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token)
        
        dtype = torch.bfloat16 if self.device == "cuda" else torch.float32
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=dtype,
            token=hf_token
        ).to(self.device)
        self.model.eval()

    def analyze(self, practice_description: str, relevant_articles: list) -> dict:
        # Build a concise, targeted context from the top 3 articles
        law_context = "\n".join([
            f"{doc.metadata['section_id']}: {doc.page_content[:200]}"
            for doc in relevant_articles[:3]
        ])
        
        system_msg = "You are a CCPA compliance expert. Respond ONLY with valid JSON."
        
        user_msg = f"""Does this violate CCPA? Practice: {practice_description[:400]}

Relevant law:
{law_context}

Reply with ONLY: {{"harmful": true, "articles": ["Section XXXX.XXX"]}} or {{"harmful": false, "articles": []}}"""

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=1400)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_new_tokens=80,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        new_tokens = output_ids[0][inputs["input_ids"].shape[1]:]
        raw_output = self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        
        print(f"[Analyzer] Raw: {raw_output!r}")
        
        try:
            json_match = re.search(r'\{[^{}]*\}', raw_output, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
            else:
                result = json.loads(raw_output)
            
            harmful = bool(result.get("harmful", False))
            articles = [str(a) for a in result.get("articles", [])]
            
            # Strict enforcement per validate_format.py rules
            if not harmful:
                articles = []
            elif harmful and not articles:
                harmful = False
                
            return {"harmful": harmful, "articles": articles}
            
        except Exception as e:
            print(f"[Analyzer] Parse error: {e}\nRaw: {raw_output!r}")
            return {"harmful": False, "articles": []}


if __name__ == "__main__":
    print("Analyzer module. Requires model weights to run.")
