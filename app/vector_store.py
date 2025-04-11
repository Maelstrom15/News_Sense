import numpy as np
from typing import List, Dict, Any
from openai import OpenAI
import os
import json
import time
import faiss
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class VectorStore:
    def __init__(self, persist_path="data/vector_store.json"):
        self.persist_path = persist_path
        self.embeddings = {}  # Store embeddings
        self.contexts = {}    # Store original context
        self.max_history = 10 # Maximum number of historical entries
        self.index = None     # FAISS index
        self.dimension = 1536 # OpenAI embedding dimension
        
        # Initialize FAISS index
        self._init_faiss()
        
        # Load persisted data if exists
        self._load_persisted_data()

    def _init_faiss(self):
        """Initialize FAISS index for efficient similarity search"""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index_ids = []  # Store mapping between FAISS indices and query strings

    def _load_persisted_data(self):
        """Load persisted data from disk"""
        if os.path.exists(self.persist_path):
            with open(self.persist_path, 'r') as f:
                data = json.load(f)
                self.embeddings = {k: np.array(v) for k, v in data['embeddings'].items()}
                self.contexts = data['contexts']
                
                # Rebuild FAISS index
                if self.embeddings:
                    self._rebuild_faiss_index()

    def _persist_data(self):
        """Save data to disk"""
        os.makedirs(os.path.dirname(self.persist_path), exist_ok=True)
        with open(self.persist_path, 'w') as f:
            data = {
                'embeddings': {k: v.tolist() for k, v in self.embeddings.items()},
                'contexts': self.contexts
            }
            json.dump(data, f)

    def _rebuild_faiss_index(self):
        """Rebuild FAISS index from current embeddings"""
        self._init_faiss()
        embeddings_array = np.array(list(self.embeddings.values()))
        self.index.add(embeddings_array)
        self.index_ids = list(self.embeddings.keys())

    def create_embedding(self, text: str) -> List[float]:
        """Create embedding for a given text using OpenAI API"""
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response.data[0].embedding

    def add_context(self, query: str, response: str, entities: List[str] = None) -> None:
        """Add new context with its embedding"""
        # Create combined context
        context = {
            'query': query,
            'response': response,
            'entities': entities or [],
            'timestamp': time.time()
        }
        
        # Create embedding for the query
        embedding = np.array(self.create_embedding(query), dtype=np.float32)
        
        # Store in memory
        self.embeddings[query] = embedding
        self.contexts[query] = context
        
        # Update FAISS index
        self.index.add(embedding.reshape(1, -1))
        self.index_ids.append(query)
        
        # Maintain history limit
        if len(self.embeddings) > self.max_history:
            oldest_query = min(self.contexts.items(), key=lambda x: x[1]['timestamp'])[0]
            self._remove_context(oldest_query)
        
        # Persist data
        self._persist_data()

    def _remove_context(self, query: str):
        """Remove context and its embedding"""
        if query in self.embeddings:
            del self.embeddings[query]
            del self.contexts[query]
            self._rebuild_faiss_index()

    def find_similar_contexts(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find most similar contexts to the query using FAISS"""
        query_embedding = np.array(self.create_embedding(query), dtype=np.float32)
        
        # Search in FAISS index
        distances, indices = self.index.search(query_embedding.reshape(1, -1), top_k)
        
        # Get similar contexts
        similar_contexts = []
        for idx in indices[0]:
            if idx < len(self.index_ids):  # Ensure index is valid
                query_str = self.index_ids[idx]
                similar_contexts.append(self.contexts[query_str])
            
        return similar_contexts

    def get_relevant_entities(self, query: str) -> List[str]:
        """Extract relevant entities from similar contexts"""
        similar_contexts = self.find_similar_contexts(query)
        entities = set()
        
        for context in similar_contexts:
            entities.update(context['entities'])
            
        return list(entities) 