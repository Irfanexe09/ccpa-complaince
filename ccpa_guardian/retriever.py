import os
import logging
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from ccpa_guardian.ingest import StatuteIngestor
from ccpa_guardian.config import FAISS_INDEX_PATH, EMBEDDING_MODEL

logger = logging.getLogger(__name__)

class CCPARetriever:
    """FAISS indexing and similarity search for CCPA sections."""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.vector_store = None
        self.index_path = FAISS_INDEX_PATH

    def build_index(self, force: bool = False):
        """Builds or loads the FAISS index."""
        if not force and os.path.exists(self.index_path):
            logger.info(f"Loading existing index from {self.index_path}")
            self.vector_store = FAISS.load_local(
                str(self.index_path), 
                self.embeddings,
                allow_dangerous_deserialization=True # Required for loading local pickle files
            )
            return

        logger.info("Building new FAISS index...")
        ingestor = StatuteIngestor()
        sections = ingestor.extract_text()
        
        texts = [s['content'] for s in sections]
        metadatas = [{"section_id": s['id']} for s in sections]
        
        self.vector_store = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        
        # Save the index for future use
        self.vector_store.save_local(str(self.index_path))
        logger.info(f"Index saved to {self.index_path}")

    def search(self, query: str, k: int = 3) -> List:
        """Similarity search for relevant CCPA sections."""
        if not self.vector_store:
            self.build_index()
        
        logger.info(f"Searching for: {query}")
        docs = self.vector_store.similarity_search(query, k=k)
        return docs

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    retriever = CCPARetriever()
    retriever.build_index()
    results = retriever.search("user right to delete data")
    for doc in results:
        print(f"[{doc.metadata.get('section_id')}] {doc.page_content[:100]}...")
