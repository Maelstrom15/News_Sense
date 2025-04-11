import unittest
from app.vector_store import VectorStore
import numpy as np

class TestVectorStore(unittest.TestCase):
    def setUp(self):
        self.vector_store = VectorStore()
        # Add some test contexts
        self.test_contexts = [
            ("What is the performance of Nifty 50?", "Nifty 50 is up 2% today", ["Nifty 50", "market"]),
            ("How is the banking sector performing?", "Banking stocks are down 1.5%", ["banking", "stocks"]),
            ("What's the latest on Reliance?", "Reliance reported strong earnings", ["Reliance", "earnings"])
        ]
        
        for query, response, entities in self.test_contexts:
            self.vector_store.add_context(query, response, entities)

    def test_embedding_creation(self):
        """Test if embeddings are created correctly"""
        text = "Test query"
        embedding = self.vector_store.create_embedding(text)
        self.assertIsInstance(embedding, list)
        self.assertEqual(len(embedding), 1536)  # OpenAI embeddings dimension

    def test_similarity_search(self):
        """Test if similar contexts are found correctly"""
        query = "How is Nifty doing?"
        similar_contexts = self.vector_store.find_similar_contexts(query)
        self.assertLessEqual(len(similar_contexts), 3)  # top_k=3
        self.assertIn("Nifty 50", similar_contexts[0]['query'])

    def test_entity_extraction(self):
        """Test if relevant entities are extracted correctly"""
        query = "Tell me about banking stocks"
        entities = self.vector_store.get_relevant_entities(query)
        self.assertIn("banking", entities)
        self.assertIn("stocks", entities)

    def test_history_limit(self):
        """Test if history limit is maintained"""
        # Add more contexts to exceed limit
        for i in range(15):
            self.vector_store.add_context(f"Query {i}", f"Response {i}", [f"entity{i}"])
        
        self.assertLessEqual(len(self.vector_store.embeddings), 10)
        self.assertLessEqual(len(self.vector_store.contexts), 10)

if __name__ == '__main__':
    unittest.main() 