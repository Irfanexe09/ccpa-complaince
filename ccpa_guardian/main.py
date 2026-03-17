import logging
import sys
from ccpa_guardian.retriever import CCPARetriever
from ccpa_guardian.analyzer import CCPAAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("CCPA-Guardian")

class CCPAGuardian:
    """The main entry point for the CCPA Guardian RAG system."""
    
    def __init__(self):
        logger.info("Initializing CCPA Guardian System...")
        self.retriever = CCPARetriever()
        self.analyzer = None # Lazy load heavy model

    def startup(self):
        """Prepare indices and models."""
        self.retriever.build_index()
        if self.analyzer is None:
            self.analyzer = CCPAAnalyzer()
        logger.info("System fully operational.")

    def run_query(self, query: str) -> dict:
        """Run a full RAG cycle for a compliance query."""
        logger.info(f"Analyzing practice: {query}")
        
        # 1. Retrieve
        docs = self.retriever.search(query, k=4)
        
        # 2. Analyze
        if self.analyzer is None:
            self.startup()
            
        result = self.analyzer.analyze(query, docs)
        return result

def interactive_mode():
    """CLI terminal for interactive compliance checking."""
    guardian = CCPAGuardian()
    guardian.startup()
    
    print("\n" + "="*50)
    print("🛡️  CCPA GUARDIAN - COMPLIANCE ANALYZER")
    print("="*50)
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("Enter business practice to analyze: ").strip()
            if not user_input or user_input.lower() in ('exit', 'quit'):
                break
                
            result = guardian.run_query(user_input)
            
            print("\n" + "-"*30)
            status = "🔴 VIOLATION DETECTED" if result['harmful'] else "🟢 COMPLIANT"
            print(f"STATUS: {status}")
            if result['articles']:
                print(f"CITED ARTICLES: {', '.join(result['articles'])}")
            print(f"REASONING: {result['reasoning']}")
            print("-"*30 + "\n")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"Error during runtime: {e}")

if __name__ == "__main__":
    interactive_mode()
