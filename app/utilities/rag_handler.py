import os
import logging
import warnings
from utilities.config import HUGGINGFACE_ACCESS_TOKEN
from embedchain import App
import re

os.environ["HUGGINGFACE_ACCESS_TOKEN"] = HUGGINGFACE_ACCESS_TOKEN

class RAGHandler:
    _instance = None
    
    def __new__(cls, model_config):
        if cls._instance is None:
            cls._instance = super(RAGHandler, cls).__new__(cls)
            cls._instance._rag_app = App.from_config(model_config)
        return cls._instance

    @property
    def rag_app(self):
        """Get RAG app."""
        return self._rag_app
    
    def get_rag_response(self,question) -> str:
        """Get response from RAG model."""
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=FutureWarning)
                response = self.rag_app.query(question)
                pattern = r'Answer:(.*)'
                match = re.search(pattern, response, re.DOTALL)
                if match:
                    extracted_text = match.group(1).strip()
                    logging.info("Extracted text: ", extracted_text)
                return extracted_text
        except Exception as e:
            logging.exception("Unexpected error occurred when checking unseen emails.")
            return ({"detail": " An unexpected error occurred, " + str(e)}) 
        
    def add_rag_source(self, path: str, data_type):
        """Add source to RAG model."""
        if data_type == "json":
            self.rag_app.add(path)
        else:
            self.rag_app.add(path, data_type)

        return {"detail": "Source added successfully."} 