# CCPA Guardian: Intelligent Privacy Compliance
### 🛡️ Developed with ❤️ by Quantum Coders (First Year B.Tech Students)

Hello! We are **Quantum Coders**. For this hackathon, we set out to solve a real-world problem: making the complex California Consumer Privacy Act (CCPA) understandable for everyone. We built **CCPA Guardian**—an AI assistant that doesn't just guess, it actually *reasons* using the rule of law.

---

## 💡 Our Approach: "Retrieval-Augmented Reasoning"
We quickly realized that most AI chatbots tend to "hallucinate" legal advice. To fix this, we built a **RAG (Retrieval-Augmented Generation)** pipeline. 

### How we built the "Brain":
1.  **Digital Librarian**: We processed the official 65-page CCPA statute into a searchable FAISS vector database.
2.  **Contextual Search**: When you ask a question, our system acts like a librarian—it finds the 5 most relevant legal sections first before the AI even looks at it.
3.  **Expert Analysis**: We use the **Qwen-2.5-1.5B-Instruct** model to read those exact sections and your practice description.
4.  **Proof in Citations**: If our system finds a violation, it doesn't just say "No"—it gives you the specific **Section ID** (e.g., Section 1798.100) so you can verify the truth yourself.

---

## 🚀 Deployment Guide (For Evaluators)

We’ve fully containerized the system so you can get it running in a single step.

### 1. Run the Multi-Platform Container
Our image is optimized for both Mac and Windows/Linux. 
```bash
# Simply paste your HF_TOKEN to start the engine
docker run -p 8000:8000 -e HF_TOKEN=<here> mregamerz/ccpa-compliance:latest
```

### 2. Experience the Dashboard
Once the "System Ready" message appears, open your browser and go to your local host:
👉 **[http://localhost:8000](http://localhost:8000)**
*We built a sleek, modern UI for you to test prompts visually!*

### 3. Rapid API Testing (JSON Response)
If you prefer the terminal, you can get a raw JSON response (compliant with `validate_format.py`) using these commands:

#### Mac / Linux:
```bash
curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d '{"prompt": "We sell email addresses of 13-year-olds to toy brands without permission."}'
```

#### Windows (PowerShell):
```powershell
Invoke-RestMethod -Uri http://localhost:8000/analyze -Method Post -ContentType "application/json" -Body '{"prompt": "We sell email addresses of 13-year-olds to toy brands without permission."}'
```

---

## 🛠️ The Under-the-Hood Details

### 🌍 Environment Variables
- `HF_TOKEN`: (Optional for Qwen) Your Hugging Face access token for model authentication.
- `IS_DOCKER`: Automatically set inside the container to handle file paths dynamically.

### 💻 Hardware & GPU
- **GPU Support**: Fully CUDA-compatible! It will automatically detect your NVIDIA GPU for lightning-fast inference.
- **CPU Fallback**: We optimized the system to run smoothly on CPUs as well, so it works on any evaluator's machine.
- **VRAM**: Minimum 4GB-8GB recommended for best performance.

### � Local Setup (Fallback Instructions)
If you need to run the code without Docker:
1.  **Python 3.10+** is required.
2.  Install our dependencies: `pip install -r requirements.txt`
3.  Launch the server: `python3 main.py`
4.  Test it: Access `http://localhost:8000/health` to confirm the engine is warm.

---

### 📝 Technical Stack Highlights
- **FastAPI**: Used for its insane performance and automatic validation.
- **Eager Loading**: We pre-initialize the legal index and AI weights at startup (200ms health-check response!).
- **FAISS & LangChain**: Our engine for high-speed vector retrieval.

*Built with passion, late-night coding, and a lot of coffee during the **IISC OPENHACK 2026**.*
